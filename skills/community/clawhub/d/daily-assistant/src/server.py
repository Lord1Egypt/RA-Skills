"""
日常小助手 MCP Server — v2.1（双语版本）

自包含 MCP Server：core.py + config.json，不依赖 Obsidian。
通过 stdio 连接 Claude Code / Cursor / Kiro / Windsurf。

Tools (6):
  - recommend_next  — 推荐下一步行动
  - get_today       — 读取今日待办
  - inherit_tasks   — 继承昨日未完成任务
  - check_overdue   — 检测超期任务
  - generate_review — 生成日终回顾
  - scan_split      — 检测需要拆分的大任务

Resources (3):
  - daily://today     — 今日待办内容
  - daily://dashboard — Dashboard 面板内容
  - daily://history   — 最近 7 天完成统计

用法:
    py -X utf8 server.py
    py -X utf8 server.py --config path/to/config.json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from fastmcp import FastMCP

from core import (
    parse_task, rank_tasks, format_recommendation,
    format_deadline_label,
    scan_overdue_files,
    find_latest_daily, extract_uncompleted_tasks, create_today_file,
    mark_tasks_inherited,
    parse_all_tasks, generate_review as _generate_review_text,
    scan_split_needed,
    t,
)


# ============================================================
# 配置加载
# ============================================================

def load_config(config_path: Path = None) -> dict:
    """
    加载配置文件。搜索顺序：
    1. 显式传入的路径
    2. server.py 同目录下的 config.json
    """
    if config_path and config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))

    default = Path(__file__).parent / "config.json"
    if default.exists():
        return json.loads(default.read_text(encoding="utf-8"))

    raise FileNotFoundError(
        "找不到 config.json。请在 server.py 同目录下放置 config.json，"
        "或用 --config 指定路径。"
    )


# 解析命令行 --config 参数
_config_path = None
if "--config" in sys.argv:
    idx = sys.argv.index("--config")
    if idx + 1 < len(sys.argv):
        _config_path = Path(sys.argv[idx + 1])

_config = load_config(_config_path)

DAILY_DIR = Path(_config["daily_dir"])
DASHBOARD_FILE = Path(_config.get("dashboard_file", str(DAILY_DIR.parent / "Dashboard.md")))
LANG = _config.get("language", "zh")


# ============================================================
# MCP Server 定义
# ============================================================

mcp = FastMCP(
    name="日常小助手",
    instructions="""你是一个个人任务管理助手。
通过 MCP tools 可以读取用户的每日待办、推荐下一步行动、继承任务、检测超期、生成回顾。
确定性操作（读取/排序/统计）由 tool 完成，零 token 消耗。
只在用户需要 AI 创造力时（如任务拆分、卡住求建议）才需要你的推理能力。

可用 tools:
- recommend_next: 推荐下一步该做什么
- get_today: 读取今日待办文件
- inherit_tasks: 将昨天未完成的任务继承到今天
- check_overdue: 检测所有超期任务
- generate_review: 生成日终回顾并写入文件
- scan_split: 检测需要拆分的大任务（>80min 或缺预估时间）

可用 resources:
- daily://today: 今日待办内容
- daily://dashboard: Dashboard 面板
- daily://history: 最近 7 天完成统计"""
)


# ============================================================
# Tools
# ============================================================

@mcp.tool()
def recommend_next(date: str = "") -> str:
    """Recommend the next task the user should work on.

    Scans the Daily file for the given date, ranks incomplete tasks
    by priority and deadline, and returns the top recommendation.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_file = DAILY_DIR / f"{today_str}.md"

    if not today_file.exists():
        return t("srv_no_daily_file", LANG, file=f"{today_str}.md")

    content = today_file.read_text(encoding="utf-8")
    tasks = [parse_task(line, today) for line in content.split("\n")]
    tasks = [tk for tk in tasks if tk]

    if not tasks:
        has_completed = any(
            l.strip().startswith("- [x] ") for l in content.split("\n")
        )
        if has_completed:
            return t("all_done", LANG)
        else:
            return t("srv_no_tasks_yet", LANG, file=f"{today_str}.md")

    ranked = rank_tasks(tasks)
    return format_recommendation(ranked, today, LANG)


@mcp.tool()
def get_today(date: str = "") -> str:
    """Read the full content of a Daily file.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_file = DAILY_DIR / f"{today_str}.md"

    if not today_file.exists():
        return t("srv_file_not_exist", LANG, file=f"{today_str}.md")

    content = today_file.read_text(encoding="utf-8")
    return f"{t('srv_file_header', LANG, file=f'{today_str}.md')}\n\n{content}"


@mcp.tool()
def inherit_tasks(date: str = "") -> str:
    """Inherit incomplete tasks from the previous day into a new Daily file.

    Will not overwrite if the target file already exists.

    Args:
        date: Target date in YYYY-MM-DD format. Defaults to today.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_file = DAILY_DIR / f"{today_str}.md"

    if today_file.exists():
        return t("srv_already_exists", LANG, file=f"{today_str}.md")

    latest = find_latest_daily(DAILY_DIR, before_date=today)

    if not latest:
        create_today_file(DAILY_DIR, today, [], None, LANG)
        return t("srv_no_previous", LANG, file=f"{today_str}.md")

    uncompleted = extract_uncompleted_tasks(latest)

    if not uncompleted:
        create_today_file(DAILY_DIR, today, [], None, LANG)
        return t("srv_all_completed", LANG, src=latest.name, file=f"{today_str}.md")

    source_date = latest.stem
    create_today_file(DAILY_DIR, today, uncompleted, source_date, LANG)

    # 标记源文件中的任务为已继承，避免重复计数
    marked = mark_tasks_inherited(latest, today_str)

    task_list = "\n".join(f"  {tk}" for tk in uncompleted)
    return (
        t("srv_inherit_done", LANG,
          file=f"{today_str}.md", src=latest.name,
          marked=marked, count=len(uncompleted))
        + f"\n\n{task_list}"
    )


@mcp.tool()
def check_overdue(date: str = "") -> str:
    """Detect all overdue Daily files (past dates with incomplete tasks).

    Args:
        date: Current date in YYYY-MM-DD format. Defaults to today.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    overdue = scan_overdue_files(DAILY_DIR, today)

    if not overdue:
        return t("srv_no_overdue", LANG, date=today_str)

    total_tasks = sum(len(item["uncompleted"]) for item in overdue)
    lines = [t("srv_overdue_found", LANG, files=len(overdue), tasks=total_tasks), ""]

    for item in overdue:
        lines.append(t("srv_overdue_file", LANG, date=item["date"], days=item["days_ago"]))
        for task in item["uncompleted"]:
            lines.append(f"   {task}")
        lines.append("")

    lines.append(t("srv_overdue_tip", LANG))
    return "\n".join(lines)


@mcp.tool()
def generate_review(date: str = "", write: bool = True) -> str:
    """Generate an end-of-day review (completion rate + time stats + suggestions).

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
        write: Whether to write the review into the Daily file. Default True.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_file = DAILY_DIR / f"{today_str}.md"

    if not today_file.exists():
        return t("srv_no_daily_file", LANG, file=f"{today_str}.md")

    content = today_file.read_text(encoding="utf-8")
    completed, uncompleted = parse_all_tasks(content)

    total = len(completed) + len(uncompleted)
    if total == 0:
        return t("srv_no_task_record", LANG)

    review = _generate_review_text(completed, uncompleted, today_str, LANG)

    if write:
        marker = "## 📊 日终回顾（自动生成"
        marker_en = "## 📊 Daily Review (auto-generated"
        if marker in content or marker_en in content:
            split_marker = marker if marker in content else marker_en
            parts = content.split(split_marker)
            before = parts[0].rstrip()
            new_content = before + "\n\n" + review + "\n"
        else:
            manual_marker = "## 📊 日终回顾"
            manual_marker_en = "## 📊 End of Day Review"
            if manual_marker in content:
                idx = content.index(manual_marker)
                before = content[:idx].rstrip()
                new_content = before + "\n\n" + review + "\n"
            elif manual_marker_en in content:
                idx = content.index(manual_marker_en)
                before = content[:idx].rstrip()
                new_content = before + "\n\n" + review + "\n"
            else:
                new_content = content.rstrip() + "\n\n" + review + "\n"

        today_file.write_text(new_content, encoding="utf-8")
        return f"{review}\n\n{t('srv_review_written', LANG, file=f'{today_str}.md')}"

    return review


@mcp.tool()
def scan_split(date: str = "") -> str:
    """Detect tasks that need splitting (>80min or missing time estimate).

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    today = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    issues = scan_split_needed(DAILY_DIR, today)

    if not issues:
        return t("srv_split_ok", LANG, date=today_str)

    too_long = [i for i in issues if i["type"] == "too_long"]
    no_est = [i for i in issues if i["type"] == "no_estimate"]

    lines = []
    if too_long:
        lines.append(t("srv_split_too_long", LANG, n=len(too_long)))
        for item in too_long:
            lines.append(f"  ⚠️ 『{item['description']}』— {item['minutes']}min")
        lines.append("")

    if no_est:
        lines.append(t("srv_split_no_est", LANG, n=len(no_est)))
        for item in no_est:
            lines.append(f"  ❓ 『{item['description']}』")
        lines.append("")

    lines.append(t("srv_split_tip", LANG))
    return "\n".join(lines)


# ============================================================
# Resources
# ============================================================

@mcp.resource("daily://today")
def resource_today() -> str:
    """今日 Daily 待办文件的完整内容。"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_file = DAILY_DIR / f"{today_str}.md"

    if not today_file.exists():
        return t("srv_file_not_exist", LANG, file=f"{today_str}.md")
    return today_file.read_text(encoding="utf-8")


@mcp.resource("daily://dashboard")
def resource_dashboard() -> str:
    """Dashboard 面板内容。"""
    if not DASHBOARD_FILE.exists():
        return "⚠️ Dashboard.md 不存在"
    return DASHBOARD_FILE.read_text(encoding="utf-8")


@mcp.resource("daily://history")
def resource_history() -> str:
    """最近 7 天的任务完成统计。"""
    today = datetime.now()
    hdr = t("srv_history_hdr", LANG)
    lines = [t("srv_history_title", LANG), ""]
    lines.append(f"| {hdr[0]} | {hdr[1]} | {hdr[2]} | {hdr[3]} |")
    lines.append("|------|:----:|:------:|:------:|")

    for i in range(7):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_file = DAILY_DIR / f"{day_str}.md"

        if not day_file.exists():
            lines.append(f"| {day_str} | — | — | {t('srv_no_file', LANG)} |")
            continue

        content = day_file.read_text(encoding="utf-8")
        completed, uncompleted = parse_all_tasks(content)
        total = len(completed) + len(uncompleted)

        if total == 0:
            lines.append(f"| {day_str} | 0 | 0 | {t('srv_no_tasks', LANG)} |")
        else:
            pct = round(len(completed) / total * 100)
            lines.append(f"| {day_str} | {len(completed)} | {len(uncompleted)} | {pct}% |")

    return "\n".join(lines)


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    mcp.run()
