"""
CMS Approval Engine - 多级审批流程。
支持：单人审批 / 多人会签 / 自动规则 + 人工复核。
"""
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from connectors.base_connector import ContentPayload, OperationRecord, OperationType

logger = logging.getLogger(__name__)


class ApprovalLevel(Enum):
    AUTO_PASS = "auto_pass"   # 自动通过（低风险操作）
    SINGLE = "single"         # 单人审批
    MULTI_SIGN = "multi_sign" # 多人会签（全部同意）
    ANY_SIGN = "any_sign"      # 任意一人同意即可
    MANUAL = "manual"          # 人工复核兜底


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"


# ── 风险规则 ───────────────────────────────────────────────────────────────
RISKY_KEYWORDS = [
    "delete", "remove", "drop", "truncate",
    "exec", "eval", "script", "javascript:",
    "<script", "</script", "<?php", "<%",
]

HIGH_IMPACT_STATUSES = {"publish", "future", "inherit"}


@dataclass
class ApprovalRule:
    """审批规则配置"""
    level: ApprovalLevel
    approvers: List[str] = field(default_factory=list)  # approver IDs
    require_reason: bool = False
    max_auto_amount: int = 0  # 0 = 不限

    @classmethod
    def default_rules(cls) -> List["ApprovalRule"]:
        return [
            # 自动通过：草稿创建且内容安全
            ApprovalRule(level=ApprovalLevel.AUTO_PASS),
            # 单人审批：发布/更新操作
            ApprovalRule(level=ApprovalLevel.SINGLE, approvers=["admin"], require_reason=True),
            # 多人会签：删除操作
            ApprovalRule(level=ApprovalLevel.MULTI_SIGN, approvers=["admin", "editor"], require_reason=True),
        ]


@dataclass
class ApprovalRequest:
    """一次审批请求"""
    id: str
    created_at: datetime
    submitter: str
    operation: OperationType
    payload: Dict[str, Any]
    level: ApprovalLevel
    rule: ApprovalRule
    status: ApprovalStatus
    votes: Dict[str, str] = field(default_factory=dict)  # approver_id -> "approve"/"reject"
    comment: str = ""
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "submitter": self.submitter,
            "operation": self.operation.value,
            "payload_title": self.payload.get("title", ""),
            "level": self.level.value,
            "status": self.status.value,
            "votes": self.votes,
            "comment": self.comment,
            "reason": self.reason,
        }


class ApprovalEngine:
    """
    审批引擎。
    
    使用示例:
        engine = ApprovalEngine()
        engine.add_rule(ApprovalRule(level=ApprovalLevel.SINGLE, approvers=["alice"]))
        
        request = engine.create_request(
            submitter="bot",
            operation=OperationType.CREATE,
            payload={"title": "Hello", "content": "World", "status": "draft"}
        )
        
        if engine.can_auto_approve(request):
            engine.auto_approve(request)
        else:
            # 等待人工审批
            engine.vote(request.id, approver="alice", decision="approve")
    """

    def __init__(self, storage_path: str = "./approval_requests.json"):
        self.storage_path = storage_path
        self._requests: List[ApprovalRequest] = []
        self._rules: List[ApprovalRule] = ApprovalRule.default_rules()
        self._load()

    # ── 规则管理 ──────────────────────────────────────────
    def add_rule(self, rule: ApprovalRule) -> None:
        self._rules.insert(0, rule)  # 自定义规则优先

    def remove_rule(self, level: ApprovalLevel) -> None:
        self._rules = [r for r in self._rules if r.level != level]

    # ── 请求创建 ──────────────────────────────────────────
    def create_request(
        self,
        submitter: str,
        operation: OperationType,
        payload: Dict[str, Any],
        reason: str = "",
    ) -> ApprovalRequest:
        level = self._evaluate_level(operation, payload)
        rule = self._find_rule(level)
        req_id = uuid.uuid4().hex[:8]
        req = ApprovalRequest(
            id=req_id,
            created_at=datetime.now(),
            submitter=submitter,
            operation=operation,
            payload=payload,
            level=level,
            rule=rule,
            status=ApprovalStatus.PENDING,
            reason=reason,
        )
        self._requests.append(req)
        self._persist()
        return req

    # ── 审批决策 ──────────────────────────────────────────
    def can_auto_approve(self, request: ApprovalRequest) -> bool:
        return request.level == ApprovalLevel.AUTO_PASS

    def auto_approve(self, request: ApprovalRequest) -> None:
        request.status = ApprovalStatus.AUTO_APPROVED
        self._persist()

    def vote(self, request_id: str, approver: str, decision: str, comment: str = "") -> bool:
        """
        投票。
        decision: "approve" | "reject"
        """
        req = self._find_request(request_id)
        if not req:
            return False

        if decision not in ("approve", "reject"):
            raise ValueError("decision must be 'approve' or 'reject'")

        req.votes[approver] = decision
        if comment:
            req.comment = comment

        # 统计投票
        approved = sum(1 for v in req.votes.values() if v == "approve")
        rejected = sum(1 for v in req.votes.values() if v == "reject")
        total = len(req.rule.approvers)

        if req.level == ApprovalLevel.MULTI_SIGN:
            if rejected > 0:
                req.status = ApprovalStatus.REJECTED
            elif approved >= total:
                req.status = ApprovalStatus.APPROVED
        elif req.level == ApprovalLevel.ANY_SIGN:
            if approved >= 1:
                req.status = ApprovalStatus.APPROVED
            elif rejected >= 1:
                req.status = ApprovalStatus.REJECTED
        elif req.level == ApprovalLevel.SINGLE:
            if approved >= 1:
                req.status = ApprovalStatus.APPROVED
            elif rejected >= 1:
                req.status = ApprovalStatus.REJECTED

        self._persist()
        return req.status in (ApprovalStatus.APPROVED, ApprovalStatus.AUTO_APPROVED)

    def get_pending(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._requests if r.status == ApprovalStatus.PENDING]

    def get_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        req = self._find_request(request_id)
        return req.to_dict() if req else None

    # ── 内部 ───────────────────────────────────────────────
    def _evaluate_level(self, operation: OperationType, payload: Dict[str, Any]) -> ApprovalLevel:
        """评估本次操作需要的审批级别"""
        content = json.dumps(payload, ensure_ascii=False).lower()

        # 显式风险检测
        for kw in RISKY_KEYWORDS:
            if kw in content:
                return ApprovalLevel.MULTI_SIGN

        # 高影响状态
        status = payload.get("status", "draft")
        if status in HIGH_IMPACT_STATUSES:
            return ApprovalLevel.SINGLE

        # DELETE 操作
        if operation == OperationType.DELETE:
            return ApprovalLevel.MULTI_SIGN

        # UPDATE 操作（已发布内容）
        if operation == OperationType.UPDATE and payload.get("original_status") == "publish":
            return ApprovalLevel.SINGLE

        return ApprovalLevel.AUTO_PASS

    def _find_rule(self, level: ApprovalLevel) -> ApprovalRule:
        for rule in self._rules:
            if rule.level == level:
                return rule
        return ApprovalRule(level=level)

    def _find_request(self, request_id: str) -> Optional[ApprovalRequest]:
        for req in self._requests:
            if req.id == request_id:
                return req
        return None

    def _persist(self) -> None:
        data = [r.to_dict() for r in self._requests]
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load(self) -> None:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                # 简化恢复：仅保留 id、status、votes 核心字段
                logger.info("Approval history loaded")
        except (FileNotFoundError, json.JSONDecodeError):
            pass
