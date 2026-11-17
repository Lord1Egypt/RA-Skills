#!/usr/bin/env python3
"""Business regression checks using synthetic data; no network or live queries.

Copyright 2026 aimeGeo contributors. SPDX-License-Identifier: MIT-0
"""

import copy
import csv
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MODULE = importlib.util.spec_from_file_location("aggregate", ROOT / "scripts" / "aggregate.py")
agg = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(agg)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="geo-report-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / "inputs"
        shutil.copytree(ROOT / "examples" / "success", self.base)
        self.config = json.loads((self.base / "config.json").read_text(encoding="utf-8"))

    def run_build(self):
        return agg.build(copy.deepcopy(self.config), self.base.resolve())

    def metric(self, result, key, period="本期"):
        return result[period]["指标"][key]["value"]

    def rows(self, name):
        return json.loads((self.base / name).read_text(encoding="utf-8-sig"))

    def save(self, name, rows):
        (self.base / name).write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    def actual_answers(self):
        # Algorithm-only controlled fixture. These are never live measurement results.
        self.config["数据性质"] = "实际"
        for name in ("answers.json", "previous-answers.json"):
            rows = self.rows(name)
            for row in rows:
                if row["运行状态"] == "模拟":
                    row["运行状态"] = "已完成"
            self.save(name, rows)

    def add_business(self, **changes):
        row = {"项目": self.config["项目"], "日期": "2026-10-12", "记录ID": "biz1", "账号": "内容甲",
               "会话": 100, "转化会话": 5, "归因收入": 300, "成本": 100, "币种": "CNY", **changes}
        self.save("business.json", [row])
        self.config["本期"]["数据"]["经营"] = {"路径": "business.json", "覆盖": "完整", "数据截至": "2026-10-18",
                                                 "说明": "合成经营数据", "统计口径": "organic；7日点击归因；不重叠账号"}

    def test_article_and_publication_units_and_independent_states(self):
        r = self.run_build()
        expected = {"articles": 2, "publications": 4, "published_articles": 2,
                    "submitted": 3, "submission_failed": 1, "approved": 2,
                    "reviewing": 1, "review_unknown": 1, "public": 2,
                    "public_pending": 1, "not_public": 1, "indexed": 1,
                    "index_unrun": 2, "index_failed": 1}
        self.assertEqual({k: self.metric(r, k) for k in expected}, expected)
        self.assertEqual(r["比较"]["articles"]["delta"], 1)
        self.assertEqual(r["比较"]["articles"]["percent"], 100)
        self.assertIsNone(self.metric(r, "roi"))

    def test_simulation_is_never_actual_zero_citations(self):
        r = self.run_build()
        self.assertEqual(self.metric(r, "ai_completed"), 0)
        self.assertIsNone(self.metric(r, "ai_cited"))
        self.assertIsNone(self.metric(r, "ai_citation_rate"))
        self.assertEqual(self.metric(r, "ai_simulated"), 2)
        self.assertEqual(self.metric(r, "ai_failed"), 1)
        self.assertEqual(self.metric(r, "ai_unrun"), 1)
        self.assertEqual(self.metric(r, "sim_citation_rate"), 50)

    def test_actual_denominator_excludes_failed_unrun_and_simulated(self):
        self.actual_answers()
        rows = self.rows("answers.json")
        extra = {**rows[0], "记录ID": "sim-extra", "运行状态": "模拟"}
        rows.append(extra)
        rows[0]["原生引用"].append({"url": "https://example.org/second", "归属": "本项目"})
        self.save("answers.json", rows)
        r = self.run_build()
        self.assertEqual(self.metric(r, "ai_citation_rate"), 50)
        self.assertEqual(r["本期"]["指标"]["ai_citation_rate"]["denominator"], 2)
        self.assertEqual(self.metric(r, "ai_cited"), 1)  # two citations, one cited answer
        self.assertEqual(self.metric(r, "ai_mentions"), 1)

    def test_only_native_target_citations_count(self):
        self.actual_answers()
        rows = self.rows("answers.json")
        rows[0]["原生引用"][0]["归属"] = "其他"
        rows[0]["回答"] = "品牌提及与普通文本链接 https://example.org/article/a1"
        self.save("answers.json", rows)
        r = self.run_build()
        self.assertEqual(self.metric(r, "ai_citation_rate"), 0)
        self.assertEqual(self.metric(r, "ai_mentions"), 1)

    def test_empty_samples_and_absent_baseline_are_na(self):
        p = ROOT / "examples" / "no-samples"
        r = agg.build(json.loads((p / "config.json").read_text()), p)
        self.assertIsNone(self.metric(r, "ai_citation_rate"))
        self.assertEqual(r["本期"]["指标"]["ai_citation_rate"]["denominator"], 0)
        self.assertTrue(all(v["delta"] is None and v["percent"] is None for v in r["比较"].values()))
        self.assertIsNone(r["上期"])

    def test_known_empty_article_export_is_zero_not_missing(self):
        self.save("empty.json", [])
        self.config["本期"]["数据"]["文章"]["路径"] = "empty.json"
        r = self.run_build()
        self.assertEqual(self.metric(r, "articles"), 0)
        del self.config["本期"]["数据"]["文章"]
        self.assertIsNone(self.metric(self.run_build(), "articles"))

    def test_account_filter_keeps_project_article_and_ai_scope(self):
        self.config["账号"] = ["内容乙"]
        r = self.run_build()
        self.assertEqual(self.metric(r, "articles"), 2)
        self.assertEqual(self.metric(r, "publications"), 2)
        self.assertEqual(self.metric(r, "indexed"), 1)
        self.assertEqual(self.metric(r, "ai_simulated"), 2)

    def test_account_whitespace_is_normalized_before_filtering(self):
        self.config["账号"] = [" \t内容甲 \u3000"]
        self.add_business(账号=" \t内容甲 \u3000")
        business = self.rows("business.json")
        business.append({**business[0], "记录ID": "biz2", "账号": "内容乙", "会话": 900})
        publications = {}
        for period in ("本期", "上期"):
            spec = self.config[period]["数据"]["发布"]
            with (self.base / spec["路径"]).open(encoding="utf-8-sig", newline="") as handle:
                publications[period] = list(csv.DictReader(handle))
            for row in publications[period]:
                if row["账号"] == "内容甲":
                    row["账号"] = " \t内容甲 \u3000"
        for suffix in ("json", "csv"):
            with self.subTest(format=suffix):
                exports = [(period, "发布", rows) for period, rows in publications.items()]
                exports.append(("本期", "经营", business))
                for period, table, rows in exports:
                    filename = f"{period}-{table}.{suffix}"
                    self.config[period]["数据"][table]["路径"] = filename
                    if suffix == "json":
                        self.save(filename, rows)
                    else:
                        with (self.base / filename).open("w", encoding="utf-8", newline="") as handle:
                            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                            writer.writeheader()
                            writer.writerows(rows)
                r = self.run_build()
                self.assertEqual(r["账号筛选"], ["内容甲"])
                self.assertEqual(self.metric(r, "publications"), 2)
                self.assertEqual(self.metric(r, "publications", "上期"), 1)
                self.assertEqual(self.metric(r, "published_articles"), 2)
                self.assertEqual(self.metric(r, "sessions"), 100)
                self.assertEqual(self.metric(r, "revenue"), 300)
                self.assertEqual(self.metric(r, "cvr"), 5)
                self.assertEqual(self.metric(r, "roi"), 200)
                self.assertEqual(r["比较"]["publications"]["delta"], 1)
                for table, counts in (("发布", (2, 2)), ("经营", (1, 1))):
                    source = r["本期"]["来源"][table]
                    self.assertEqual((source["选中行数"], source["排除行数"]), counts)

    def test_duplicate_config_accounts_are_checked_after_trimming(self):
        self.config["账号"] = [" 内容甲 ", "内容甲\u3000"]
        with self.assertRaisesRegex(agg.DataError, "账号筛选重复"):
            self.run_build()

    def test_invalid_account_is_rejected_before_filtering(self):
        self.config["账号"] = ["内容甲"]
        self.add_business()
        with (self.base / "publications.csv").open(encoding="utf-8-sig", newline="") as handle:
            publications = list(csv.DictReader(handle))
        original = copy.deepcopy(self.config)
        for table, rows in (("发布", publications), ("经营", self.rows("business.json"))):
            for invalid in (None, " \t\u3000", 123, ["内容甲"]):
                with self.subTest(table=table, account=invalid):
                    self.config = copy.deepcopy(original)
                    changed = copy.deepcopy(rows)
                    changed[0]["账号"] = invalid
                    self.save("invalid-account.json", changed)
                    self.config["本期"]["数据"][table]["路径"] = "invalid-account.json"
                    with self.assertRaisesRegex(agg.DataError, f"{table} 第 1 条: 账号 必须为非空字符串"):
                        self.run_build()

    def test_csv_account_scope_matches_metric_values(self):
        self.actual_answers()
        self.add_business(账号="内容乙")
        business = self.rows("business.json")
        business.append({**business[0], "记录ID": "biz2", "账号": "内容甲", "会话": 900})
        self.save("business.json", business)
        for accounts, scope, publications, sessions in (
                (["内容乙"], "内容乙", 2, 100), ([], "全部导出账号", 4, 1000)):
            with self.subTest(accounts=accounts):
                self.config["账号"] = accounts
                r = self.run_build()
                out = Path(self.temp.name) / f"scope-{len(accounts)}"
                agg.write_outputs(r, out)
                with (out / "指标明细.csv").open(encoding="utf-8-sig", newline="") as handle:
                    rows = {row["指标"]: row for row in csv.DictReader(handle)}
                self.assertEqual(rows["新增文章数"]["本期"], "2")
                self.assertEqual(float(rows["实际原生引用率"]["本期"]), 50)
                self.assertEqual(rows["实际原生引用率"]["本期分母"], "2")
                self.assertEqual(rows["发布记录数"]["本期"], str(publications))
                self.assertEqual(rows["会话数"]["本期"], str(sessions))
                for label in ("新增文章数", "实际完成回答", "实际原生引用率", "实际品牌提及率", "模拟原生引用率"):
                    self.assertEqual(rows[label]["账号范围"], "项目级（账号筛选不适用）")
                for label in ("发布记录数", "涉及文章数", "公开已验证", "会话数", "归因收入", "ROI"):
                    self.assertEqual(rows[label]["账号范围"], scope)

    def test_period_and_project_filter_and_excluded_audit(self):
        rows = self.rows("answers.json")
        rows.extend([{**rows[0], "项目": "其他项目"}, {**rows[0], "日期": "2026-10-11"}])
        self.save("answers.json", rows)
        r = self.run_build()
        self.assertEqual(r["本期"]["来源"]["AI回答"]["排除行数"], 2)
        self.assertEqual(self.metric(r, "ai_simulated"), 2)

    def test_missing_prior_and_zero_prior_have_distinct_deltas(self):
        del self.config["上期"]
        r = self.run_build()
        self.assertIsNone(r["比较"]["articles"]["delta"])
        self.setUp_baseline_zero()
        r = self.run_build()
        self.assertEqual(r["比较"]["articles"]["delta"], 2)
        self.assertIsNone(r["比较"]["articles"]["percent"])

    def setUp_baseline_zero(self):
        self.save("zero.json", [])
        self.config["上期"] = {"开始": "2026-10-05", "结束": "2026-10-11", "数据": {
            "文章": {"路径": "zero.json", "覆盖": "完整", "数据截至": "2026-10-11", "说明": "合成零文章基线"}}}

    def test_panel_period_coverage_and_snapshot_changes_block_comparison(self):
        original = copy.deepcopy(self.config)
        for change in ("panel", "duration", "coverage", "lag", "definition"):
            with self.subTest(change=change):
                self.config = copy.deepcopy(original)
                key = "articles"
                if change == "panel":
                    self.config["本期"]["数据"]["AI回答"]["路径"] = "changed.json"
                    rows = self.rows("answers.json"); rows[0]["问题ID"] = "other"
                    self.save("changed.json", rows); key = "sim_citation_rate"
                elif change == "duration": self.config["上期"]["开始"] = "2026-10-04"
                elif change == "coverage": self.config["本期"]["数据"]["文章"]["覆盖"] = "部分"
                elif change == "lag":
                    self.config["本期"]["数据"]["发布"]["数据截至"] = "2026-10-19"; key = "public"
                else: self.config["本期"]["数据"]["文章"]["统计口径"] = "变更"
                r = self.run_build()
                self.assertIsNone(r["比较"][key]["delta"])
                self.assertTrue(r["比较"][key]["reason"])

    def test_percentage_points_and_relative_change(self):
        self.actual_answers()
        rows = self.rows("previous-answers.json")
        rows[1]["原生引用"] = rows[0]["原生引用"]
        self.save("previous-answers.json", rows)
        r = self.run_build()
        self.assertEqual(r["比较"]["ai_citation_rate"]["delta"], -50)
        self.assertEqual(r["比较"]["ai_citation_rate"]["percent"], -50)

    def test_actual_effect_comparison_rejects_a_failed_or_unrun_answer_in_the_same_plan(self):
        self.actual_answers()
        original = self.rows("answers.json")
        for state in ("查询失败", "未运行"):
            with self.subTest(state=state):
                rows = copy.deepcopy(original)
                rows[1]["运行状态"] = state
                for field in ("回答", "品牌提及", "原生引用", "证据"):
                    rows[1].pop(field, None)
                if state == "查询失败":
                    rows[1]["错误"] = "合成超时"
                self.save("answers.json", rows)
                r = self.run_build()
                self.assertEqual(self.metric(r, "ai_citation_rate"), 100)
                self.assertEqual(self.metric(r, "ai_citation_rate", "上期"), 50)
                for key in ("ai_mentions", "ai_cited", "ai_mention_rate", "ai_citation_rate"):
                    self.assertIsNone(r["比较"][key]["delta"])
                    self.assertIsNone(r["比较"][key]["percent"])
                    self.assertIn("实际有效回答", r["比较"][key]["reason"])
                # Operational counts still compare the same planned panel.
                self.assertEqual(r["比较"]["ai_completed"]["delta"], -1)

    def test_equal_answer_counts_do_not_hide_a_changed_effective_question_panel(self):
        self.actual_answers()
        rows = self.rows("answers.json")
        replacement = {**rows[1], "记录ID": rows[2]["记录ID"], "问题ID": rows[2]["问题ID"]}
        rows[1] = {key: value for key, value in rows[1].items()
                   if key not in ("回答", "品牌提及", "原生引用", "证据")}
        rows[1].update({"运行状态": "查询失败", "错误": "合成超时"})
        rows[2] = replacement
        self.save("answers.json", rows)
        r = self.run_build()
        self.assertEqual(r["本期"]["指标"]["ai_citation_rate"]["denominator"], 2)
        self.assertEqual(r["上期"]["指标"]["ai_citation_rate"]["denominator"], 2)
        self.assertIsNone(r["比较"]["ai_citation_rate"]["delta"])
        self.assertIn("实际有效回答", r["比较"]["ai_citation_rate"]["reason"])

    def test_repeated_runs_are_compared_as_counts_not_only_unique_questions(self):
        self.actual_answers()
        rows = self.rows("answers.json")
        rows.append({**rows[0], "记录ID": "second-run"})
        self.save("answers.json", rows)
        r = self.run_build()
        self.assertEqual(r["本期"]["指标"]["ai_citation_rate"]["denominator"], 3)
        self.assertIsNone(r["比较"]["ai_citation_rate"]["delta"])

    def test_business_totals_cvr_and_roi(self):
        self.add_business()
        r = self.run_build()
        self.assertEqual(self.metric(r, "sessions"), 100)
        self.assertEqual(self.metric(r, "cvr"), 5)
        self.assertEqual(self.metric(r, "roi"), 200)
        self.assertEqual(r["本期"]["指标"]["revenue"]["unit"], "CNY")

    def test_csv_preserves_each_period_currency_and_never_labels_usd_as_cny(self):
        self.add_business()
        self.save("previous-business.json", [{**self.rows("business.json")[0],
                  "日期": "2026-10-05", "归因收入": 50, "成本": 25, "币种": "USD"}])
        self.config["上期"]["数据"]["经营"] = {**self.config["本期"]["数据"]["经营"],
                                                     "路径": "previous-business.json", "数据截至": "2026-10-11"}
        r = self.run_build()
        out = Path(self.temp.name) / "currency-output"
        agg.write_outputs(r, out)
        with (out / "指标明细.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["指标"]: row for row in csv.DictReader(handle)}
        revenue = rows["归因收入"]
        self.assertEqual((float(revenue["本期"]), float(revenue["上期"])), (300, 50))
        self.assertEqual((revenue["本期单位"], revenue["上期单位"]), ("CNY", "USD"))
        self.assertEqual(revenue["单位"], "本期/上期不同")
        self.assertEqual((revenue["变化量"], revenue["变化单位"]), ("N/A", "N/A"))
        self.assertIn("币种不同", revenue["比较说明"])
        self.assertEqual((rows["成本"]["本期单位"], rows["成本"]["上期单位"]), ("CNY", "USD"))

    def test_csv_keeps_units_when_one_period_has_no_business_data(self):
        self.add_business()
        r = self.run_build()
        out = Path(self.temp.name) / "missing-currency-output"
        agg.write_outputs(r, out)
        with (out / "指标明细.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = {row["指标"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["归因收入"]["本期单位"], "CNY")
        self.assertEqual(rows["归因收入"]["上期单位"], "货币单位未提供")
        self.assertEqual(rows["归因收入"]["上期"], "N/A")

    def test_missing_or_zero_inputs_never_create_roi(self):
        for fields in ({"成本": None}, {"成本": 0}, {"会话": None}, {"会话": 0, "转化会话": 0}, {"归因收入": None}):
            with self.subTest(fields=fields):
                self.add_business(**fields)
                self.assertIsNone(self.metric(self.run_build(), "roi"))
        self.add_business()
        del self.config["本期"]["数据"]["经营"]["统计口径"]
        self.assertIsNone(self.metric(self.run_build(), "roi"))

    def test_partial_numeric_fields_do_not_silently_sum_subset(self):
        self.add_business()
        rows = self.rows("business.json")
        rows.append({**rows[0], "记录ID": "biz2", "成本": None})
        self.save("business.json", rows)
        r = self.run_build()
        self.assertEqual(self.metric(r, "sessions"), 200)
        self.assertIsNone(self.metric(r, "cost"))
        self.assertIsNone(self.metric(r, "roi"))

    def test_csv_json_equivalence(self):
        original = self.run_build()
        for table in ("文章", "发布"):
            spec = self.config["本期"]["数据"][table]
            with (self.base / spec["路径"]).open(encoding="utf-8-sig", newline="") as h:
                rows = list(csv.DictReader(h))
            spec["路径"] = f"{table}.json"
            self.save(spec["路径"], rows)
        # Also test CSV's JSON-encoded citation arrays.
        rows = self.rows("answers.json")
        fields = list(dict.fromkeys(k for row in rows for k in row))
        with (self.base / "answers.csv").open("w", encoding="utf-8", newline="") as h:
            writer = csv.DictWriter(h, fieldnames=fields); writer.writeheader()
            for row in rows:
                if "原生引用" in row: row["原生引用"] = json.dumps(row["原生引用"])
                writer.writerow(row)
        self.config["本期"]["数据"]["AI回答"]["路径"] = "answers.csv"
        self.assertEqual(original["本期"]["指标"], self.run_build()["本期"]["指标"])

    def test_failure_fixture_rejects_unknown_citation_collection(self):
        p = ROOT / "examples" / "failure"
        with self.assertRaisesRegex(agg.DataError, "空白不等于零引用"):
            agg.build(json.loads((p / "config.json").read_text()), p)

    def test_reject_bad_state_duplicate_missing_answer_or_evidence(self):
        original = self.rows("answers.json")
        for issue in ("state", "duplicate", "answer", "evidence", "url", "false_failed_result"):
            with self.subTest(issue=issue):
                rows = copy.deepcopy(original)
                if issue == "state": rows[0]["运行状态"] = "成功啦"
                elif issue == "duplicate": rows.append(rows[0])
                elif issue == "answer": rows[0]["回答"] = ""
                elif issue == "evidence": del rows[0]["证据"]
                elif issue == "url": rows[0]["原生引用"][0]["url"] = "file:///made-up"
                else: rows[2]["品牌提及"] = "否"
                self.save("answers.json", rows)
                with self.assertRaises(agg.DataError): self.run_build()

    def test_reject_unverified_publication_and_index_claims(self):
        self.config["本期"]["数据"]["发布"]["路径"] = "pubs.json"
        with (self.base / "publications.csv").open(encoding="utf-8-sig", newline="") as h:
            original = list(csv.DictReader(h))
        for field, idx in (("投稿证据", 0), ("公开证据", 0), ("收录证据", 1)):
            rows = copy.deepcopy(original); rows[idx][field] = ""
            self.save("pubs.json", rows)
            with self.assertRaises(agg.DataError): self.run_build()

    def test_reject_mixed_currency_nonfinite_negative_and_invalid_conversion(self):
        for fields in ({"成本": -1}, {"成本": "NaN"}, {"成本": "Infinity"}, {"会话": 1.5}, {"转化会话": 101}):
            with self.subTest(fields=fields):
                self.add_business(**fields)
                with self.assertRaises(agg.DataError): self.run_build()
        self.add_business()
        rows = self.rows("business.json"); rows.append({**rows[0], "记录ID": "biz2", "币种": "USD"})
        self.save("business.json", rows)
        with self.assertRaisesRegex(agg.DataError, "币种混用"): self.run_build()

    def test_reject_bad_dates_overlap_stale_source_and_path_escape(self):
        original = copy.deepcopy(self.config)
        for issue in ("date", "overlap", "stale", "escape"):
            self.config = copy.deepcopy(original)
            if issue == "date": self.config["本期"]["开始"] = "2026-02-30"
            elif issue == "overlap": self.config["上期"]["结束"] = "2026-10-12"
            elif issue == "stale": self.config["本期"]["数据"]["文章"]["数据截至"] = "2026-10-17"
            else: self.config["本期"]["数据"]["文章"]["路径"] = "../other.csv"
            with self.assertRaises(agg.DataError): self.run_build()

    def test_cli_outputs_and_failure_exit_without_artifacts(self):
        out = Path(self.temp.name) / "result"
        cmd = [sys.executable, "-B", str(ROOT / "scripts" / "aggregate.py"), "--input", str(self.base / "config.json"), "--output", str(out)]
        completed = subprocess.run(cmd, cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        r = json.loads((out / "summary.json").read_text())
        self.assertEqual(self.metric(r, "publications"), 4)
        with (out / "指标明细.csv").open(encoding="utf-8-sig", newline="") as h:
            rows = {row["指标"]: row for row in csv.DictReader(h)}
        self.assertEqual(rows["实际原生引用率"]["本期"], "N/A")
        self.assertEqual(rows["模拟原生引用率"]["本期分母"], "2")
        self.assertEqual(rows["新增文章数"]["变化量"], "1")
        again = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(again.returncode, 2)
        bad_out = Path(self.temp.name) / "bad-result"
        cmd[cmd.index("--input") + 1] = str(ROOT / "examples" / "failure" / "config.json")
        cmd[-1] = str(bad_out)
        failed = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 2)
        self.assertFalse(bad_out.exists())

    def test_csv_formula_cells_are_escaped_but_numbers_are_numeric(self):
        self.assertEqual(agg.csv_safe("=1+1"), "'=1+1")
        self.assertEqual(agg.csv_safe(" @SUM(A1)"), "' @SUM(A1)")
        self.assertEqual(agg.csv_safe(-50), -50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
