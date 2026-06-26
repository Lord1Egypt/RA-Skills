"""
Task data models for Volcengine API Skill.

This module contains models for representing tasks and their results.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from .base import TaskStatus, TaskType, BaseModelConfig


class TaskParams(BaseModelConfig):
    """
    Base class for task parameters.
    
    Specific task types should extend this class with their
    required parameters.
    """
    pass


class TaskResult(BaseModel):
    """
    Model for representing task execution results.
    
    Attributes:
        url: URL to the generated resource (if available)
        local_path: Local filesystem path to the resource (if downloaded)
        metadata: Additional metadata about the result
    """
    
    url: Optional[str] = None
    local_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskInfo(BaseModel):
    """
    Complete information about a task.
    
    Attributes:
        id: Unique task identifier
        type: Type of task
        status: Current status of the task
        params: Task parameters
        result: Task result (if completed)
        error: Error message (if failed)
        created_at: Task creation timestamp
        updated_at: Last update timestamp
    """
    
    id: str
    type: TaskType
    status: TaskStatus
    params: TaskParams
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
