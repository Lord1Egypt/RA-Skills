"""
Task Executor Module
High-level task execution interface
"""

import time
import json
from typing import Dict, Any, Optional
from .client import AutoXClient, WorkspaceFileManager, TaskResult


class TaskExecutor:
    """High-level task execution interface"""

    def __init__(self, autox_host: str = "localhost", autox_port: int = 8765):
        self.client = AutoXClient(host=autox_host, port=autox_port)
        self.file_manager = WorkspaceFileManager()

    def execute_click(self, x: int, y: int, description: str = "Click action") -> Optional[TaskResult]:
        """
        Execute a simple click action

        Args:
            x: X coordinate
            y: Y coordinate
            description: Action description

        Returns:
            TaskResult or None
        """
        from .client import create_click_task

        task = create_click_task(x, y, description)
        return self.execute_task(task)

    def execute_input(self, x: int, y: int, text: str, description: str = "Input text") -> Optional[TaskResult]:
        """
        Execute a text input action

        Args:
            x: X coordinate
            y: Y coordinate
            text: Text to input
            description: Action description

        Returns:
            TaskResult or None
        """
        from .client import create_input_task

        task = create_input_task(x, y, text, description)
        return self.execute_task(task)

    def execute_swipe(self, start_x: int, start_y: int, end_x: int, end_y: int,
                     duration: int = 300, description: str = "Swipe action") -> Optional[TaskResult]:
        """
        Execute a swipe action

        Args:
            start_x: Start X coordinate
            start_y: Start Y coordinate
            end_x: End X coordinate
            end_y: End Y coordinate
            duration: Swipe duration in ms
            description: Action description

        Returns:
            TaskResult or None
        """
        task = {
            "id": f"task_{int(time.time())}",
            "type": "sequence",
            "kernel_type": "coordinate",
            "priority": "normal",
            "timeout": 30000,
            "anti_detection": {
                "random_speed": True
            },
            "steps": [
                {
                    "step_id": "step_001",
                    "action": "swipe",
                    "kernel_type": "coordinate",
                    "start": [start_x, start_y],
                    "end": [end_x, end_y],
                    "duration": duration,
                    "description": description
                }
            ],
            "metadata": {
                "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                "source": "openclaw"
            }
        }

        return self.execute_task(task)

    def execute_task(self, task: Dict[str, Any], wait_for_completion: bool = True) -> Optional[TaskResult]:
        """
        Execute a custom task

        Args:
            task: Task definition
            wait_for_completion: Whether to wait for task completion

        Returns:
            TaskResult or None
        """
        # Check server status first
        status = self.client.check_status()
        if not status or not status.running:
            raise Exception("AutoX.js server is not running")

        # Write task to workspace
        task_file = self.file_manager.write_task(task)
        print(f"📝 Task written to: {task_file}")

        if wait_for_completion:
            # Wait for result
            result = self.file_manager.read_result(task["id"])
            if result:
                print(f"✅ Task completed: {result.status}")
                return result
            else:
                print(f"⏰ Task timeout")
                return None

        return None

    def stop_current_task(self) -> bool:
        """
        Stop the currently running task

        Returns:
            True if successful, False otherwise
        """
        return self.client.stop_task()

    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current executor status

        Returns:
            Server status or None
        """
        status = self.client.check_status()
        if status:
            return {
                "server_running": status.running,
                "current_task": status.current_task,
                "uptime": status.uptime,
                "kernel_type": status.kernel_type,
                "memory_usage": status.memory_usage,
                "cpu_usage": status.cpu_usage
            }
        return None

    def wait_for_idle(self, timeout: int = 60) -> bool:
        """
        Wait for server to be idle (no task running)

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            True if server is idle, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.client.check_status()
            if status and not status.current_task:
                return True
            time.sleep(1)

        return False


class SimpleExecutor:
    """Simplified executor for basic operations"""

    @staticmethod
    def click(x: int, y: int) -> bool:
        """
        Execute a simple click

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if successful
        """
        try:
            executor = TaskExecutor()
            result = executor.execute_click(x, y)
            return result and result.status == "completed"
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False

    @staticmethod
    def input_text(x: int, y: int, text: str) -> bool:
        """
        Execute text input

        Args:
            x: X coordinate
            y: Y coordinate
            text: Text to input

        Returns:
            True if successful
        """
        try:
            executor = TaskExecutor()
            result = executor.execute_input(x, y, text)
            return result and result.status == "completed"
        except Exception as e:
            print(f"❌ Input failed: {e}")
            return False

    @staticmethod
    def swipe(start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """
        Execute a swipe

        Args:
            start_x: Start X coordinate
            start_y: Start Y coordinate
            end_x: End X coordinate
            end_y: End Y coordinate

        Returns:
            True if successful
        """
        try:
            executor = TaskExecutor()
            result = executor.execute_swipe(start_x, start_y, end_x, end_y)
            return result and result.status == "completed"
        except Exception as e:
            print(f"❌ Swipe failed: {e}")
            return False
