"""管理本地生产力管控系统。"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

from .config_manager import load_config
from .dida_semantics import is_current_task_completed, normalize_priority_name

DEFAULT_PRODUCTIVITY_ROOT = "~/.dida-coach/productivity"
PRODUCTIVITY_DIRECTORIES = (
    "commitments",
    "planning",
    "reviews",
    "focus",
    "routines",
    "goals",
    "projects",
    "habits",
    "someday",
    "sync",
)
MANAGED_FILE_ORDER = (
    "dashboard.md",
    "commitments/promises.md",
    "commitments/delegated.md",
    "planning/daily.md",
    "planning/weekly.md",
    "planning/focus-blocks.md",
    "reviews/weekly.md",
    "reviews/monthly.md",
    "focus/sessions.md",
    "focus/distractions.md",
    "routines/morning.md",
    "routines/shutdown.md",
    "goals/active.md",
    "projects/active.md",
    "habits/active.md",
    "someday/ideas.md",
    "sync/last-sync.md",
    "sync/latest-summary.json",
)


def _parse_iso_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _format_when(value: Optional[datetime]) -> str:
    if not value:
        return "未设置"
    return value.strftime("%Y-%m-%d %H:%M")


def _as_title(task: Mapping[str, object]) -> str:
    return str(task.get("title") or "未命名任务").strip() or "未命名任务"


def _as_project(task: Mapping[str, object]) -> str:
    for key in ("project_name", "project", "list_name"):
        value = task.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "未归类清单"


def _as_priority(task: Mapping[str, object]) -> str:
    raw = task.get("priority")
    if isinstance(raw, str):
        normalized = normalize_priority_name(raw)
        if normalized in {"low", "medium", "high"}:
            return normalized
    if isinstance(raw, int):
        if raw >= 5:
            return "high"
        if raw >= 3:
            return "medium"
    return "low"


def _priority_rank(task: Mapping[str, object]) -> int:
    label = _as_priority(task)
    if label == "high":
        return 3
    if label == "medium":
        return 2
    return 1


def _priority_label(priority: str) -> str:
    return {"high": "高", "medium": "中", "low": "低"}.get(priority, "低")


def _looks_waiting(task: Mapping[str, object]) -> bool:
    haystack = " ".join(
        str(task.get(key, ""))
        for key in ("title", "content", "desc", "notes", "status")
    ).lower()
    tags = " ".join(str(tag).lower() for tag in task.get("tags", []))
    combined = f"{haystack} {tags}"
    markers = ("等待", "待反馈", "blocked", "waiting", "delegate", "delegated", "跟进")
    return any(marker in combined for marker in markers)


def _task_brief(task: Mapping[str, object], *, now: Optional[datetime]) -> Dict[str, str]:
    due = _parse_iso_datetime(str(task.get("due_date") or task.get("start_date") or ""))
    priority = _as_priority(task)
    status = "已完成" if is_current_task_completed(dict(task)) else "待办"
    risk = ""
    if now and due and not is_current_task_completed(dict(task)):
        if due < now:
            risk = "已逾期"
        elif (due - now).total_seconds() <= 24 * 3600:
            risk = "24 小时内到期"
    return {
        "title": _as_title(task),
        "project": _as_project(task),
        "priority": priority,
        "priority_label": _priority_label(priority),
        "due": _format_when(due),
        "status": status,
        "risk": risk,
    }


def _top_items(
    tasks: Sequence[Mapping[str, object]],
    *,
    now: Optional[datetime],
    limit: int,
) -> List[Dict[str, str]]:
    ranked = sorted(
        tasks,
        key=lambda item: (
            0 if _task_brief(item, now=now)["risk"] == "已逾期" else 1,
            0 if _task_brief(item, now=now)["risk"] == "24 小时内到期" else 1,
            -_priority_rank(item),
            _format_when(_parse_iso_datetime(str(item.get("due_date") or item.get("start_date") or ""))),
        ),
    )
    return [_task_brief(task, now=now) for task in ranked[:limit]]


def _frequency_map(tasks: Sequence[Mapping[str, object]]) -> Dict[str, int]:
    counters: Dict[str, int] = {}
    for task in tasks:
        title = _as_title(task)
        counters[title] = counters.get(title, 0) + 1
    return counters


def get_productivity_root(config: Optional[Mapping[str, object]] = None) -> Path:
    """返回本地生产力系统目录。"""

    override = os.environ.get("DIDA_COACH_PRODUCTIVITY_ROOT")
    if override:
        return Path(override).expanduser()

    if config is None:
        config = load_config()
    root = (
        config.get("productivity_system", {}).get("root", DEFAULT_PRODUCTIVITY_ROOT)
        if isinstance(config, Mapping)
        else DEFAULT_PRODUCTIVITY_ROOT
    )
    return Path(str(root)).expanduser()


def get_managed_file_paths(root: Optional[Path] = None) -> Dict[str, Path]:
    """返回所有受管文件路径。"""

    base = Path(root) if root else get_productivity_root()
    return {relative: base / relative for relative in MANAGED_FILE_ORDER}


def is_productivity_system_initialized(root: Optional[Path] = None) -> bool:
    """检查本地生产力系统是否已初始化。"""

    paths = get_managed_file_paths(root)
    return all(path.exists() for path in paths.values())


def build_productivity_snapshot(
    projects: Sequence[Mapping[str, object]],
    undone_tasks: Sequence[Mapping[str, object]],
    completed_tasks: Sequence[Mapping[str, object]],
    *,
    now: Optional[datetime] = None,
) -> Dict[str, object]:
    """把滴答数据归纳成本地生产力系统所需的摘要。"""

    current_time = now or datetime.now().astimezone()
    active_undone = [task for task in undone_tasks if not is_current_task_completed(dict(task))]
    waiting = [task for task in active_undone if _looks_waiting(task)]
    top_focus = _top_items(active_undone, now=current_time, limit=3)
    risk_items = [item for item in _top_items(active_undone, now=current_time, limit=8) if item["risk"]]
    promises = _top_items(
        [task for task in active_undone if _priority_rank(task) >= 2],
        now=current_time,
        limit=6,
    )
    delegated = [_task_brief(task, now=current_time) for task in waiting[:6]]
    completed_briefs = [_task_brief(task, now=current_time) for task in completed_tasks[:5]]
    project_names = [
        str(item.get("name") or item.get("title") or "").strip()
        for item in projects
        if str(item.get("name") or item.get("title") or "").strip()
    ][:10]
    repeated = [
        {"title": title, "count": count}
        for title, count in _frequency_map(active_undone).items()
        if count >= 2
    ][:5]

    return {
        "generated_at": current_time.isoformat(),
        "counts": {
            "projects": len(projects),
            "undone": len(active_undone),
            "completed_recent": len(completed_tasks),
            "waiting": len(waiting),
        },
        "focus_now": top_focus,
        "risks": risk_items,
        "promises": promises,
        "delegated": delegated,
        "completed_recent": completed_briefs,
        "project_names": project_names,
        "repeated_titles": repeated,
        "notes": [
            "本地系统只保存摘要与管理视角，不复制完整滴答任务库。",
            "任务执行、提醒、完成状态仍以滴答清单为准。",
        ],
    }


def _render_brief_list(items: Sequence[Mapping[str, str]], empty: str) -> List[str]:
    if not items:
        return [f"- {empty}"]
    lines = []
    for item in items:
        title = str(item.get("title", "未命名任务"))
        project = str(item.get("project", "未归类清单"))
        due = str(item.get("due", "未设置"))
        risk = str(item.get("risk", ""))
        suffix = f"｜{project}｜{due}"
        if risk:
            suffix += f"｜{risk}"
        lines.append(f"- {title}（{suffix}）")
    return lines


def render_dashboard(snapshot: Mapping[str, object]) -> str:
    counts = snapshot.get("counts", {})
    focus_now = snapshot.get("focus_now", [])
    risks = snapshot.get("risks", [])
    notes = snapshot.get("notes", [])
    lines = [
        "# Dashboard",
        "",
        f"- 最近同步：{snapshot.get('generated_at', '')}",
        f"- 当前未完成：{counts.get('undone', 0)}",
        f"- 近期已完成：{counts.get('completed_recent', 0)}",
        f"- 等待项：{counts.get('waiting', 0)}",
        "",
        "## 当前最该推进",
        *_render_brief_list(focus_now, "暂无明确焦点，先从最高承诺里挑 1 件"),
        "",
        "## 风险与过载",
        *_render_brief_list(risks, "暂无高风险项"),
        "",
        "## 系统说明",
    ]
    for note in notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def render_promises(snapshot: Mapping[str, object]) -> str:
    lines = [
        "# 承诺清单",
        "",
        "这些事项用于提醒你真正答应过自己或他人的事情，不等于完整任务库。",
        "",
        "## 当前承诺",
        *_render_brief_list(snapshot.get("promises", []), "暂无明确承诺项"),
    ]
    return "\n".join(lines) + "\n"


def render_delegated(snapshot: Mapping[str, object]) -> str:
    lines = [
        "# 等待与委派",
        "",
        "## 等待别人推进或反馈",
        *_render_brief_list(snapshot.get("delegated", []), "暂无等待项"),
        "",
        "## 本周跟进提醒",
    ]
    for item in snapshot.get("delegated", [])[:3]:
        lines.append(f"- 跟进 {item.get('title')}，确认下一步和反馈时间。")
    if not snapshot.get("delegated", []):
        lines.append("- 本周无需额外跟进委派项。")
    return "\n".join(lines) + "\n"


def render_weekly_plan(snapshot: Mapping[str, object]) -> str:
    lines = [
        "# 本周计划",
        "",
        "## 本周必须推进",
        *_render_brief_list(snapshot.get("focus_now", []), "从 dashboard 里补 1-3 个重点"),
        "",
        "## 承诺检查",
        *_render_brief_list(snapshot.get("promises", [])[:3], "暂无高压承诺"),
        "",
        "## 等待项",
        *_render_brief_list(snapshot.get("delegated", [])[:3], "暂无等待项"),
    ]
    return "\n".join(lines) + "\n"


def render_weekly_review(snapshot: Mapping[str, object]) -> str:
    lines = [
        "# 周复盘",
        "",
        f"- 同步时间：{snapshot.get('generated_at', '')}",
        "",
        "## 本周走势",
        "- 先看承诺项是否推进，再看等待项是否卡住，最后确认过载来自优先级、等待还是精力。",
        "",
        "## 本周亮点",
        *_render_brief_list(snapshot.get("completed_recent", []), "本周亮点待补"),
        "",
        "## 本周阻塞",
        *_render_brief_list(snapshot.get("risks", []), "暂无明显阻塞"),
        "",
        "## 下周重点",
        *_render_brief_list(snapshot.get("focus_now", []), "下周重点待补"),
    ]
    return "\n".join(lines) + "\n"


def render_monthly_review(snapshot: Mapping[str, object]) -> str:
    repeated = snapshot.get("repeated_titles", [])
    lines = [
        "# 月复盘",
        "",
        f"- 同步时间：{snapshot.get('generated_at', '')}",
        "",
        "## 月度判断",
        "- 结合承诺堆积、等待项数量、重复拖延主题和专注摩擦，找出一个最核心瓶颈。",
        "",
        "## 重复出现的话题",
    ]
    if repeated:
        for item in repeated:
            lines.append(f"- {item.get('title')}（{item.get('count')} 次）")
    else:
        lines.append("- 暂无明显重复主题")
    lines.extend(
        [
            "",
            "## 下月重点",
            *_render_brief_list(snapshot.get("focus_now", []), "先从 dashboard 里挑 1-2 个重点"),
        ]
    )
    return "\n".join(lines) + "\n"


def render_static_template(title: str, bullets: Sequence[str]) -> str:
    lines = [f"# {title}", ""]
    for bullet in bullets:
        lines.append(f"- {bullet}")
    return "\n".join(lines) + "\n"


def _managed_content(snapshot: Mapping[str, object]) -> Dict[str, str]:
    return {
        "dashboard.md": render_dashboard(snapshot),
        "commitments/promises.md": render_promises(snapshot),
        "commitments/delegated.md": render_delegated(snapshot),
        "planning/daily.md": render_static_template(
            "今日计划",
            [
                "先从 dashboard 的当前重点里选 1-3 件必须推进的事。",
                "如果今天精力有限，先收缩承诺，再安排时间盒。",
            ],
        ),
        "planning/weekly.md": render_weekly_plan(snapshot),
        "planning/focus-blocks.md": render_static_template(
            "专注时间块",
            [
                "记录本周深度工作块、恢复块和会议密集段。",
                "只写摘要，不复制完整任务明细。",
            ],
        ),
        "reviews/weekly.md": render_weekly_review(snapshot),
        "reviews/monthly.md": render_monthly_review(snapshot),
        "focus/sessions.md": render_static_template(
            "专注记录",
            [
                "记录每次深度工作主题、是否达成成果、持续时长和偏差。",
                "重点看哪些任务最容易进入状态。",
            ],
        ),
        "focus/distractions.md": render_static_template(
            "干扰清单",
            [
                "记录打断来源、发生时段、下次要减少的摩擦。",
                "只保留重复模式，不要写成流水账。",
            ],
        ),
        "routines/morning.md": render_static_template(
            "晨间流程",
            [
                "确认今天的 1-3 个重点。",
                "检查最关键承诺和第一段专注时间。",
            ],
        ),
        "routines/shutdown.md": render_static_template(
            "收尾流程",
            [
                "更新未完成项的下一步，不把模糊任务直接带到明天。",
                "确认等待项、委派项和次日第一件事。",
            ],
        ),
        "goals/active.md": render_static_template(
            "活跃目标",
            ["记录当前正在推进的结果型目标及其下一阶段项目。"],
        ),
        "projects/active.md": render_static_template(
            "活跃项目",
            ["记录当前进行中的项目摘要和关键里程碑。"],
        ),
        "habits/active.md": render_static_template(
            "活跃习惯",
            ["记录支持执行系统的核心习惯，以及最常见的失效摩擦。"],
        ),
        "someday/ideas.md": render_static_template(
            "搁置想法",
            ["把暂不承诺的机会和想法停放在这里。"],
        ),
        "sync/last-sync.md": render_static_template(
            "最近同步",
            [f"最近一次从滴答摘要同步：{snapshot.get('generated_at', '')}"],
        ),
        "sync/latest-summary.json": json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
    }


def initialize_productivity_system(
    snapshot: Mapping[str, object],
    *,
    root: Optional[Path] = None,
    overwrite: bool = False,
) -> List[Path]:
    """初始化本地生产力系统目录和受管文件。"""

    base = Path(root) if root else get_productivity_root()
    base.mkdir(parents=True, exist_ok=True)
    for directory in PRODUCTIVITY_DIRECTORIES:
        (base / directory).mkdir(parents=True, exist_ok=True)

    written: List[Path] = []
    for relative, content in _managed_content(snapshot).items():
        path = base / relative
        if path.exists() and not overwrite:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def update_productivity_files(
    snapshot: Mapping[str, object],
    *,
    root: Optional[Path] = None,
    files: Optional[Iterable[str]] = None,
) -> List[Path]:
    """刷新指定受管文件。"""

    base = Path(root) if root else get_productivity_root()
    content_map = _managed_content(snapshot)
    targets = list(files or content_map.keys())
    written: List[Path] = []
    for relative in targets:
        if relative not in content_map:
            continue
        path = base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content_map[relative], encoding="utf-8")
        written.append(path)
    return written


def summarize_productivity_state(root: Optional[Path] = None) -> Dict[str, object]:
    """返回本地生产力系统的当前初始化状态。"""

    base = Path(root) if root else get_productivity_root()
    paths = get_managed_file_paths(base)
    existing = [relative for relative, path in paths.items() if path.exists()]
    return {
        "root": str(base),
        "initialized": len(existing) == len(paths),
        "existing_files": existing,
        "missing_files": [relative for relative, path in paths.items() if not path.exists()],
    }
