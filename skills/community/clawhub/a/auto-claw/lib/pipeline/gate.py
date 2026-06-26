# -*- coding: utf-8 -*-
"""
Gate Pipeline - 操作授权与执行管道

职责：
1. 接收AI/用户操作请求
2. 执行安全检查（权限、参数验证）
3. 执行业务逻辑
4. 返回结果并记录审计日志

设计思路：
- Gate模式：每个操作必须过"门卫"
- 支持白名单/黑名单规则
- 操作可追溯、可撤销
"""
import time
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Any, Optional, Dict
from datetime import datetime
from lib.audit.logger import AuditLogger


class OperationType(Enum):
    """操作类型枚举"""
    READ = "read"           # 读取操作
    WRITE = "write"         # 写入操作  
    DELETE = "delete"       # 删除操作（高风险）
    ADMIN = "admin"         # 管理操作（最高风险）


class GateDecision(Enum):
    """Gate裁决结果"""
    ALLOW = "allow"
    DENY = "deny"
    NEED_APPROVAL = "need_approval"  # 需要人工审批
    ERROR = "error"


@dataclass
class Operation:
    """
    操作请求
    
    代表一个待执行的操作，包含操作者、操作类型、目标资源等
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    op_type: OperationType = OperationType.READ
    actor: str = "ai_agent"
    resource: str = ""          # 资源标识 (如 "site:demo/post:123")
    action: str = ""            # 具体动作 (如 "publish", "delete")
    params: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def __str__(self):
        return f"[{self.id}] {self.actor}:{self.op_type.value} {self.resource}/{self.action}"


@dataclass  
class OperationResult:
    """操作结果"""
    operation: Operation
    decision: GateDecision = GateDecision.DENY
    executed: bool = False
    result: Any = None
    error: Optional[str] = None
    duration_ms: float = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.operation.id,
            "decision": self.decision.value,
            "executed": self.executed,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms
        }


class GatePipeline:
    """
    Gate Pipeline - 操作执行管道
    
    处理流程：
    1. pre_check() - 前置检查（权限、参数）
    2. execute() - 执行实际操作
    3. post_check() - 后置处理（记录结果）
    """
    
    def __init__(self, config, audit_logger: AuditLogger):
        self.config = config
        self.audit = audit_logger
        self._handlers: Dict[str, Callable] = {}
        
        # 注册默认处理器
        self._register_default_gates()
    
    def _register_default_gates(self):
        """注册默认Gate规则"""
        # 读取操作默认允许
        self.add_rule(OperationType.READ, lambda op: True)
        
        # 删除操作需要额外确认
        self.add_rule(OperationType.DELETE, self._check_delete)
        
        # 管理操作需要审批
        if self.config.pipeline.require_approval:
            self.add_rule(OperationType.ADMIN, self._check_admin)
    
    def add_rule(self, op_type: OperationType, checker: Callable[[Operation], bool]):
        """添加Gate规则"""
        self._handlers[op_type.value] = checker
    
    def _check_delete(self, op: Operation) -> bool:
        """删除操作检查"""
        # 危险操作二次确认
        dangerous = op.params.get("dangerous", False)
        return dangerous or op.params.get("confirmed", False)
    
    def _check_admin(self, op: Operation) -> bool:
        """管理操作检查"""
        # TODO: 实现真正的审批流程
        return False  # 默认需要审批
    
    def execute(self, operation: Operation, executor: Optional[Callable] = None) -> OperationResult:
        """
        执行操作的主入口
        
        Args:
            operation: 操作请求
            executor: 实际执行函数 (op) -> result
            
        Returns:
            OperationResult
        """
        start = time.time()
        result = OperationResult(operation=operation)
        
        self.audit.log("pipeline", "request", {
            "op_id": operation.id,
            "type": operation.op_type.value,
            "resource": operation.resource,
            "action": operation.action
        })
        
        # 1. Pre-check: Gate裁决
        checker = self._handlers.get(operation.op_type.value)
        if checker and not checker(operation):
            result.decision = GateDecision.NEED_APPROVAL
            result.error = f"Operation {operation.op_type.value} requires approval"
            self.audit.log("pipeline", "denied", {"op_id": operation.id, "reason": result.error})
            return result
        
        result.decision = GateDecision.ALLOW
        
        # 2. Execute: 执行实际操作
        if executor:
            try:
                result.result = executor(operation)
                result.executed = True
                self.audit.log("pipeline", "executed", {"op_id": operation.id})
            except Exception as e:
                result.error = str(e)
                self.audit.log("pipeline", "error", {"op_id": operation.id, "error": result.error})
        else:
            result.executed = True
            result.result = {"msg": "no executor provided, operation allowed but not run"}
        
        result.duration_ms = int((time.time() - start) * 1000)
        return result
    
    def execute_batch(self, operations: list[Operation], 
                      executor: Optional[Callable] = None) -> list[OperationResult]:
        """批量执行操作"""
        return [self.execute(op, executor) for op in operations]
