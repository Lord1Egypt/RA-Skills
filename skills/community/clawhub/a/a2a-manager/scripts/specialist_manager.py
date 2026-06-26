#!/usr/bin/env python3
"""Specialist Manager - Quản lý Specialist/Sub-agents theo Task-Steward"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

# === CONFIG ===
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
SPECIALISTS_DIR = WORKSPACE_ROOT / "specialists"

# === SPECIALIST TYPES ===
SPECIALIST_TYPES = {
    "temp_worker": {
        "description": "Task đơn giản, ngắn gọn",
        "default_model": "flash",
        "auto_dispose": True,
        "lifetime": "1h"
    },
    "researcher": {
        "description": "Nghiên cứu sâu, tìm hiểu",
        "default_model": "pro",
        "auto_dispose": True,
        "lifetime": "4h"
    },
    "coder": {
        "description": "Viết code, debug",
        "default_model": "glm4",
        "auto_dispose": True,
        "lifetime": "2h"
    },
    "qa_reviewer": {
        "description": "Review chất lượng",
        "default_model": "flash",
        "auto_dispose": True,
        "lifetime": "1h"
    },
    "runner": {
        "description": "Chạy lệnh, script",
        "default_model": "flash",
        "auto_dispose": True,
        "lifetime": "30m"
    }
}

# === SPECIALIST TEMPLATE ===
def create_specialist(
    specialist_type: str,
    task: str,
    parent_agent: str = None,
    skills: List[str] = None,
    custom_model: str = None
) -> Dict[str, Any]:
    """
    Tạo một Specialist (sub-agent) tạm thời
    """
    if specialist_type not in SPECIALIST_TYPES:
        raise ValueError(f"Invalid specialist type: {specialist_type}. Valid: {list(SPECIALIST_TYPES.keys())}")
    
    config = SPECIALIST_TYPES[specialist_type]
    
    specialist_id = f"spec_{uuid.uuid4().hex[:8]}"
    
    specialist = {
        "id": specialist_id,
        "type": specialist_type,
        "subtype": "Specialist",
        "task": task,
        "parent_agent": parent_agent,
        "model": custom_model or config["default_model"],
        "skills": skills or [],
        "status": "spawning",
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=int(config["lifetime"].replace("h", "").replace("m", "") or 1))).isoformat(),
        "lifetime": config["lifetime"],
        "auto_dispose": config["auto_dispose"],
        "context": []
    }
    
    # Save to file
    SPECIALISTS_DIR.mkdir(parents=True, exist_ok=True)
    spec_file = SPECIALISTS_DIR / f"{specialist_id}.json"
    
    with open(spec_file, "w") as f:
        json.dump(specialist, f, indent=2)
    
    # Update active list
    _update_active_list(specialist_id, "add")
    
    return specialist

def dispose_specialist(specialist_id: str, reason: str = "completed") -> Dict[str, Any]:
    """
    Dispose một Specialist - xóa sau khi task hoàn thành
    """
    spec_file = SPECIALISTS_DIR / f"{specialist_id}.json"
    
    if not spec_file.exists():
        return {"success": False, "error": "Specialist not found"}
    
    with open(spec_file) as f:
        specialist = json.load(f)
    
    # Mark as disposed
    specialist["status"] = "disposed"
    specialist["disposed_at"] = datetime.now().isoformat()
    specialist["dispose_reason"] = reason
    
    # Save disposal record
    with open(spec_file, "w") as f:
        json.dump(specialist, f, indent=2)
    
    # Remove from active list
    _update_active_list(specialist_id, "remove")
    
    return {
        "success": True,
        "specialist_id": specialist_id,
        "reason": reason
    }

def get_specialist(specialist_id: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin Specialist"""
    spec_file = SPECIALISTS_DIR / f"{specialist_id}.json"
    
    if not spec_file.exists():
        return None
    
    with open(spec_file) as f:
        return json.load(f)

def list_active_specialists() -> List[Dict[str, Any]]:
    """Liệt kê các Specialist đang hoạt động"""
    active_file = SPECIALISTS_DIR / "active.json"
    
    if not active_file.exists():
        return []
    
    with open(active_file) as f:
        active_ids = json.load(f)
    
    specialists = []
    for spec_id in active_ids:
        spec = get_specialist(spec_id)
        if spec and spec.get("status") != "disposed":
            specialists.append(spec)
    
    return specialists

def add_context(specialist_id: str, message: str, sender: str = "system"):
    """Thêm context cho Specialist"""
    spec = get_specialist(specialist_id)
    
    if not spec:
        return None
    
    spec["context"].append({
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "message": message
    })
    
    spec_file = SPECIALISTS_DIR / f"{specialist_id}.json"
    with open(spec_file, "w") as f:
        json.dump(spec, f, indent=2)
    
    return spec

def cleanup_expired():
    """Dọn dẹp các Specialist hết hạn"""
    active = list_active_specialists()
    cleaned = []
    
    now = datetime.now()
    
    for spec in active:
        expires = datetime.fromisoformat(spec["expires_at"])
        if now > expires:
            dispose_specialist(spec["id"], "expired")
            cleaned.append(spec["id"])
    
    return cleaned

# === HELPER ===
def _update_active_list(specialist_id: str, action: str):
    """Cập nhật danh sách active specialists"""
    active_file = SPECIALISTS_DIR / "active.json"
    
    if not active_file.exists():
        active_ids = []
    else:
        with open(active_file) as f:
            active_ids = json.load(f)
    
    if action == "add":
        if specialist_id not in active_ids:
            active_ids.append(specialist_id)
    elif action == "remove":
        if specialist_id in active_ids:
            active_ids.remove(specialist_id)
    
    with open(active_file, "w") as f:
        json.dump(active_ids, f, indent=2)

class SpecialistManager:
    """Wrapper class cho Specialist management"""
    
    def spawn(self, specialist_type: str, task: str, parent: str = None, skills: List[str] = None, model: str = None):
        return create_specialist(specialist_type, task, parent, skills, model)
    
    def dispose(self, specialist_id: str, reason: str = "completed"):
        return dispose_specialist(specialist_id, reason)
    
    def get(self, specialist_id: str):
        return get_specialist(specialist_id)
    
    def list_active(self):
        return list_active_specialists()
    
    def add_context(self, specialist_id: str, message: str, sender: str = "system"):
        return add_context(specialist_id, message, sender)
    
    def cleanup(self):
        return cleanup_expired()

if __name__ == "__main__":
    import sys
    
    sm = SpecialistManager()
    
    if len(sys.argv) < 2:
        print("""Specialist Manager - Sub-agent management theo Task-Steward

Commands:
  spawn <type> <task> [parent]    - Tạo specialist tạm thời
  dispose <id> [reason]            - Xóa specialist
  get <id>                        - Lấy thông tin
  list                             - Liệt kê active specialists
  cleanup                          - Dọn dẹp expired specialists

Types:
  temp_worker  - Task đơn giản
  researcher   - Nghiên cứu
  coder       - Viết code
  qa_reviewer - Review chất lượng
  runner      - Chạy lệnh
""")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "spawn" and len(sys.argv) >= 4:
        specialist_type = sys.argv[2]
        task = sys.argv[3]
        parent = sys.argv[4] if len(sys.argv) > 4 else None
        result = sm.spawn(specialist_type, task, parent)
        print(json.dumps(result, indent=2))
    
    elif action == "dispose" and len(sys.argv) >= 3:
        specialist_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "completed"
        print(json.dumps(sm.dispose(specialist_id, reason), indent=2))
    
    elif action == "get" and len(sys.argv) >= 3:
        print(json.dumps(sm.get(sys.argv[2]), indent=2))
    
    elif action == "list":
        print(json.dumps(sm.list_active(), indent=2))
    
    elif action == "cleanup":
        cleaned = sm.cleanup()
        print(json.dumps({"cleaned": cleaned}, indent=2))
    
    else:
        print("Invalid command")
