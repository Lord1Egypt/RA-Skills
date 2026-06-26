"""
Gate Pipeline - 安全操作审批门
所有写操作必须通过风险评估和审批
"""
import hashlib
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Optional
try:
    from .audit import AuditLogger
except ImportError:
    from audit import AuditLogger  # noqa: F401

class RiskLevel(Enum):
    LOW = "low"       # 读取、查询 - 直接执行
    MEDIUM = "medium" # 安装插件、更新内容 - 需要审批
    HIGH = "high"     # 删除、核心更新 - 强制审批

@dataclass
class Operation:
    id: str
    type: str  # read/write/delete/admin
    action: str
    resource: str
    payload: dict = field(default_factory=dict)

@dataclass
class GateDecision:
    decision: str  # allow / deny / need_approval
    reason: str
    op_id: str

class GatePipeline:
    """
    风险分级：
    - LOW: 直接执行
    - MEDIUM: 发审批请求，等人工
    - HIGH: 强制审批，阻断操作
    """
    def __init__(self, audit: AuditLogger, approval_callback: Callable[[Operation], bool] = None):
        self.audit = audit
        self.approval_callback = approval_callback or self._default_approval
        self._risk_map = {
            "read": RiskLevel.LOW,
            "get_posts": RiskLevel.LOW,
            "get_users": RiskLevel.LOW,
            "get_plugins": RiskLevel.LOW,
            "write": RiskLevel.MEDIUM,
            "create_post": RiskLevel.MEDIUM,
            "update_post": RiskLevel.MEDIUM,
            "install_plugin": RiskLevel.HIGH,
            "activate_plugin": RiskLevel.MEDIUM,
            "update_theme": RiskLevel.HIGH,
            "delete_post": RiskLevel.HIGH,
            "core_update": RiskLevel.HIGH,
            "run_sql": RiskLevel.HIGH,
            "delete": RiskLevel.HIGH,
        }
    
    def _default_approval(self, op: Operation) -> bool:
        """默认审批逻辑 - 简单演示用"""
        return True  # 生产环境应发 webhook 等待人工确认
    
    def assess_risk(self, action: str) -> RiskLevel:
        return self._risk_map.get(action, RiskLevel.MEDIUM)
    
    def request(self, op: Operation) -> GateDecision:
        """请求执行操作，返回决策"""
        risk = self.assess_risk(op.action)
        
        self.audit.log("pipeline", "request", details={
            "op_id": op.id, "type": op.type,
            "action": op.action, "risk": risk.value
        })
        
        if risk == RiskLevel.LOW:
            decision = GateDecision("allow", "LOW risk - auto approved", op.id)
        elif risk == RiskLevel.MEDIUM:
            approved = self.approval_callback(op)
            if approved:
                decision = GateDecision("allow", "MEDIUM risk - manually approved", op.id)
            else:
                decision = GateDecision("need_approval", "Waiting for approval", op.id)
        else:  # HIGH
            approved = self.approval_callback(op)
            if approved:
                decision = GateDecision("allow", "HIGH risk - explicitly approved", op.id)
            else:
                decision = GateDecision("deny", "HIGH risk - blocked", op.id)
        
        self.audit.log("pipeline", decision.decision, details={
            "op_id": op.id, "reason": decision.reason
        })
        return decision
    
    def new_operation(self, op_type: str, action: str, resource: str, payload: dict = None) -> Operation:
        return Operation(
            id=uuid.uuid4().hex[:8],
            type=op_type,
            action=action,
            resource=resource,
            payload=payload or {}
        )
