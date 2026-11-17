#!/usr/bin/env python3
"""Business checks using only the packaged fixtures and Python standard library."""

import contextlib
import copy
import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import knowledge as tool


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="knowledge-distill-test-")
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.sources = self.work / "sources"
        shutil.copytree(ROOT / "examples" / "input", self.sources)
        self.index = tool.make_index(self.sources)
        self.index_path = self.work / "index.json"
        self.index_path.write_text(json.dumps(self.index, ensure_ascii=False), encoding="utf-8")
        self.bundle = tool.read_json(ROOT / "examples" / "success.bundle.json")

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = tool.main(list(map(str, args)))
        return code, out.getvalue(), err.getvalue()

    def save_bundle(self):
        path = self.work / "bundle.json"
        path.write_text(json.dumps(self.bundle, ensure_ascii=False), encoding="utf-8")
        return path

    def assert_invalid(self, message):
        with self.assertRaisesRegex(tool.Invalid, message):
            tool.validate(self.bundle, self.index)

    def load_same_paragraph_fixture(self, name="success.bundle.json"):
        fixture = ROOT / "examples" / "same-paragraph-conflict"
        self.sources = self.work / "same-paragraph-sources"
        shutil.copytree(fixture / "input", self.sources)
        self.index = tool.make_index(self.sources)
        self.index_path.write_text(json.dumps(self.index, ensure_ascii=False), encoding="utf-8")
        self.bundle = tool.read_json(fixture / name)

    def test_five_questions_have_real_source_mappings(self):
        usage = tool.validate(self.bundle, self.index)
        self.assertEqual(len(self.bundle["questions"]), 5)
        self.assertEqual([q["status"] for q in self.bundle["questions"]],
                         ["answered", "answered", "answered", "conflict", "answered"])
        self.assertEqual(len(self.index["sources"]), 4)
        self.assertEqual(len(usage), 8)
        by_file = {s["path"]: s for s in self.index["sources"]}
        manual = by_file["软件说明.md"]
        first = manual["locators"][0]
        self.assertEqual(first["location"], "示例协作软件 2.0 软件说明 / 导入文件")
        self.assertEqual((first["line_start"], first["line_end"]), (5, 5))
        self.assertEqual(usage[first["id"]], {"Q001"})
        self.assertEqual(usage[manual["locators"][2]["id"]], {"Q004", "C001"})
        self.assertEqual(usage[by_file["教程3-导出下载.md"]["locators"][0]["id"]], {"Q004", "C001"})
        self.assertEqual(self.bundle["issues"][1]["question_ids"], [])

    def test_export_matches_all_three_reviewed_deliverables(self):
        destination = self.work / "result"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out), {"ok": True, "questions": 5, "claims": 7, "missing": 1, "conflicts": 1})
        expected = ROOT / "examples" / "output"
        self.assertEqual({p.name for p in destination.iterdir()},
                         {"常见问答.md", "资料索引.csv", "待补及冲突信息.md"})
        for filename in ("常见问答.md", "资料索引.csv", "待补及冲突信息.md"):
            self.assertEqual((destination / filename).read_bytes(), (expected / filename).read_bytes())
        with (destination / "资料索引.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 8)
        self.assertEqual({r["path"] for r in rows}, {p.name for p in self.sources.iterdir()})
        for row in rows:
            source = next(s for s in self.index["sources"] if s["id"] == row["source_id"])
            self.assertEqual(row["sha256"], source["sha256"])

    def test_failure_fixture_exits_two_and_creates_no_output(self):
        destination = self.work / "rejected"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", ROOT / "examples" / "failure" / "无引文答案.json",
                                  "--out", destination)
        self.assertEqual((code, out), (2, ""))
        self.assertIn("each claim requires evidence", json.loads(err)["error"])
        self.assertFalse(destination.exists())

    def test_quote_must_be_a_literal_source_passage(self):
        self.bundle["questions"][0]["claims"][0]["refs"][0]["quote"] = "单个文件不得超过 100 MB。"
        self.assert_invalid("quote not found")

    def test_dangling_locator_is_rejected(self):
        self.bundle["questions"][0]["claims"][0]["refs"][0]["locator"] = "S-unknown:P999"
        self.assert_invalid("unknown locator")

    def test_source_changes_invalidate_index_without_export(self):
        manual = self.sources / "软件说明.md"
        manual.write_text(manual.read_text(encoding="utf-8").replace("10 MB", "20 MB"), encoding="utf-8")
        destination = self.work / "stale-result"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, out), (2, ""))
        self.assertIn("stale or modified", json.loads(err)["error"])
        self.assertFalse(destination.exists())

    def test_edited_index_cannot_fabricate_source_text(self):
        self.index["sources"][0]["locators"][0]["text"] = "所有客户都享有无限存储。"
        self.index_path.write_text(json.dumps(self.index), encoding="utf-8")
        with self.assertRaisesRegex(tool.Invalid, "stale or modified"):
            tool.verified_index(self.index_path, self.sources)

    def test_one_side_of_registered_conflict_cannot_be_answered(self):
        q = self.bundle["questions"][3]
        q["status"], q["issue_ids"], q["claims"] = "answered", [], q["claims"][:1]
        self.assert_invalid("conflicting evidence must link C001")

    def test_same_paragraph_independent_fact_exports_as_answered(self):
        self.load_same_paragraph_fixture()
        destination = self.work / "same-paragraph-result"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out), {"ok": True, "questions": 2, "claims": 3, "missing": 0, "conflicts": 1})
        faq = (destination / "常见问答.md").read_text(encoding="utf-8")
        import_answer, download_answer = faq.split("## Q002", 1)
        self.assertIn("状态：可回答", import_answer)
        self.assertIn("支持 CSV 导入。", import_answer)
        self.assertNotIn("C001", import_answer)
        self.assertIn("状态：资料冲突", download_answer)
        self.assertIn("待核实：C001", download_answer)
        notes = (destination / "待补及冲突信息.md").read_text(encoding="utf-8")
        self.assertIn("关联问答：Q002", notes)
        self.assertNotIn("Q001", notes)
        with (destination / "资料索引.csv").open(encoding="utf-8", newline="") as handle:
            rows = {row["path"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["manual.txt"]["used_by"], "C001;Q001;Q002")
        self.assertEqual(rows["deadlines.txt"]["used_by"], "C001;Q002")

    def test_same_paragraph_independent_fact_can_be_partial(self):
        self.load_same_paragraph_fixture()
        question = self.bundle["questions"][0]
        question["status"], question["issue_ids"] = "partial", ["G001"]
        self.bundle["issues"].append({"id": "G001", "kind": "missing", "topic": "CSV 大小限制",
                                      "detail": "资料只说明支持 CSV，没有大小限制。",
                                      "needed": "补充 CSV 大小限制。", "question_ids": ["Q001"], "refs": []})
        usage = tool.validate(self.bundle, self.index)
        faq = tool.render(self.bundle, self.index, usage)["常见问答.md"].split("## Q002", 1)[0]
        self.assertIn("状态：部分可答", faq)
        self.assertIn("待核实：G001", faq)
        self.assertNotIn("C001", faq)

    def test_same_paragraph_one_sided_conflict_cannot_export(self):
        self.load_same_paragraph_fixture("failure.bundle.json")
        destination = self.work / "one-sided-result"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(json.loads(err), {"ok": False,
                         "error": "Q002: conflicting evidence must link C001 and use conflict status"})
        self.assertFalse(destination.exists())

    def test_conflict_quote_overlap_cannot_be_hidden_by_quote_length(self):
        self.load_same_paragraph_fixture()
        question = self.bundle["questions"][1]
        question["status"], question["issue_ids"] = "answered", []
        question["claims"] = question["claims"][:1]
        self.bundle["issues"][0]["question_ids"] = []
        ref = question["claims"][0]["refs"][0]
        for quote in ("下载链接保留 7 天。", "保留 7 天", "支持 CSV 导入。下载链接保留 7 天。"):
            with self.subTest(quote=quote):
                ref["quote"] = quote
                self.assert_invalid("conflicting evidence must link C001")
        # Neither quote contains the other, but their source spans overlap.
        self.bundle["issues"][0]["refs"][0]["quote"] = "下载链接保留 7 天"
        ref["quote"] = "保留 7 天。"
        self.assert_invalid("conflicting evidence must link C001")

    def test_repeated_quote_needs_context_to_distinguish_independent_fact(self):
        self.load_same_paragraph_fixture()
        (self.sources / "manual.txt").write_text("导入日志保留 7 天。下载链接保留 7 天。\n", encoding="utf-8")
        self.index = tool.make_index(self.sources)
        question = self.bundle["questions"][0]
        question["question"] = "导入日志保留多久？"
        question["claims"][0]["text"] = "导入日志保留 7 天。"
        ref = question["claims"][0]["refs"][0]
        ref["quote"] = "保留 7 天。"
        self.assert_invalid("conflicting evidence must link C001")
        ref["quote"] = "导入日志保留 7 天。"
        usage = tool.validate(self.bundle, self.index)
        faq = tool.render(self.bundle, self.index, usage)["常见问答.md"].split("## Q002", 1)[0]
        self.assertIn("状态：可回答", faq)
        self.assertNotIn("C001", faq)

    def test_self_conflicting_paragraph_does_not_taint_independent_fact(self):
        self.load_same_paragraph_fixture()
        (self.sources / "manual.txt").write_text(
            "支持 CSV 导入。下载链接保留 7 天。下载链接保留 30 天。\n", encoding="utf-8")
        self.index = tool.make_index(self.sources)
        locator = self.bundle["questions"][0]["claims"][0]["refs"][0]["locator"]
        self.bundle["issues"][0]["refs"][1]["locator"] = locator
        self.bundle["questions"][1]["claims"][1]["refs"][0]["locator"] = locator
        usage = tool.validate(self.bundle, self.index)
        self.assertEqual(usage[locator], {"Q001", "Q002", "C001"})

    def test_conflict_requires_evidence_for_both_sides(self):
        self.bundle["issues"][0]["refs"] = self.bundle["issues"][0]["refs"][:1]
        self.assert_invalid("at least two distinct source passages")

    def test_conflicting_sentences_in_one_paragraph_can_be_recorded(self):
        material = self.work / "self-contradiction"
        material.mkdir()
        (material / "规则.txt").write_text("链接保留 7 天。链接保留 30 天。", encoding="utf-8")
        index = tool.make_index(material)
        locator = index["sources"][0]["locators"][0]["id"]
        issue = {"id": "C001", "kind": "conflict", "topic": "链接有效期",
                 "detail": "同一段落同时写 7 天和 30 天。", "needed": "确认适用规则。",
                 "question_ids": [], "refs": [{"locator": locator, "quote": "链接保留 7 天。"},
                                               {"locator": locator, "quote": "链接保留 30 天。"}]}
        bundle = {"schema_version": 1, "questions": [], "issues": [issue]}
        self.assertEqual(tool.validate(bundle, index)[locator], {"C001"})

    def test_issue_links_must_match_both_directions(self):
        self.bundle["issues"][0]["question_ids"] = []
        self.assert_invalid("question links must match both directions")

    def test_partial_answer_retains_known_fact_and_specific_gap(self):
        q = self.bundle["questions"][0]
        q["status"], q["issue_ids"] = "partial", ["G002"]
        self.bundle["issues"].append({"id": "G002", "kind": "missing", "topic": "导入行数上限",
                                      "detail": "材料只说明大小限制，没有行数限制。",
                                      "needed": "补充当前版本的行数限制。", "question_ids": ["Q001"], "refs": []})
        usage = tool.validate(self.bundle, self.index)
        self.assertEqual(len(q["claims"]), 1)
        self.assertIn("G002", tool.render(self.bundle, self.index, usage)["常见问答.md"])

    def test_missing_only_bundle_does_not_invent_questions(self):
        self.bundle["questions"] = []
        self.bundle["issues"] = [self.bundle["issues"][1]]
        usage = tool.validate(self.bundle, self.index)
        outputs = tool.render(self.bundle, self.index, usage)
        self.assertEqual(sum(bool(x) for x in usage.values()), 0)
        self.assertEqual(len(list(csv.DictReader(io.StringIO(outputs["资料索引.csv"])))), 8)
        self.assertIn("G001", outputs["待补及冲突信息.md"])

    def test_one_useful_question_has_no_minimum_count_gate(self):
        self.bundle["questions"] = self.bundle["questions"][:1]
        self.bundle["issues"] = []
        self.assertEqual(len(tool.validate(self.bundle, self.index)), 8)

    def test_missing_status_cannot_hide_factual_answers(self):
        q = self.bundle["questions"][0]
        q["status"], q["issue_ids"] = "missing", ["G001"]
        self.bundle["issues"][1]["question_ids"] = ["Q001"]
        self.assert_invalid("missing cannot contain factual answers")

    def test_duplicate_questions_and_ids_are_rejected(self):
        duplicate = copy.deepcopy(self.bundle["questions"][0])
        self.bundle["questions"].append(duplicate)
        self.assert_invalid("duplicate ID")
        duplicate["id"] = "Q099"
        duplicate["question"] = "  " + duplicate["question"].rstrip("？") + "?"
        self.assert_invalid("duplicate question")

    def test_decimal_size_conditions_export_distinct_answers(self):
        first = copy.deepcopy(self.bundle["questions"][0])
        second = copy.deepcopy(first)
        first["question"] = "单个 CSV 文件 1.5 MB 是否超过导入大小限制？"
        second.update(id="Q002", question="单个 CSV 文件 15 MB 是否超过导入大小限制？")
        first["claims"][0]["text"] = "按 10 MB 上限比较，1.5 MB 不超过大小限制。"
        second["claims"][0]["text"] = "按 10 MB 上限比较，15 MB 超过大小限制。"
        self.bundle = {"schema_version": 1, "questions": [first, second], "issues": []}
        destination = self.work / "decimal-result"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out)["questions"], 2)
        faq = (destination / "常见问答.md").read_text(encoding="utf-8")
        for question in self.bundle["questions"]:
            self.assertIn(question["question"], faq)
            self.assertIn(question["claims"][0]["text"], faq)

    def test_version_dots_preserve_different_supported_formats(self):
        root = self.work / "versions"
        root.mkdir()
        facts = ["版本 1.5 仅支持 TXT。", "版本 15 支持 TXT 和 Markdown。",
                 "版本 v1.5.0 仅支持 TXT。", "版本 v15.0 支持 TXT 和 Markdown。"]
        (root / "formats.txt").write_text("\n\n".join(facts), encoding="utf-8")
        index = tool.make_index(root)
        questions = []
        for number, (version, paragraph) in enumerate(zip(
                ("1.5", "15", "v1.5.0", "v15.0"), index["sources"][0]["locators"]), 1):
            questions.append({"id": f"Q{number:03d}", "question": f"版本 {version} 支持哪些格式？",
                              "status": "answered", "issue_ids": [],
                              "claims": [{"text": paragraph["text"],
                                          "refs": [{"locator": paragraph["id"], "quote": paragraph["text"]}]}]})
        bundle = {"schema_version": 1, "questions": questions, "issues": []}
        usage = tool.validate(bundle, index)
        faq = tool.render(bundle, index, usage)["常见问答.md"]
        for fact in facts:
            self.assertIn(fact, faq)

    def test_sentence_ending_punctuation_still_merges_duplicate_questions(self):
        question = copy.deepcopy(self.bundle["questions"][0])
        question["question"] = "文件 1.5 MB 是否超过大小限制？"
        for suffix in ("?", "。", ".", "！", "?!", "……", "？ ！ "):
            with self.subTest(suffix=suffix):
                duplicate = copy.deepcopy(question)
                duplicate.update(id="Q002", question="  文件１．５ MB 是否超过大小限制" + suffix)
                self.bundle = {"schema_version": 1, "questions": [question, duplicate], "issues": []}
                self.assert_invalid("duplicate question")

    def test_export_preserves_existing_output(self):
        destination = self.work / "existing"
        destination.mkdir()
        (destination / "original.txt").write_text("keep", encoding="utf-8")
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, out), (2, ""))
        self.assertFalse(json.loads(err)["ok"])
        self.assertEqual([p.name for p in destination.iterdir()], ["original.txt"])
        self.assertEqual((destination / "original.txt").read_text(), "keep")

    def test_export_cannot_contaminate_its_source_corpus(self):
        destination = self.sources / "generated"
        code, out, err = self.cli("export", "--sources", self.sources, "--index", self.index_path,
                                  "--bundle", self.save_bundle(), "--out", destination)
        self.assertEqual((code, out), (2, ""))
        self.assertIn("outside the source directory", json.loads(err)["error"])
        self.assertFalse(destination.exists())

    def test_index_does_not_overwrite_files(self):
        before = self.index_path.read_bytes()
        code, out, _ = self.cli("index", "--sources", self.sources, "--out", self.index_path)
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(self.index_path.read_bytes(), before)

    def test_empty_or_heading_only_material_fails(self):
        empty = self.work / "empty"
        empty.mkdir()
        (empty / "heading.md").write_text("# 标题\n\n## 子标题\n", encoding="utf-8")
        (empty / "not-parsed.pdf").write_bytes(b"not a text source")
        with self.assertRaisesRegex(tool.Invalid, "no nonempty"):
            tool.make_index(empty)

    def test_source_symlink_is_rejected(self):
        outside = self.work / "outside.txt"
        outside.write_text("not part of the selected corpus", encoding="utf-8")
        (self.sources / "linked.txt").symlink_to(outside)
        with self.assertRaisesRegex(tool.Invalid, "symbolic links"):
            tool.make_index(self.sources)

    def test_heading_locations_and_fenced_code_line_numbers(self):
        blocks = list(tool.paragraphs("# 手册\n## 安装\n\n第一段\n\n```sh\n# 代码中的井号\n\nrun\n```\n", True))
        self.assertEqual(len(blocks), 2)
        self.assertEqual([p["location"] for p in blocks], ["手册 / 安装", "手册 / 安装"])
        self.assertEqual((blocks[0]["line_start"], blocks[0]["line_end"]), (4, 4))
        self.assertEqual((blocks[1]["line_start"], blocks[1]["line_end"]), (6, 10))

    def test_txt_bom_unicode_and_csv_escaping(self):
        text_root = self.work / "text"
        text_root.mkdir()
        (text_root / '="表,一".txt').write_text("# 这是正文\n\n第二段", encoding="utf-8-sig")
        indexed = tool.make_index(text_root)
        self.assertEqual(indexed["sources"][0]["locators"][0]["text"], "# 这是正文")
        gap_only = {"schema_version": 1, "questions": [], "issues": [self.bundle["issues"][1]]}
        usage = tool.validate(gap_only, indexed)
        rows = list(csv.DictReader(io.StringIO(tool.render(gap_only, indexed, usage)["资料索引.csv"])))
        self.assertEqual(rows[0]["path"], "'=" + '"表,一".txt')
        self.assertEqual(len(rows), 2)

    def test_invalid_json_rejected_without_creating_output(self):
        path = self.work / "bad.json"
        for content in ('{"schema_version":1,"schema_version":1}', '{"schema_version":NaN}'):
            path.write_text(content, encoding="utf-8")
            code, out, err = self.cli("check", "--sources", self.sources, "--index", self.index_path, "--bundle", path)
            self.assertEqual((code, out), (2, ""))
            self.assertFalse(json.loads(err)["ok"])

    def test_portable_cli_needs_no_host_license_icon_or_configuration(self):
        package = self.work / "standalone"
        (package / "scripts").mkdir(parents=True)
        shutil.copy2(ROOT / "scripts" / "knowledge.py", package / "scripts" / "knowledge.py")
        shutil.copytree(ROOT / "examples" / "input", package / "input")
        shutil.copy2(ROOT / "examples" / "success.bundle.json", package / "bundle.json")
        (package / "index.json").write_text(json.dumps(self.index), encoding="utf-8")
        elsewhere = self.work / "different-working-directory"
        elsewhere.mkdir()
        completed = subprocess.run([sys.executable, str(package / "scripts" / "knowledge.py"), "check",
                                    "--sources", str(package / "input"), "--index", str(package / "index.json"),
                                    "--bundle", str(package / "bundle.json")], cwd=elsewhere,
                                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                                   capture_output=True, text=True, timeout=30)
        self.assertEqual((completed.returncode, completed.stderr), (0, ""))
        self.assertEqual(json.loads(completed.stdout)["questions"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
