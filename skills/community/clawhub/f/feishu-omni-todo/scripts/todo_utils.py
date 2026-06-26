#!/usr/bin/env python3
import json
import os
import dateparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional

TODO_FILE = os.path.expanduser("~/.openclaw/workspace/todo.json")

def load_todos() -> Dict:
    """加载Todo数据"""
    if not os.path.exists(TODO_FILE):
        return {"todos": []}
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_todos(data: Dict):
    """保存Todo数据"""
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_time(time_str: str) -> Optional[str]:
    """解析自然语言时间，返回ISO格式字符串"""
    if not time_str:
        return None
    
    now = datetime.now()
    time_str = time_str.strip().lower()
    
    # 处理简单时间格式
    if '今晚' in time_str or '今天晚上' in time_str:
        time_part = time_str.replace('今晚', '').replace('今天晚上', '').strip()
        if not time_part:
            time_part = '23:59:59'
        dt = datetime(now.year, now.month, now.day, 23, 59, 59)
        if ':' in time_part:
            h, m = map(int, time_part.split(':'))
            dt = datetime(now.year, now.month, now.day, h, m)
        return dt.isoformat()
    
    if '明晚' in time_str or '明天晚上' in time_str:
        time_part = time_str.replace('明晚', '').replace('明天晚上', '').strip()
        tomorrow = now + timedelta(days=1)
        dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
        if ':' in time_part:
            h, m = map(int, time_part.split(':'))
            dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, h, m)
        return dt.isoformat()
    
    if '明天' in time_str:
        time_part = time_str.replace('明天', '').strip()
        tomorrow = now + timedelta(days=1)
        dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
        if '下午' in time_part:
            time_part = time_part.replace('下午', '').strip()
            if ':' in time_part:
                h, m = map(int, time_part.split(':'))
                dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, h+12, m)
        elif '上午' in time_part:
            time_part = time_part.replace('上午', '').strip()
            if ':' in time_part:
                h, m = map(int, time_part.split(':'))
                dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, h, m)
        elif ':' in time_part:
            h, m = map(int, time_part.split(':'))
            dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day, h, m)
        return dt.isoformat()
    
    if '周三前' in time_str:
        # 计算下周三
        days_ahead = 2 - now.weekday()
        if days_ahead <= 0: # 今天已经是周三或之后
            days_ahead += 7
        next_wed = now + timedelta(days=days_ahead)
        return datetime(next_wed.year, next_wed.month, next_wed.day, 23, 59, 59).isoformat()
    
    if '周五前' in time_str:
        # 计算下周五
        days_ahead = 4 - now.weekday()
        if days_ahead <= 0: # 今天已经是周五或之后
            days_ahead += 7
        next_fri = now + timedelta(days=days_ahead)
        return datetime(next_fri.year, next_fri.month, next_fri.day, 23, 59, 59).isoformat()
    
    # 尝试ISO格式解析
    try:
        dt = datetime.fromisoformat(time_str)
        return dt.isoformat()
    except:
        pass
    
    # 尝试dateparser
    settings = {
        'PREFER_DAY_OF_MONTH': 'first',
        'PREFER_DATES_FROM': 'future',
        'TIMEZONE': 'Asia/Shanghai',
        'RETURN_AS_TIMEZONE_AWARE': False
    }
    
    dt = dateparser.parse(time_str, languages=['zh', 'en'], settings=settings)
    if dt:
        return dt.isoformat()
    
    return None

def add_todo(content: str, due_time: Optional[str] = None, source: str = "") -> int:
    """添加新待办，返回新待办的ID"""
    data = load_todos()
    todos = data["todos"]
    
    # 解析时间
    parsed_due_time = None
    if due_time:
        # 尝试解析自然语言时间
        parsed = parse_time(due_time)
        if parsed:
            parsed_due_time = parsed
        else:
            # 尝试直接解析ISO格式
            try:
                dt = datetime.fromisoformat(due_time)
                parsed_due_time = due_time
            except:
                pass
    
    # 生成新ID
    new_id = max([todo["id"] for todo in todos], default=0) + 1
    
    new_todo = {
        "id": new_id,
        "content": content,
        "created_at": datetime.now().isoformat(),
        "due_time": parsed_due_time,
        "status": "pending",
        "source": source,
        "tags": [],
        "priority": "medium"
    }
    
    todos.append(new_todo)
    save_todos(data)
    return new_id

def list_todos(include_completed: bool = False) -> List[Dict]:
    """列出待办，默认只显示未完成的"""
    data = load_todos()
    todos = data["todos"]
    
    if not include_completed:
        todos = [todo for todo in todos if todo["status"] == "pending"]
    
    # 按截止时间排序，没有截止时间的排在后面
    def sort_key(todo):
        if todo["due_time"]:
            try:
                return datetime.fromisoformat(todo["due_time"])
            except:
                return datetime.max
        return datetime.max
    
    todos.sort(key=sort_key)
    return todos

def mark_done(todo_id: int) -> Optional[Dict]:
    """标记待办为完成，返回被修改的待办"""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["status"] = "done"
            save_todos(data)
            return todo
    return None

def delete_todo(todo_id: int) -> Optional[Dict]:
    """删除待办，返回被删除的待办"""
    data = load_todos()
    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            deleted = data["todos"].pop(i)
            save_todos(data)
            return deleted
    return None

def clear_completed() -> int:
    """清空已完成的待办，返回删除的数量"""
    data = load_todos()
    original_count = len(data["todos"])
    data["todos"] = [todo for todo in data["todos"] if todo["status"] != "done"]
    save_todos(data)
    return original_count - len(data["todos"])

def set_reminder(todo_id: int, remind_time: str) -> Optional[Dict]:
    """设置提醒时间，支持自然语言"""
    data = load_todos()
    parsed_time = parse_time(remind_time)
    if not parsed_time:
        return None
    
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["due_time"] = parsed_time
            save_todos(data)
            return todo
    return None

def get_todos_with_display_order(include_completed: bool = False) -> tuple[List[Dict], Dict]:
    """获取带显示序号的待办列表，返回(列表, 序号到ID的映射)"""
    todos = list_todos(include_completed)
    display_map = {}
    for idx, todo in enumerate(todos, 1):
        display_map[idx] = todo["id"]
        todo["display_id"] = idx
    return todos, display_map

def get_id_by_display_number(display_num: int, include_completed: bool = False) -> Optional[int]:
    """根据显示序号获取真实ID"""
    _, display_map = get_todos_with_display_order(include_completed)
    return display_map.get(display_num)

def set_priority(todo_id: int, priority: str) -> Optional[Dict]:
    """设置待办优先级：high/medium/low"""
    if priority not in ["high", "medium", "low"]:
        return None
    
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["priority"] = priority
            save_todos(data)
            return todo
    return None

def add_tag(todo_id: int, tag: str) -> Optional[Dict]:
    """为待办添加标签"""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            if tag not in todo["tags"]:
                todo["tags"].append(tag)
                save_todos(data)
            return todo
    return None

def filter_by_tag(tag: str) -> List[Dict]:
    """按标签筛选待办"""
    todos = list_todos()
    return [todo for todo in todos if tag in todo.get("tags", [])]

def sync_todo_to_calendar(todo_id: int) -> Optional[str]:
    """同步待办到飞书日历"""
    todo = get_todo_by_id(todo_id)
    if not todo or not todo.get("due_time"):
        return None
    
    try:
        from feishu_calendar import sync_todo_to_calendar
        due_time = datetime.fromisoformat(todo["due_time"])
        event_id = sync_todo_to_calendar(todo["content"], due_time)
        
        if event_id:
            # 保存日历事件ID到待办
            data = load_todos()
            for t in data["todos"]:
                if t["id"] == todo_id:
                    t["calendar_event_id"] = event_id
                    save_todos(data)
                    break
            return event_id
    except Exception as e:
        print(f"同步日历失败: {e}")
    
    return None

def get_calendar_agenda(days: int = 7) -> List[Dict]:
    """获取日历日程和待办的合并视图"""
    try:
        from feishu_calendar import get_calendar_events
        calendar_events = get_calendar_events(days)
    except Exception as e:
        print(f"获取日历事件失败: {e}")
        calendar_events = []
    
    # 获取待办
    todos = list_todos()
    all_events = []
    
    # 添加日历事件
    for event in calendar_events:
        all_events.append({
            "type": "calendar",
            "title": event["title"],
            "start_time": event["start_time"],
            "end_time": event["end_time"],
            "location": event.get("location", ""),
            "priority": "medium"
        })
    
    # 添加待办事件
    for todo in todos:
        if todo.get("due_time"):
            try:
                due_time = datetime.fromisoformat(todo["due_time"])
                if due_time <= datetime.now() + timedelta(days=days):
                    all_events.append({
                        "type": "todo",
                        "title": f"[待办] {todo['content']}",
                        "start_time": due_time,
                        "end_time": due_time + timedelta(hours=1),
                        "priority": todo.get("priority", "medium"),
                        "todo_id": todo["id"]
                    })
            except:
                pass
    
    # 按时间排序
    all_events.sort(key=lambda x: x["start_time"])
    return all_events

def get_todo_by_id(todo_id: int) -> Optional[Dict]:
    """根据ID获取待办"""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            return todo
    return None

if __name__ == "__main__":
    # 测试用
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            content = " ".join(sys.argv[2:])
            todo_id = add_todo(content)
            print(f"Added todo #{todo_id}: {content}")
        elif sys.argv[1] == "list":
            todos = list_todos()
            for todo in todos:
                status = "✓" if todo["status"] == "done" else " "
                print(f"[{status}] #{todo['id']}: {todo['content']}")
