"""
集成模块
包含ADK/Agent Runtime和女娲Agent的集成能力
支持接入多种AI平台和Agent服务
融入主流Agent框架特性: Google ADK/LangGraph/CrewAI/AutoGen/Smolagents/Phidata/Cognee/Mem0
核心: Agent化身控制器 - 让AI真正主导大模型调用
"""

from .adk_agent_runtime import ADKIntegration, AgentStateMachine, PersonalityDistiller, OrchestratorAgent
from .platform_adapters import PlatformManager, PlatformAdapter, OpenAIAdapter, ClaudeAdapter, GeminiAdapter, LocalAdapter
from .framework_enhancements import (
    CheckpointManager, Checkpoint, CheckpointState,
    StateGraph, WorkflowNode, WorkflowState,
    AgentRole, Task, CrewAgent, Crew,
    ConversableAgent, GroupChat, ConversationMessage,
    CodeAgent,
    KnowledgeGraph, KnowledgeNode,
    MemoryManager, MemoryEntry, MemoryType,
    FrameworkIntegration
)
from .avatar_controller import (
    AvatarController, AvatarManager,
    ContextManager, ContextSpace,
    ThinkingEngine, ThinkingStep,
    IntentParser, UserIntent, IntentType,
    ModelOrchestrator
)

__all__ = [
    "ADKIntegration", 
    "AgentStateMachine", 
    "PersonalityDistiller", 
    "OrchestratorAgent",
    "PlatformManager", 
    "PlatformAdapter", 
    "OpenAIAdapter", 
    "ClaudeAdapter", 
    "GeminiAdapter", 
    "LocalAdapter",
    "CheckpointManager",
    "Checkpoint",
    "CheckpointState",
    "StateGraph",
    "WorkflowNode",
    "WorkflowState",
    "AgentRole",
    "Task",
    "CrewAgent",
    "Crew",
    "ConversableAgent",
    "GroupChat",
    "ConversationMessage",
    "CodeAgent",
    "KnowledgeGraph",
    "KnowledgeNode",
    "MemoryManager",
    "MemoryEntry",
    "MemoryType",
    "FrameworkIntegration",
    "AvatarController",
    "AvatarManager",
    "ContextManager",
    "ContextSpace",
    "ThinkingEngine",
    "ThinkingStep",
    "IntentParser",
    "UserIntent",
    "IntentType",
    "ModelOrchestrator"
]
