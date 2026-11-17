#!/usr/bin/env python3
"""Offline business tests for the delivered article and rewrite checker.

New implementation by aimeGeo, MIT-0. All numeric test data below is
synthetic test input, not product evidence or an AI performance measurement.
"""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_rewrite import InputError, read_text, validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCOPES = ["## 账号如何分开", "## 相同内容如何复用", "## 发布前怎么检查"]


class RewriteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = read_text(ROOT / "examples/input/原稿.md")
        cls.good = read_text(ROOT / "examples/success/增强后的原稿.md")
        cls.plan = json.loads(read_text(ROOT / "examples/input/check-plan.json"))

    def codes(self, result):
        return {error["code"] for error in result["errors"]}

    def append_to_scope(self, text):
        return self.good.replace("## 我的建议", text + "\n\n## 我的建议", 1)

    def cli(self, root=ROOT, cwd=None, original=None, revised=None, plan=None):
        return subprocess.run(
            [sys.executable, str(root / "scripts/check_rewrite.py"),
             "--original", str(original or root / "examples/input/原稿.md"),
             "--revised", str(revised or root / "examples/success/增强后的原稿.md"),
             "--plan", str(plan or root / "examples/input/check-plan.json")],
            capture_output=True, text=True, cwd=cwd, check=False,
        )

    def test_complete_article_preserves_intent_and_scope(self):
        result = validate(self.original, self.good, self.plan)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["changed_sections"], SCOPES)
        self.assertEqual((result["covered_questions"], result["total_questions"]), (3, 3))
        self.assertEqual(result["introduced_numbers"], {})
        for protected in ("## 为什么选免费多账号工具", "## 开始前的准备", "## 我的建议"):
            before = self.original.split(protected, 1)[1].split("\n## ", 1)[0]
            after = self.good.split(protected, 1)[1].split("\n## ", 1)[0]
            self.assertEqual(before, after)
        self.assertIn("先理清账号和内容，再考虑把流程做快", self.good)
        self.assertIn("不要一上来就追求全自动", self.good)

    def test_negative_fixture_fails_expected_business_rules(self):
        bad = read_text(ROOT / "examples/failure/不合格增强稿.md")
        expected = set(json.loads(read_text(ROOT / "examples/failure/expected-errors.json")))
        result = validate(self.original, bad, self.plan)
        self.assertFalse(result["ok"])
        self.assertEqual(self.codes(result), expected)

    def test_title_change_rejected(self):
        bad = self.good.replace("# 免费多账号工具怎么用：先把账号和内容理清楚", "# 新标题", 1)
        self.assertIn("title_changed", self.codes(validate(self.original, bad, self.plan)))

    def test_protected_paragraph_change_rejected(self):
        bad = self.good.replace("是否适合自己的工作习惯更重要", "无需考虑自己的工作习惯", 1)
        self.assertIn("out_of_scope_change", self.codes(validate(self.original, bad, self.plan)))

    def test_whitespace_outside_scope_is_not_silently_normalized(self):
        bad = self.good.replace("## 开始前的准备\n\n", "## 开始前的准备\n\n\n", 1)
        self.assertIn("out_of_scope_change", self.codes(validate(self.original, bad, self.plan)))

    def test_unbacked_arabic_fullwidth_and_chinese_numbers(self):
        for text, token in (("演示指标提高40%。", "40%"), ("演示指标提高４０％。", "40%"),
                            ("演示指标提高百分之四十。", "百分之四十"), ("演示操作需要三天。", "三天")):
            with self.subTest(text=text):
                result = validate(self.original, self.append_to_scope(text), self.plan)
                self.assertIn("unbacked_numeric", self.codes(result))
                self.assertEqual(result["introduced_numbers"], {token: 1})

    def test_list_indices_and_url_digits_are_not_statistics(self):
        revised = self.append_to_scope("1. 核对账号。\n2. 查看状态。\n\n[演示链接](https://example.org/2026/40)")
        result = validate(self.original, revised, self.plan)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["introduced_numbers"], {})

    def sourced_numeric_case(self):
        plan = copy.deepcopy(self.plan)
        text = "本次演示整理了2个账号。"
        plan["sources"].append({"id": "synthetic", "kind": "user_provided",
                                "reference": "人工构造的校验资料，不是产品数据", "excerpt": text})
        plan["numeric_claims"].append({"text": text, "source_id": "synthetic", "evidence_quote": text})
        return self.append_to_scope(text), plan

    def test_supplied_numeric_evidence_is_accepted(self):
        revised, plan = self.sourced_numeric_case()
        result = validate(self.original, revised, plan)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["introduced_numbers"], {"2": 1})

    def test_false_evidence_quote_does_not_authorize_number(self):
        revised, plan = self.sourced_numeric_case()
        plan["sources"][-1]["excerpt"] = "这份资料没有账号数量。"
        result = validate(self.original, revised, plan)
        self.assertIn("quote_not_in_source", self.codes(result))
        self.assertIn("unbacked_numeric", self.codes(result))

    def test_wrong_number_in_claim_rejected(self):
        revised, plan = self.sourced_numeric_case()
        revised = revised.replace("本次演示整理了2个账号。", "本次演示整理了4个账号。")
        plan["numeric_claims"][-1]["text"] = "本次演示整理了4个账号。"
        result = validate(self.original, revised, plan)
        self.assertIn("claim_number_not_in_evidence", self.codes(result))
        self.assertIn("unbacked_numeric", self.codes(result))

    def test_evidence_cannot_be_reused_for_extra_unsupported_occurrences(self):
        revised, plan = self.sourced_numeric_case()
        revised = revised.replace("## 我的建议", "本演示还有2个平台。\n\n## 我的建议")
        self.assertIn("unbacked_numeric", self.codes(validate(self.original, revised, plan)))

    def test_absent_claim_is_not_numeric_permission(self):
        revised, plan = self.sourced_numeric_case()
        plan["numeric_claims"][-1]["text"] = "另一句有2个账号。"
        self.assertIn("claim_not_in_revision", self.codes(validate(self.original, revised, plan)))

    def test_fake_original_excerpt_rejected(self):
        plan = copy.deepcopy(self.plan)
        plan["sources"][0]["excerpt"] = "原稿没有这条事实。"
        with self.assertRaises(InputError):
            validate(self.original, self.good, plan)

    def test_verified_source_needs_timezone(self):
        revised, plan = self.sourced_numeric_case()
        plan["sources"][-1].update(kind="verified", verified_at="2026-10-19T10:00:00")
        with self.assertRaises(InputError):
            validate(self.original, revised, plan)
        plan["sources"][-1]["verified_at"] = "2026-10-19T10:00:00+08:00"
        self.assertTrue(validate(self.original, revised, plan)["ok"])

    def test_missing_or_wrongly_placed_answer_rejected(self):
        question = self.plan["questions"][0]
        for bad in (self.good.replace("### " + question["question"], "### 另一个问题", 1),
                    self.good.replace(question["answer"], "只有问题没有答案。", 1)):
            result = validate(self.original, bad, self.plan)
            self.assertIn("question_not_covered", self.codes(result))
            self.assertEqual(result["covered_questions"], 2)

    def test_fenced_question_is_not_an_answer_heading(self):
        q = self.plan["questions"][0]
        bad = self.good.replace("### " + q["question"], "```markdown\n### " + q["question"], 1)
        bad = bad.replace(q["answer"], q["answer"] + "\n```", 1)
        self.assertIn("question_not_covered", self.codes(validate(self.original, bad, self.plan)))

    def test_answer_without_source_is_not_passed(self):
        plan = copy.deepcopy(self.plan)
        plan["questions"][0]["support_ids"] = []
        self.assertIn("missing_answer_support", self.codes(validate(self.original, self.good, plan)))

    def test_unknown_sources_and_malformed_plan_rejected(self):
        mutations = [[], {**self.plan, "schema_version": True}, {**self.plan, "questions": []},
                     {**self.plan, "editable_sections": ["## 不存在的章节"]}]
        unknown = copy.deepcopy(self.plan)
        unknown["questions"][0]["support_ids"] = ["absent"]
        mutations.append(unknown)
        for plan in mutations:
            with self.subTest(plan=type(plan).__name__):
                with self.assertRaises(InputError):
                    validate(self.original, self.good, plan)

    def test_h2_added_removed_or_reordered_is_rejected(self):
        for bad in (self.good + "\n## 新章节\n内容\n",
                    self.good.replace("## 账号如何分开", "## 改过的章节", 1),
                    self.good.replace("## 账号如何分开", "## 临时名称", 1)
                    .replace("## 相同内容如何复用", "## 账号如何分开", 1)
                    .replace("## 临时名称", "## 相同内容如何复用", 1)):
            self.assertIn("section_structure_changed", self.codes(validate(self.original, bad, self.plan)))

    def test_duplicate_original_headings_rejected(self):
        with self.assertRaises(InputError):
            validate(self.original + "\n## 账号如何分开\n", self.good, self.plan)

    def test_h2_inside_code_fence_does_not_expand_scope(self):
        for fence in ("```", "~~~~"):
            code = f"\n{fence}markdown\n## 演示代码里的标题\n{fence}\n"
            original = self.original.replace("## 我的建议", code + "\n## 我的建议", 1)
            revised = self.good.replace("## 我的建议", code + "\n## 我的建议", 1)
            self.assertTrue(validate(original, revised, self.plan)["ok"])

    def test_crlf_is_supported_but_not_normalized(self):
        self.assertTrue(validate(self.original.replace("\n", "\r\n"), self.good.replace("\n", "\r\n"), self.plan)["ok"])
        self.assertIn("out_of_scope_change", self.codes(validate(self.original, self.good.replace("\n", "\r\n"), self.plan)))

    def test_cli_exit_codes_and_json_results(self):
        good = self.cli()
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertTrue(json.loads(good.stdout)["ok"])
        bad = self.cli(revised=ROOT / "examples/failure/不合格增强稿.md")
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertIn("unbacked_numeric", self.codes(json.loads(bad.stdout)))
        with tempfile.TemporaryDirectory() as temporary:
            missing = self.cli(original=Path(temporary) / "missing.md")
            self.assertEqual(missing.returncode, 2)
            self.assertEqual(self.codes(json.loads(missing.stdout)), {"invalid_input"})
            plan_path = Path(temporary) / "bad.json"
            for text in ("{broken", "[]", '{"schema_version":1,"schema_version":1}'):
                plan_path.write_text(text, encoding="utf-8")
                result = self.cli(plan=plan_path)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(self.codes(json.loads(result.stdout)), {"invalid_input"})

    def test_portable_package_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "moved-skill"
            shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", ".git"))
            result = self.cli(root=destination, cwd=temporary)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["covered_questions"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
