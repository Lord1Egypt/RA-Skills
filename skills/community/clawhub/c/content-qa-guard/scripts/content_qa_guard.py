#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""content-qa-guard 统一入口脚本

V58.0修复: call_skill函数将skill_name 'content-qa-guard' 转换为 'content_qa_guard.py',
但实际脚本为qa_guard.py(三级审核)和check_compliance.py(U19管道合规)。
本文件作为统一入口,根据action参数分派到对应函数。

调用方式(来自content_orchestrator.call_skill):
  命令行: python content_qa_guard.py --action <action> --params <json>
  stdin: {"action": <action>, ...params}

action分派:
  check       → check_compliance() (U19管道合规模式)
  qa_guard    → qa_guard()         (三级审核模式)
  score       → qa_guard()         (兼容pipeline action别名)
"""
import sys
import json
import argparse
import os
from pathlib import Path

# R18统一入口: 使用db_logger + 添加项目根到sys.path
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
from mcps.shared.db_logger import get_logger
logger = get_logger("_lazy", source="skills/_lazy/content-qa-guard/scripts/content_qa_guard.py")

# 添加同目录到path (支持导入同目录脚本)
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))


def main() -> int:
    """统一入口: 解析参数并分派到对应函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="content-qa-guard统一入口")
    parser.add_argument("--action", default="", help="操作类型: check/qa_guard")
    parser.add_argument("--params", default="{}", help="参数JSON")
    args = parser.parse_args()

    # 合并命令行参数和stdin数据
    params = {}
    if args.params and args.params != "{}":
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            logger.warning(f"命令行params JSON解析失败,使用空字典: {e}")
            params = {}

    # 读取stdin (call_skill通过stdin传递 {"action": action, ...params})
    stdin_data = {}
    if not sys.stdin.isatty():
        try:
            stdin_text = sys.stdin.read().strip()
            if stdin_text:
                stdin_data = json.loads(stdin_text)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"stdin JSON读取失败,使用空字典: {e}")

    # action优先级: 命令行 > stdin
    action = args.action or stdin_data.get("action", "")

    # 合并stdin数据到params (stdin中的非action字段)
    for k, v in stdin_data.items():
        if k != "action" and k not in params:
            params[k] = v

    # 分派到对应函数
    if action == "check":
        # U19管道合规模式 → check_compliance
        from check_compliance import check_compliance
        content = params.get("content", "")
        platform = params.get("platform", "")
        content_type = params.get("content_type", "")
        result = check_compliance(content, platform, content_type)
    elif action in ("qa_guard", "score", "audit"):
        # 三级审核模式 → qa_guard
        from qa_guard import qa_guard
        text = params.get("text", params.get("content", ""))
        platform = params.get("platform", "default")
        context = params.get("context", "")
        result = qa_guard(text, platform, context)
    else:
        # 未知action → 默认使用check_compliance
        from check_compliance import check_compliance
        content = params.get("content", "")
        platform = params.get("platform", "")
        content_type = params.get("content_type", "")
        result = check_compliance(content, platform, content_type)

    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
