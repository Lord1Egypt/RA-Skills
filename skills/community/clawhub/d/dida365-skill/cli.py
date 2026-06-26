"""Dida365 CLI Logic."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


from auth import load_env_file, run_oauth_flow
from cache import get_cached_data, set_cached_data, invalidate_project_cache, clear_all_cache
from client import Dida365Client
from models import Project, Task


try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # type: ignore


PRIORITY_LABELS = {0: "  ", 1: "低", 3: "中", 5: "高"}


class DidaCLI:
    """
    滴答清单 CLI 处理器。
    负责业务逻辑封装与 CLI 命令分发。
    """

    def __init__(self):
        self.client = Dida365Client()

    # --- 数据获取与业务逻辑 ---

    def list_projects(self, force: bool = False) -> List[Project]:
        """列出所有项目（带缓存支持）。"""
        if not force:
            cached = get_cached_data("projects")
            if cached is not None:
                return cached
        
        projects = self.client.list_projects()
        set_cached_data("projects", projects)
        return projects

    def get_project_data(self, project_id: str, force: bool = False) -> Dict[str, Any]:
        """获取项目数据（带缓存支持）。"""
        if not force:
            cached = get_cached_data("project_data", sub_key=project_id)
            if cached is not None:
                return cached
        
        data = self.client.get_project_data(project_id)
        set_cached_data("project_data", data, sub_key=project_id)
        return data

    def get_today_tasks(self, force: bool = False) -> List[Task]:
        """获取今日到期的未完成任务。"""
        today_start = datetime.now().date().isoformat()
        return self.get_due_range_tasks(today_start, today_start, include_completed=False, force=force)

    def get_due_range_tasks(
        self,
        start_date: str,
        end_date: str,
        include_completed: bool = False,
        project_id: Optional[str] = None,
        force: bool = False,
    ) -> List[Task]:
        """使用 API 筛选器获取指定日期范围内到期的任务。"""
        # 1. 准备查询参数
        # API 的 startDate/endDate 是闭区间，且通常对应任务的时间范围
        payload: Dict[str, Any] = {
            "startDate": normalize_date(start_date),
            "endDate": normalize_date(end_date).replace("00:00:00", "23:59:59"),
            "status": [0, 2] if include_completed else [0]
        }
        if project_id:
            payload["projectIds"] = [project_id]

        # 2. 调用 API 筛选
        tasks = self.client.filter_tasks(payload)

        # 3. 补充项目名称（为了保持原有的输出格式）
        projects = self.list_projects(force=force)
        proj_map = {p["id"]: p.get("name", "") for p in projects}
        
        results: List[Task] = []
        for t in tasks:
            enriched = dict(t)
            enriched["_projectName"] = proj_map.get(t.get("projectId", ""), "未知项目")
            results.append(enriched)

        # 4. 排序：按截止日期、优先级、项目名、标题
        results.sort(key=lambda t: (
            self._get_task_date(t, "dueDate"),
            -int(t.get("priority", 0) or 0),
            t.get("_projectName", ""),
            t.get("title", ""),
        ))
        return results

    def get_inbox_data(self, force: bool = False) -> Tuple[Project, List[Task]]:
        """获取收集箱。"""

        data = self.get_project_data("inbox", force=force)
        project = data.get("project") or {"id": "inbox", "name": "收集箱"}
        return project, data.get("tasks", [])
    # --- 辅助方法 ---

    def _get_task_date(self, task: Task, field: str) -> str:
        """解析日期字段为 YYYY-MM-DD。"""
        val = task.get(field)
        if not val:
            return ""
        
        parsed = self._parse_api_datetime(val)
        if not parsed:
            return ""
        
        # 时区处理
        tz_info = datetime.now().astimezone().tzinfo
        tz_name = task.get("timeZone")
        if tz_name and ZoneInfo:
            try:
                tz_info = ZoneInfo(tz_name)
            except Exception:
                pass
        
        return parsed.astimezone(tz_info).date().isoformat()

    def _parse_api_datetime(self, value: Any) -> Optional[datetime]:
        """通用 API 日期解析。"""
        if not value:
            return None
        if isinstance(value, (int, float)):
            ts = float(value)
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts, tz=datetime.now().astimezone().tzinfo)
        
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    # --- 格式化方法 ---

    def format_task_list(self, tasks: List[Task], title: str = "任务列表") -> str:
        if not tasks: return f"{title}: 无任务"
        lines = [f"{title}:\n"]
        for t in tasks:
            prio = PRIORITY_LABELS.get(t.get("priority", 0), "  ")
            due = self._get_task_date(t, "dueDate")
            due_str = f" 截止:{due}" if due else ""
            tags = f" [{','.join(t.get('tags', []))}]" if t.get("tags") else ""
            proj = f" ({t['_projectName']})" if "_projectName" in t else ""
            status = " ✓" if t.get("status") == 2 else ""
            lines.append(f"  [{prio}] {t.get('title', '')}{status}{due_str}{tags}{proj}")
            lines.append(f"       ID: {t.get('id')}  项目ID: {t.get('projectId')}")
        lines.append(f"\n共 {len(tasks)} 个任务")
        return "\n".join(lines)

    def format_project_detail(self, data: Dict[str, Any]) -> str:
        proj = data.get("project", {})
        tasks = data.get("tasks", [])
        lines = [f"项目: {proj.get('name')} [{proj.get('id')}]", ""]
        if not tasks:
            lines.append("  无任务")
        else:
            for t in tasks:
                prio = PRIORITY_LABELS.get(t.get("priority", 0), "  ")
                due = self._get_task_date(t, "dueDate")
                due_str = f" 截止:{due}" if due else ""
                status = " ✓" if t.get("status") == 2 else ""
                lines.append(f"  [{prio}] {t.get('title')}{status}{due_str}")
                lines.append(f"       ID: {t.get('id')}")
        lines.append(f"\n共 {len(tasks)} 个任务")
        return "\n".join(lines)


# --- 命令处理函数 ---

def cmd_auth(args, cli: DidaCLI):
    run_oauth_flow(args.code)

def cmd_project_list(args, cli: DidaCLI):
    projects = cli.list_projects(force=args.force)
    lines = ["项目列表:\n"]
    for p in projects:
        archived = " (已归档)" if p.get("closed") else ""
        lines.append(f"  [{p['id']}] {p['name']}{archived}")
    lines.append(f"\n共 {len(projects)} 个项目")
    print("\n".join(lines))

def cmd_project_get(args, cli: DidaCLI):
    print(cli.format_project_detail(cli.get_project_data(args.id, force=args.force)))

def cmd_project_create(args, cli: DidaCLI):
    payload: Project = {"name": args.name}
    if args.color: payload["color"] = args.color
    if args.kind: payload["kind"] = args.kind.upper()
    if args.view_mode: payload["viewMode"] = args.view_mode
    if args.sort_order is not None: payload["sortOrder"] = args.sort_order
    
    res = cli.client.create_project(payload)
    invalidate_project_cache()
    print(f"项目创建成功: {res['name']} [{res['id']}]")

def cmd_project_update(args, cli: DidaCLI):
    payload: Project = {}
    if args.name: payload["name"] = args.name
    if args.color: payload["color"] = args.color
    if args.view_mode: payload["viewMode"] = args.view_mode
    if args.sort_order is not None: payload["sortOrder"] = args.sort_order
    
    res = cli.client.update_project(args.id, payload)
    invalidate_project_cache(args.id)
    print(f"项目更新成功: {res['name']} [{res['id']}]")

def cmd_project_delete(args, cli: DidaCLI):
    cli.client.delete_project(args.id)
    invalidate_project_cache(args.id)
    print(f"项目已删除: {args.id}")

def cmd_task_create(args, cli: DidaCLI):
    payload: Task = {"title": args.title}
    if args.project: payload["projectId"] = args.project
    if args.content: payload["content"] = args.content
    if args.due: payload["dueDate"] = normalize_date(args.due)
    if args.priority is not None: payload["priority"] = args.priority
    if args.tags: payload["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.all_day is not None: payload["isAllDay"] = args.all_day
    if args.tz: payload["timeZone"] = args.tz
    if args.repeat: payload["repeatFlag"] = args.repeat
    if args.desc: payload["desc"] = args.desc
    
    res = cli.client.create_task(payload)
    invalidate_project_cache(res.get("projectId"))
    print(f"任务创建成功: {res['title']} [{res['id']}]")

def cmd_task_update(args, cli: DidaCLI):
    payload: Task = {}
    if args.title: payload["title"] = args.title
    if args.content: payload["content"] = args.content
    if args.due: payload["dueDate"] = normalize_date(args.due)
    if args.priority is not None: payload["priority"] = args.priority
    if args.tags: payload["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.all_day is not None: payload["isAllDay"] = args.all_day
    if args.tz: payload["timeZone"] = args.tz
    if args.repeat: payload["repeatFlag"] = args.repeat
    if args.desc: payload["desc"] = args.desc
    
    res = cli.client.update_task(args.id, args.project, payload)
    invalidate_project_cache(args.project)
    print(f"任务更新成功: {res['title']} [{res['id']}]")

def cmd_task_create_checklist(args, cli: DidaCLI):
    items = [{"title": item.strip(), "status": 0} for item in args.items.split("|")]
    payload: Task = {
        "title": args.title,
        "projectId": args.project,
        "items": items,
        "kind": "CHECKLIST"
    }
    if args.content: payload["content"] = args.content
    if args.due: payload["dueDate"] = normalize_date(args.due)
    if args.priority is not None: payload["priority"] = args.priority
    
    res = cli.client.create_task(payload)
    invalidate_project_cache(args.project)
    print(f"Checklist 创建成功: {res['title']} [{res['id']}]")

def cmd_project_info(args, cli: DidaCLI):
    res = cli.client.get_project(args.id)
    lines = [
        f"项目: {res.get('name')} [{res.get('id')}]",
        f"类型: {res.get('kind')}",
        f"视图: {res.get('viewMode')}",
        f"颜色: {res.get('color')}",
        f"已关闭: {'是' if res.get('closed') else '否'}"
    ]
    print("\n".join(lines))

def cmd_project_clear_cache(args, cli: DidaCLI):
    clear_all_cache()
    print("缓存已清除。")

def cmd_task_get(args, cli: DidaCLI):
    task = cli.client.get_task(args.project, args.id)
    print(json.dumps(task, ensure_ascii=False, indent=2))

def cmd_task_complete(args, cli: DidaCLI):
    cli.client.complete_task(args.project, args.id)
    invalidate_project_cache(args.project)
    print(f"任务已完成: {args.id}")

def cmd_task_delete(args, cli: DidaCLI):
    cli.client.delete_task(args.project, args.id)
    invalidate_project_cache(args.project)
    print(f"任务已删除: {args.id}")

def cmd_task_move(args, cli: DidaCLI):
    ops = [{"fromProjectId": args.from_project, "toProjectId": args.to_project, "taskId": args.id}]
    res = cli.client.move_tasks(ops)
    invalidate_project_cache(args.from_project)
    invalidate_project_cache(args.to_project)
    print("任务移动成功。")

def cmd_search_today(args, cli: DidaCLI):
    print(cli.format_task_list(cli.get_today_tasks(force=args.force), "今日待办"))

def cmd_search_upcoming(args, cli: DidaCLI):
    start = datetime.now().date()
    end = start + timedelta(days=args.days - 1)
    tasks = cli.get_due_range_tasks(start.isoformat(), end.isoformat(), project_id=args.project, force=args.force)
    print(cli.format_task_list(tasks, f"未来 {args.days} 天到期任务 ({start.isoformat()} ~ {end.isoformat()})"))

def cmd_search_due_range(args, cli: DidaCLI):
    tasks = cli.get_due_range_tasks(args.start, args.end, project_id=args.project, force=args.force)
    print(cli.format_task_list(tasks, f"到期任务 ({args.start} ~ {args.end})"))

def cmd_search_completed(args, cli: DidaCLI):
    project_ids = [args.project] if args.project else None
    tasks = cli.client.list_completed_tasks(project_ids=project_ids, start_date=args.start, end_date=args.end)
    print(cli.format_task_list(tasks, f"已完成任务 ({args.start} ~ {args.end})"))

def cmd_search_filter(args, cli: DidaCLI):
    payload: Dict[str, Any] = {}
    if args.project: payload["projectIds"] = [args.project]
    if args.start: payload["startDate"] = normalize_date(args.start)
    if args.end: payload["endDate"] = normalize_date(args.end)
    if args.priority: payload["priority"] = [int(p) for p in args.priority.split(",")]
    if args.tags: payload["tag"] = [t.strip() for t in args.tags.split(",")]
    if args.status: payload["status"] = [int(s) for s in args.status.split(",")]
    
    tasks = cli.client.filter_tasks(payload)
    print(cli.format_task_list(tasks, "筛选结果"))

def cmd_search_inbox(args, cli: DidaCLI):
    project, tasks = cli.get_inbox_data(force=args.force)
    print(cli.format_task_list(tasks, f"收集箱 ({project['name']})"))


# --- 辅助工具 ---

def normalize_date(date_str: str) -> str:
    if "T" in date_str: return date_str
    offset = datetime.now().astimezone().strftime("%z") or "+0000"
    return f"{date_str}T00:00:00{offset}"

def repair_argv():
    if len(sys.argv) < 2: return
    categories = ["project", "task", "search", "auth", "check"]
    cat_arg = sys.argv[1]
    for cat in categories:
        if cat_arg.startswith(cat) and len(cat_arg) > len(cat):
            sys.argv[1] = cat
            sys.argv.insert(2, cat_arg[len(cat):])
            break

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="滴答清单 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Auth
    p_auth = subparsers.add_parser("auth", help="认证")
    p_auth.add_argument("--code", help="手动授权码")
    p_auth.set_defaults(func=cmd_auth)

    # Project
    p_proj = subparsers.add_parser("project", help="项目管理")
    ps_proj = p_proj.add_subparsers(dest="sub", required=True)
    
    pp_list = ps_proj.add_parser("list", help="列表")
    pp_list.add_argument("--force", action="store_true")
    pp_list.set_defaults(func=cmd_project_list)
    
    pp_get = ps_proj.add_parser("get", help="详情")
    pp_get.add_argument("id")
    pp_get.add_argument("--force", action="store_true")
    pp_get.set_defaults(func=cmd_project_get)
    
    pp_create = ps_proj.add_parser("create", help="创建")
    pp_create.add_argument("name")
    pp_create.add_argument("--color")
    pp_create.add_argument("--kind", choices=["TASK", "NOTE"])
    pp_create.add_argument("--view-mode", choices=["list", "kanban", "timeline"])
    pp_create.add_argument("--sort-order", type=int)
    pp_create.set_defaults(func=cmd_project_create)
    
    pp_update = ps_proj.add_parser("update", help="更新")
    pp_update.add_argument("id")
    pp_update.add_argument("--name")
    pp_update.add_argument("--color")
    pp_update.add_argument("--view-mode", choices=["list", "kanban", "timeline"])
    pp_update.add_argument("--sort-order", type=int)
    pp_update.set_defaults(func=cmd_project_update)
    
    ps_proj.add_parser("info").add_argument("id")
    ps_proj.choices["info"].set_defaults(func=cmd_project_info)
    
    ps_proj.add_parser("delete").add_argument("id")
    ps_proj.choices["delete"].set_defaults(func=cmd_project_delete)
    
    ps_proj.add_parser("clear-cache").set_defaults(func=cmd_project_clear_cache)

    # Task
    p_task = subparsers.add_parser("task", help="任务管理")
    ps_task = p_task.add_subparsers(dest="sub", required=True)
    
    t_get = ps_task.add_parser("get")
    t_get.add_argument("project")
    t_get.add_argument("id")
    t_get.set_defaults(func=cmd_task_get)

    tt_checklist = ps_task.add_parser("create-checklist", help="创建清单任务")
    tt_checklist.add_argument("title")
    tt_checklist.add_argument("--project", required=True)
    tt_checklist.add_argument("--items", required=True, help='子项，用 "|" 分隔')
    tt_checklist.add_argument("--content")
    tt_checklist.add_argument("--due")
    tt_checklist.add_argument("--priority", type=int, choices=[0, 1, 3, 5])
    tt_checklist.set_defaults(func=cmd_task_create_checklist)
    
    tt_create = ps_task.add_parser("create", help="创建")
    tt_create.add_argument("title")
    tt_create.add_argument("--project")
    tt_create.add_argument("--content")
    tt_create.add_argument("--due")
    tt_create.add_argument("--priority", type=int, choices=[0, 1, 3, 5])
    tt_create.add_argument("--tags")
    tt_create.add_argument("--all-day", type=lambda x: x.lower() == 'true')
    tt_create.add_argument("--repeat")
    tt_create.add_argument("--tz")
    tt_create.add_argument("--desc")
    tt_create.set_defaults(func=cmd_task_create)
    
    tt_update = ps_task.add_parser("update")
    tt_update.add_argument("project")
    tt_update.add_argument("id")
    tt_update.add_argument("--title")
    tt_update.add_argument("--content")
    tt_update.add_argument("--due")
    tt_update.add_argument("--priority", type=int, choices=[0, 1, 3, 5])
    tt_update.add_argument("--tags")
    tt_update.add_argument("--all-day", type=lambda x: x.lower() == 'true')
    tt_update.add_argument("--repeat")
    tt_update.add_argument("--tz")
    tt_update.add_argument("--desc")
    tt_update.set_defaults(func=cmd_task_update)
    
    ps_task.add_parser("complete").add_argument("project")
    ps_task.choices["complete"].add_argument("id")
    ps_task.choices["complete"].set_defaults(func=cmd_task_complete)
    
    ps_task.add_parser("delete").add_argument("project")
    ps_task.choices["delete"].add_argument("id")
    ps_task.choices["delete"].set_defaults(func=cmd_task_delete)
    
    t_move = ps_task.add_parser("move")
    t_move.add_argument("from_project")
    t_move.add_argument("to_project")
    t_move.add_argument("id")
    t_move.set_defaults(func=cmd_task_move)

    # Search
    p_search = subparsers.add_parser("search", help="查询")
    ps_search = p_search.add_subparsers(dest="sub", required=True)
    
    ps_search.add_parser("today").set_defaults(func=cmd_search_today, force=False)
    
    ps_upcoming = ps_search.add_parser("upcoming")
    ps_upcoming.add_argument("days", type=int, nargs="?", default=7)
    ps_upcoming.add_argument("--project")
    ps_upcoming.add_argument("--force", action="store_true")
    ps_upcoming.set_defaults(func=cmd_search_upcoming)
    
    ps_range = ps_search.add_parser("due-range")
    ps_range.add_argument("start")
    ps_range.add_argument("end")
    ps_range.add_argument("--project")
    ps_range.add_argument("--force", action="store_true")
    ps_range.set_defaults(func=cmd_search_due_range)
    
    ps_completed = ps_search.add_parser("completed")
    ps_completed.add_argument("start")
    ps_completed.add_argument("end")
    ps_completed.add_argument("--project")
    ps_completed.set_defaults(func=cmd_search_completed)
    
    ps_filter = ps_search.add_parser("filter")
    ps_filter.add_argument("--project")
    ps_filter.add_argument("--start")
    ps_filter.add_argument("--end")
    ps_filter.add_argument("--priority")
    ps_filter.add_argument("--tags")
    ps_filter.add_argument("--status")
    ps_filter.set_defaults(func=cmd_search_filter)
    
    ps_inbox = ps_search.add_parser("inbox")
    ps_inbox.add_argument("--force", action="store_true")
    ps_inbox.set_defaults(func=cmd_search_inbox)

    return parser

def main():
    load_env_file()
    repair_argv()
    parser = setup_parser()
    args = parser.parse_args()
    cli = DidaCLI()
    if hasattr(args, "func"):
        args.func(args, cli)
    else:
        parser.print_help()
