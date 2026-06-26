#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw cron 任务 JSON 构造器。

用途：
- 基于本地业务配置，生成 OpenClaw `cron.add` / `cron.update` 所需 JSON
- 推荐默认使用 `sessionTarget: current`
- `current` 语义是绑定创建任务时所在的当前会话
- 不直接写 jobs.json
- 不直接调用 OpenClaw CLI，只负责生成可审查的载荷
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config_manager import (  # type: ignore
    DEFAULT_SESSION_TARGET,
    DEFAULT_TIMEZONE,
    load_config,
    validate_cron,
)

DEFAULT_JOB_PREFIX = "arXiv Monitor"
MAX_NAME_LEN = 80


def slugify_keyword(keyword: str) -> str:
    compact = re.sub(r"\s+", " ", keyword).strip()
    compact = compact.replace('"', "'")
    if len(compact) <= 48:
        return compact
    return compact[:45].rstrip() + "..."


def build_analysis_message(config: Dict[str, Any]) -> str:
    keyword = config.get("keyword")
    max_results = config.get("max_results")
    sort = config.get("sort")
    timezone = config.get("timezone") or DEFAULT_TIMEZONE

    if not keyword:
        raise ValueError("当前配置缺少 keyword，无法构造任务消息")

    return (
        "请使用当前技能的已保存配置执行一次完整 arXiv 监控流程。"
        f"检索关键词是 {keyword}。"
        f"返回数量是 {max_results}。"
        f"排序方式是 {sort}。"
        f"时区按 {timezone} 处理。"
        "请先搜索最新论文，再基于标题和摘要逐篇分析，最后输出完整结构化报告。"
        "报告必须包含论文列表、每篇论文的关注热点、创新性评估、热点研究方向 Top 10，以及 3 到 5 条趋势判断。"
    )


def derive_job_name(keyword: str) -> str:
    name = f"{DEFAULT_JOB_PREFIX} · {slugify_keyword(keyword)}"
    if len(name) <= MAX_NAME_LEN:
        return name
    return name[: MAX_NAME_LEN - 3] + "..."


def build_schedule(kind: str, expr: Optional[str], tz: Optional[str], every_ms: Optional[int], at: Optional[str]) -> Dict[str, Any]:
    if kind == "cron":
        if not expr:
            raise ValueError("schedule.kind=cron 时必须提供 --cron")
        validate_cron(expr)
        return {"kind": "cron", "expr": expr, "tz": tz or DEFAULT_TIMEZONE}
    if kind == "every":
        if every_ms is None or every_ms <= 0:
            raise ValueError("schedule.kind=every 时必须提供正整数 --every-ms")
        return {"kind": "every", "everyMs": every_ms}
    if kind == "at":
        if not at:
            raise ValueError("schedule.kind=at 时必须提供 --at")
        return {"kind": "at", "at": at}
    raise ValueError(f"不支持的 schedule.kind：{kind}")


def build_add_payload(
    schedule: Dict[str, Any],
    session_target: str,
    job_name: Optional[str] = None,
) -> Dict[str, Any]:
    config = load_config()
    if not config or not config.get("keyword"):
        raise ValueError("请先用 config_manager.py 保存 keyword / max_results / sort 后再构造 cron 任务")

    payload: Dict[str, Any] = {
        "name": job_name or derive_job_name(config["keyword"]),
        "schedule": schedule,
        "sessionTarget": session_target,
        "payload": {
            "kind": "agentTurn",
            "message": build_analysis_message(config),
        },
    }

    # 推荐路径是 current，不额外设置 delivery。
    # 这意味着任务默认回到创建时所在的当前会话。
    # 若该会话后续被删除，是否能自动回退到新对话取决于运行时能力，因此需要在用户提示文案里显式提醒。
    # 若用户明确要求 isolated，可显式指定 announce 目标。
    return payload


def build_update_payload(
    job_id: str,
    schedule: Optional[Dict[str, Any]],
    session_target: Optional[str],
    job_name: Optional[str],
    enabled: Optional[bool],
) -> Dict[str, Any]:
    patch: Dict[str, Any] = {}
    if schedule is not None:
        patch["schedule"] = schedule
    if session_target is not None:
        patch["sessionTarget"] = session_target
    if job_name is not None:
        patch["name"] = job_name
    if enabled is not None:
        patch["enabled"] = enabled
    if not patch:
        raise ValueError("update 模式下至少需要提供一项 patch 内容")
    return {"jobId": job_id, "patch": patch}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenClaw cron 任务 JSON 构造器")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build-add", action="store_true", help="构造 cron.add JSON")
    mode.add_argument("--build-update", action="store_true", help="构造 cron.update JSON")

    parser.add_argument("--session-target", choices=["current", "isolated", "main"], default=DEFAULT_SESSION_TARGET)
    parser.add_argument("--job-name", type=str, default=None, help="任务名称")
    parser.add_argument("--job-id", type=str, default=None, help="更新时使用的 jobId")

    parser.add_argument("--schedule-kind", choices=["cron", "every", "at"], default="cron")
    parser.add_argument("--cron", type=str, default=None, help="5 段 cron 表达式")
    parser.add_argument("--tz", type=str, default=DEFAULT_TIMEZONE, help="cron 时区")
    parser.add_argument("--every-ms", type=int, default=None, help="every 调度毫秒数")
    parser.add_argument("--at", type=str, default=None, help="at 调度时间戳")

    parser.add_argument("--enable", action="store_true", help="update 时将任务启用")
    parser.add_argument("--disable", action="store_true", help="update 时将任务禁用")
    parser.add_argument("--output", "-o", type=str, default=None, help="输出 JSON 文件路径")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    enabled_patch: Optional[bool] = None
    if args.enable and args.disable:
        parser.error("--enable 和 --disable 不能同时使用")
    if args.enable:
        enabled_patch = True
    elif args.disable:
        enabled_patch = False

    schedule = None
    if args.schedule_kind in {"cron", "every", "at"}:
        schedule = build_schedule(args.schedule_kind, args.cron, args.tz, args.every_ms, args.at)

    if args.build_add:
        payload = build_add_payload(
            schedule=schedule,
            session_target=args.session_target,
            job_name=args.job_name,
        )
    else:
        if not args.job_id:
            parser.error("--build-update 需要提供 --job-id")
        payload = build_update_payload(
            job_id=args.job_id,
            schedule=schedule,
            session_target=args.session_target,
            job_name=args.job_name,
            enabled=enabled_patch,
        )

    output = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"已写入：{args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
