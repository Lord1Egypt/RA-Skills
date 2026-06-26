"""
ClawMobile Python Client for OpenClaw Skill
Handles HTTP communication with AutoX.js server
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskResult:
    """Result of task execution"""
    task_id: str
    status: str
    steps_result: List[Dict[str, Any]]
    total_duration_ms: int
    error: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class ServerStatus:
    """AutoX.js server status"""
    running: bool
    current_task: Optional[Dict[str, Any]]
    uptime: int
    kernel_type: str
    memory_usage: str
    cpu_usage: str
    version: str = "6.5.5.10"


class AutoXClient:
    """AutoX.js HTTP Client"""

    def __init__(self, host: str = "localhost", port: int = 8765, token: str = None):
        self.base_url = f"http://{host}:{port}"
        self.token = token or "clawmobile-secret-token-change-in-production"
        self.timeout = 300  # 5 minutes default

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        Execute a task on AutoX.js

        Args:
            task: Task definition

        Returns:
            TaskResult
        """
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json=task,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()

            if data.get("success"):
                result = data["result"]
                return TaskResult(
                    task_id=result["task_id"],
                    status=result["status"],
                    steps_result=result.get("steps_result", []),
                    total_duration_ms=result.get("total_duration_ms", 0),
                    completed_at=result.get("completed_at")
                )
            else:
                return TaskResult(
                    task_id=task["id"],
                    status="error",
                    steps_result=[],
                    total_duration_ms=0,
                    error=data.get("error", "Unknown error")
                )

        except requests.exceptions.Timeout:
            return TaskResult(
                task_id=task["id"],
                status="timeout",
                steps_result=[],
                total_duration_ms=self.timeout * 1000,
                error="Request timeout"
            )
        except requests.exceptions.RequestException as e:
            return TaskResult(
                task_id=task["id"],
                status="error",
                steps_result=[],
                total_duration_ms=0,
                error=str(e)
            )

    def check_status(self) -> Optional[ServerStatus]:
        """Check AutoX.js server status"""
        try:
            response = requests.post(
                f"{self.base_url}/check_status",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return ServerStatus(
                running=data.get("running", False),
                current_task=data.get("current_task"),
                uptime=data.get("uptime", 0),
                kernel_type=data.get("kernel_type"),
                memory_usage=data.get("memory_usage", "0MB"),
                cpu_usage=data.get("cpu_usage", "0%"),
                version=data.get("version", "6.5.5.10")
            )

        except requests.exceptions.RequestException:
            return None

    def stop_task(self) -> bool:
        """Stop current task"""
        try:
            response = requests.post(
                f"{self.base_url}/stop",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return data.get("success", False)

        except requests.exceptions.RequestException:
            return False

    def get_server_status(self) -> Optional[Dict[str, Any]]:
        """Get detailed server status"""
        try:
            response = requests.get(
                f"{self.base_url}/status",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException:
            return None


class WorkspaceFileManager:
    """Manage workspace file operations"""

    def __init__(self, workspace_path: str = "/sdcard/autox-workspace/ClawMobile"):
        self.workspace_path = workspace_path
        self.tasks_dir = f"{workspace_path}/tasks"
        self.results_dir = f"{workspace_path}/results"
        self.scripts_dir = f"{workspace_path}/scripts"
        self.workflows_dir = f"{workspace_path}/workflows"
        self.logs_dir = f"{workspace_path}/logs"

    def write_task(self, task: Dict[str, Any]) -> str:
        """
        Write task to file system

        Args:
            task: Task definition

        Returns:
            Task file path
        """
        import os
        import uuid

        # Ensure directories exist
        os.makedirs(self.tasks_dir, exist_ok=True)

        # Generate task ID if not provided
        if "id" not in task:
            task["id"] = f"task_{uuid.uuid4().hex[:6]}"

        # Write task file
        task_file = f"{self.tasks_dir}/{task['id']}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)

        return task_file

    def read_result(self, task_id: str, timeout: int = 300) -> Optional[Dict[str, Any]]:
        """
        Wait for and read task result

        Args:
            task_id: Task ID
            timeout: Timeout in seconds

        Returns:
            Task result or None
        """
        import os
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            # Look for result files
            if os.path.exists(self.results_dir):
                result_files = [
                    f for f in os.listdir(self.results_dir)
                    if f.startswith(f"result_{task_id}_")
                ]

                if result_files:
                    # Read most recent result
                    result_file = os.path.join(self.results_dir, sorted(result_files)[-1])
                    with open(result_file, 'r') as f:
                        return json.load(f)

            time.sleep(0.5)

        return None

    def get_task_status(self, task_id: str) -> Optional[str]:
        """
        Get current task status

        Args:
            task_id: Task ID

        Returns:
            Task status or None
        """
        import os

        task_file = f"{self.tasks_dir}/{task_id}.json"
        processing_file = f"{self.tasks_dir}/{task_id}.json.processing"

        if os.path.exists(processing_file):
            return "processing"

        if os.path.exists(task_file):
            return "pending"

        return None


# Convenience functions for OpenClaw Skill
def execute_workflow(task: Dict[str, Any], wait_for_result: bool = True) -> Optional[TaskResult]:
    """
    Execute a workflow task

    Args:
        task: Task definition
        wait_for_result: Whether to wait for completion

    Returns:
        TaskResult or None
    """
    client = AutoXClient()
    file_manager = WorkspaceFileManager()

    # Write task to workspace
    task_file = file_manager.write_task(task)
    print(f"✅ Task written to: {task_file}")

    if wait_for_result:
        # Wait for result
        result = file_manager.read_result(task["id"])
        return result

    return None


def create_click_task(x: int, y: int, description: str = "Click action") -> Dict[str, Any]:
    """Create a simple click task"""
    return {
        "id": f"task_{int(time.time())}",
        "type": "sequence",
        "kernel_type": "coordinate",
        "priority": "normal",
        "timeout": 30000,
        "anti_detection": {
            "random_offset": True,
            "random_delay": True
        },
        "steps": [
            {
                "step_id": "step_001",
                "action": "click",
                "kernel_type": "coordinate",
                "coordinate": {"x": x, "y": y},
                "description": description
            }
        ],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "source": "openclaw"
        }
    }


def create_input_task(x: int, y: int, text: str, description: str = "Input text") -> Dict[str, Any]:
    """Create an input task"""
    return {
        "id": f"task_{int(time.time())}",
        "type": "sequence",
        "kernel_type": "accessibility",
        "priority": "normal",
        "timeout": 30000,
        "anti_detection": {
            "random_offset": True,
            "random_delay": True
        },
        "steps": [
            {
                "step_id": "step_001",
                "action": "click",
                "kernel_type": "accessibility",
                "selector": {"id": f"auto_input_{int(time.time())}"},
                "coordinate": {"x": x, "y": y},
                "description": "Focus input field"
            },
            {
                "step_id": "step_002",
                "action": "input",
                "kernel_type": "accessibility",
                "selector": {"id": f"auto_input_{int(time.time())}"},
                "value": text,
                "options": {
                    "clear": True,
                    "delay": 100
                },
                "description": description
            }
        ],
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "source": "openclaw"
        }
    }
