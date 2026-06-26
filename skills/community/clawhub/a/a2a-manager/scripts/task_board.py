#!/usr/bin/env python3
"""Task Board Manager - Quản lý task board trên Notion (Task-Steward style)"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# === CONFIG ===
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
CONFIG_FILE = WORKSPACE_ROOT / "a2a-manager" / "task_config.json"

# Task States (Sections)
TASK_STATES = {
    "NOW": {"name": "Now/Today", "description": "Ưu tiên cao nhất"},
    "WAITING": {"name": "Waiting", "description": "Chờ input bên ngoài"},
    "IN_PROGRESS": {"name": "In Progress", "description": "Đang làm"},
    "REVIEW": {"name": "Ready for Review", "description": "Chờ QA"},
    "DONE": {"name": "Done", "description": "Hoàn thành"}
}

# Task Tags
TASK_TAGS = {
    "working": {"name": "cora-working", "color": "blue"},
    "research": {"name": "needs-research", "color": "yellow"},
    "blocked": {"name": "blocked", "color": "red"},
    "verified": {"name": "quality-verified", "color": "green"}
}

# === NOTION API ===
NOTION_KEY_FILE = Path.home() / ".config" / "notion" / "api_key"

def get_notion_key() -> str:
    """Lấy Notion API key"""
    if NOTION_KEY_FILE.exists():
        return NOTION_KEY_FILE.read_text().strip()
    return os.environ.get("NOTION_API_KEY", "")

def notion_request(method: str, endpoint: str, data: dict = None) -> dict:
    """Gọi Notion API"""
    import urllib.request
    import urllib.error
    
    api_key = get_notion_key()
    if not api_key:
        return {"error": "No Notion API key found"}
    
    url = f"https://api.notion.com/v1{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}

# === TASK BOARD ===
def load_config() -> dict:
    """Load cấu hình task board"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"database_id": "", "tasks": {}}

def save_config(config: dict):
    """Lưu cấu hình"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def create_task_board(database_id: str = None) -> dict:
    """Tạo task board database trên Notion"""
    if not database_id:
        return {"error": "database_id required"}
    
    # Verify database exists
    result = notion_request("GET", f"/databases/{database_id}")
    if "error" in result:
        return result
    
    config = load_config()
    config["database_id"] = database_id
    config["created_at"] = datetime.now().isoformat()
    save_config(config)
    
    return {"success": True, "database_id": database_id}

# === TASK CRUD ===
def create_task(
    title: str,
    description: str = "",
    state: str = "IN_PROGRESS",
    tags: List[str] = None,
    assignee: str = None,
    due_date: str = None
) -> dict:
    """
    Tạo task mới trên Notion
    """
    config = load_config()
    database_id = config.get("database_id")
    
    if not database_id:
        return {"error": "No database_id configured. Run create_task_board first."}
    
    # Build properties
    properties = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Status": {"select": {"name": TASK_STATES.get(state, {}).get("name", "In Progress")}},
        "Description": {"rich_text": [{"text": {"content": description}}]} if description else {"rich_text": []}
    }
    
    # Add tags as multi-select
    if tags:
        properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}
    
    # Add assignee
    if assignee:
        properties["Assignee"] {"people": [{"name": assignee}]} =  # Notion API format for people is different
    
    # Add due date
    if due_date:
        properties["Due Date"] = {"date": {"start": due_date}}
    
    result = notion_request("POST", "/pages", {
        "parent": {"database_id": database_id},
        "properties": properties
    })
    
    if "error" in result:
        return result
    
    return {
        "success": True,
        "task_id": result.get("id"),
        "title": title,
        "state": state
    }

def update_task_state(task_id: str, new_state: str) -> dict:
    """Cập nhật task state"""
    state_name = TASK_STATES.get(new_state, {}).get("name", "In Progress")
    
    result = notion_request("PATCH", f"/pages/{task_id}", {
        "properties": {
            "Status": {"select": {"name": state_name}}
        }
    })
    
    if "error" in result:
        return result
    
    return {"success": True, "task_id": task_id, "new_state": new_state}

def add_task_tag(task_id: str, tag: str) -> dict:
    """Thêm tag cho task"""
    # Get current tags
    result = notion_request("GET", f"/pages/{task_id}")
    if "error" in result:
        return result
    
    current_tags = result.get("properties", {}).get("Tags", {}).get("multi_select", [])
    current_tag_names = [t.get("name") for t in current_tags]
    
    if tag not in current_tag_names:
        current_tag_names.append(tag)
    
    result = notion_request("PATCH", f"/pages/{task_id}", {
        "properties": {
            "Tags": {"multi_select": [{"name": t} for t in current_tag_names]}
        }
    })
    
    return {"success": True, "task_id": task_id, "tags": current_tag_names}

def remove_task_tag(task_id: str, tag: str) -> dict:
    """Xóa tag khỏi task"""
    result = notion_request("GET", f"/pages/{task_id}")
    if "error" in result:
        return result
    
    current_tags = result.get("properties", {}).get("Tags", {}).get("multi_select", [])
    current_tag_names = [t.get("name") for t in current_tags if t.get("name") != tag]
    
    result = notion_request("PATCH", f"/pages/{task_id}", {
        "properties": {
            "Tags": {"multi_select": [{"name": t} for t in current_tag_names]}
        }
    })
    
    return {"success": True, "task_id": task_id, "tags": current_tag_names}

def get_task(task_id: str) -> dict:
    """Lấy thông tin task"""
    return notion_request("GET", f"/pages/{task_id}")

def get_tasks_by_state(state: str = None) -> dict:
    """Lấy tasks theo state"""
    config = load_config()
    database_id = config.get("database_id")
    
    if not database_id:
        return {"error": "No database_id configured"}
    
    # Build filter
    filter_obj = None
    if state:
        state_name = TASK_STATES.get(state, {}).get("name", "In Progress")
        filter_obj = {
            "property": "Status",
            "select": {"equals": state_name}
        }
    
    query_data = {}
    if filter_obj:
        query_data["filter"] = filter_obj
    
    result = notion_request("POST", f"/databases/{database_id}/query", query_data)
    
    if "error" in result:
        return result
    
    tasks = []
    for page in result.get("results", []):
        props = page.get("properties", {})
        
        task = {
            "id": page.get("id"),
            "title": props.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Untitled"),
            "status": props.get("Status", {}).get("select", {}).get("name", ""),
            "description": props.get("Description", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
            "tags": [t.get("name") for t in props.get("Tags", {}).get("multi_select", [])],
            "created_time": page.get("created_time"),
            "last_edited_time": page.get("last_edited_time")
        }
        tasks.append(task)
    
    return {"tasks": tasks, "total": len(tasks)}

# === TASK WORKFLOW (Task-Steward) ===
def classify_task(user_input: str) -> dict:
    """
    Phân loại task: Q&A hay Task?
    Task-Steward logic
    """
    qa_signals = ["?", "what is", "how do", "can you tell", "explain"]
    task_signals = ["please", "handle", "do this", "add to", "create", "make", "build"]
    
    user_lower = user_input.lower()
    
    # Check for Q&A signals
    for signal in qa_signals:
        if signal in user_lower:
            return {"type": "QA", "reason": f"Q&A signal: {signal}"}
    
    # Check for Task signals
    for signal in task_signals:
        if signal in user_lower:
            return {"type": "TASK", "reason": f"Task signal: {signal}"}
    
    # Default to Q&A (safer)
    return {"type": "QA", "reason": "Default classification"}

def start_working(task_id: str) -> dict:
    """Bắt đầu làm task - thêm working tag"""
    # Add cora-working tag
    result = add_task_tag(task_id, "cora-working")
    
    # Move to IN_PROGRESS
    update_task_state(task_id, "IN_PROGRESS")
    
    return result

def mark_blocked(task_id: str, reason: str) -> dict:
    """Đánh dấu task bị block"""
    # Add blocked tag
    result = add_task_tag(task_id, "blocked")
    
    # Move to WAITING
    update_task_state(task_id, "WAITING")
    
    # Add comment with reason (would need block API)
    return result

def complete_task(task_id: str) -> dict:
    """Hoàn thành task - chuyển sang REVIEW"""
    # Remove cora-working tag
    remove_task_tag(task_id, "cora-working")
    
    # Move to REVIEW
    result = update_task_state(task_id, "REVIEW")
    
    return result

def approve_task(task_id: str) -> dict:
    """QA approve - chuyển sang DONE"""
    # Add quality-verified tag
    result = add_task_tag(task_id, "quality-verified")
    
    # Move to DONE
    update_task_state(task_id, "DONE")
    
    return result

def reject_task(task_id: str, feedback: str) -> dict:
    """QA reject - chuyển về IN_PROGRESS với feedback"""
    # Add feedback as comment (simplified)
    # Remove quality-verified if exists
    remove_task_tag(task_id, "quality-verified")
    
    # Move back to IN_PROGRESS
    result = update_task_state(task_id, "IN_PROGRESS")
    
    return result

class TaskBoard:
    """Wrapper class"""
    
    def __init__(self):
        self.config = load_config()
    
    def setup(self, database_id: str):
        return create_task_board(database_id)
    
    def create(self, title: str, description: str = "", state: str = "IN_PROGRESS", tags: List[str] = None):
        return create_task(title, description, state, tags)
    
    def update_state(self, task_id: str, state: str):
        return update_task_state(task_id, state)
    
    def get(self, task_id: str):
        return get_task(task_id)
    
    def list(self, state: str = None):
        return get_tasks_by_state(state)
    
    def start(self, task_id: str):
        return start_working(task_id)
    
    def block(self, task_id: str, reason: str):
        return mark_blocked(task_id, reason)
    
    def complete(self, task_id: str):
        return complete_task(task_id)
    
    def approve(self, task_id: str):
        return approve_task(task_id)
    
    def reject(self, task_id: str, feedback: str):
        return reject_task(task_id, feedback)

if __name__ == "__main__":
    import sys
    
    tb = TaskBoard()
    
    if len(sys.argv) < 2:
        print("""Task Board Manager - Notion-based task management (Task-Steward style)

Commands:
  setup <database_id>              - Thiết lập Notion database
  create <title> [desc]           - Tạo task mới
  update <task_id> <state>         - Cập nhật state (NOW/WAITING/IN_PROGRESS/REVIEW/DONE)
  get <task_id>                   - Lấy task
  list [state]                     - Liệt kê tasks
  start <task_id>                 - Bắt đầu làm (add working tag)
  block <task_id> <reason>        - Đánh dấu blocked
  complete <task_id>              - Hoàn thành, chuyển sang REVIEW
  approve <task_id>               - QA approve, chuyển sang DONE
  reject <task_id> <feedback>     - QA reject, feedback

States:
  NOW, WAITING, IN_PROGRESS, REVIEW, DONE
""")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "setup" and len(sys.argv) >= 3:
        print(json.dumps(tb.setup(sys.argv[2]), indent=2))
    
    elif action == "create" and len(sys.argv) >= 3:
        title = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        print(json.dumps(tb.create(title, desc), indent=2))
    
    elif action == "update" and len(sys.argv) >= 4:
        print(json.dumps(tb.update_state(sys.argv[2], sys.argv[3]), indent=2))
    
    elif action == "get" and len(sys.argv) >= 3:
        print(json.dumps(tb.get(sys.argv[2]), indent=2))
    
    elif action == "list":
        state = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(tb.list(state), indent=2))
    
    elif action == "start" and len(sys.argv) >= 3:
        print(json.dumps(tb.start(sys.argv[2]), indent=2))
    
    elif action == "block" and len(sys.argv) >= 4:
        print(json.dumps(tb.block(sys.argv[2], sys.argv[3]), indent=2))
    
    elif action == "complete" and len(sys.argv) >= 3:
        print(json.dumps(tb.complete(sys.argv[2]), indent=2))
    
    elif action == "approve" and len(sys.argv) >= 3:
        print(json.dumps(tb.approve(sys.argv[2]), indent=2))
    
    elif action == "reject" and len(sys.argv) >= 4:
        print(json.dumps(tb.reject(sys.argv[2], sys.argv[3]), indent=2))
    
    else:
        print("Invalid command")
