#!/usr/bin/env python3
"""检查生成的 AI 职业机会与学习路线报告。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CONCEPT_GROUPS = {
    "执行摘要": ("执行摘要", "核心结论", "executive summary"),
    "个人画像": ("个人画像", "候选人画像", "profile"),
    "产业方向": ("产业发展", "产业地图", "行业趋势", "industry map"),
    "公司机会": ("公司地图", "公司机会", "目标公司", "company"),
    "职位方向": ("职位方向", "岗位方向", "岗位地图", "role"),
    "能力差距": ("能力差距", "技能差距", "gap analysis"),
    "学习计划": ("学习计划", "学习路线", "weekly plan"),
    "作品集": ("作品集", "项目作品", "portfolio"),
    "求职行动": ("求职行动", "投递策略", "申请策略", "application"),
    "来源": ("来源", "参考资料", "sources"),
}

LAYER_GROUPS = {
    "通用知识": ("通用知识", "通识", "共通知识", "common knowledge"),
    "职位知识": ("职位知识", "岗位知识", "岗位专项", "role-specific"),
    "行业知识": ("行业知识", "行业专项", "领域知识", "industry-specific"),
}

PLACEHOLDER_PATTERNS = (
    r"YYYY-MM-DD",
    r"第\s*[NnXx]\s*周",
    r"\bTODO\b",
    r"\[\s*TODO[^\]]*\]",
    r"<\s*(?:name|duration|date|role|company)\s*>",
)


def _contains_any(text_lower: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text_lower for term in terms)


def validate_text(text: str) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    text_lower = text.lower()

    if "\ufffd" in text:
        errors.append("文件包含无法识别的替换字符，可能存在编码问题。")
    if len(text.strip()) < 1000:
        errors.append("报告正文少于 1000 个字符，内容可能不完整。")

    missing_sections = [
        label
        for label, terms in CONCEPT_GROUPS.items()
        if not _contains_any(text_lower, terms)
    ]
    if missing_sections:
        errors.append("缺少必要章节或概念：" + "、".join(missing_sections))

    missing_layers = [
        label
        for label, terms in LAYER_GROUPS.items()
        if not _contains_any(text_lower, terms)
    ]
    if missing_layers:
        errors.append("学习计划缺少分层：" + "、".join(missing_layers))

    if not re.search(r"20\d{2}-\d{2}-\d{2}", text):
        errors.append("未找到 YYYY-MM-DD 格式的报告或证据日期。")

    link_count = len(re.findall(r"https?://[^\s)>\]]+", text))
    if link_count < 5:
        errors.append(f"有效网页链接不足 5 个（当前 {link_count} 个）。")

    if not re.search(r"\d+\s*(?:周|weeks?\b)", text, re.IGNORECASE):
        errors.append("未明确计划时长（周数）。")
    if not re.search(
        r"(?:每周|weekly)[^\n]{0,30}\d+(?:\s*[-–—至]\s*\d+)?\s*(?:小时|hours?|h\b)",
        text,
        re.IGNORECASE,
    ):
        errors.append("未明确每周可投入时间。")

    placeholders = [
        pattern for pattern in PLACEHOLDER_PATTERNS if re.search(pattern, text, re.IGNORECASE)
    ]
    if placeholders:
        errors.append("仍含未替换的模板占位符：" + "、".join(placeholders))

    week_markers = len(re.findall(r"第\s*\d+\s*周", text))
    if week_markers == 0:
        warnings.append("未找到“第1周”形式的周计划标记，请确认计划是否足够具体。")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "characters": len(text),
            "links": link_count,
            "week_markers": week_markers,
        },
    }


def run_self_test() -> int:
    good = """
# AI职业机会与学习路线报告
报告日期：2026-07-12
## 执行摘要
这是基于候选人资料形成的核心结论。目标计划为12周，每周投入8-10小时。
## 个人画像
候选人画像包括经验、能力、约束与偏好。
## AI与泛AI产业地图
产业发展、行业趋势和关键触发条件分为当前事实与预测。
## 公司机会
公司地图覆盖平台、应用、服务、具身智能与垂直行业。
## 职位方向
岗位方向按照证据、可迁移能力与可达性排序。
## 能力差距
能力差距分成可立即迁移、短期补足和长期建设。
## 学习策略
通用知识、职位知识和行业知识分别安排，并随阶段调整比例。
## 每周学习计划
### 第1周
学习目标、中文文档、中文视频、练习、作品和验收标准完整。
### 第2周
继续完成岗位专项练习和行业案例。
## 作品集
作品集项目具有业务问题、过程、结果和证据。
## 求职行动
求职行动包含简历改写、目标公司、投递策略与面试复盘。
## 来源
https://example.com/a
https://example.com/b
https://example.com/c
https://example.com/d
https://example.com/e
""" + ("有效的个性化分析内容。" * 80)
    bad = "# 报告\n日期：YYYY-MM-DD\nTODO\n"

    good_result = validate_text(good)
    bad_result = validate_text(bad)
    if good_result["ok"] and not bad_result["ok"]:
        print("自测：通过")
        return 0

    print("自测：失败")
    print(json.dumps({"good": good_result, "bad": bad_result}, ensure_ascii=False, indent=2))
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查AI职业机会与学习路线报告的结构、证据和计划完整性。"
    )
    parser.add_argument("report", nargs="?", type=Path, help="待检查的 Markdown 报告")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出检查结果")
    parser.add_argument("--self-test", action="store_true", help="运行内置测试")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.report is None:
        parser.error("必须提供报告路径，或使用 --self-test。")
    if not args.report.is_file():
        print(f"ERROR: 文件不存在：{args.report}", file=sys.stderr)
        return 2

    try:
        text = args.report.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: 文件不是有效的 UTF-8：{exc}", file=sys.stderr)
        return 2

    result = validate_text(text)
    result["report"] = str(args.report.resolve())

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
        metrics = result["metrics"]
        print(
            f"统计：{metrics['characters']} 字符，{metrics['links']} 个链接，"
            f"{metrics['week_markers']} 个周计划标记。"
        )

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
