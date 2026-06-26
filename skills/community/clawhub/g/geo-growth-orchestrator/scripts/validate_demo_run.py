#!/usr/bin/env python3
"""Validate the Spanish ham demo run artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "spanish_ham_demo"

REQUIRED_DIRS = [
    "00_input",
    "01_brand_knowledge_base",
    "02_geo_audit",
    "03_gap_matrix",
    "04_content_task_plan",
    "05_content_assets",
    "06_platform_drafts",
    "07_delivery",
    "08_monitoring",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not RUN.exists():
        errors.append("runs/spanish_ham_demo/ does not exist")
        return errors, warnings

    for directory in REQUIRED_DIRS:
        if not (RUN / directory).is_dir():
            errors.append(f"required directory missing: {directory}")

    summary_path = RUN / "orchestrator_run_summary.json"
    summary = {}
    if not summary_path.exists():
        errors.append("orchestrator_run_summary.json is missing")
    else:
        try:
            summary = load_json(summary_path)
        except json.JSONDecodeError as exc:
            errors.append(f"orchestrator_run_summary.json is invalid JSON: {exc}")

    gap_path = RUN / "03_gap_matrix" / "geo_gap_matrix.json"
    if not gap_path.exists():
        errors.append("03_gap_matrix/geo_gap_matrix.json is missing")
    else:
        gap_data = load_json(gap_path)
        gaps = gap_data.get("gaps", [])
        if len(gaps) < 7:
            errors.append(f"geo_gap_matrix.json must contain at least 7 gaps, got {len(gaps)}")
        required_gap_fields = {
            "gap_id",
            "gap_name",
            "severity",
            "affected_model",
            "affected_queries",
            "evidence_summary",
            "business_impact",
            "recommended_content_direction",
            "target_platforms",
            "expected_geo_effect",
        }
        for gap in gaps:
            missing = required_gap_fields - set(gap)
            if missing:
                errors.append(f"{gap.get('gap_id', '<unknown>')} missing gap fields: {', '.join(sorted(missing))}")

    task_path = RUN / "04_content_task_plan" / "content_task_plan.json"
    if not task_path.exists():
        errors.append("04_content_task_plan/content_task_plan.json is missing")
    else:
        task_data = load_json(task_path)
        tasks = task_data.get("tasks", [])
        if len(tasks) < 19:
            errors.append(f"content_task_plan.json must contain at least 19 tasks, got {len(tasks)}")
        counts = {}
        for task in tasks:
            counts[task.get("platform", "")] = counts.get(task.get("platform", ""), 0) + 1
        expected_counts = {
            "知乎": 5,
            "今日头条": 5,
            "官网 FAQ": 3,
            "小红书": 3,
            "抖音": 3,
        }
        for platform, minimum in expected_counts.items():
            if counts.get(platform, 0) < minimum:
                errors.append(f"{platform} must contain at least {minimum} tasks, got {counts.get(platform, 0)}")

    if not (RUN / "04_content_task_plan" / "platform_distribution_plan.json").exists():
        errors.append("04_content_task_plan/platform_distribution_plan.json is missing")

    report_path = RUN / "07_delivery" / "client_delivery_report.md"
    if not report_path.exists():
        errors.append("07_delivery/client_delivery_report.md is missing")
    else:
        report = report_path.read_text(encoding="utf-8")
        if "老板能看懂的 3 句话结论" not in report:
            errors.append("client_delivery_report.md missing 老板能看懂的 3 句话结论")
        if len(report.strip().splitlines()) < 80:
            errors.append("client_delivery_report.md is too short and may be summary-only")
        required_sections = [
            "本次 GEO 工作流做了什么",
            "当前 AI 对西班牙火腿的认知现状",
            "DeepSeek / Doubao 评估摘要",
            "双模型共同盲区",
            "中国本地化场景缺口",
            "内容增长机会",
            "建议优先发布的内容清单",
            "各平台发布建议",
            "30 天执行计划",
            "7 / 14 / 30 天复测机制",
            "本次生成文件清单",
        ]
        for section in required_sections:
            if section not in report:
                errors.append(f"client_delivery_report.md missing section: {section}")
        if summary.get("execution_mode") == "mock_orchestration_demo":
            if "本报告为编排演示" not in report or "不代表真实模型实测结果" not in report:
                errors.append("mock execution mode requires explicit mock disclaimer in client report")

    if not (RUN / "08_monitoring" / "retest_plan.md").exists():
        errors.append("08_monitoring/retest_plan.md is missing")

    if summary:
        if summary.get("execution_mode") not in {"mock_orchestration_demo", "real_skill_call"}:
            errors.append("orchestrator_run_summary.json has invalid execution_mode")
        if not summary.get("stages"):
            errors.append("orchestrator_run_summary.json missing stages")
        if not summary.get("generated_artifacts"):
            warnings.append("orchestrator_run_summary.json generated_artifacts is empty")

    return errors, warnings


def main() -> int:
    errors, warnings = validate()
    result = {
        "status": "failed" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
        "run_dir": str(RUN),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
