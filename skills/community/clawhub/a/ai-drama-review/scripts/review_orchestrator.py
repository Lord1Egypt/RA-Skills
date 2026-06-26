"""
审查流程编排器

协调版权检测、年龄分级、魔改检测三大模块，
输出统一的合规报告。
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from env_detect import run_full_detection, determine_run_mode, detect_api_keys
from text_similarity import scan_for_plagiarism, CopyrightReport
from age_rating_scanner import run_age_rating_scan, RatingResult
from adaptation_detector import detect_adaptation, AdaptationReport
from report_generator import (
    build_full_report, generate_json_report, generate_markdown_report,
)


def load_input_text(file_path: str) -> str:
    """加载输入文件（支持 .txt / .srt / .json）。"""
    path = Path(file_path)
    suffix = path.suffix.lower()

    text = path.read_text(encoding="utf-8")

    if suffix == ".json":
        data = json.loads(text)
        # 尝试提取常见字段
        if isinstance(data, dict):
            parts = []
            for key in ["script", "text", "content", "dialogue", "subtitles"]:
                if key in data:
                    val = data[key]
                    if isinstance(val, str):
                        parts.append(val)
                    elif isinstance(val, list):
                        parts.extend(
                            item.get("text", str(item))
                            if isinstance(item, dict) else str(item)
                            for item in val
                        )
            return "\n".join(parts) if parts else text
        return text

    if suffix == ".srt":
        # 提取 SRT 字幕中的文本行
        lines = []
        for line in text.split("\n"):
            line = line.strip()
            # 跳过序号行、时间码行、空行
            if not line or line.isdigit() or "-->" in line:
                continue
            lines.append(line)
        return "\n".join(lines)

    return text


def load_reference_texts(reference_dir: str) -> dict:
    """加载参考文本库。"""
    ref_dir = Path(reference_dir)
    if not ref_dir.exists():
        return {}

    texts = {}
    for f in ref_dir.iterdir():
        if f.suffix.lower() in (".txt", ".md"):
            texts[f.stem] = f.read_text(encoding="utf-8")
    return texts


def _copyright_result_to_dict(report: CopyrightReport) -> dict:
    """将 CopyrightReport 转为字典。"""
    return {
        "total_paragraphs": report.total_paragraphs,
        "suspicious_paragraphs": report.suspicious_paragraphs,
        "max_similarity_score": report.max_similarity_score,
        "risk_level": report.risk_level,
        "results": [
            {
                "source_paragraph_index": r.source_paragraph_index,
                "source_text": r.source_text,
                "reference_id": r.reference_id,
                "combined_score": r.combined_score,
            }
            for r in report.results
        ],
    }


def _rating_result_to_dict(result: RatingResult) -> dict:
    """将 RatingResult 转为字典。"""
    return {
        "suggested_rating": result.suggested_rating,
        "target_rating": result.target_rating,
        "is_compliant": result.is_compliant,
        "total_hits": result.total_hits,
        "hits_by_category": result.hits_by_category,
        "hits_by_severity": result.hits_by_severity,
        "risk_level": result.risk_level,
        "keyword_hits": [
            {
                "keyword": h.keyword,
                "category": h.category,
                "severity": h.severity,
                "paragraph_index": h.paragraph_index,
                "context": h.context,
                "timestamp": h.timestamp,
            }
            for h in result.keyword_hits[:50]  # 限制数量
        ],
    }


def _adaptation_result_to_dict(report: AdaptationReport) -> dict:
    """将 AdaptationReport 转为字典。"""
    return {
        "deviation_score": report.deviation_score,
        "adaptation_type": report.adaptation_type,
        "total_deviations": report.total_deviations,
        "deviations_by_type": report.deviations_by_type,
        "deviations_by_severity": report.deviations_by_severity,
        "deviation_items": [
            {
                "type": d.deviation_type,
                "severity": d.severity,
                "description": d.description,
                "original": d.original_content[:100],
                "adapted": d.adapted_content[:100],
            }
            for d in report.deviation_items[:20]
        ],
    }


def format_user_warning(report_dict: dict) -> str:
    """
    格式化用户风险提示文本。

    当检测到违规时，标注并提示模型告知用户该视频可能存在的违规风险。
    """
    risk = report_dict.get("overall_risk_level", "low")
    score = report_dict.get("overall_score", 100)
    violations = report_dict.get("violation_summary", [])

    if risk == "low" and not violations:
        return "当前内容未发现明显合规风险。"

    risk_labels = {
        "low": "低风险",
        "medium": "中等风险",
        "high": "高风险",
        "critical": "严重风险",
    }

    lines = [
        f"[合规警告] 该内容存在 {risk_labels.get(risk, risk)} (合规得分: {score}/100)",
        "",
    ]

    for v in violations:
        type_labels = {
            "copyright": "版权侵权",
            "age_rating": "年龄分级",
            "adaptation": "小说魔改",
        }
        label = type_labels.get(v["type"], v["type"])
        lines.append(f"  - [{v['severity'].upper()}] {label}: {v['description']}")

    lines.append("")

    suggestions = report_dict.get("remediation_suggestions", [])
    if suggestions:
        lines.append("整改建议:")
        for s in suggestions:
            lines.append(f"  - {s}")

    lines.append("")
    lines.append("注意: 以上检测结果仅供参考，不作为法律依据。建议进行人工复核。")

    return "\n".join(lines)


def run_full_review(input_file: str,
                    reference_dir: str = None,
                    original_file: str = None,
                    target_rating: str = "all_ages",
                    checks: list = None,
                    output_format: str = "json") -> dict:
    """
    执行完整审查流程。

    Args:
        input_file: 输入剧本/台词文件
        reference_dir: 参考文本库目录（版权检测用）
        original_file: 原著文件路径（魔改检测用）
        target_rating: 目标年龄分级
        checks: 要执行的检测模块列表
        output_format: 输出格式 ("json" 或 "markdown")

    Returns:
        完整审查结果字典
    """
    if checks is None:
        checks = ["copyright", "rating", "adaptation"]

    # 加载输入
    input_text = load_input_text(input_file)

    copyright_result = None
    age_rating_result = None
    adaptation_result = None

    # 版权检测
    if "copyright" in checks and reference_dir:
        ref_texts = load_reference_texts(reference_dir)
        if ref_texts:
            cr = scan_for_plagiarism(input_text, ref_texts)
            copyright_result = _copyright_result_to_dict(cr)

    # 年龄分级检测
    if "rating" in checks:
        rr = run_age_rating_scan(input_text, target_rating)
        age_rating_result = _rating_result_to_dict(rr)

    # 魔改检测
    if "adaptation" in checks and original_file:
        orig_path = Path(original_file)
        if orig_path.exists():
            orig_text = orig_path.read_text(encoding="utf-8")
            ar = detect_adaptation(orig_text, input_text)
            adaptation_result = _adaptation_result_to_dict(ar)

    # 构建报告
    report = build_full_report(
        input_file, copyright_result, age_rating_result, adaptation_result
    )

    if output_format == "markdown":
        formatted = generate_markdown_report(report)
    else:
        formatted = generate_json_report(report)

    # 生成用户警告
    report_dict = json.loads(generate_json_report(report))
    warning = format_user_warning(report_dict)

    return {
        "report": report_dict,
        "formatted": formatted,
        "warning": warning,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI短剧规范审查")
    parser.add_argument("--input", required=True, help="剧本/台词文件路径")
    parser.add_argument("--reference-dir", help="参考文本库目录（版权检测用）")
    parser.add_argument("--original", help="原著文件路径（魔改检测用）")
    parser.add_argument("--target-rating", default="all_ages",
                        choices=["all_ages", "12+", "18+"])
    parser.add_argument("--checks", nargs="+",
                        default=["copyright", "rating", "adaptation"],
                        choices=["copyright", "rating", "adaptation"])
    parser.add_argument("--output", default="json",
                        choices=["json", "markdown"])

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    result = run_full_review(
        input_file=str(input_path),
        reference_dir=args.reference_dir,
        original_file=args.original,
        target_rating=args.target_rating,
        checks=args.checks,
        output_format=args.output,
    )

    print(result["formatted"])
    print()
    print("=== 风险提示 ===")
    print(result["warning"])
