"""
ClawHub Automation Skill - 零代码跨生态自动化
No-code cross-platform automation for ClawHub
"""

__version__ = "1.0.0"
__author__ = "ClawHub Platform"

from .workflow_engine import WorkflowEngine, Workflow, WorkflowNode
from .connector_manager import ConnectorManager, PlatformConnector
from .ai_flow_generator import AIFlowGenerator
from .template_center import TemplateCenter
from .execution_monitor import ExecutionMonitor
from .permission_manager import PermissionManager

__all__ = [
    'WorkflowEngine',
    'Workflow',
    'WorkflowNode',
    'ConnectorManager',
    'PlatformConnector',
    'AIFlowGenerator',
    'TemplateCenter',
    'ExecutionMonitor',
    'PermissionManager'
]