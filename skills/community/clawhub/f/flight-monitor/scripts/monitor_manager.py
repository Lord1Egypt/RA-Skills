#!/usr/bin/env python3
"""
monitor_manager.py — Manage scheduled flight price monitoring tasks.

Uses WorkBuddy automation system (TOML-based) under:
  ~/.workbuddy/automations/

Supports cron-like schedule expressions compatible with both WorkBuddy and OpenClaw.

Usage:
    python monitor_manager.py add   --from BJS --to SYX --date 2026-03-25 --freq daily --threshold 1500
    python monitor_manager.py add   --from HGH --to SIA --date 2026-03-26 --freq 6h
    python monitor_manager.py list
    python monitor_manager.py pause --id flight-BJS-SYX-2026-03-25
    python monitor_manager.py remove --id flight-BJS-SYX-2026-03-25
    python monitor_manager.py run   --id flight-BJS-SYX-2026-03-25  # manual trigger
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import tomllib          # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None       # fallback: manual parsing

AUTOMATIONS_DIR = Path.home() / ".workbuddy" / "automations"
SCRIPTS_DIR = Path(__file__).parent

# ── Frequency → cron expression ─────────────────────────────────────────────
FREQ_MAP = {
    "hourly": "FREQ=HOURLY;INTERVAL=1",
    "1h": "FREQ=HOURLY;INTERVAL=1",
    "2h": "FREQ=HOURLY;INTERVAL=2",
    "3h": "FREQ=HOURLY;INTERVAL=3",
    "6h": "FREQ=HOURLY;INTERVAL=6",
    "12h": "FREQ=HOURLY;INTERVAL=12",
    "daily": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=9;BYMINUTE=0",
    "morning": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=9;BYMINUTE=0",
    "twice-daily": "FREQ=HOURLY;INTERVAL=12",
}

FREQ_LABELS = {
    "hourly": "每小时", "1h": "每1小时", "2h": "每2小时",
    "3h": "每3小时", "6h": "每6小时", "12h": "每12小时",
    "daily": "每天9:00", "morning": "每天早上9:00", "twice-daily": "每天早晚各1次",
}


_TASK_ID_RE = re.compile(r'^flight-[A-Z]{2,4}-[A-Z]{2,4}-\d{4}-\d{2}-\d{2}$')

# Individual field validators (whitelist approach)
_CITY_CODE_RE = re.compile(r'^[A-Za-z]{2,4}$')
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_FREQ_RE = re.compile(r'^(hourly|1h|2h|3h|6h|12h|daily|morning|twice-daily)$')


def _validate_city_code(code: str) -> bool:
    """Only allow 2-4 letter IATA city/airport codes."""
    return bool(_CITY_CODE_RE.match(code))


def _validate_date(date: str) -> bool:
    """Only allow dates in YYYY-MM-DD format with plausible values."""
    if not _DATE_RE.match(date):
        return False
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _safe_resolve_under(path: Path, base: Path) -> bool:
    """Return True only if resolved path is strictly under base directory."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def validate_task_id(task_id: str) -> bool:
    """
    Whitelist check: only allow IDs of the form flight-XXX-XXX-YYYY-MM-DD.
    Prevents path traversal (e.g. '../../etc/passwd') and shell metacharacters.
    """
    return bool(_TASK_ID_RE.match(task_id))


def make_task_id(dep: str, arr: str, date: str) -> str:
    return f"flight-{dep.upper()}-{arr.upper()}-{date}"


def add_monitor(dep: str, arr: str, date: str, freq: str,
                threshold: float = None, return_date: str = None) -> str:
    # ── Input validation ────────────────────────────────────────────────────
    if not _validate_city_code(dep):
        return f"❌ 无效的出发城市代码 `{dep}`（只允许 2-4 位字母 IATA 代码，如 BJS、SHA）"
    if not _validate_city_code(arr):
        return f"❌ 无效的到达城市代码 `{arr}`（只允许 2-4 位字母 IATA 代码，如 SYX、CTU）"
    if not _validate_date(date):
        return f"❌ 无效的日期 `{date}`（格式应为 YYYY-MM-DD，如 2026-04-10）"
    if return_date and not _validate_date(return_date):
        return f"❌ 无效的返程日期 `{return_date}`（格式应为 YYYY-MM-DD）"
    if freq not in FREQ_MAP:
        return f"❌ 无效的频率 `{freq}`，支持：{', '.join(FREQ_MAP.keys())}"

    task_id = make_task_id(dep, arr, date)
    # Double-check the generated ID still passes whitelist (belt-and-suspenders)
    if not validate_task_id(task_id):
        return f"❌ 生成的任务 ID `{task_id}` 未通过安全校验"

    task_dir = AUTOMATIONS_DIR / task_id
    # Path boundary check: ensure target is strictly inside AUTOMATIONS_DIR
    if not _safe_resolve_under(task_dir, AUTOMATIONS_DIR):
        return f"❌ 安全错误：任务目录超出允许范围"

    task_dir.mkdir(parents=True, exist_ok=True)

    rrule = FREQ_MAP.get(freq, FREQ_MAP["daily"])
    threshold_note = f"，低于¥{threshold}提醒" if threshold else ""
    label_freq = FREQ_LABELS.get(freq, freq)
    route_label = f"{dep.upper()} → {arr.upper()}"

    # Build the monitoring prompt — with strict date locking
    threshold_note = f"，若最低价 ≤ ¥{threshold} 则触发低价提醒" if threshold else ""
    rt_note = f"，同时关注 {return_date} 返程价格" if return_date else ""
    notify_step = (
        f"4. 若触发低价提醒，运行推送通知：python {SCRIPTS_DIR / 'notify.py'} "
        f"--title \"机票低价提醒 {dep}→{arr}\" "
        f"--body \"{dep}→{arr} 出行日期{date} 最低价¥<最低价>，低于阈值¥{threshold}！推荐航班<航班号>\" "
        f"--url \"https://flights.ctrip.com/itinerary/oneway/{dep.lower()}-{arr.lower()}?depdate={date}\""
    ) if threshold else ""

    prompt = (
        f"【机票价格监控】出行日期：{date}（注意：搜索时必须使用此出行日期，不能用今天日期）。"
        f"请按以下步骤执行：\n"
        f"1. 运行：python {SCRIPTS_DIR / 'search_flights.py'} --from {dep} --to {arr} --date {date}"
        + (f" --max-price {threshold}" if threshold else "")
        + f"\n2. 若脚本 source 为 fallback，使用 search_query 字段执行 web_search（仅一次），"
        f"搜索词必须包含出行日期 {date}{rt_note}{threshold_note}。"
        f"\n3. 运行：python {SCRIPTS_DIR / 'price_history.py'} append "
        f"--from {dep} --to {arr} --date {date} --price <最低价> --flight \"<航班号>\""
        + (f" --threshold {threshold}" if threshold else "")
        + (f"\n{notify_step}" if notify_step else "")
    )

    toml_content = f'''# Flight Monitor Task
# Auto-generated by flight-monitor skill

[automation]
name = "机票监控 {route_label} {date}"
prompt = """{prompt}"""
rrule = "{rrule}"
status = "ACTIVE"

[meta]
dep = "{dep.upper()}"
arr = "{arr.upper()}"
date = "{date}"
freq = "{freq}"
threshold = {threshold if threshold else "null"}
return_date = "{return_date or ""}"
created_at = "{datetime.now().isoformat()}"
'''

    toml_file = task_dir / "automation.toml"
    toml_file.write_text(toml_content, encoding="utf-8")

    return (
        f"✅ 已添加监控任务\n\n"
        f"- **ID:** `{task_id}`\n"
        f"- **航线:** {route_label}\n"
        f"- **出行日期:** {date}\n"
        f"- **监控频率:** {label_freq}{threshold_note}\n"
        f"- **配置文件:** `{toml_file}`\n\n"
        f"> 提示：任务已写入 WorkBuddy 自动化目录，下次触发时将自动执行。"
    )


def list_monitors() -> str:
    AUTOMATIONS_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [
        d for d in AUTOMATIONS_DIR.iterdir()
        if d.is_dir() and d.name.startswith("flight-")
    ]
    if not tasks:
        return "暂无机票监控任务。"

    lines = ["## 当前机票监控任务", "", "| ID | 航线 | 日期 | 频率 | 阈值 | 状态 |",
             "|----|------|------|------|------|------|"]
    for task_dir in sorted(tasks):
        toml_file = task_dir / "automation.toml"
        if not toml_file.exists():
            continue
        try:
            content = toml_file.read_text(encoding="utf-8")
            meta = _simple_toml_parse(content, "meta")
            auto = _simple_toml_parse(content, "automation")
            dep = meta.get("dep", "")
            arr = meta.get("arr", "")
            date = meta.get("date", "")
            freq = FREQ_LABELS.get(meta.get("freq", ""), meta.get("freq", ""))
            threshold = meta.get("threshold", "−")
            status = auto.get("status", "ACTIVE")
            lines.append(
                f"| `{task_dir.name}` | {dep}→{arr} | {date} | {freq} "
                f"| {f'¥{threshold}' if threshold and threshold != 'null' else '−'} | {status} |"
            )
        except Exception as e:
            lines.append(f"| `{task_dir.name}` | (解析失败: {e}) | | | | |")
    return "\n".join(lines)


def pause_monitor(task_id: str) -> str:
    if not validate_task_id(task_id):
        return f"❌ 无效的任务 ID `{task_id}`（格式应为 flight-DEP-ARR-YYYY-MM-DD）"
    toml_file = AUTOMATIONS_DIR / task_id / "automation.toml"
    if not toml_file.exists():
        return f"❌ 未找到任务 `{task_id}`"
    content = toml_file.read_text(encoding="utf-8")
    updated = content.replace('status = "ACTIVE"', 'status = "PAUSED"')
    toml_file.write_text(updated, encoding="utf-8")
    return f"⏸ 已暂停任务 `{task_id}`"


def remove_monitor(task_id: str) -> str:
    if not validate_task_id(task_id):
        return f"❌ 无效的任务 ID `{task_id}`（格式应为 flight-DEP-ARR-YYYY-MM-DD）"
    task_dir = AUTOMATIONS_DIR / task_id
    if not task_dir.exists():
        return f"❌ 未找到任务 `{task_id}`"
    for f in task_dir.iterdir():
        f.unlink()
    task_dir.rmdir()
    return f"🗑 已删除任务 `{task_id}`"


def run_monitor(task_id: str) -> str:
    """
    Show the monitoring prompt for a task.

    NOTE: This function intentionally does NOT execute any shell commands.
    Monitoring tasks are driven by the WorkBuddy automation scheduler which
    reads the TOML prompt directly — no subprocess or os.system() calls are
    needed or used here.
    """
    if not validate_task_id(task_id):
        return f"❌ 无效的任务 ID `{task_id}`（格式应为 flight-DEP-ARR-YYYY-MM-DD）"
    toml_file = AUTOMATIONS_DIR / task_id / "automation.toml"
    if not toml_file.exists():
        return f"❌ 未找到任务 `{task_id}`"
    content = toml_file.read_text(encoding="utf-8")
    meta = _simple_toml_parse(content, "meta")
    dep = meta.get("dep", "")
    arr = meta.get("arr", "")
    date = meta.get("date", "")
    threshold = meta.get("threshold", "")
    threshold_arg = f" --max-price {threshold}" if threshold and threshold != "null" else ""

    return (
        f"🔍 任务详情：{dep} → {arr}，出行日期 {date}\n\n"
        f"如需手动执行一次查询，请运行：\n"
        f"```\n"
        f"python scripts/search_flights.py --from {dep} --to {arr} --date {date}{threshold_arg}\n"
        f"```\n"
        f"（此脚本仅做查询，不执行任何系统命令。）"
    )


def _simple_toml_parse(content: str, section: str) -> dict:
    """Minimal TOML section parser (no dependency on tomllib)."""
    result = {}
    in_section = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"[{section}]"):
            in_section = True
            continue
        if stripped.startswith("[") and in_section:
            break
        if in_section and "=" in stripped and not stripped.startswith("#"):
            key, _, val = stripped.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            result[key] = val
    return result


def main():
    parser = argparse.ArgumentParser(description="Flight monitor task manager")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add")
    p_add.add_argument("--from", dest="dep", required=True)
    p_add.add_argument("--to", dest="arr", required=True)
    p_add.add_argument("--date", required=True)
    p_add.add_argument("--freq", default="daily",
                       help="Frequency: hourly/1h/2h/3h/6h/12h/daily/twice-daily")
    p_add.add_argument("--threshold", type=float)
    p_add.add_argument("--return-date", dest="return_date")

    p_pause = sub.add_parser("pause")
    p_pause.add_argument("--id", required=True)

    p_remove = sub.add_parser("remove")
    p_remove.add_argument("--id", required=True)

    p_run = sub.add_parser("run")
    p_run.add_argument("--id", required=True)

    sub.add_parser("list")

    args = parser.parse_args()

    if args.cmd == "add":
        print(add_monitor(args.dep, args.arr, args.date, args.freq,
                          args.threshold, args.return_date))
    elif args.cmd == "list":
        print(list_monitors())
    elif args.cmd == "pause":
        print(pause_monitor(args.id))
    elif args.cmd == "remove":
        print(remove_monitor(args.id))
    elif args.cmd == "run":
        run_monitor(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
