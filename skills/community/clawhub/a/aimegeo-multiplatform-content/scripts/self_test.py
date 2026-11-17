#!/usr/bin/env python3
"""Run offline business checks and execute the complete tutorial code."""

import csv
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
from content_bundle import BundleError, handoff_csv, read_article, validate_bundle

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "success"
FAILURES = ROOT / "examples" / "failure"
CLI = ROOT / "scripts" / "content_bundle.py"


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_package_yaml(text):
    """Read this package's one-level mappings and metadata lists, not arbitrary YAML."""
    result, nested = {}, None
    for line in text.splitlines():
        if not line.strip():
            continue
        item = re.fullmatch(r"  - (.+)", line)
        if item:
            if not isinstance(nested, list):
                raise ValueError("Unexpected YAML list item")
            nested.append(json.loads(item[1]))
            continue
        match = re.fullmatch(r"( {0,2})([a-z_]+):(?: (.+))?", line)
        if not match or len(match[1]) == 1:
            raise ValueError(f"Unsupported package YAML: {line}")
        indent, key, value = match.groups()
        if not indent:
            target = result
            nested = None
        elif isinstance(nested, dict):
            target = nested
        else:
            raise ValueError("Unexpected nested YAML")
        if key in target:
            raise ValueError(f"Duplicate YAML key: {key}")
        if value is None:
            if indent:
                raise ValueError("Only one nested level is used")
            target[key] = [] if key in {"tags", "trigger_words"} else {}
            nested = target[key]
        else:
            try:
                target[key] = json.loads(value)
            except json.JSONDecodeError:
                if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value):
                    raise ValueError(f"Quote this YAML string: {value}")
                target[key] = value
    return result


class PackageTests(unittest.TestCase):
    def test_metadata_contract(self):
        slug = "aimegeo-multiplatform-content"
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = re.match(r"---\n(.*?)\n---\n", skill, re.S)
        self.assertIsNotNone(frontmatter)
        meta = read_package_yaml(frontmatter[1])
        self.assertEqual(set(meta), {"name", "description"})
        self.assertEqual(meta["name"], slug)
        self.assertTrue(meta["description"])
        manifest = read_package_yaml((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest), {"name", "slug", "display_name", "description", "version",
                         "icon", "license", "repository", "tags", "trigger_words", "self_test"})
        self.assertEqual((manifest["name"], manifest["slug"]), (slug, slug))
        self.assertEqual(manifest["version"], "1.0.1")
        self.assertEqual(manifest["display_name"], "GEO 多平台内容制作")
        self.assertEqual(manifest["icon"], "icon-512.png")
        self.assertEqual(manifest["license"], "MIT-0")
        icon = ROOT / manifest["icon"]
        self.assertTrue(icon.is_file(), "manifest icon must be included in this package")
        with icon.open("rb") as image:
            self.assertEqual(image.read(8), b"\x89PNG\r\n\x1a\n")
            image.seek(16)
            self.assertEqual(image.read(8), (512).to_bytes(4, "big") * 2)
        self.assertEqual(manifest["self_test"], "python3 scripts/self_test.py")
        self.assertTrue(manifest["repository"].startswith("https://"))
        self.assertIsInstance(manifest["tags"], list)
        self.assertIsInstance(manifest["trigger_words"], list)
        agents = read_package_yaml((ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        self.assertEqual(set(agents), {"interface"})
        interface = agents["interface"]
        self.assertEqual(set(interface), {"display_name", "short_description", "default_prompt", "icon_small", "icon_large"})
        self.assertEqual(interface["display_name"], manifest["display_name"])
        self.assertIn("$" + slug, interface["default_prompt"])
        self.assertEqual(interface["icon_small"], "./icon-512.png")
        self.assertEqual(interface["icon_large"], "./icon-512.png")
        for filename in ("README.md", "README.en.md"):
            self.assertTrue((ROOT / filename).read_text(encoding="utf-8").strip())

    def test_license_is_preserved_in_source_or_distribution(self):
        license_file = ROOT / "LICENSE"
        if not license_file.exists():
            license_file = ROOT / "NOTICE.md"
        text = license_file.read_text(encoding="utf-8")
        self.assertIn("MIT No Attribution", text)
        self.assertIn("Permission is hereby granted", text)
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("MIT-0", notice)
        self.assertNotIn("MIT License", notice)

    def test_local_document_links_are_portable_and_resolve(self):
        for document in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                target_path = Path(target.split("#", 1)[0])
                with self.subTest(document=str(document.relative_to(ROOT)), target=target):
                    self.assertFalse(target_path.is_absolute())
                    resolved = (document.parent / target_path).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists())


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="multiplatform-self-test-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.bundle = self.folder / "bundle"
        shutil.copytree(SAMPLE, self.bundle)

    def ledger(self):
        return json.loads((self.bundle / "事实与来源清单.json").read_text(encoding="utf-8"))

    def write_ledger(self, ledger):
        save_json(self.bundle / "事实与来源清单.json", ledger)

    def request(self):
        return json.loads((self.bundle / "request.json").read_text(encoding="utf-8"))

    def fail_with(self, code):
        with self.assertRaises(BundleError) as caught:
            validate_bundle(self.bundle)
        self.assertEqual(caught.exception.code, code)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)], cwd=self.folder,
                              capture_output=True, text=True, encoding="utf-8")

    def set_existing(self, operation="preserve", allowed=None):
        (self.bundle / "originals").mkdir()
        shutil.copyfile(self.bundle / "zhihu.md", self.bundle / "originals" / "zhihu.md")
        request = self.request()
        request["articles"][0].update(operation=operation, original="originals/zhihu.md",
                                       allowed_changes=allowed or [])
        if operation == "edit":
            request["articles"][0]["change_request"] = "仅修改明确授权的字段"
        save_json(self.bundle / "request.json", request)

    def replace_article(self, filename, before, after):
        path = self.bundle / filename
        text = path.read_text(encoding="utf-8")
        self.assertIn(before, text)
        path.write_text(text.replace(before, after), encoding="utf-8")

    def test_complete_bundle_and_included_handoff_fixture(self):
        report, rows = validate_bundle(self.bundle)
        self.assertTrue(report["valid"])
        self.assertEqual((report["article_count"], report["fact_count"]), (3, 6))
        self.assertEqual([row["content_type"] for row in rows], ["explainer", "tutorial", "note"])
        self.assertEqual([row["handoff_status"] for row in rows],
                         ["待规则确认", "待规则确认", "待素材及规则确认"])
        self.assertEqual(rows[-1]["asset_status"], "pending_creation")
        self.assertIsNone(report["geo"]["observed_mention_count"])
        self.assertIsNone(report["geo"]["observed_native_citation_count"])
        expected = (SAMPLE / "发布交接清单.csv").read_text(encoding="utf-8")
        self.assertEqual(handoff_csv(rows), expected)

    def test_conflicting_capacity_fixture_is_rejected(self):
        shutil.copyfile(FAILURES / "容量冲突.md", self.bundle / "xiaohongshu.md")
        self.fail_with("FACT_MISMATCH")
        result = self.cli("check", self.bundle)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["error"], "FACT_MISMATCH")

    def test_source_and_article_fact_links(self):
        ledger = self.ledger()
        ledger["facts"][1]["canonical"] = "每批最多 300 行"
        self.write_ledger(ledger)
        self.fail_with("FACT_SOURCE")
        self.write_ledger(json.loads((SAMPLE / "事实与来源清单.json").read_text(encoding="utf-8")))
        self.replace_article("zhihu.md", '"F01", "F02", "F03", "F04", "F05"', '"F01"')
        self.fail_with("FACT_REFERENCE")

    def test_preserve_keeps_title_and_body(self):
        self.set_existing()
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "整理品牌资料前，先分清格式检查与事实核验", "未经授权的新标题")
        self.fail_with("PRESERVE_TITLE")

    def test_preserve_body_detects_even_small_changes(self):
        self.set_existing()
        self.replace_article("zhihu.md", "小团队准备多平台内容时", "团队准备多平台内容时")
        self.fail_with("PRESERVE_BODY")

    def test_edit_scope_allows_title_but_not_body(self):
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", "整理品牌资料前，先分清格式检查与事实核验", "资料整理中的格式与事实")
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "小团队准备多平台内容时", "团队准备多平台内容时")
        self.fail_with("PRESERVE_BODY")

    def test_body_edit_does_not_authorize_title_changes(self):
        self.set_existing("edit", ["body"])
        self.replace_article("zhihu.md", "小团队准备多平台内容时", "团队准备多平台内容时")
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "整理品牌资料前，先分清格式检查与事实核验", "新的标题")
        self.fail_with("PRESERVE_TITLE")

    def test_metadata_and_visible_h1_must_agree(self):
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", 'title: "整理品牌资料前，先分清格式检查与事实核验"',
                             'title: "新的标题"')
        self.fail_with("TITLE_MISMATCH")
        self.replace_article("zhihu.md", 'title: "新的标题"',
                             'title: "整理品牌资料前，先分清格式检查与事实核验"')
        self.replace_article("zhihu.md", "# 整理品牌资料前，先分清格式检查与事实核验\n", "# 新的标题\n")
        self.fail_with("TITLE_MISMATCH")

    def test_title_only_preserves_remaining_bytes_and_crlf(self):
        article = self.bundle / "zhihu.md"
        before = article.read_bytes().replace(b"\n", b"\r\n")
        article.write_bytes(before)
        self.set_existing("edit", ["title"])
        old = "整理品牌资料前，先分清格式检查与事实核验".encode()
        new = "资料整理中的格式与事实".encode()
        article.write_bytes(before.replace(old, new))
        validate_bundle(self.bundle)
        self.assertEqual(article.read_bytes().split(b"\r\n\r\n", 2)[2],
                         before.split(b"\r\n\r\n", 2)[2])
        article.write_bytes(article.read_bytes() + b" ")
        self.fail_with("PRESERVE_BODY")

    def test_no_leading_h1_keeps_internal_heading_in_body(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.replace_article("zhihu.md", "# " + old + "\n", "")
        self.replace_article("zhihu.md", "## 格式检查解决什么问题？", "# 正文内的一级标题\n\n## 格式检查解决什么问题？")
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", 'title: "' + old + '"', 'title: "只有元数据标题"')
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "# 正文内的一级标题", "# 不能顺便改的正文标题")
        self.fail_with("PRESERVE_BODY")

    def test_title_authorization_does_not_cover_internal_h1(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.replace_article("zhihu.md", "## 格式检查解决什么问题？", "# 正文内的一级标题\n\n## 格式检查解决什么问题？")
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", old, "资料整理中的格式与事实")
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "# 正文内的一级标题", "# 另改正文一级标题")
        self.fail_with("PRESERVE_BODY")

    def test_body_only_cannot_add_or_remove_visible_title(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.set_existing("edit", ["body"])
        self.replace_article("zhihu.md", "# " + old + "\n", "")
        self.fail_with("PRESERVE_TITLE")
        # An original with no document H1 cannot acquire one under body scope.
        shutil.copyfile(self.bundle / "zhihu.md", self.bundle / "originals" / "zhihu.md")
        self.replace_article("zhihu.md", "\n\n小团队准备多平台内容时", "\n\n# " + old + "\n\n小团队准备多平台内容时")
        self.fail_with("PRESERVE_TITLE")

    def test_title_only_does_not_strip_code_fence_headings(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.replace_article("zhihu.md", "# " + old + "\n", "```markdown\n# 代码中的标题\n```\n")
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", 'title: "' + old + '"', 'title: "新的元数据标题"')
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "# 代码中的标题", "# 不能改的代码标题")
        self.fail_with("PRESERVE_BODY")

    def test_title_only_supports_leading_setext_h1_without_changing_its_markup(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.replace_article("zhihu.md", "# " + old + "\n", old + "\n===\n")
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", old, "资料整理中的格式与事实")
        validate_bundle(self.bundle)
        self.replace_article("zhihu.md", "\n===\n", "\n====\n")
        self.fail_with("PRESERVE_BODY")

    def test_title_only_preserves_atx_closing_hashes(self):
        old = "整理品牌资料前，先分清格式检查与事实核验"
        self.replace_article("zhihu.md", "# " + old + "\n", "# " + old + " ###\n")
        self.set_existing("edit", ["title"])
        self.replace_article("zhihu.md", old, "资料整理中的格式与事实")
        validate_bundle(self.bundle)

    def test_available_image_requires_a_real_file(self):
        ledger = self.ledger()
        ledger["assets"][0].update(state="available", path="missing.png")
        self.write_ledger(ledger)
        self.fail_with("ASSET_FILE")
        ledger["assets"][0]["path"] = "materials.csv"
        self.write_ledger(ledger)
        self.fail_with("ASSET_FILE")

    def test_rule_confirmation_does_not_complete_missing_artwork(self):
        ledger = self.ledger()
        for rule in ledger["platform_rules"]:
            rule.update(state="confirmed", basis="受控测试：用户本次编辑要求已记录", checked_at="2026-10-19")
        self.write_ledger(ledger)
        _, rows = validate_bundle(self.bundle)
        self.assertEqual([row["handoff_status"] for row in rows], ["可交接", "可交接", "待素材"])

    def test_paths_cannot_escape_bundle(self):
        ledger = self.ledger()
        ledger["sources"][0]["path"] = "../outside.md"
        self.write_ledger(ledger)
        self.fail_with("PATH")
        outside = self.folder / "outside.md"
        outside.write_text("test", encoding="utf-8")
        (self.bundle / "escape.md").symlink_to(outside)
        ledger["sources"][0]["path"] = "escape.md"
        self.write_ledger(ledger)
        self.fail_with("PATH")

    def test_unknown_geo_counts_are_not_zero(self):
        for status in ("not_run", "query_failed", "simulated"):
            with self.subTest(status=status):
                ledger = self.ledger()
                record = dict(status=status, answer="模拟内容" if status == "simulated" else None,
                              mention_count=0, native_citations=[], error="受控失败" if status == "query_failed" else None)
                ledger["geo_observations"] = [record]
                self.write_ledger(ledger)
                self.fail_with("GEO_UNKNOWN_COUNT")

    def test_failed_and_simulated_observations_stay_separate(self):
        ledger = self.ledger()
        ledger["geo_observations"] = [
            dict(status="query_failed", answer=None, mention_count=None,
                 native_citations=None, error="受控测试：网络失败"),
            dict(status="simulated", answer="模拟回答提到青禾知识卡", mention_count=None, native_citations=None),
            dict(status="not_run", answer=None, mention_count=None, native_citations=None),
        ]
        self.write_ledger(ledger)
        report, _ = validate_bundle(self.bundle)
        self.assertEqual(report["geo"]["samples_by_status"],
                         {"observed": 0, "simulated": 1, "not_run": 1, "query_failed": 1})
        self.assertIsNone(report["geo"]["observed_native_citation_count"])

    def test_observed_aggregation_uses_supplied_raw_records(self):
        # This is a constructed parser regression fixture, not an AI-engine test.
        ledger = self.ledger()
        ledger["sources"].append(dict(id="G01", kind="provided_excerpt", label="受控解析夹具",
                                      locator="self_test.py constructed input",
                                      text="测试回答：青禾知识卡。\n原生来源：https://example.org/source"))
        record = dict(status="observed", engine="fixture-parser", query="受控测试问题",
                      collected_at="2026-10-19T00:00:00+00:00", answer="测试回答：青禾知识卡。",
                      brand_terms=["青禾", "青禾知识卡"], mention_count=1, evidence_source_id="G01",
                      native_citations=[dict(kind="native", url="https://example.org/source")])
        ledger["geo_observations"] = [record]
        self.write_ledger(ledger)
        report, _ = validate_bundle(self.bundle)
        self.assertEqual(report["geo"]["observed_mention_count"], 1)
        self.assertEqual(report["geo"]["observed_native_citation_count"], 1)
        record["mention_count"] = 2
        self.write_ledger(ledger)
        self.fail_with("GEO_MENTIONS")
        record["mention_count"] = 1
        record["native_citations"][0]["kind"] = "body_link"
        self.write_ledger(ledger)
        self.fail_with("GEO_EVIDENCE")

    def test_successful_empty_observation_can_be_zero(self):
        ledger = self.ledger()
        ledger["sources"].append(dict(id="G01", kind="provided_excerpt", label="受控零结果夹具",
                                      locator="self_test.py constructed input", text="测试回答：只讨论通用方法。"))
        ledger["geo_observations"] = [dict(status="observed", engine="fixture-parser", query="受控测试",
            collected_at="2026-10-19T00:00:00+00:00", answer="测试回答：只讨论通用方法。",
            brand_terms=["青禾知识卡"], mention_count=0, native_citations=[], evidence_source_id="G01")]
        self.write_ledger(ledger)
        report, _ = validate_bundle(self.bundle)
        self.assertEqual(report["geo"]["observed_mention_count"], 0)
        self.assertEqual(report["geo"]["observed_native_citation_count"], 0)

    def test_cli_portability_and_csv_business_fields(self):
        output = self.folder / "handoff.csv"
        result = self.cli("handoff", self.bundle, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        with output.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[-1]["source_ids"], "S01")
        self.assertEqual(rows[-1]["handoff_status"], "待素材及规则确认")
        self.assertIn("图片待制作", rows[-1]["pending_actions"])

    def test_cli_failure_has_no_output_and_cannot_overwrite_article(self):
        original = (self.bundle / "zhihu.md").read_bytes()
        result = self.cli("handoff", self.bundle, "--output", self.bundle / "zhihu.md")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["error"], "OUTPUT_PATH")
        self.assertEqual((self.bundle / "zhihu.md").read_bytes(), original)
        shutil.copyfile(FAILURES / "容量冲突.md", self.bundle / "xiaohongshu.md")
        output = self.folder / "must-not-exist.csv"
        result = self.cli("handoff", self.bundle, "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())

    def test_invalid_json_and_unknown_state_report_failure(self):
        (self.bundle / "request.json").write_text("{", encoding="utf-8")
        result = self.cli("check", self.bundle)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stderr)["valid"])
        shutil.copyfile(SAMPLE / "request.json", self.bundle / "request.json")
        ledger = self.ledger()
        ledger["geo_observations"][0]["status"] = {"invalid": "type"}
        self.write_ledger(ledger)
        self.fail_with("GEO_STATUS")

    def test_csv_formula_escape_preserves_manuscript_title(self):
        self.replace_article("zhihu.md", "整理品牌资料前，先分清格式检查与事实核验", "=1+1")
        _, rows = validate_bundle(self.bundle)
        exported = list(csv.DictReader(io.StringIO(handoff_csv(rows))))
        self.assertEqual(exported[0]["title"], "'=1+1")
        self.assertEqual(read_article(self.bundle / "zhihu.md")[0]["title"], "=1+1")


class TutorialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csv-tutorial-self-test-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        article = (SAMPLE / "csdn.md").read_text(encoding="utf-8")
        code = re.search(r"```python\n(.*?)\n```", article, re.S)[1]
        self.script = self.folder / "preflight.py"
        self.script.write_text(code + "\n", encoding="utf-8")

    def run_input(self, contents):
        path = self.folder / "input.csv"
        path.write_bytes(contents if isinstance(contents, bytes) else contents.encode("utf-8"))
        return subprocess.run([sys.executable, str(self.script), str(path)], cwd=self.folder,
                              capture_output=True, text=True, encoding="utf-8")

    def test_sample_code_produces_documented_result(self):
        result = self.run_input((SAMPLE / "materials.csv").read_bytes())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "OK: 3 行；必填列 title、source 齐全\n")

    def test_capacity_boundary_and_header_exclusion(self):
        result = self.run_input("title,source\n" + "item,source\n" * 200)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "OK: 200 行；必填列 title、source 齐全\n")
        result = self.run_input("title,source\n" + "item,source\n" * 201)
        self.assertEqual(result.returncode, 2)
        self.assertIn("超过单批上限 200 行", result.stderr)

    def test_failure_files_are_rejected(self):
        for filename, message in (("缺少来源列.csv", "缺少必填列 title 或 source"),
                                   ("空来源.csv", "第 1 条记录的 title 或 source 为空")):
            with self.subTest(filename=filename):
                result = self.run_input((FAILURES / filename).read_bytes())
                self.assertEqual(result.returncode, 2)
                self.assertIn(message, result.stderr)

    def test_malformed_and_empty_inputs_fail(self):
        for contents in ("", "title,source\n", "title,title,source\na,b,c\n",
                         "title,source\na,b,c\n", "title,source,note\na,b\n",
                         "title,source\n\"unfinished,b\n", b"title,source\n\xff,b\n"):
            with self.subTest(contents=repr(contents)):
                result = self.run_input(contents)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_bom_and_quoted_newline_are_valid_records(self):
        result = self.run_input('\ufefftitle,source,note\nitem,doc,"line one\nline two"\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "OK: 1 行；必填列 title、source 齐全\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
