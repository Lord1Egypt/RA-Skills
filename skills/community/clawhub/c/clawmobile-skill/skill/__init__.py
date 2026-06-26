"""
ClawMobile OpenClaw Skill
Main skill module for ClawMobile automation framework
"""

from .client import (
    AutoXClient,
    WorkspaceFileManager,
    execute_workflow,
    create_click_task,
    create_input_task,
    TaskResult,
    ServerStatus
)

from .executor import TaskExecutor
# from .generator import ScriptGenerator  # Not implemented yet
# from .analyzer import RecordingAnalyzer  # Not implemented yet

__version__ = "1.0.0"
__all__ = [
    "AutoXClient",
    "WorkspaceFileManager",
    "execute_workflow",
    "create_click_task",
    "create_input_task",
    "TaskResult",
    "ServerStatus",
    "TaskExecutor",
    # "ScriptGenerator",  # Not implemented yet
    # "RecordingAnalyzer"  # Not implemented yet
]
