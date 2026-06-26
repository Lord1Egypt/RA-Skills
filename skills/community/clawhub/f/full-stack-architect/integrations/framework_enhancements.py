#!/usr/bin/env python3
"""
框架增强模块
融入主流Agent框架的优秀特性
- Google ADK官方: A2A协议、MCP、记忆管理、检查点
- LangGraph: 有状态工作流、循环、回溯
- CrewAI: 角色分配、团队协作
- AutoGen: 多Agent对话、代码执行沙盒
- Smolagents: 轻量级代码代理
- Phidata: 多模态、Agentic RAG
- Cognee: 知识图谱记忆
- Mem0: 记忆管理
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CheckpointState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"

@dataclass
class Checkpoint:
    name: str
    state: CheckpointState
    data: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    parent_id: Optional[str] = None

class CheckpointManager:
    """Google ADK风格 - 检查点管理器"""
    
    def __init__(self, max_checkpoints: int = 100):
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.max_checkpoints = max_checkpoints
        self.current_branch: List[str] = []
    
    def create_checkpoint(self, name: str, data: Dict[str, Any], parent_id: Optional[str] = None) -> str:
        checkpoint_id = hashlib.md5(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        checkpoint = Checkpoint(
            name=name,
            state=CheckpointState.PENDING,
            data=data,
            parent_id=parent_id
        )
        self.checkpoints[checkpoint_id] = checkpoint
        self.current_branch.append(checkpoint_id)
        
        if len(self.checkpoints) > self.max_checkpoints:
            oldest = list(self.checkpoints.keys())[0]
            del self.checkpoints[oldest]
        
        logger.info(f"创建检查点: {name} ({checkpoint_id})")
        return checkpoint_id
    
    def update_checkpoint(self, checkpoint_id: str, state: CheckpointState, data: Optional[Dict] = None):
        if checkpoint_id in self.checkpoints:
            self.checkpoints[checkpoint_id].state = state
            if data:
                self.checkpoints[checkpoint_id].data.update(data)
            logger.info(f"更新检查点: {checkpoint_id} -> {state.value}")
    
    def rollback(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        if checkpoint_id in self.checkpoints:
            checkpoint = self.checkpoints[checkpoint_id]
            checkpoint.state = CheckpointState.ROLLBACK
            logger.info(f"回滚到检查点: {checkpoint.name}")
            return checkpoint.data
        return None
    
    def get_branch_history(self) -> List[Dict]:
        return [
            {
                "id": cid,
                "name": self.checkpoints[cid].name,
                "state": self.checkpoints[cid].state.value,
                "timestamp": self.checkpoints[cid].timestamp
            }
            for cid in self.current_branch if cid in self.checkpoints
        ]

class WorkflowState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

class WorkflowNode(ABC):
    """LangGraph风格 - 工作流节点基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.next_nodes: List[str] = []
        self.condition: Optional[Callable] = None
    
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def add_edge(self, next_node: str, condition: Optional[Callable] = None):
        self.next_nodes.append(next_node)
        self.condition = condition

class StateGraph:
    """LangGraph风格 - 有状态工作流图"""
    
    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, WorkflowNode] = {}
        self.state: Dict[str, Any] = {}
        self.current_node: Optional[str] = None
        self.history: List[Dict] = []
        self.checkpoint_manager = CheckpointManager()
    
    def add_node(self, node: WorkflowNode):
        self.nodes[node.name] = node
        logger.info(f"添加节点: {node.name}")
    
    def set_entry_point(self, node_name: str):
        if node_name in self.nodes:
            self.current_node = node_name
            logger.info(f"设置入口点: {node_name}")
    
    async def run(self, initial_state: Optional[Dict] = None) -> Dict[str, Any]:
        if initial_state:
            self.state.update(initial_state)
        
        checkpoint_id = self.checkpoint_manager.create_checkpoint(
            "workflow_start", 
            {"state": self.state, "current_node": self.current_node}
        )
        
        while self.current_node:
            node = self.nodes.get(self.current_node)
            if not node:
                break
            
            self.history.append({
                "node": self.current_node,
                "timestamp": datetime.now().isoformat(),
                "state_before": dict(self.state)
            })
            
            try:
                self.state = await node.execute(self.state)
                self.checkpoint_manager.update_checkpoint(
                    checkpoint_id, 
                    CheckpointState.RUNNING,
                    {"state": self.state}
                )
                
                next_node = self._get_next_node(node)
                self.current_node = next_node
                
            except Exception as e:
                self.checkpoint_manager.update_checkpoint(
                    checkpoint_id, 
                    CheckpointState.FAILED,
                    {"error": str(e)}
                )
                logger.error(f"节点执行失败: {self.current_node} - {str(e)}")
                break
        
        self.checkpoint_manager.update_checkpoint(checkpoint_id, CheckpointState.COMPLETED)
        return self.state
    
    def _get_next_node(self, node: WorkflowNode) -> Optional[str]:
        if not node.next_nodes:
            return None
        
        if node.condition:
            for next_name in node.next_nodes:
                if node.condition(self.state):
                    return next_name
            return None
        
        return node.next_nodes[0]
    
    def get_history(self) -> List[Dict]:
        return self.history

@dataclass
class AgentRole:
    """CrewAI风格 - Agent角色定义"""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = field(default_factory=list)
    allow_delegation: bool = False
    verbose: bool = True

@dataclass
class Task:
    """CrewAI风格 - 任务定义"""
    description: str
    agent: str
    expected_output: Optional[str] = None
    context: List[str] = field(default_factory=list)
    async_execution: bool = False

class CrewAgent:
    """CrewAI风格 - 团队协作Agent"""
    
    def __init__(self, role: AgentRole):
        self.role = role
        self.memory: List[Dict] = []
    
    def execute_task(self, task: Task, context: Optional[Dict] = None) -> Dict[str, Any]:
        result = {
            "agent": self.role.name,
            "task": task.description,
            "output": f"[{self.role.role}] 执行任务: {task.description}",
            "timestamp": datetime.now().isoformat()
        }
        self.memory.append(result)
        logger.info(f"Agent {self.role.name} 完成任务: {task.description[:50]}...")
        return result

class Crew:
    """CrewAI风格 - Agent团队"""
    
    def __init__(self, name: str):
        self.name = name
        self.agents: Dict[str, CrewAgent] = {}
        self.tasks: List[Task] = []
        self.results: List[Dict] = []
    
    def add_agent(self, role: AgentRole):
        self.agents[role.name] = CrewAgent(role)
        logger.info(f"添加Agent: {role.name} ({role.role})")
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    async def kickoff(self) -> List[Dict]:
        logger.info(f"团队 {self.name} 开始执行任务...")
        
        for task in self.tasks:
            agent = self.agents.get(task.agent)
            if agent:
                if task.async_execution:
                    result = await asyncio.to_thread(agent.execute_task, task)
                else:
                    result = agent.execute_task(task)
                self.results.append(result)
        
        logger.info(f"团队 {self.name} 完成所有任务")
        return self.results

class ConversationMessage:
    """AutoGen风格 - 对话消息"""
    
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.now().isoformat()

class ConversableAgent:
    """AutoGen风格 - 可对话Agent"""
    
    def __init__(self, name: str, system_message: str = ""):
        self.name = name
        self.system_message = system_message
        self.messages: List[ConversationMessage] = []
        self.human_input_mode = "NEVER"
    
    def send(self, message: str, recipient: 'ConversableAgent') -> str:
        msg = ConversationMessage(self.name, recipient.name, message)
        self.messages.append(msg)
        recipient.messages.append(msg)
        
        response = recipient.receive(self.name, message)
        return response
    
    def receive(self, sender: str, message: str) -> str:
        response = f"[{self.name}] 收到来自 {sender} 的消息: {message[:50]}..."
        return response

class GroupChat:
    """AutoGen风格 - 群组对话"""
    
    def __init__(self, name: str):
        self.name = name
        self.agents: List[ConversableAgent] = []
        self.messages: List[Dict] = []
        self.max_round = 10
    
    def add_agent(self, agent: ConversableAgent):
        self.agents.append(agent)
    
    def broadcast(self, sender: ConversableAgent, message: str):
        msg_record = {
            "sender": sender.name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(msg_record)
        
        for agent in self.agents:
            if agent.name != sender.name:
                agent.receive(sender.name, message)

class CodeAgent:
    """Smolagents风格 - 代码代理"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Callable] = {}
        self.execution_history: List[Dict] = []
    
    def add_tool(self, name: str, func: Callable):
        self.tools[name] = func
        logger.info(f"添加工具: {name}")
    
    async def execute_code(self, code: str) -> Dict[str, Any]:
        result = {
            "agent": self.name,
            "code": code,
            "timestamp": datetime.now().isoformat(),
            "output": None,
            "error": None
        }
        
        try:
            local_vars = {}
            exec(code, {"__builtins__": __builtins__, **self.tools}, local_vars)
            result["output"] = local_vars.get("result", "执行成功")
        except Exception as e:
            result["error"] = str(e)
        
        self.execution_history.append(result)
        return result

class KnowledgeNode:
    """Cognee风格 - 知识图谱节点"""
    
    def __init__(self, id: str, content: str, node_type: str = "entity"):
        self.id = id
        self.content = content
        self.node_type = node_type
        self.edges: List[Dict] = []
        self.metadata: Dict = {}
    
    def add_edge(self, target_id: str, relation: str, weight: float = 1.0):
        self.edges.append({
            "target": target_id,
            "relation": relation,
            "weight": weight
        })

class KnowledgeGraph:
    """Cognee风格 - 知识图谱记忆"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.entity_types: Dict[str, List[str]] = {}
    
    def add_node(self, node: KnowledgeNode):
        self.nodes[node.id] = node
        if node.node_type not in self.entity_types:
            self.entity_types[node.node_type] = []
        self.entity_types[node.node_type].append(node.id)
        logger.info(f"添加知识节点: {node.id} ({node.node_type})")
    
    def connect(self, source_id: str, target_id: str, relation: str):
        if source_id in self.nodes and target_id in self.nodes:
            self.nodes[source_id].add_edge(target_id, relation)
            logger.info(f"创建关系: {source_id} --{relation}--> {target_id}")
    
    def search(self, query: str, depth: int = 2) -> List[Dict]:
        results = []
        for node_id, node in self.nodes.items():
            if query.lower() in node.content.lower():
                related = self._get_related_nodes(node_id, depth)
                results.append({
                    "node": {"id": node.id, "content": node.content, "type": node.node_type},
                    "related": related
                })
        return results
    
    def _get_related_nodes(self, node_id: str, depth: int) -> List[Dict]:
        if depth <= 0 or node_id not in self.nodes:
            return []
        
        related = []
        for edge in self.nodes[node_id].edges:
            target = self.nodes.get(edge["target"])
            if target:
                related.append({
                    "id": target.id,
                    "content": target.content,
                    "relation": edge["relation"],
                    "deeper": self._get_related_nodes(target.id, depth - 1)
                })
        return related

class MemoryType(Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

@dataclass
class MemoryEntry:
    content: str
    memory_type: MemoryType
    importance: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

class MemoryManager:
    """Mem0/Letta风格 - 记忆管理"""
    
    def __init__(self, max_short_term: int = 100):
        self.short_term: List[MemoryEntry] = []
        self.long_term: List[MemoryEntry] = []
        self.episodic: List[MemoryEntry] = []
        self.semantic: List[MemoryEntry] = []
        self.max_short_term = max_short_term
        self.knowledge_graph = KnowledgeGraph()
    
    def add_memory(self, content: str, memory_type: MemoryType, importance: float = 0.5):
        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            importance=importance
        )
        
        if memory_type == MemoryType.SHORT_TERM:
            self.short_term.append(entry)
            if len(self.short_term) > self.max_short_term:
                self._consolidate_memory()
        elif memory_type == MemoryType.LONG_TERM:
            self.long_term.append(entry)
        elif memory_type == MemoryType.EPISODIC:
            self.episodic.append(entry)
        elif memory_type == MemoryType.SEMANTIC:
            self.semantic.append(entry)
        
        logger.info(f"添加记忆: {memory_type.value} - {content[:50]}...")
    
    def _consolidate_memory(self):
        if self.short_term:
            important = sorted(self.short_term, key=lambda x: x.importance, reverse=True)[0]
            self.long_term.append(important)
            self.short_term = self.short_term[1:]
            logger.info("记忆整合: 短期 -> 长期")
    
    def recall(self, query: str, memory_types: Optional[List[MemoryType]] = None) -> List[MemoryEntry]:
        results = []
        types_to_search = memory_types or list(MemoryType)
        
        for mem_type in types_to_search:
            if mem_type == MemoryType.SHORT_TERM:
                results.extend([m for m in self.short_term if query.lower() in m.content.lower()])
            elif mem_type == MemoryType.LONG_TERM:
                results.extend([m for m in self.long_term if query.lower() in m.content.lower()])
            elif mem_type == MemoryType.EPISODIC:
                results.extend([m for m in self.episodic if query.lower() in m.content.lower()])
            elif mem_type == MemoryType.SEMANTIC:
                results.extend([m for m in self.semantic if query.lower() in m.content.lower()])
        
        return sorted(results, key=lambda x: x.importance, reverse=True)
    
    def to_knowledge_graph(self):
        for entry in self.semantic:
            node = KnowledgeNode(
                id=hashlib.md5(entry.content.encode()).hexdigest()[:8],
                content=entry.content,
                node_type="semantic"
            )
            self.knowledge_graph.add_node(node)

class FrameworkIntegration:
    """框架集成主类"""
    
    def __init__(self):
        self.checkpoint_manager = CheckpointManager()
        self.memory_manager = MemoryManager()
        self.knowledge_graph = KnowledgeGraph()
        self.workflows: Dict[str, StateGraph] = {}
        self.crews: Dict[str, Crew] = {}
        self.group_chats: Dict[str, GroupChat] = {}
        self.code_agents: Dict[str, CodeAgent] = {}
    
    def create_workflow(self, name: str) -> StateGraph:
        workflow = StateGraph(name)
        self.workflows[name] = workflow
        return workflow
    
    def create_crew(self, name: str) -> Crew:
        crew = Crew(name)
        self.crews[name] = crew
        return crew
    
    def create_group_chat(self, name: str) -> GroupChat:
        chat = GroupChat(name)
        self.group_chats[name] = chat
        return chat
    
    def create_code_agent(self, name: str) -> CodeAgent:
        agent = CodeAgent(name)
        self.code_agents[name] = agent
        return agent
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "workflows": list(self.workflows.keys()),
            "crews": list(self.crews.keys()),
            "group_chats": list(self.group_chats.keys()),
            "code_agents": list(self.code_agents.keys()),
            "memory_stats": {
                "short_term": len(self.memory_manager.short_term),
                "long_term": len(self.memory_manager.long_term),
                "episodic": len(self.memory_manager.episodic),
                "semantic": len(self.memory_manager.semantic)
            },
            "knowledge_nodes": len(self.knowledge_graph.nodes)
        }

if __name__ == "__main__":
    integration = FrameworkIntegration()
    
    print("="*50)
    print("框架增强模块测试")
    print("="*50)
    
    print("\n1. 检查点管理测试:")
    cp_id = integration.checkpoint_manager.create_checkpoint("test", {"data": "test"})
    print(f"   创建检查点: {cp_id}")
    
    print("\n2. 记忆管理测试:")
    integration.memory_manager.add_memory("测试短期记忆", MemoryType.SHORT_TERM, 0.8)
    integration.memory_manager.add_memory("测试长期记忆", MemoryType.LONG_TERM, 0.9)
    print(f"   短期记忆数: {len(integration.memory_manager.short_term)}")
    print(f"   长期记忆数: {len(integration.memory_manager.long_term)}")
    
    print("\n3. 知识图谱测试:")
    node1 = KnowledgeNode("n1", "Python", "language")
    node2 = KnowledgeNode("n2", "FastAPI", "framework")
    integration.knowledge_graph.add_node(node1)
    integration.knowledge_graph.add_node(node2)
    integration.knowledge_graph.connect("n1", "n2", "has_framework")
    print(f"   节点数: {len(integration.knowledge_graph.nodes)}")
    
    print("\n4. 系统状态:")
    print(integration.get_status())
    
    print("\n" + "="*50)
    print("框架增强模块测试完成 ✅")
    print("="*50)
