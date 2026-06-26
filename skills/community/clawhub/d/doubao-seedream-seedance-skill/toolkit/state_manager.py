"""
State management for Volcengine API Skill.

Manages task state, user preferences, and operation history.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class StateManager:
    """
    Manages persistent state for the Volcengine API Skill.
    
    Handles:
    - Task state persistence
    - User preferences
    - Operation history
    """
    
    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or Path.home() / ".volcengine"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.state_file = self.state_dir / "state.json"
        self.tasks_file = self.state_dir / "tasks.json"
        self.history_file = self.state_dir / "history.json"
        
        self._state: Dict[str, Any] = self._load_json(self.state_file, {})
        self._tasks: Dict[str, Any] = self._load_json(self.tasks_file, {})
        self._history: List[Dict[str, Any]] = self._load_json(self.history_file, [])
    
    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Load JSON from file or return default."""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return default
        return default
    
    def _save_json(self, file_path: Path, data: Any) -> None:
        """Save data to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # User Preferences
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference."""
        return self._state.get("preferences", {}).get(key, default)
    
    def set_preference(self, key: str, value: Any) -> None:
        """Set user preference."""
        if "preferences" not in self._state:
            self._state["preferences"] = {}
        self._state["preferences"][key] = value
        self._save_json(self.state_file, self._state)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all user preferences."""
        return self._state.get("preferences", {}).copy()
    
    # Task State Management
    
    def save_task_state(self, task_id: str, task_data: Dict[str, Any]) -> None:
        """Save task state."""
        task_data["updated_at"] = datetime.now().isoformat()
        self._tasks[task_id] = task_data
        self._save_json(self.tasks_file, self._tasks)
    
    def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task state by ID."""
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Any]:
        """Get all task states."""
        return self._tasks.copy()
    
    def delete_task_state(self, task_id: str) -> bool:
        """Delete task state."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save_json(self.tasks_file, self._tasks)
            return True
        return False
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get all tasks with a specific status."""
        return [
            task for task in self._tasks.values()
            if task.get("status") == status
        ]
    
    # Operation History
    
    def add_history_entry(self, operation: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Add entry to operation history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details or {}
        }
        self._history.append(entry)
        self._save_json(self.history_file, self._history)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get operation history."""
        if limit:
            return self._history[-limit:]
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear operation history."""
        self._history = []
        self._save_json(self.history_file, self._history)
    
    # Statistics
    
    def get_operation_count(self, operation: str) -> int:
        """Get count of specific operation."""
        return sum(
            1 for entry in self._history
            if entry.get("operation") == operation
        )
    
    def get_total_operations(self) -> int:
        """Get total operation count."""
        return len(self._history)
