"""
Approval Workflow — 审批流程引擎

基于风险等级的四级审批链：
- LOW:     自动通过
- MEDIUM:  Agent 自审
- HIGH:    Chief-of-Staff 审批
- CRITICAL: 人工介入

Features:
- 异步审批（webhook / polling）
- 审批超时自动处理
- 审批历史追踪
- 多级升级机制
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from cms_executor.connectors.base_connector import RiskLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ApprovalTier(Enum):
    """审批层级"""
    AUTO = "auto"            # 自动审批
    AGENT_SELF = "agent_self"  # Agent 自审
    CHIEF = "chief"          # 幕僚长审批
    HUMAN = "human"          # 人工介入


@dataclass
class ApprovalRequest:
    """审批请求"""
    approval_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    plan_id: str = ""
    plan_summary: dict = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    agent_id: str = ""
    agent_role: str = ""
    status: ApprovalStatus = ApprovalStatus.PENDING
    tier: ApprovalTier = ApprovalTier.AUTO
    approver: str = ""      # 审批人
    reason: str = ""        # 审批意见
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = ""
    expires_at: str = ""     # 超时截止时间
    history: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "approval_id": self.approval_id,
            "plan_id": self.plan_id,
            "risk_level": self.risk_level.value,
            "agent_id": self.agent_id,
            "agent_role": self.agent_role,
            "status": self.status.value,
            "tier": self.tier.value,
            "approver": self.approver,
            "reason": self.reason,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "history": self.history,
        }

    def add_history(self, action: str, actor: str, note: str = "") -> None:
        self.history.append({
            "action": action,
            "actor": actor,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


# =============================================================================
# 审批链
# =============================================================================

class ApprovalChain:
    """
    审批链（策略模式）
    
    风险等级 → 审批层级映射 + 超时配置
    """

    TIER_MAP: dict[str, tuple[ApprovalTier, int]] = {
        # risk_level: (tier, timeout_seconds)
        "low": (ApprovalTier.AUTO, 0),
        "medium": (ApprovalTier.AGENT_SELF, 600),      # 10 min
        "high": (ApprovalTier.CHIEF, 3600),            # 1 hour
        "critical": (ApprovalTier.HUMAN, 86400),       # 24 hours
    }

    # 危险操作强制升级（使用正则匹配）
    DANGEROUS_PATTERNS = [
        "delete_all", "truncate", "drop_table",
        "DROP TABLE", "DELETE FROM", "TRUNCATE",
    ]

    @classmethod
    def get_tier(cls, risk_level: RiskLevel) -> tuple[ApprovalTier, int]:
        return cls.TIER_MAP.get(risk_level.value, (ApprovalTier.CHIEF, 3600))

    @classmethod
    def is_dangerous(cls, plan_summary: dict) -> bool:
        ops = plan_summary.get("operations", [])
        for op in ops:
            data_str = json.dumps(op, ensure_ascii=False)
            for pattern in cls.DANGEROUS_PATTERNS:
                if pattern in data_str:
                    return True
        return False


# =============================================================================
# 审批工作流
# =============================================================================

class ApprovalWorkflow:
    """
    CMS 执行审批工作流
    
    核心职责：
    - 接收审批请求
    - 确定审批层级
    - 管理审批状态
    - 超时自动处理
    """

    # 审批存储路径
    STORAGE_DIR = Path("cms_approvals")
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    def __init__(self):
        self._pending: dict[str, ApprovalRequest] = {}
        self._approved: dict[str, ApprovalRequest] = {}
        self._rejected: dict[str, ApprovalRequest] = {}

    async def submit(
        self,
        plan: Any,  # ExecutionPlan
        risk_level: RiskLevel,
        agent_id: str,
    ) -> str:
        """
        提交审批请求
        
        Returns:
            approval_id: 审批单ID
        """
        tier, timeout_sec = ApprovalChain.get_tier(risk_level)

        # 危险操作强制升级
        if ApprovalChain.is_dangerous(plan.to_dict()):
            tier = ApprovalTier.CHIEF
            timeout_sec = 3600

        # AUTO 立即返回已批准
        if tier == ApprovalTier.AUTO:
            approval_id = str(uuid.uuid4())
            logger.info(f"[approval] AUTO approved for plan {plan.plan_id}")
            return approval_id

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=timeout_sec)
        req = ApprovalRequest(
            plan_id=plan.plan_id,
            plan_summary=plan.to_dict(),
            risk_level=risk_level,
            agent_id=agent_id,
            agent_role=getattr(plan, "agent_role", ""),
            tier=tier,
            expires_at=expires_at.isoformat(),
        )
        req.add_history("submit", agent_id, f"Risk: {risk_level.value}, Tier: {tier.value}")
        self._pending[req.approval_id] = req
        self._save_request(req)

        # 触发通知（异步）
        asyncio.create_task(self._notify_approvers(req))
        logger.info(f"[approval] Request {req.approval_id} submitted (tier={tier.value}, expires={req.expires_at})")
        return req.approval_id

    async def approve(self, approval_id: str, reason: str, approver: str) -> bool:
        """批准审批请求"""
        req = self._pending.pop(approval_id, None)
        if not req:
            logger.warning(f"[approval] Approval {approval_id} not found")
            return False
        req.status = ApprovalStatus.APPROVED
        req.approver = approver
        req.reason = reason
        req.updated_at = datetime.now(timezone.utc).isoformat()
        req.add_history("approve", approver, reason)
        self._approved[approval_id] = req
        self._save_request(req)
        logger.info(f"[approval] {approval_id} APPROVED by {approver}: {reason}")
        return True

    async def reject(self, approval_id: str, reason: str, rejector: str) -> bool:
        """拒绝审批请求"""
        req = self._pending.pop(approval_id, None)
        if not req:
            logger.warning(f"[approval] Approval {approval_id} not found")
            return False
        req.status = ApprovalStatus.REJECTED
        req.approver = rejector
        req.reason = reason
        req.updated_at = datetime.now(timezone.utc).isoformat()
        req.add_history("reject", rejector, reason)
        self._rejected[approval_id] = req
        self._save_request(req)
        logger.warning(f"[approval] {approval_id} REJECTED by {rejector}: {reason}")
        return True

    async def escalate(self, approval_id: str, note: str = "") -> bool:
        """升级审批请求（向上级转移）"""
        req = self._pending.get(approval_id)
        if not req:
            return False
        old_tier = req.tier
        # 从 AGENT_SELF 升级到 CHIEF
        if req.tier == ApprovalTier.AGENT_SELF:
            req.tier = ApprovalTier.CHIEF
            req.expires_at = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        elif req.tier == ApprovalTier.CHIEF:
            req.tier = ApprovalTier.HUMAN
            req.expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        req.status = ApprovalStatus.ESCALATED
        req.updated_at = datetime.now(timezone.utc).isoformat()
        req.add_history("escalate", "system", f"Tier: {old_tier.value} -> {req.tier.value}, note: {note}")
        self._save_request(req)
        logger.info(f"[approval] {approval_id} escalated from {old_tier.value} to {req.tier.value}")
        return True

    async def get_status(self, approval_id: str) -> ApprovalStatus:
        """查询审批状态"""
        if approval_id in self._approved:
            return ApprovalStatus.APPROVED
        if approval_id in self._rejected:
            return ApprovalStatus.REJECTED
        req = self._pending.get(approval_id)
        if not req:
            return ApprovalStatus.CANCELLED
        # 检查超时
        if req.expires_at:
            expires = datetime.fromisoformat(req.expires_at.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires:
                req.status = ApprovalStatus.TIMEOUT
                self._pending.pop(approval_id, None)
                self._save_request(req)
                return ApprovalStatus.TIMEOUT
        return ApprovalStatus.PENDING

    async def list_pending(self, agent_role: str = "") -> list[ApprovalRequest]:
        """列出待审批请求（可选按角色过滤）"""
        pending = list(self._pending.values())
        if agent_role:
            pending = [r for r in pending if r.agent_role == agent_role or r.tier.value in agent_role]
        return sorted(pending, key=lambda r: r.created_at)

    async def cancel(self, approval_id: str) -> bool:
        """取消审批请求"""
        req = self._pending.pop(approval_id, None)
        if not req:
            return False
        req.status = ApprovalStatus.CANCELLED
        req.updated_at = datetime.now(timezone.utc).isoformat()
        req.add_history("cancel", "requester")
        self._save_request(req)
        return True

    # ── 内部工具 ──────────────────────────────────────────────────────────

    def _save_request(self, req: ApprovalRequest) -> None:
        """持久化审批请求到文件系统"""
        try:
            path = self.STORAGE_DIR / f"{req.approval_id}.json"
            path.write_text(json.dumps(req.to_dict(), indent=2, ensure_ascii=False))
        except Exception as e:
            logger.warning(f"[approval] Failed to save request {req.approval_id}: {e}")

    async def _notify_approvers(self, req: ApprovalRequest) -> None:
        """异步通知审批人（实际应接入飞书/企微/邮件等）"""
        tier_messages = {
            ApprovalTier.AGENT_SELF: f"[CMS审批] Agent自审: {req.plan_summary.get('title', req.plan_id)} (风险:{req.risk_level.value})",
            ApprovalTier.CHIEF: f"[CMS审批-HIGH] 需要幕僚长审批: {req.plan_summary.get('title', req.plan_id)}",
            ApprovalTier.HUMAN: f"[CMS审批-CRITICAL] 需要人工介入: {req.plan_summary.get('title', req.plan_id)}",
        }
        message = tier_messages.get(req.tier, f"[CMS审批] 新审批请求: {req.plan_id}")
        logger.info(f"[approval] Notify: {message}")
        # TODO: 接入实际的通知渠道（飞书机器人/企业微信/Slack等）
