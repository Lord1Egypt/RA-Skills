#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理脚本 v2

职责边界：
1. 只管理技能自己的“业务配置”
2. 记录 OpenClaw cron 任务的绑定结果（job_id / 名称 / 快照）
3. 不再把本地 config.json 当作调度真相源

说明：
- 默认时区为 Asia/Shanghai
- OpenClaw cron 才是定时任务的唯一调度真相源
- 本脚本不会创建、修改、删除 OpenClaw cron 任务
- 本脚本仅保存查询参数与 job 绑定信息，供技能后续复用
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

CHINA_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_TIMEZONE = "Asia/Shanghai"
DEFAULT_MAX_RESULTS = 20
DEFAULT_SORT = "date"
DEFAULT_SESSION_TARGET = "current"
DEFAULT_CURRENT_SESSION_NOTE = "默认发送到创建任务时所在的当前会话。请勿删除当前会话；若发送时当前会话已不存在，可回退到新对话继续发送，但原会话上下文连续性会中断。"
SCHEMA_VERSION = 2

CRON_FIELD_SPECS = [
    ("分钟", 0, 59),
    ("小时", 0, 23),
    ("日", 1, 31),
    ("月", 1, 12),
    ("星期", 0, 7),
]


class ConfigError(ValueError):
    """配置错误。"""


def resolve_config_dir() -> str:
    """解析配置目录，优先环境变量，其次推断技能目录，最后回退到标准路径。"""
    env_root = os.environ.get("OPENCLAW_SKILL_ROOT")
    if env_root:
        return os.path.abspath(os.path.expanduser(env_root))

    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    parent_dir = os.path.dirname(current_dir)

    if os.path.basename(current_dir) == "scripts":
        return parent_dir

    return os.path.expanduser("~/.openclaw/workspace/skills/arxiv-paper-searcher")


CONFIG_DIR = resolve_config_dir()
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def now_iso() -> str:
    return datetime.now(CHINA_TZ).isoformat(timespec="seconds")


def validate_positive_int(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("论文数量必须是整数") from exc
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("论文数量必须大于 0")
    return ivalue


def _validate_cron_value(token: str, min_value: int, max_value: int, field_name: str) -> None:
    if not token.isdigit():
        raise argparse.ArgumentTypeError(f"{field_name}字段包含非法值：{token}")
    value = int(token)
    if value < min_value or value > max_value:
        raise argparse.ArgumentTypeError(f"{field_name}字段超出范围：{value}，允许范围 {min_value}-{max_value}")


def _validate_cron_item(item: str, min_value: int, max_value: int, field_name: str) -> None:
    if not item:
        raise argparse.ArgumentTypeError(f"{field_name}字段不能为空项")
    if "/" in item:
        base, step = item.split("/", 1)
        if not step.isdigit() or int(step) <= 0:
            raise argparse.ArgumentTypeError(f"{field_name}字段步长非法：{item}")
        if base == "*":
            return
        if "-" in base:
            start, end = base.split("-", 1)
            _validate_cron_value(start, min_value, max_value, field_name)
            _validate_cron_value(end, min_value, max_value, field_name)
            if int(start) > int(end):
                raise argparse.ArgumentTypeError(f"{field_name}字段范围非法：{item}")
            return
        _validate_cron_value(base, min_value, max_value, field_name)
        return
    if item == "*":
        return
    if "-" in item:
        start, end = item.split("-", 1)
        _validate_cron_value(start, min_value, max_value, field_name)
        _validate_cron_value(end, min_value, max_value, field_name)
        if int(start) > int(end):
            raise argparse.ArgumentTypeError(f"{field_name}字段范围非法：{item}")
        return
    _validate_cron_value(item, min_value, max_value, field_name)


def validate_cron(expr: str) -> str:
    parts = expr.strip().split()
    if len(parts) != 5:
        raise argparse.ArgumentTypeError("cron 表达式必须是 5 段，例如：0 9 * * *")
    for part, (field_name, min_value, max_value) in zip(parts, CRON_FIELD_SPECS):
        for item in part.split(","):
            _validate_cron_item(item, min_value, max_value, field_name)
    return expr


def normalize_job_binding(job: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    job = job or {}
    schedule = job.get("schedule") or {}
    return {
        "job_id": job.get("job_id"),
        "name": job.get("name"),
        "enabled": bool(job.get("enabled", False)),
        "session_target": job.get("session_target") or DEFAULT_SESSION_TARGET,
        "schedule": {
            "kind": schedule.get("kind"),
            "expr": schedule.get("expr"),
            "tz": schedule.get("tz") or DEFAULT_TIMEZONE,
        },
        "bound_at": job.get("bound_at"),
        "updated_at": job.get("updated_at"),
        "notes": job.get("notes"),
    }


def default_config() -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "keyword": None,
        "max_results": DEFAULT_MAX_RESULTS,
        "sort": DEFAULT_SORT,
        "timezone": DEFAULT_TIMEZONE,
        "job": normalize_job_binding(None),
        "updated_at": None,
    }


def migrate_legacy_config(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 v1 配置迁移到 v2。

    旧版 schedule 只能代表“用户曾经想要的时间”，不能证明 OpenClaw cron 中真的存在对应 job。
    因此迁移后不自动视为 enabled，而是保留为 notes，避免制造虚假的调度状态。
    """
    migrated = default_config()
    migrated["keyword"] = data.get("keyword")
    migrated["max_results"] = data.get("max_results", DEFAULT_MAX_RESULTS)
    migrated["sort"] = data.get("sort", DEFAULT_SORT)
    migrated["timezone"] = (data.get("schedule") or {}).get("timezone") or data.get("timezone") or DEFAULT_TIMEZONE
    migrated["updated_at"] = data.get("updated_at")

    legacy_schedule = data.get("schedule") or {}
    if legacy_schedule:
        migrated["job"] = {
            "job_id": None,
            "name": None,
            "enabled": False,
            "session_target": DEFAULT_SESSION_TARGET,
            "schedule": {
                "kind": "cron" if legacy_schedule.get("cron") else None,
                "expr": legacy_schedule.get("cron"),
                "tz": legacy_schedule.get("timezone") or DEFAULT_TIMEZONE,
            },
            "bound_at": None,
            "updated_at": now_iso(),
            "notes": "从旧版 schedule 字段迁移而来。请重新创建或重新绑定 OpenClaw cron job_id。",
        }
    return migrated


def load_config() -> Optional[Dict[str, Any]]:
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("schema_version") == SCHEMA_VERSION:
        normalized = default_config()
        normalized.update({
            "schema_version": SCHEMA_VERSION,
            "keyword": data.get("keyword"),
            "max_results": data.get("max_results", DEFAULT_MAX_RESULTS),
            "sort": data.get("sort", DEFAULT_SORT),
            "timezone": data.get("timezone") or DEFAULT_TIMEZONE,
            "job": normalize_job_binding(data.get("job")),
            "updated_at": data.get("updated_at"),
        })
        return normalized

    return migrate_legacy_config(data)


def write_config(config: Dict[str, Any]) -> Dict[str, Any]:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config["schema_version"] = SCHEMA_VERSION
    config["updated_at"] = now_iso()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"配置已保存：{CONFIG_FILE}")
    return config


def save_config(
    keyword: Optional[str] = None,
    max_results: Optional[int] = None,
    sort: Optional[str] = None,
    timezone: Optional[str] = None,
) -> Dict[str, Any]:
    current = load_config() or default_config()

    if current.get("keyword") is None and keyword is None:
        raise ConfigError("首次保存配置时必须提供 --keyword")

    current["keyword"] = keyword if keyword is not None else current.get("keyword")
    current["max_results"] = max_results if max_results is not None else current.get("max_results", DEFAULT_MAX_RESULTS)
    current["sort"] = sort if sort is not None else current.get("sort", DEFAULT_SORT)
    current["timezone"] = timezone if timezone is not None else current.get("timezone", DEFAULT_TIMEZONE)
    return write_config(current)


def bind_job(
    job_id: str,
    name: Optional[str] = None,
    enabled: bool = True,
    schedule_kind: Optional[str] = None,
    schedule_expr: Optional[str] = None,
    schedule_tz: Optional[str] = None,
    session_target: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    current = load_config() or default_config()
    if current.get("keyword") is None:
        raise ConfigError("绑定 job 之前请先保存查询配置")

    job = normalize_job_binding(current.get("job"))
    job.update(
        {
            "job_id": job_id,
            "name": name if name is not None else job.get("name"),
            "enabled": enabled,
            "session_target": session_target or job.get("session_target") or DEFAULT_SESSION_TARGET,
            "schedule": {
                "kind": schedule_kind or job.get("schedule", {}).get("kind"),
                "expr": schedule_expr if schedule_expr is not None else job.get("schedule", {}).get("expr"),
                "tz": schedule_tz or job.get("schedule", {}).get("tz") or current.get("timezone") or DEFAULT_TIMEZONE,
            },
            "bound_at": job.get("bound_at") or now_iso(),
            "updated_at": now_iso(),
            "notes": notes if notes is not None else (job.get("notes") or (DEFAULT_CURRENT_SESSION_NOTE if (session_target or job.get("session_target") or DEFAULT_SESSION_TARGET) == DEFAULT_SESSION_TARGET else None)),
        }
    )
    current["job"] = job
    return write_config(current)


def unbind_job(clear_schedule_snapshot: bool = False) -> Dict[str, Any]:
    current = load_config() or default_config()
    job = normalize_job_binding(current.get("job"))
    schedule = {"kind": None, "expr": None, "tz": current.get("timezone") or DEFAULT_TIMEZONE}
    if not clear_schedule_snapshot:
        schedule = job.get("schedule") or schedule

    current["job"] = {
        "job_id": None,
        "name": None,
        "enabled": False,
        "session_target": DEFAULT_SESSION_TARGET,
        "schedule": schedule,
        "bound_at": None,
        "updated_at": now_iso(),
        "notes": "本地已解绑 job。请确认 OpenClaw cron 侧是否已删除或停用。若后续重新绑定 current，会默认发送到新的当前会话。",
    }
    return write_config(current)


def set_job_enabled(enabled: bool) -> Dict[str, Any]:
    current = load_config() or default_config()
    job = normalize_job_binding(current.get("job"))
    if not job.get("job_id"):
        raise ConfigError("当前没有已绑定的 job_id，无法更新启用状态")
    job["enabled"] = enabled
    job["updated_at"] = now_iso()
    current["job"] = job
    return write_config(current)


def clear_config() -> bool:
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("配置文件已删除")
        return True
    return False


def print_config(config: Dict[str, Any]) -> None:
    print("当前配置:")
    print(json.dumps(config, ensure_ascii=False, indent=2))
    print()
    print(f"schema_version：{config.get('schema_version')}")
    print(f"关键词：{config.get('keyword')}")
    print(f"数量：{config.get('max_results')}")
    print(f"排序：{config.get('sort')}")
    print(f"时区：{config.get('timezone')}")

    job = normalize_job_binding(config.get("job"))
    if job.get("job_id"):
        print(f"job_id：{job.get('job_id')}")
        print(f"任务名：{job.get('name')}")
        print(f"已绑定：是")
        print(f"启用：{'是' if job.get('enabled') else '否'}")
        print(f"sessionTarget：{job.get('session_target')}")
        if job.get("schedule", {}).get("expr"):
            print(
                "计划快照："
                f"{job.get('schedule', {}).get('kind')} / "
                f"{job.get('schedule', {}).get('expr')} / "
                f"{job.get('schedule', {}).get('tz')}"
            )
    else:
        print("job_id：未绑定")
        print("已绑定：否")

    if job.get("notes"):
        print(f"备注：{job.get('notes')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="配置管理工具 v2")
    parser.add_argument("--save", action="store_true", help="保存或更新查询配置")
    parser.add_argument("--show", action="store_true", help="显示当前配置")
    parser.add_argument("--clear-config", action="store_true", help="彻底删除配置文件")

    parser.add_argument("--bind-job", action="store_true", help="绑定 OpenClaw cron job")
    parser.add_argument("--unbind-job", action="store_true", help="解绑本地 job 记录")
    parser.add_argument("--clear-schedule-snapshot", action="store_true", help="解绑时同时清空本地计划快照")
    parser.add_argument("--enable-job", action="store_true", help="仅更新本地 job 状态为启用")
    parser.add_argument("--disable-job", action="store_true", help="仅更新本地 job 状态为禁用")

    parser.add_argument("--keyword", "-k", type=str, help="搜索关键词")
    parser.add_argument("--max", "-m", type=validate_positive_int, help="论文数量")
    parser.add_argument("--sort", choices=["date", "updated", "relevance"], help="排序方式")
    parser.add_argument("--timezone", default=None, help="业务时区")

    parser.add_argument("--job-id", type=str, help="OpenClaw cron jobId")
    parser.add_argument("--job-name", type=str, help="OpenClaw cron 任务名")
    parser.add_argument("--session-target", choices=["current", "isolated", "main"], help="绑定记录中的 sessionTarget")
    parser.add_argument("--schedule-kind", choices=["cron", "every", "at"], help="计划类型快照")
    parser.add_argument("--schedule-expr", type=validate_cron, help="5 段 cron 计划快照")
    parser.add_argument("--notes", type=str, help="备注")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.show:
            config = load_config()
            if config:
                print_config(config)
            else:
                print("暂无配置")
            return 0

        if args.clear_config:
            if clear_config():
                print("✓ 配置已彻底删除")
            else:
                print("✗ 配置文件不存在")
            return 0

        if args.save:
            config = save_config(
                keyword=args.keyword,
                max_results=args.max,
                sort=args.sort,
                timezone=args.timezone,
            )
            print()
            print("✓ 查询配置已更新")
            print_config(config)
            return 0

        if args.bind_job:
            if not args.job_id:
                parser.error("--bind-job 需要提供 --job-id")
            config = bind_job(
                job_id=args.job_id,
                name=args.job_name,
                enabled=True,
                schedule_kind=args.schedule_kind or ("cron" if args.schedule_expr else None),
                schedule_expr=args.schedule_expr,
                schedule_tz=args.timezone,
                session_target=args.session_target or DEFAULT_SESSION_TARGET,
                notes=args.notes,
            )
            print()
            print("✓ 已绑定 OpenClaw cron job")
            print_config(config)
            return 0

        if args.unbind_job:
            config = unbind_job(clear_schedule_snapshot=args.clear_schedule_snapshot)
            print()
            print("✓ 已解绑本地 job 记录")
            print_config(config)
            return 0

        if args.enable_job:
            config = set_job_enabled(True)
            print()
            print("✓ 已将本地 job 状态标记为启用")
            print_config(config)
            return 0

        if args.disable_job:
            config = set_job_enabled(False)
            print()
            print("✓ 已将本地 job 状态标记为禁用")
            print_config(config)
            return 0

        parser.print_help()
        return 0
    except ConfigError as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
