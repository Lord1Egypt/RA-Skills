"""
Permission Manager - 权限管理模块

实现RBAC（基于角色的访问控制）权限管理系统
支持：
- 角色与权限矩阵
- 操作权限校验
- 数据范围隔离
- 权限变更审计
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class PermissionResult(Enum):
    """权限校验结果"""
    GRANTED = "granted"             # 允许
    DENIED = "denied"              # 拒绝
    NEED_APPROVAL = "need_approval" # 需要人工审批
    NEED_AUDIT = "need_audit"      # 需要审计


@dataclass
class PermissionContext:
    """权限上下文"""
    user_id: str
    user_role: str
    agent_id: str
    action: str
    resource: Optional[str] = None
    parameters: Optional[dict] = None
    risk_score: float = 0.0
    ip_address: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class PermissionDecision:
    """权限决策"""
    result: PermissionResult
    reason: str
    requires_approval_from: Optional[str] = None
    approval_ticket_id: Optional[str] = None
    risk_level: str = "low"
    conditions: Optional[dict] = None


@dataclass
class AuditEntry:
    """审计条目"""
    timestamp: str
    event_type: str
    user_id: str
    user_role: str
    agent_id: str
    action: str
    resource: Optional[str]
    decision: str
    reason: str
    risk_score: float
    parameters: Optional[dict] = None
    request_id: Optional[str] = None


# =============================================================================
# 角色权限矩阵
# =============================================================================

ROLE_PERMISSIONS = {
    "admin": {
        "*": {"access": "full", "approval_required": False},
    },
    "finance_manager": {
        "finance_agent.query_budget": {"access": "granted", "approval_required": False},
        "finance_agent.audit_payment": {"access": "granted", "approval_required": False},
        "finance_agent.financial_reporting": {"access": "granted", "approval_required": False},
        "inventory_agent.query_stock": {"access": "granted", "approval_required": False},
        "doc_agent.generate_document": {"access": "granted", "approval_required": False},
    },
    "procurement_manager": {
        "procurement_agent.supplier_lookup": {"access": "granted", "approval_required": False},
        "procurement_agent.place_order": {"access": "granted", "approval_required": False, "amount_threshold": 50000},
        "procurement_agent.track_order": {"access": "granted", "approval_required": False},
        "finance_agent.query_budget": {"access": "granted", "approval_required": False},
        "inventory_agent.query_stock": {"access": "granted", "approval_required": False},
        "logistics_agent.query_freight": {"access": "granted", "approval_required": False},
    },
    "warehouse_operator": {
        "inventory_agent.query_stock": {"access": "granted", "approval_required": False},
        "inventory_agent.calculate_safety_stock": {"access": "granted", "approval_required": False},
        "inventory_agent.trigger_replenishment": {"access": "granted", "approval_required": False},
        "logistics_agent.track_shipment": {"access": "granted", "approval_required": False},
    },
    "logistics_operator": {
        "logistics_agent.query_freight": {"access": "granted", "approval_required": False},
        "logistics_agent.plan_route": {"access": "granted", "approval_required": False},
        "logistics_agent.track_shipment": {"access": "granted", "approval_required": False},
    },
    "viewer": {
        "inventory_agent.query_stock": {"access": "granted", "approval_required": False},
        "logistics_agent.query_freight": {"access": "granted", "approval_required": False},
        "doc_agent.generate_document": {"access": "granted", "approval_required": False},
    },
}

# 高风险操作阈值配置
HIGH_RISK_OPERATIONS = {
    "procurement_agent.place_order": {
        "threshold_amount": 50000,
        "always_require_approval": True,
        "approval_role": "finance_manager",
    },
    "finance_agent.audit_payment": {
        "threshold_amount": 10000,
        "always_require_approval": False,
        "approval_role": "finance_manager",
    },
    "procurement_agent.cancel_order": {
        "always_require_approval": True,
        "approval_role": "procurement_manager",
    },
    "finance_agent.adjust_budget": {
        "always_require_approval": True,
        "approval_role": "finance_manager",
    },
}

# 风险评分权重
RISK_WEIGHTS = {
    "high_amount": 0.4,
    "sensitive_data": 0.3,
    "irreversible": 0.3,
    "external_api": 0.2,
    "financial_operation": 0.3,
}


# =============================================================================
# 权限管理器
# =============================================================================

class PermissionManager:
    """
    企业级权限管理器

    功能：
    - RBAC权限校验
    - 风险评分计算
    - 动态审批流触发
    - 权限变更追踪
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化权限管理器

        Args:
            config_path: 权限配置文件路径（YAML格式）
        """
        self._role_permissions = ROLE_PERMISSIONS.copy()
        self._high_risk_ops = HIGH_RISK_OPERATIONS.copy()
        self._risk_weights = RISK_WEIGHTS.copy()
        self._audit_log: list[AuditEntry] = []
        self._pending_approvals: dict[str, dict] = {}

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)

        logger.info("权限管理器初始化完成")

    def _load_config(self, config_path: str) -> None:
        """从配置文件加载权限设置"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            # 合并配置（配置文件优先级更高）
            logger.info(f"从{config_path}加载权限配置")
        except Exception as e:
            logger.warning(f"配置文件加载失败: {e}，使用默认配置")

    def check_permission(self, ctx: PermissionContext) -> PermissionDecision:
        """
        核心权限校验方法

        校验流程：
        1. 检查角色权限矩阵
        2. 计算风险评分
        3. 判断是否需要审批
        4. 生成决策

        Args:
            ctx: 权限上下文

        Returns:
            权限决策结果
        """
        permission_key = f"{ctx.agent_id}.{ctx.action}"
        role = ctx.user_role

        # Step 1: 检查权限矩阵
        decision = self._check_role_permission(role, permission_key, ctx)

        # Step 2: 如果权限矩阵允许，进行风险评分
        if decision.result == PermissionResult.DENIED:
            return decision

        # Step 3: 风险评分
        risk_score = self._calculate_risk_score(ctx)
        ctx.risk_score = risk_score

        # Step 4: 检查高风险操作阈值
        high_risk = self._check_high_risk_threshold(ctx, permission_key)

        # 记录审计日志
        self._log_audit(ctx, decision, risk_score)

        return decision

    def _check_role_permission(
        self,
        role: str,
        permission_key: str,
        ctx: PermissionContext
    ) -> PermissionDecision:
        """检查角色权限"""
        if role not in self._role_permissions:
            return PermissionDecision(
                result=PermissionResult.DENIED,
                reason=f"未知角色: {role}",
                risk_level="high",
            )

        role_perms = self._role_permissions[role]

        # 通配符匹配（admin角色）
        if "*" in role_perms:
            return PermissionDecision(
                result=PermissionResult.GRANTED,
                reason=f"管理员权限",
                risk_level="low",
            )

        # 精确匹配
        if permission_key in role_perms:
            perm = role_perms[permission_key]
            if perm.get("approval_required"):
                return PermissionDecision(
                    result=PermissionResult.NEED_APPROVAL,
                    reason="操作需要人工审批",
                    risk_level="medium",
                    requires_approval_from=perm.get("approval_role", "admin"),
                )
            return PermissionDecision(
                result=PermissionResult.GRANTED,
                reason="权限校验通过",
                risk_level="low",
            )

        return PermissionDecision(
            result=PermissionResult.DENIED,
            reason=f"角色{role}无权限执行{permission_key}",
            risk_level="medium",
        )

    def _check_high_risk_threshold(
        self,
        ctx: PermissionContext,
        permission_key: str
    ) -> Optional[PermissionDecision]:
        """检查高风险操作阈值"""
        if permission_key not in self._high_risk_ops:
            return None

        rule = self._high_risk_ops[permission_key]
        params = ctx.parameters or {}

        # 检查金额阈值
        if "threshold_amount" in rule:
            amount = params.get("total_amount") or params.get("amount") or 0
            if amount >= rule["threshold_amount"]:
                return PermissionDecision(
                    result=PermissionResult.NEED_APPROVAL,
                    reason=f"金额({amount})超过阈值({rule['threshold_amount']})，需要审批",
                    risk_level="high",
                    requires_approval_from=rule.get("approval_role"),
                    conditions={"min_amount": rule["threshold_amount"]},
                )

        # 强制审批检查
        if rule.get("always_require_approval"):
            return PermissionDecision(
                result=PermissionResult.NEED_APPROVAL,
                reason="高风险操作，需要人工审批",
                risk_level="high",
                requires_approval_from=rule.get("approval_role"),
            )

        return None

    def _calculate_risk_score(self, ctx: PermissionContext) -> float:
        """计算风险评分 (0.0 - 1.0)"""
        score = 0.0
        params = ctx.parameters or {}

        # 金额风险
        amount = params.get("total_amount") or params.get("amount") or 0
        if amount > 100000:
            score += self._risk_weights["high_amount"]
        elif amount > 50000:
            score += self._risk_weights["high_amount"] * 0.5

        # 敏感数据访问
        sensitive_fields = ["password", "token", "secret", "api_key", "private_key"]
        if any(f in str(params) for f in sensitive_fields):
            score += self._risk_weights["sensitive_data"]

        # 不可逆操作
        irreversible_actions = ["delete", "cancel", "revoke", "terminate"]
        if any(a in ctx.action.lower() for a in irreversible_actions):
            score += self._risk_weights["irreversible"]

        # 外部API调用
        if params.get("external_call") or params.get("api_call"):
            score += self._risk_weights["external_api"]

        # 财务操作
        financial_actions = ["payment", "transfer", "refund", "adjustment"]
        if any(a in ctx.action.lower() for a in financial_actions):
            score += self._risk_weights["financial_operation"]

        return min(score, 1.0)

    def _log_audit(
        self,
        ctx: PermissionContext,
        decision: PermissionDecision,
        risk_score: float
    ) -> None:
        """记录审计日志"""
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            event_type="permission_check",
            user_id=ctx.user_id,
            user_role=ctx.user_role,
            agent_id=ctx.agent_id,
            action=ctx.action,
            resource=ctx.resource,
            decision=decision.result.value,
            reason=decision.reason,
            risk_score=risk_score,
            parameters=ctx.parameters,
            request_id=ctx.session_id,
        )
        self._audit_log.append(entry)

        # 高风险事件告警
        if decision.result == PermissionResult.NEED_APPROVAL or risk_score > 0.5:
            logger.warning(
                f"[权限告警] user={ctx.user_id} role={ctx.user_role} "
                f"action={ctx.agent_id}.{ctx.action} "
                f"risk={risk_score:.2f} decision={decision.result.value}"
            )

    # -------------------------------------------------------------------------
    # 审批管理
    # -------------------------------------------------------------------------

    def create_approval_ticket(
        self,
        ctx: PermissionContext,
        reason: str
    ) -> str:
        """
        创建审批工单

        Args:
            ctx: 权限上下文
            reason: 审批原因

        Returns:
            工单ID
        """
        ticket_id = f"APR{datetime.now().strftime('%Y%m%d%H%M')}{len(self._pending_approvals):04d}"
        self._pending_approvals[ticket_id] = {
            "ticket_id": ticket_id,
            "context": {
                "user_id": ctx.user_id,
                "user_role": ctx.user_role,
                "agent_id": ctx.agent_id,
                "action": ctx.action,
                "parameters": ctx.parameters,
            },
            "reason": reason,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "risk_score": ctx.risk_score,
        }
        logger.info(f"创建审批工单: {ticket_id}")
        return ticket_id

    def approve_ticket(self, ticket_id: str, approver_role: str) -> dict[str, Any]:
        """审批工单"""
        if ticket_id not in self._pending_approvals:
            return {"success": False, "error": "工单不存在"}

        ticket = self._pending_approvals[ticket_id]
        required_role = ticket["context"]["user_role"]

        if approver_role != required_role and approver_role != "admin":
            return {"success": False, "error": "权限不足"}

        ticket["status"] = "approved"
        ticket["approved_by"] = approver_role
        ticket["approved_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": "approved",
        }

    def get_pending_approvals(self, role: Optional[str] = None) -> list[dict]:
        """获取待审批工单"""
        results = [
            t for t in self._pending_approvals.values()
            if t["status"] == "pending" and (role is None or t["context"]["user_role"] == role)
        ]
        return results

    # -------------------------------------------------------------------------
    # 辅助方法
    # -------------------------------------------------------------------------

    def get_user_permissions(self, role: str) -> dict[str, Any]:
        """获取用户角色对应的所有权限"""
        perms = self._role_permissions.get(role, {})
        return {
            "role": role,
            "permissions": perms,
            "count": len(perms) if "*" not in perms else "full_access",
        }

    def export_audit_log(self, path: str) -> None:
        """导出审计日志"""
        with open(path, "w", encoding="utf-8") as f:
            for entry in self._audit_log:
                f.write(json.dumps({
                    "timestamp": entry.timestamp,
                    "event_type": entry.event_type,
                    "user_id": entry.user_id,
                    "user_role": entry.user_role,
                    "agent_id": entry.agent_id,
                    "action": entry.action,
                    "decision": entry.decision,
                    "reason": entry.reason,
                    "risk_score": entry.risk_score,
                }, ensure_ascii=False) + "\n")
        logger.info(f"审计日志已导出: {path}")


# =============================================================================
# 便捷函数
# =============================================================================

def require_permission(role: str, agent: str, action: str):
    """
    装饰器：方法级权限控制

    Usage:
        @require_permission("procurement_manager", "procurement_agent", "place_order")
        async def create_order(...):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            ctx = PermissionContext(
                user_id=kwargs.get("user_id", "system"),
                user_role=role,
                agent_id=agent,
                action=action,
                parameters=kwargs,
            )
            pm = PermissionManager()
            decision = pm.check_permission(ctx)

            if decision.result == PermissionResult.DENIED:
                raise PermissionError(f"权限不足: {decision.reason}")

            if decision.result == PermissionResult.NEED_APPROVAL:
                raise PermissionError(f"需要审批: {decision.reason}")

            return await func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    print("=" * 60)
    print("  权限管理器测试")
    print("=" * 60)

    pm = PermissionManager()

    test_cases = [
        # 管理员权限测试
        PermissionContext(
            user_id="admin001",
            user_role="admin",
            agent_id="procurement_agent",
            action="place_order",
            parameters={"total_amount": 100000}
        ),
        # 采购经理测试
        PermissionContext(
            user_id="buyer001",
            user_role="procurement_manager",
            agent_id="procurement_agent",
            action="place_order",
            parameters={"total_amount": 60000}
        ),
        # 财务测试
        PermissionContext(
            user_id="fin001",
            user_role="finance_manager",
            agent_id="finance_agent",
            action="audit_payment",
            parameters={"amount": 15000}
        ),
        # 仓库操作员测试（无权操作）
        PermissionContext(
            user_id="op001",
            user_role="warehouse_operator",
            agent_id="finance_agent",
            action="audit_payment",
        ),
        # 高金额审批测试
        PermissionContext(
            user_id="buyer002",
            user_role="procurement_manager",
            agent_id="procurement_agent",
            action="place_order",
            parameters={"total_amount": 80000}
        ),
    ]

    for ctx in test_cases:
        decision = pm.check_permission(ctx)
        print(f"\n[{ctx.user_id}@{ctx.user_role}] → {ctx.agent_id}.{ctx.action}")
        print(f"  参数: {ctx.parameters}")
        print(f"  结果: {decision.result.value}")
        print(f"  原因: {decision.reason}")
        print(f"  风险: {decision.risk_level} ({ctx.risk_score:.2f})")
        if decision.requires_approval_from:
            print(f"  审批人: {decision.requires_approval_from}")

    print("\n\n[审计日志摘要]")
    print(f"  总记录数: {len(pm._audit_log)}")
    high_risk = [e for e in pm._audit_log if e.risk_score > 0.3]
    print(f"  高风险事件: {len(high_risk)}")
