#!/usr/bin/env python3
"""scheduler_integration.py - Connect scheduler API v0.5.0"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

class SchedulerClient:
    """Client for agent-zero scheduler."""

    def __init__(self, project_path="/a0/usr/projects/frugal_orchestrator"):
        self.project = Path(project_path)
        self.scheduled_dir = self.project / "scheduled_tasks"
        self.scheduled_dir.mkdir(exist_ok=True)

    def create_scheduled_task(self, name, system_prompt, user_prompt, schedule_meta, attachments=None):
        task_id = hashlib.sha256(name.encode()).hexdigest()[:16]
        task_def = {
            "task_id": task_id, "name": name,
            "system_prompt": system_prompt, "user_prompt": user_prompt,
            "schedule": schedule_meta, "attachments": attachments or [],
            "enabled": True, "created": datetime.now().isoformat()
        }
        task_file = self.scheduled_dir / f"{task_id}.json"
        with open(task_file, "w") as f:
            json.dump(task_def, f, indent=2)
        return {"status": "created", "task_id": task_id, "file": str(task_file)}

    def list_tasks(self, enabled_only=False):
        tasks = []
        for task_file in self.scheduled_dir.glob("*.json"):
            with open(task_file) as f:
                task = json.load(f)
                if not enabled_only or task.get("enabled", True):
                    tasks.append(task)
        return tasks

    def disable_task(self, task_id):
        task_file = self.scheduled_dir / f"{task_id}.json"
        if task_file.exists():
            with open(task_file) as f:
                task = json.load(f)
            task["enabled"] = False
            with open(task_file, "w") as f:
                json.dump(task, f, indent=2)
            return {"status": "disabled", "task_id": task_id}
        return {"error": "Task not found", "task_id": task_id}

    def delete_task(self, task_id):
        task_file = self.scheduled_dir / f"{task_id}.json"
        if task_file.exists():
            task_file.unlink()
            return {"status": "deleted", "task_id": task_id}
        return {"error": "Task not found", "task_id": task_id}

def crontab_to_json(crontab):
    parts = crontab.split()
    if len(parts) != 5:
        return None
    return {
        "minute": parts[0], "hour": parts[1], "day": parts[2],
        "month": parts[3], "weekday": parts[4]
    }

if __name__ == "__main__":
    sc = SchedulerClient()
    result = sc.create_scheduled_task(
        name="Daily Report",
        system_prompt="You are a reporting agent",
        user_prompt="Generate daily metrics report",
        schedule_meta=crontab_to_json("0 9 * * *") or {}
    )
    print(f"Created: {result.get('task_id', 'N/A')}")
    print(f"Tasks: {len(sc.list_tasks())}")
