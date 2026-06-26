#!/usr/bin/env python3
"""Smoke test for full_report output mode.

This test uses mock model outputs and verifies that the workflow produces a
client-delivery final_report.md instead of only a short summary.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_SECTIONS = [
    "## 老板能看懂的3句话结论",
    "## 执行摘要",
    "## 评估方法",
    "## 输入参数与目标市场",
    "## 探针问题列表",
    "## 双模型总评分表",
    "## 分场景检测结果",
    "## 品牌/产地/渠道提及分析",
    "## 竞品格局",
    "## 共同知识盲区",
    "## 本地化内容缺口",
    "## GEO 优化建议",
    "## 内容生产建议",
    "### 知乎选题",
    "### 小红书选题",
    "### 抖音短视频选题",
    "### 官网 FAQ 问题",
    "### GEO 友好型文章标题",
    "## 30天内容行动清单",
    "## 复测机制",
    "## 原始数据附录",
]

REQUIRED_SCORE_FIELDS = [
    "mention_rate",
    "ranking_position",
    "sentiment",
    "answer_depth",
    "factual_accuracy",
    "purchase_helpfulness",
    "localization_fit",
    "commercial_value",
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    input_file = repo / "examples" / "spanish_olive_oil_input.json"
    generator = repo / "scripts" / "generate_full_report.py"

    with tempfile.TemporaryDirectory(prefix="geo-full-report-") as tmp:
        output_dir = Path(tmp) / "geo_orchestrator_v2"
        result = subprocess.run(
            [sys.executable, str(generator), str(input_file), "--output-dir", str(output_dir)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert_true(result.returncode == 0, f"generate_full_report.py failed: {result.stderr}")

        final_report = output_dir / "final_report.md"
        summary = output_dir / "summary.md"
        comparison = output_dir / "dual_model_comparison.json"
        recommendations = output_dir / "content_recommendations.json"
        geo_actions = output_dir / "geo_action_priorities.json"
        probe_file = output_dir / "probe_questions.json"
        assert_true(final_report.exists(), "final_report.md was not created")
        assert_true(summary.exists(), "summary.md was not created")
        assert_true(comparison.exists(), "dual_model_comparison.json was not created")
        assert_true(recommendations.exists(), "content_recommendations.json was not created")
        assert_true(geo_actions.exists(), "geo_action_priorities.json was not created")
        assert_true(probe_file.exists(), "probe_questions.json was not created")

        report_text = final_report.read_text(encoding="utf-8")
        summary_text = summary.read_text(encoding="utf-8")
        stdout_text = result.stdout
        for section in REQUIRED_SECTIONS:
            assert_true(section in report_text, f"Missing section in final_report.md: {section}")
            assert_true(section in stdout_text, f"Missing section in stdout full report: {section}")
        assert_true(len(stdout_text) > len(summary_text) * 3, "stdout looks like a short summary, not a full report")

        probes = json.loads(probe_file.read_text(encoding="utf-8"))
        content_recommendations = json.loads(recommendations.read_text(encoding="utf-8"))
        assert_true(len(probes) >= 8, "Probe list must contain at least 8 categories")
        assert_true(len(content_recommendations["zhihu_topics"]) == 10, "Must generate 10 Zhihu topics")
        assert_true(len(content_recommendations["xiaohongshu_topics"]) == 10, "Must generate 10 Xiaohongshu topics")
        assert_true(len(content_recommendations["douyin_topics"]) == 10, "Must generate 10 Douyin topics")
        assert_true(len(content_recommendations["website_faq"]) == 10, "Must generate 10 website FAQ questions")
        assert_true(len(content_recommendations["geo_articles"]) == 5, "Must generate 5 GEO-friendly article titles")
        for group_name, items in content_recommendations.items():
            for item in items:
                for field in ("impact", "difficulty", "speed", "priority_score"):
                    assert_true(field in item, f"Missing priority field in {group_name}: {field}")
        models = ["doubao", "deepseek"]
        for model in models:
            model_score_path = output_dir / "model_scores" / f"{model}.json"
            assert_true(model_score_path.exists(), f"Missing model score file: {model_score_path}")
            score = json.loads(model_score_path.read_text(encoding="utf-8"))
            for field in REQUIRED_SCORE_FIELDS:
                assert_true(field in score["dimension_scores"], f"Missing score field for {model}: {field}")
            for probe in probes:
                raw_path = output_dir / "raw_answers" / model / f"{probe['probe_id']}.md"
                assert_true(raw_path.exists(), f"Missing raw answer file: {raw_path}")

    print("smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
