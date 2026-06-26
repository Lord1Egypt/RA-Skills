"""
测试执行模块相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class ExecutorCreate(BaseModel):
    """创建执行器请求"""
    name: str = Field(..., description="执行器名称")
    type: str = Field(..., description="执行器类型：api/ui")
    capacity: int = Field(default=5, description="并发容量")
    max_tasks: int = Field(default=100, description="最大任务数")
    config: Optional[Dict] = Field(default={}, description="执行器配置")


class ExecutorResponse(BaseModel):
    """执行器响应"""
    id: int
    name: str
    type: str
    status: str
    capacity: int
    current_load: int
    max_tasks: int
    completed_tasks: int
    last_heartbeat: Optional[str]
    create_time: str

    class Config:
        from_attributes = True


class TaskScheduleRequest(BaseModel):
    """任务调度请求"""
    script_id: int = Field(..., description="脚本ID")
    script_type: str = Field(..., description="脚本类型：api/ui")
    priority: int = Field(default=5, description="优先级（1-10）")
    scheduled_time: Optional[datetime] = Field(None, description="计划执行时间")
    max_retries: int = Field(default=2, description="最大重试次数")
    config: Optional[Dict] = Field(default={}, description="执行配置")


class TaskCancelRequest(BaseModel):
    """取消任务请求"""
    task_id: str = Field(..., description="任务ID")


class ExecutionQueueResponse(BaseModel):
    """执行队列响应"""
    id: int
    task_id: str
    script_id: int
    script_type: str
    priority: int
    status: str
    executor_id: Optional[int]
    retry_count: int
    scheduled_time: Optional[str]
    started_time: Optional[str]
    completed_time: Optional[str]
    create_time: str

    class Config:
        from_attributes = True


class ExecutionStats(BaseModel):
    """执行统计响应"""
    total_executors: int
    active_executors: int
    idle_executors: int
    busy_executors: int
    offline_executors: int
    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
