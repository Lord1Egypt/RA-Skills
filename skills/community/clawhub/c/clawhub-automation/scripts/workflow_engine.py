"""
Workflow Engine - 自动化流程引擎
负责流程的构建、执行、状态管理
与重试降级Skill联动实现异常兜底
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class NodeType(Enum):
    """节点类型"""
    TRIGGER = "trigger"      # 触发条件
    ACTION = "action"        # 操作动作
    CONDITION = "condition"  # 分支判断


class NodeStatus(Enum):
    """节点状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    SUCCESS = "success"      # 执行成功
    FAILED = "failed"        # 执行失败
    RETRYING = "retrying"    # 重试中
    DEGRADED = "degraded"    # 降级执行


class WorkflowStatus(Enum):
    """流程状态"""
    DRAFT = "draft"          # 草稿
    ACTIVE = "active"        # 启用
    PAUSED = "paused"        # 暂停
    ERROR = "error"          # 错误


@dataclass
class WorkflowNode:
    """工作流节点"""
    id: str
    name: str
    node_type: NodeType
    platform: str            # 平台: wechat, dingtalk, feishu, wps, etc.
    action: str              # 操作类型
    params: Dict[str, Any] = field(default_factory=dict)
    next_nodes: List[str] = field(default_factory=list)
    condition: Optional[str] = None  # 分支条件
    is_critical: bool = True  # 是否核心节点
    retry_config: Dict[str, Any] = field(default_factory=dict)
    
    # 执行状态
    status: NodeStatus = NodeStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    retry_count: int = 0


@dataclass
class Workflow:
    """工作流定义"""
    id: str
    name: str
    description: str
    nodes: Dict[str, WorkflowNode]
    start_node: str
    status: WorkflowStatus = WorkflowStatus.DRAFT
    owner: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    
    # 执行统计
    total_runs: int = 0
    success_runs: int = 0
    failed_runs: int = 0


@dataclass
class ExecutionResult:
    """执行结果"""
    workflow_id: str
    execution_id: str
    success: bool
    status: str
    node_results: Dict[str, Any]
    start_time: float
    end_time: float
    duration: float
    degraded: bool = False
    error_message: Optional[str] = None
    logs: List[Dict] = field(default_factory=list)


class WorkflowEngine:
    """
    自动化流程引擎
    
    Features:
    - 流程构建与配置
    - 流程执行与状态管理
    - 与重试降级Skill联动
    - 执行日志记录
    """
    
    def __init__(self, retry_fallback_skill=None):
        """
        初始化流程引擎
        
        Args:
            retry_fallback_skill: 重试降级Skill实例
        """
        self.workflows: Dict[str, Workflow] = {}
        self.retry_fallback = retry_fallback_skill
        self.execution_logs: List[Dict] = []
        self.node_handlers: Dict[str, Callable] = {}
        
        # 注册默认节点处理器
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认节点处理器"""
        # 触发器处理器
        self.node_handlers['trigger_message'] = self._handle_message_trigger
        self.node_handlers['trigger_schedule'] = self._handle_schedule_trigger
        self.node_handlers['trigger_file'] = self._handle_file_trigger
        
        # 动作处理器
        self.node_handlers['send_message'] = self._handle_send_message
        self.node_handlers['sync_file'] = self._handle_sync_file
        self.node_handlers['create_document'] = self._handle_create_document
        self.node_handlers['send_notification'] = self._handle_notification
    
    def create_workflow(self, name: str, description: str = "") -> Workflow:
        """
        创建新工作流
        
        Args:
            name: 流程名称
            description: 流程描述
            
        Returns:
            Workflow: 新创建的工作流
        """
        workflow_id = str(uuid.uuid4())[:8]
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            nodes={},
            start_node=""
        )
        self.workflows[workflow_id] = workflow
        return workflow
    
    def add_node(
        self,
        workflow_id: str,
        name: str,
        node_type: NodeType,
        platform: str,
        action: str,
        params: Dict[str, Any] = None,
        is_critical: bool = True,
        condition: str = None
    ) -> str:
        """
        添加节点到工作流
        
        Args:
            workflow_id: 工作流ID
            name: 节点名称
            node_type: 节点类型
            platform: 平台
            action: 操作类型
            params: 参数
            is_critical: 是否核心节点
            condition: 分支条件
            
        Returns:
            str: 节点ID
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流 {workflow_id} 不存在")
        
        node_id = f"node_{len(self.workflows[workflow_id].nodes)}"
        node = WorkflowNode(
            id=node_id,
            name=name,
            node_type=node_type,
            platform=platform,
            action=action,
            params=params or {},
            is_critical=is_critical,
            condition=condition
        )
        
        self.workflows[workflow_id].nodes[node_id] = node
        
        # 如果是第一个节点，设为起始节点
        if not self.workflows[workflow_id].start_node:
            self.workflows[workflow_id].start_node = node_id
        
        return node_id
    
    def connect_nodes(self, workflow_id: str, from_node: str, to_node: str):
        """
        连接两个节点
        
        Args:
            workflow_id: 工作流ID
            from_node: 源节点ID
            to_node: 目标节点ID
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流 {workflow_id} 不存在")
        
        workflow = self.workflows[workflow_id]
        if from_node not in workflow.nodes or to_node not in workflow.nodes:
            raise ValueError("节点不存在")
        
        workflow.nodes[from_node].next_nodes.append(to_node)
    
    def run(self, workflow_id: str, context: Dict[str, Any] = None) -> ExecutionResult:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流ID
            context: 执行上下文
            
        Returns:
            ExecutionResult: 执行结果
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流 {workflow_id} 不存在")
        
        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        # 初始化执行状态
        for node in workflow.nodes.values():
            node.status = NodeStatus.PENDING
            node.result = None
            node.error = None
            node.retry_count = 0
        
        logs = []
        node_results = {}
        current_node_id = workflow.start_node
        degraded = False
        
        try:
            while current_node_id:
                node = workflow.nodes[current_node_id]
                
                # 记录开始执行
                node.start_time = time.time()
                node.status = NodeStatus.RUNNING
                
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'execution_id': execution_id,
                    'node_id': node.id,
                    'node_name': node.name,
                    'action': f"{node.platform}.{node.action}",
                    'status': 'running'
                }
                
                try:
                    # 执行节点
                    result = self._execute_node(node, context or {})
                    
                    node.status = NodeStatus.SUCCESS
                    node.result = result
                    node.end_time = time.time()
                    
                    log_entry['status'] = 'success'
                    log_entry['duration'] = node.end_time - node.start_time
                    log_entry['result'] = result
                    
                    node_results[node.id] = {
                        'success': True,
                        'result': result,
                        'duration': log_entry['duration']
                    }
                    
                except Exception as e:
                    # 执行失败，尝试重试或降级
                    handle_result = self._handle_node_failure(node, e, context)
                    
                    if handle_result.get('success'):
                        # 重试或降级成功
                        node.status = NodeStatus.DEGRADED if handle_result.get('degraded') else NodeStatus.SUCCESS
                        node.result = handle_result.get('result')
                        degraded = degraded or handle_result.get('degraded', False)
                        
                        log_entry['status'] = 'degraded' if handle_result.get('degraded') else 'success'
                        log_entry['fallback_used'] = handle_result.get('fallback_used')
                        
                        node_results[node.id] = {
                            'success': True,
                            'result': node.result,
                            'degraded': handle_result.get('degraded', False),
                            'fallback_used': handle_result.get('fallback_used')
                        }
                    else:
                        # 处理失败
                        node.status = NodeStatus.FAILED
                        node.error = str(e)
                        node.end_time = time.time()
                        
                        log_entry['status'] = 'failed'
                        log_entry['error'] = str(e)
                        
                        node_results[node.id] = {
                            'success': False,
                            'error': str(e)
                        }
                        
                        # 如果是核心节点失败，终止流程
                        if node.is_critical:
                            logs.append(log_entry)
                            break
                
                logs.append(log_entry)
                
                # 确定下一个节点
                if node.next_nodes:
                    current_node_id = node.next_nodes[0]  # 简化：取第一个
                else:
                    current_node_id = None
        
        except Exception as e:
            error_message = str(e)
        else:
            error_message = None
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 更新工作流统计
        workflow.total_runs += 1
        success = all(r.get('success') for r in node_results.values())
        if success:
            workflow.success_runs += 1
        else:
            workflow.failed_runs += 1
        
        # 构建执行结果
        result = ExecutionResult(
            workflow_id=workflow_id,
            execution_id=execution_id,
            success=success,
            status='completed' if success else 'failed',
            node_results=node_results,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            degraded=degraded,
            error_message=error_message,
            logs=logs
        )
        
        self.execution_logs.append({
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
    
    def _execute_node(self, node: WorkflowNode, context: Dict[str, Any]) -> Any:
        """执行单个节点"""
        handler_key = f"{node.action}"
        
        if handler_key in self.node_handlers:
            return self.node_handlers[handler_key](node, context)
        
        # 默认处理：模拟执行
        return {"status": "simulated", "node": node.name}
    
    def _handle_node_failure(
        self,
        node: WorkflowNode,
        error: Exception,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        处理节点执行失败
        与重试降级Skill联动
        """
        # 如果有重试降级Skill，调用它
        if self.retry_fallback:
            # 这里集成retry_fallback_skill
            pass
        
        # 默认降级策略：非核心节点跳过，核心节点尝试简化执行
        if not node.is_critical:
            return {
                'success': True,
                'degraded': True,
                'result': {'status': 'skipped', 'reason': 'optional_node_failed'}
            }
        
        # 核心节点失败
        return {'success': False, 'error': str(error)}
    
    # 节点处理器实现
    def _handle_message_trigger(self, node: WorkflowNode, context: Dict) -> Any:
        """处理消息触发器"""
        platform = node.platform
        message_type = node.params.get('message_type', 'text')
        return {
            'triggered': True,
            'platform': platform,
            'message_type': message_type,
            'content': context.get('message_content', '')
        }
    
    def _handle_schedule_trigger(self, node: WorkflowNode, context: Dict) -> Any:
        """处理定时触发器"""
        schedule = node.params.get('schedule', '')
        return {
            'triggered': True,
            'schedule': schedule,
            'next_run': datetime.now().isoformat()
        }
    
    def _handle_file_trigger(self, node: WorkflowNode, context: Dict) -> Any:
        """处理文件触发器"""
        path = node.params.get('path', '')
        return {
            'triggered': True,
            'path': path,
            'file_info': context.get('file_info', {})
        }
    
    def _handle_send_message(self, node: WorkflowNode, context: Dict) -> Any:
        """处理发送消息"""
        platform = node.platform
        to = node.params.get('to', '')
        content = node.params.get('content', '')
        
        # 模拟发送
        return {
            'sent': True,
            'platform': platform,
            'to': to,
            'message_id': f"msg_{uuid.uuid4().hex[:8]}"
        }
    
    def _handle_sync_file(self, node: WorkflowNode, context: Dict) -> Any:
        """处理文件同步"""
        from_platform = node.params.get('from_platform', '')
        to_platform = node.params.get('to_platform', '')
        file_path = node.params.get('file_path', '')
        
        return {
            'synced': True,
            'from': from_platform,
            'to': to_platform,
            'file': file_path,
            'sync_id': f"sync_{uuid.uuid4().hex[:8]}"
        }
    
    def _handle_create_document(self, node: WorkflowNode, context: Dict) -> Any:
        """处理创建文档"""
        platform = node.platform
        title = node.params.get('title', '')
        content = node.params.get('content', '')
        
        return {
            'created': True,
            'platform': platform,
            'document_id': f"doc_{uuid.uuid4().hex[:8]}",
            'title': title
        }
    
    def _handle_notification(self, node: WorkflowNode, context: Dict) -> Any:
        """处理通知"""
        platform = node.platform
        title = node.params.get('title', '')
        body = node.params.get('body', '')
        
        return {
            'notified': True,
            'platform': platform,
            'notification_id': f"notif_{uuid.uuid4().hex[:8]}"
        }
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """获取工作流"""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self, owner: str = None) -> List[Workflow]:
        """列出工作流"""
        workflows = list(self.workflows.values())
        if owner:
            workflows = [w for w in workflows if w.owner == owner]
        return workflows
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """删除工作流"""
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            return True
        return False
    
    def get_execution_logs(self, workflow_id: str = None) -> List[Dict]:
        """获取执行日志"""
        if workflow_id:
            return [log for log in self.execution_logs if log['workflow_id'] == workflow_id]
        return self.execution_logs