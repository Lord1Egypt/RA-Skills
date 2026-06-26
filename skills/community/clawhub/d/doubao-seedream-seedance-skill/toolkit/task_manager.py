"""
Task manager for Volcengine API Skill.

Manages task lifecycle: create, update, query, delete.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import uuid
from toolkit.models.base import TaskStatus, TaskType
from toolkit.models.task import TaskParams, TaskResult, TaskInfo
from toolkit.models.validation import ValidationResult
from toolkit.state_manager import StateManager
from toolkit.api_client import VolcengineAPIClient
from toolkit.validator import Validator
from toolkit.error_handler import TaskError


class TaskManager:
    """
    Manages task lifecycle and state.
    
    Features:
    - Create tasks
    - Update task status
    - Query task state
    - Poll for completion
    - Download results
    """
    
    def __init__(
        self,
        api_client: VolcengineAPIClient,
        state_manager: Optional[StateManager] = None
    ):
        """
        Initialize task manager.
        
        Args:
            api_client: API client for requests
            state_manager: State manager for persistence
        """
        self.api_client = api_client
        self.state_manager = state_manager or StateManager()
    
    def create_task(
        self,
        task_type: TaskType,
        params: Union[Dict[str, Any], TaskParams]  # Accept dict or TaskParams
    ) -> TaskInfo:
        """
        Create new task.
        
        Args:
            task_type: Type of task
            params: Task parameters
            
        Returns:
            TaskInfo with created task details
            
        Raises:
            InvalidInputError: If parameters invalid
        """
        # Validate parameters
        validation_result = self._validate_params(task_type, params)
        if not validation_result.is_valid:
            raise TaskError(
                message=f"Invalid parameters: {', '.join(validation_result.errors)}",
                context={"errors": validation_result.errors}
            )
        
        # Create task info
        task_id = str(uuid.uuid4())
        now = datetime.now()
        
        task_info = TaskInfo(
            id=task_id,
            type=task_type,
            status=TaskStatus.QUEUED,
            params=params,
            created_at=now,
            updated_at=now
        )
        
        # Save state
        self.state_manager.save_task_state(task_id, task_info.model_dump())
        
        # Record operation
        self.state_manager.add_history_entry(
            f"create_{task_type.value}",
            {"task_id": task_id}
        )
        
        return task_info
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[TaskResult] = None,
        error: Optional[str] = None
    ) -> TaskInfo:
        """
        Update task status.
        
        Args:
            task_id: Task identifier
            status: New status
            result: Task result (if completed)
            error: Error message (if failed)
            
        Returns:
            Updated TaskInfo
            
        Raises:
            TaskError: If task not found
        """
        task_data = self.state_manager.get_task_state(task_id)
        if not task_data:
            raise TaskError(
                message=f"Task not found: {task_id}",
                task_id=task_id
            )
        
        # Update fields
        task_data["status"] = status.value
        task_data["updated_at"] = datetime.now().isoformat()
        
        if result:
            task_data["result"] = result.model_dump()
        
        if error:
            task_data["error"] = error
        
        # Save state
        self.state_manager.save_task_state(task_id, task_data)
        
        return TaskInfo(**task_data)
    
    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """
        Get task by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            TaskInfo or None if not found
        """
        task_data = self.state_manager.get_task_state(task_id)
        if task_data:
            return TaskInfo(**task_data)
        return None
    
    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        task_type: Optional[TaskType] = None,
        limit: int = 100
    ) -> List[TaskInfo]:
        """
        List tasks with optional filters.
        
        Args:
            status: Filter by status
            task_type: Filter by type
            limit: Maximum tasks to return
            
        Returns:
            List of TaskInfo
        """
        all_tasks = self.state_manager.get_all_tasks()
        
        tasks = []
        for task_data in all_tasks.values():
            task = TaskInfo(**task_data)
            
            # Apply filters
            if status and task.status != status:
                continue
            if task_type and task.type != task_type:
                continue
            
            tasks.append(task)
            
            if len(tasks) >= limit:
                break
        
        return tasks
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if deleted, False if not found
        """
        result = self.state_manager.delete_task_state(task_id)
        
        if result:
            self.state_manager.add_history_entry(
                "delete_task",
                {"task_id": task_id}
            )
        
        return result
    
    def _validate_params(self, task_type: TaskType, params: Union[Dict[str, Any], TaskParams]) -> Any:
        """Validate task parameters."""
        # Convert params to dict for validation
        if hasattr(params, 'model_dump'):
            params_dict = params.model_dump()
        else:
            params_dict = params  # Already a dict
        if task_type in [TaskType.IMAGE_GENERATION, TaskType.IMAGE_EDIT]:
            return Validator.validate_image_generation_params(**params_dict)
        elif task_type in [TaskType.VIDEO_T2V, TaskType.VIDEO_I2V]:
            return Validator.validate_video_generation_params(**params_dict)
        else:
            result = ValidationResult()
            Validator.validate_required(params_dict.get("prompt"), "prompt", result)
            return result
