"""Symphony Architecture Integration for Dev-Factory

This module provides Symphony-style orchestration patterns for the dev-factory skill,
enabling long-running daemon mode, parallel build processing, and GLM-5 integration.

Architecture:
    Symphony Orchestrator (NEW)
        → delegates to →
    Existing Dev-Factory Core (PRESERVED)

Components:
    - State Machine: Task lifecycle management
    - Notion Tracker: Adapter for Notion as Symphony tracker
    - Workspace Manager: Isolated per-build workspaces
    - Concurrency Manager: Parallel build limits
    - Orchestrator: Main daemon loop
    - GLM-5 Agent: HTTP API to agent protocol adapter
    - Health Check: HTTP server for monitoring
"""

from .state_machine import TaskState, TerminalReason, SymphonyStateMachine, SymphonyTask
from .notion_tracker import NotionTrackerAdapter
from .workspace import WorkspaceManager, WorkspaceHook, WorkspaceConfig
from .concurrency import ConcurrencyManager, ConcurrencyLimits
from .orchestrator import SymphonyOrchestrator
from .glm5_agent import GLM5AgentAdapter, AgentResult
from .health import HealthCheckServer, SimpleHealthChecker

__all__ = [
    'TaskState',
    'TerminalReason',
    'SymphonyStateMachine',
    'SymphonyTask',
    'NotionTrackerAdapter',
    'WorkspaceManager',
    'WorkspaceHook',
    'WorkspaceConfig',
    'ConcurrencyManager',
    'ConcurrencyLimits',
    'SymphonyOrchestrator',
    'GLM5AgentAdapter',
    'AgentResult',
    'HealthCheckServer',
    'SimpleHealthChecker',
]
