#!/usr/bin/env python3
"""
Data Bird 入口：编排 DataAgent -> AnalysisAgent -> ChartAgent -> InsightAgent。
支持命令行独立运行，或由平台/节点调用。
"""
import argparse
import json
import os
import sys
from pathlib import Path

# 允许从 skill 根目录执行
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.data_agent import run as data_run
from scripts.analysis_agent import run as analysis_run
from scripts.chart_agent import run as chart_run
from scripts.insight_agent import run as insight_run
from scripts.report_artifacts import generate_report_artifacts


def _load_skill_config() -> dict:
    cfg_path = Path(SKILL_ROOT) / "config" / "config.yaml"
    if not cfg_path.exists():
        return {}
    try:
        import yaml

        return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _apply_default_options(context: dict) -> dict:
    options = dict(context.get("options") or {})
    cfg = _load_skill_config()
    defaults = {
        "plan": cfg.get("plan", "free"),
        "min_chart_count": cfg.get("min_chart_count", 5),
        "max_chart_count": cfg.get("max_chart_count", 5),
        "max_report_chars": cfg.get("max_report_chars", 1000),
        "report_style": cfg.get("report_style", "consulting"),
        "max_rows": cfg.get("max_rows", 10000),
        "max_file_mb": cfg.get("max_file_mb", 10),
        "enable_mysql": cfg.get("enable_mysql", False),
    }
    for key, value in defaults.items():
        options.setdefault(key, value)
    context["options"] = options
    return context


def _build_report_md(context: dict) -> str:
    insight = context.get("insight") or {}
    charts = list(context.get("charts") or [])
    summary = context.get("summary") or context.get("schema") or {}
    scenario = summary.get("scenario_label") or summary.get("scenario") or "通用数据分析"
    lines = ["# 分析报告\n\n"]
    lines.append(f"- 报告风格：咨询式短报告\n")
    lines.append(f"- 数据场景：{scenario}\n")
    lines.append(f"- 图表数量：{len(charts)}\n\n")

    section_map = [
        ("## 执行摘要\n\n", insight.get("executiveSummary") or []),
        ("## 关键发现\n\n", insight.get("keyFindings") or insight.get("conclusions") or []),
        ("## 驱动分析\n\n", insight.get("driverAnalysis") or []),
        ("## 风险与机会\n\n", (insight.get("risks") or []) + (insight.get("opportunities") or [])),
        ("## 行动建议\n\n", insight.get("actionPlan") or insight.get("suggestions") or []),
    ]
    for header, items in section_map:
        if not items:
            continue
        lines.append(header)
        for item in items:
            lines.append(f"- {item}\n")
        lines.append("\n")

    chart_takeaways = [str(c.get("takeaway") or "").strip() for c in charts if str(c.get("takeaway") or "").strip()]
    if chart_takeaways:
        lines.append("## 图表要点\n\n")
        for item in chart_takeaways[:8]:
            lines.append(f"- {item}\n")
        lines.append("\n")
    return "".join(lines)


def run_pipeline(context: dict, llm_call=None, on_status=None) -> dict:
    """执行完整分析链路。"""
    context = _apply_default_options(context)
    context = data_run(context)
    if on_status:
        on_status("datasource_ready")
    context = analysis_run(context)
    if on_status:
        on_status("analyzing")
    context = chart_run(context)
    if on_status:
        on_status("chart_ready")
    context = insight_run(context, llm_call=llm_call)
    if on_status:
        on_status("insight_ready")

    context["summary"] = {
        **(context.get("schema") or {}),
        "detectedTimeColumn": next(
            (
                c["name"]
                for c in ((context.get("schema") or {}).get("columns") or [])
                if c.get("semanticType") == "time"
            ),
            None,
        ),
        "chartCount": len(context.get("charts") or []),
    }
    context["report_md"] = _build_report_md(context)

    artifacts = generate_report_artifacts(Path(SKILL_ROOT), context)
    context["artifacts"] = artifacts
    context["chart_paths"] = artifacts.get("chart_paths", [])
    context["chart_output_dir"] = artifacts.get("report_dir")
    context["chart_image_paths"] = artifacts.get("chart_image_paths", [])
    context["report_md_path"] = artifacts.get("report_md_path", "")
    context["report_html_path"] = artifacts.get("report_html_path", "")
    context["report_pdf_path"] = artifacts.get("report_pdf_path", "")
    context["report_pdf_error"] = artifacts.get("report_pdf_error", "")
    return context


def main():
    parser = argparse.ArgumentParser(description="Data Bird 数据分析")
    parser.add_argument("--query", "-q", default="分析数据趋势与分布", help="分析问题")
    parser.add_argument("--file", "-f", help="CSV/Excel 文件路径")
    parser.add_argument("--json", "-j", help="JSON 输入（含 datasource 等）")
    parser.add_argument("--stdin", "-i", action="store_true", help="从 stdin 读取 JSON 输入（供 OpenClaw invoke 调用）")
    parser.add_argument("--output", "-o", help="输出 JSON 文件")
    args = parser.parse_args()

    if args.stdin:
        try:
            context = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            out = {"success": False, "error": f"Stdin JSON 解析失败: {e}"}
            print(json.dumps(out, ensure_ascii=False))
            sys.exit(1)
    elif args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            context = json.load(f)
    elif args.file:
        context = {
            "query": args.query,
            "datasource": {
                "type": "csv",
                "config": {"file_path": os.path.abspath(args.file)},
            },
        }
    else:
        print("请提供 --file、--json 或 --stdin")
        sys.exit(1)

    try:
        result = run_pipeline(context)
        report_md = result.get("report_md", "")
        out = {
            "success": True,
            "charts": result.get("charts", []),
            "chart_paths": result.get("chart_paths", []),
            "chart_image_paths": result.get("chart_image_paths", []),
            "chart_output_dir": result.get("chart_output_dir"),
            "report_md_path": result.get("report_md_path", ""),
            "report_html_path": result.get("report_html_path", ""),
            "report_pdf_path": result.get("report_pdf_path", ""),
            "report_pdf_error": result.get("report_pdf_error", ""),
            "artifacts": result.get("artifacts", {}),
            "insight": result.get("insight", {}),
            "report_md": report_md,
            "reportMd": report_md,
            "summary": result.get("summary", {}),
            "analysis": result.get("analysis"),
        }
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(out, ensure_ascii=False, indent=2))
    except Exception as e:
        err_out = {"success": False, "error": str(e)}
        print(json.dumps(err_out, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
