#!/usr/bin/env python3
"""NEXUS管道质量门控脚本

在content-orchestrator管道间执行质量门控检查,得分≥阈值才进入下一阶段。
检查维度: 内容长度/关键词覆盖/格式合规/敏感词检测
依赖: db_logger(统一日志入口,规则18) + sensitive-word-mcp(可选,降级本地检查)
"""
import sys

import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

# R14-R7统一入口: db_logger替代logging(规则18)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger

import logging
logger = get_logger("system", source="skills/content-orchestrator/scripts/quality_gate.py")

logger = get_logger("content-orchestrator", source="skills/content-orchestrator/scripts/quality_gate.py")

# 本地敏感词降级词库(sensitive-word-mcp不可用时使用,来源:02手册§八8.1)
_SENSITIVE_WORDS = [
    "加微信", "加V", "扫码领", "转账", "支付宝账号", "100%成功", "包过",
    "必过", "绝对有效", "零风险", "稳赚", "贷款", "信用卡套现",
]

# 各阶段最低字数要求(来源:02手册§五5.2内容质量标准)
_STAGE_MIN_LENGTH = {
    "draft": 200, "script": 300, "content": 500, "final": 800, "default": 300,
}

def check_length(text: str, stage: str) -> Tuple[bool, float, str]:
    """检查内容长度是否达到最低字数

    Args:
        text (str): 参数说明
        stage (str): 参数说明

    Returns:
        Tuple[bool, float, str]: 返回值说明
    """
    min_len = _STAGE_MIN_LENGTH.get(stage, _STAGE_MIN_LENGTH["default"])
    actual_len = len(text.strip())
    passed = actual_len >= min_len
    score = min(actual_len / min_len, 1.0) if min_len > 0 else 1.0
    msg = f"字数{actual_len}/{min_len}" + ("达标" if passed else "不足")
    return passed, score, msg

def check_keywords(text: str, threshold: float) -> Tuple[bool, float, str]:
    """检查关键词覆盖(标题+段落+标签三要素)

    Args:
        text (str): 参数说明
        threshold (float): 参数说明

    Returns:
        Tuple[bool, float, str]: 返回值说明
    """
    has_title = bool(re.search(r"^#\s+.+|^【.+】", text, re.MULTILINE))
    has_paragraph = text.count("\n\n") >= 2 or text.count("\n") >= 3
    has_tags = bool(re.search(r"#[\u4e00-\u9fa5\w]+|标签[:：]", text))
    coverage = sum([has_title, has_paragraph, has_tags]) / 3.0
    passed = coverage >= threshold
    missing = [k for k, v in [("标题", has_title), ("段落", has_paragraph), ("标签", has_tags)] if not v]
    msg = f"覆盖率{coverage:.0%}" + ("" if passed else f",缺失:{','.join(missing)}")
    return passed, coverage, msg

def check_format(text: str) -> Tuple[bool, float, str]:
    """检查格式合规(标题/段落/标签结构)

    Args:
        text (str): 参数说明

    Returns:
        Tuple[bool, float, str]: 返回值说明
    """
    issues: List[str] = []
    if not re.search(r"^#\s+.+", text, re.MULTILINE) and not re.search(r"^【.+】", text, re.MULTILINE):
        issues.append("缺少标题")
    if len(text.strip().split("\n")) < 3:
        issues.append("段落过少")
    if len(text) > 5000 and "\n\n" not in text:
        issues.append("长文本无分段")
    passed = len(issues) == 0
    score = 1.0 - len(issues) * 0.33
    msg = "格式合规" if passed else "问题:" + ";".join(issues)
    return passed, max(score, 0.0), msg

def check_sensitive(text: str) -> Tuple[bool, float, str]:
    """敏感词检测(本地降级,sensitive-word-mcp不可用时使用)

    Args:
        text (str): 参数说明

    Returns:
        Tuple[bool, float, str]: 返回值说明
    """
    found = [w for w in _SENSITIVE_WORDS if w in text]
    passed = len(found) == 0
    msg = "无敏感词" if passed else f"命中:{','.join(found)}"
    return passed, (0.0 if found else 1.0), msg

def quality_gate(pipeline_name: str, stage: str, content: str, threshold: float) -> Dict:
    """执行质量门控检查,返回结构化结果

    Args:
        pipeline_name (str): 参数说明
        stage (str): 参数说明
        content (str): 参数说明
        threshold (float): 参数说明

    Returns:
        Dict: 返回值说明
    """
    try:
        if not content or not content.strip():
            return {"success": False, "data": {}, "error": "内容为空", "code": "EMPTY_CONTENT"}
        if not pipeline_name:
            return {"success": False, "data": {}, "error": "pipeline_name不能为空", "code": "INVALID_INPUT"}

        len_ok, len_score, len_msg = check_length(content, stage)
        kw_ok, kw_score, kw_msg = check_keywords(content, threshold)
        fmt_ok, fmt_score, fmt_msg = check_format(content)
        sen_ok, sen_score, sen_msg = check_sensitive(content)

        checks = {
            "length": {"passed": len_ok, "score": round(len_score, 2), "detail": len_msg},
            "keywords": {"passed": kw_ok, "score": round(kw_score, 2), "detail": kw_msg},
            "format": {"passed": fmt_ok, "score": round(fmt_score, 2), "detail": fmt_msg},
            "sensitive": {"passed": sen_ok, "score": round(sen_score, 2), "detail": sen_msg},
        }
        total_score = round((len_score + kw_score + fmt_score + sen_score) / 4.0, 2)
        passed = total_score >= threshold and sen_ok  # 敏感词不达标直接拦截

        suggestions: List[str] = []
        if not len_ok:
            suggestions.append(f"补充内容至{ _STAGE_MIN_LENGTH.get(stage, 300)}字以上")
        if not kw_ok:
            suggestions.append("补充标题/段落结构/标签关键词")
        if not fmt_ok:
            suggestions.append("优化格式:添加标题和段落分隔")
        if not sen_ok:
            suggestions.append("移除敏感词后重新检查")

        logger.info(f"质量门控[{pipeline_name}/{stage}] score={total_score} passed={passed}")

        return {
            "success": True,
            "data": {
                "passed": passed, "score": total_score,
                "pipeline": pipeline_name, "stage": stage, "threshold": threshold,
                "checks": checks,
                "suggestions": suggestions if suggestions else ["质量达标,可进入下一阶段"],
            },
            "error": None, "code": None,
        }
    except Exception as e:
        logger.error(f"quality_gate异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": f"门控检查异常: {e}", "code": "GATE_ERROR"}

def main() -> None:
    """CLI入口: python quality_gate.py --pipeline-name PL-VIDEO --stage content --content-file xxx.txt"""
    parser = argparse.ArgumentParser(description="NEXUS管道质量门控")
    parser.add_argument("--pipeline-name", required=True, help="管道名称(如PL-VIDEO)")
    parser.add_argument("--stage", default="default", help="阶段(draft/script/content/final)")
    parser.add_argument("--content-file", required=True, help="内容文件路径")
    parser.add_argument("--threshold", type=float, default=0.7, help="通过阈值(默认0.7)")
    args = parser.parse_args()

    try:
        content = Path(args.content_file).read_text(encoding="utf-8")
    except Exception as e:
        code = "FILE_NOT_FOUND" if isinstance(e, FileNotFoundError) else "READ_ERROR"
        msg = f"文件不存在: {args.content_file}" if isinstance(e, FileNotFoundError) else f"读取文件失败: {e}"
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": msg, "code": code}, ensure_ascii=False))
        sys.exit(1)

    result = quality_gate(args.pipeline_name, args.stage, content, args.threshold)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get("success") and result.get("data", {}).get("passed") else 1)

if __name__ == "__main__":
    main()
