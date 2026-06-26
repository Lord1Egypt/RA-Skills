"""
Finance Agent - 财务智能体

专注领域：预算查询、付款审核、财务报表、费用分析

角色定位：专业智能体，处理企业财务相关业务，
涉及高风险操作（付款/报销/预算调整均需审批）
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

from safety.audit_logger import AuditLogger, EventType, LogLevel, traced
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult
from safety.human_loop import HumanInTheLoop, RiskLevel, ApprovalChannel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class BudgetStatus(Enum):
    """预算状态"""
    NORMAL = "normal"
    WARNING = "warning"     # 使用率>70%
    CRITICAL = "critical"   # 使用率>90%
    OVERDRAWN = "overdrawn"  # 超支


class ApprovalDecision(Enum):
    """审批决策"""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEED_DOCUMENT = "need_document"  # 需补充材料
    ESCALATE = "escalate"            # 升级处理


@dataclass
class BudgetInfo:
    """预算信息"""
    department: str
    fiscal_year: int
    total_budget: float
    allocated: float
    spent: float
    committed: float  # 已承诺支出
    available: float
    utilization_rate: float
    status: str
    categories: dict[str, float]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PaymentApproval:
    """付款审批"""
    payment_id: str
    payee: str
    amount: float
    category: str
    purpose: str
    supporting_docs: list[str]
    risk_score: float
    decision: str
    approved_by: Optional[str] = None
    comments: str = ""
    conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FinancialReport:
    """财务报表"""
    report_type: str
    period: str
    generated_at: str
    summary: dict[str, Any]
    details: list[dict]
    comparisons: dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# 财务服务（模拟）
# =============================================================================

class FinanceAPIService:
    """财务API封装（模拟企业财务系统）"""

    DEPARTMENTS = {
        "研发部": {
            "total_budget": 5000000,
            "categories": {
                "设备采购": 2000000,
                "人员成本": 1500000,
                "研发材料": 1000000,
                "外包服务": 500000,
            },
        },
        "生产部": {
            "total_budget": 8000000,
            "categories": {
                "原材料": 4000000,
                "设备维护": 1500000,
                "人工成本": 2000000,
                "能源费用": 500000,
            },
        },
        "销售部": {
            "total_budget": 3000000,
            "categories": {
                "市场推广": 1500000,
                "差旅费用": 500000,
                "客户招待": 500000,
                "展会费用": 500000,
            },
        },
        "采购部": {
            "total_budget": 6000000,
            "categories": {
                "原材料采购": 4000000,
                "设备采购": 1500000,
                "服务采购": 500000,
            },
        },
    }

    async def get_budget(
        self,
        department: str,
        fiscal_year: Optional[int] = None,
    ) -> dict[str, Any]:
        """查询预算"""
        await asyncio.sleep(0.08)

        if fiscal_year is None:
            fiscal_year = datetime.now().year

        dept_data = self.DEPARTMENTS.get(department)
        if not dept_data:
            return {"success": False, "error": f"部门不存在: {department}"}

        total = dept_data["total_budget"]
        # 模拟实际支出（按时间进度）
        month_progress = datetime.now().month / 12
        spent = total * month_progress * 0.85  # 85%执行率
        allocated = total * month_progress
        committed = allocated * 0.9

        return {
            "success": True,
            "data": {
                "department": department,
                "fiscal_year": fiscal_year,
                "total_budget": total,
                "allocated": round(allocated, 2),
                "spent": round(spent, 2),
                "committed": round(committed, 2),
                "available": round(total - committed, 2),
                "utilization_rate": round(spent / total * 100, 2),
                "status": self._get_budget_status(spent, total),
                "categories": dept_data["categories"],
                "as_of": datetime.now().isoformat(),
            }
        }

    async def audit_payment(
        self,
        payment_id: str,
        amount: float,
        category: str,
        payee: str,
        supporting_docs: list[str],
    ) -> dict[str, Any]:
        """付款审核"""
        await asyncio.sleep(0.12)

        # 风险评分
        risk_score = self._calc_payment_risk(amount, category, payee)

        # 自动审核规则
        rules = []
        decision = "approved"
        comments = []
        conditions = []

        if amount > 50000:
            rules.append("金额>5万，需人工复核")
            decision = "need_review"
        if amount > 100000:
            rules.append("金额>10万，需CFO审批")
            decision = "escalate"

        # 供应商白名单
        white_list = ["华东轴承", "宝钢", "壳牌", "西门子"]
        if not any(w in payee for w in white_list):
            rules.append("⚠️ 非常规供应商，请确认")
            decision = "need_review"
            risk_score += 0.2

        # 发票验证
        if len(supporting_docs) == 0:
            rules.append("⚠️ 无附件发票，不合规")
            decision = "need_document"

        return {
            "success": True,
            "data": {
                "payment_id": payment_id,
                "payee": payee,
                "amount": amount,
                "category": category,
                "decision": decision,
                "risk_score": min(risk_score, 1.0),
                "audit_rules": rules,
                "comments": comments,
                "conditions": conditions,
                "approved_by": "system_auto" if decision == "approved" else None,
                "audited_at": datetime.now().isoformat(),
            }
        }

    async def get_expense_report(
        self,
        department: str,
        period: str = "month",
    ) -> dict[str, Any]:
        """费用报表"""
        await asyncio.sleep(0.1)

        dept_data = self.DEPARTMENTS.get(department, self.DEPARTMENTS["生产部"])

        # 模拟费用明细
        details = []
        for cat, budget in dept_data["categories"].items():
            actual = budget * (0.75 + 0.15 * (datetime.now().month % 12) / 12)
            details.append({
                "category": cat,
                "budget": budget,
                "actual": round(actual, 2),
                "variance": round(budget - actual, 2),
                "variance_rate": round((budget - actual) / budget * 100, 2),
                "headcount": 10,
                "cost_per_person": round(actual / 10, 2),
            })

        return {
            "success": True,
            "data": {
                "department": department,
                "period": period,
                "total_budget": dept_data["total_budget"],
                "total_actual": round(sum(d["actual"] for d in details), 2),
                "total_variance": round(sum(d["variance"] for d in details), 2),
                "details": details,
                "top_variance": max(details, key=lambda x: abs(x["variance"]))["category"]
                    if details else None,
                "generated_at": datetime.now().isoformat(),
            }
        }

    @staticmethod
    def _get_budget_status(spent: float, total: float) -> str:
        rate = spent / total
        if rate > 0.9:
            return "critical"
        elif rate > 0.7:
            return "warning"
        return "normal"

    @staticmethod
    def _calc_payment_risk(amount: float, category: str, payee: str) -> float:
        score = 0.0
        if amount > 50000:
            score += 0.3
        if amount > 100000:
            score += 0.3
        if category in ["招待费", "差旅费"]:
            score += 0.1
        if len(payee) < 4:
            score += 0.2
        return min(score, 1.0)


# =============================================================================
# 财务智能体
# =============================================================================

class FinanceAgent:
    """
    财务智能体

    核心能力：
    1. 预算查询与分析
    2. 付款审核（自动化规则引擎）
    3. 财务报表生成
    4. 费用分析
    5. 成本优化建议

    安全规范：
    - 所有财务操作强制审计
    - 大额付款（>1万）需人工审批
    - 预算调整必须经过审批流程
    """

    def __init__(
        self,
        agent_id: str = "finance_agent",
        user_id: str = "system",
        user_role: str = "finance_manager",
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.user_role = user_role

        self._api = FinanceAPIService()
        self._audit = AuditLogger(log_dir=f"./logs/{agent_id}")
        self._permission = PermissionManager()
        self._hitl = HumanInTheLoop(default_channel=ApprovalChannel.CONSOLE)

        self.capabilities = [
            "query_budget",
            "audit_payment",
            "financial_reporting",
            "expense_analysis",
            "cost_optimization",
        ]

        logger.info(f"财务智能体初始化: {agent_id}, role={user_role}")

    @traced(agent_name="finance_agent", action="query_budget")
    async def query_budget(
        self,
        department: str,
        fiscal_year: Optional[int] = None,
        include_categories: bool = True,
    ) -> BudgetInfo:
        """查询预算"""
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="query_budget",
            parameters={"department": department, "fiscal_year": fiscal_year},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return BudgetInfo(
                department=department,
                fiscal_year=fiscal_year or datetime.now().year,
                total_budget=0,
                allocated=0,
                spent=0,
                committed=0,
                available=0,
                utilization_rate=0,
                status="permission_denied",
                categories={},
            )

        result = await self._api.get_budget(department, fiscal_year)

        if not result["success"]:
            return BudgetInfo(
                department=department,
                fiscal_year=fiscal_year or datetime.now().year,
                total_budget=0,
                allocated=0,
                spent=0,
                committed=0,
                available=0,
                utilization_rate=0,
                status="error",
                categories={},
            )

        data = result["data"]
        return BudgetInfo(
            department=data["department"],
            fiscal_year=data["fiscal_year"],
            total_budget=data["total_budget"],
            allocated=data["allocated"],
            spent=data["spent"],
            committed=data["committed"],
            available=data["available"],
            utilization_rate=data["utilization_rate"],
            status=data["status"],
            categories=data.get("categories", {}) if include_categories else {},
        )

    @traced(agent_name="finance_agent", action="audit_payment")
    async def audit_payment(
        self,
        payment_id: str,
        amount: float,
        category: str,
        payee: str,
        supporting_docs: list[str] = None,
        auto_decision: bool = False,
    ) -> dict[str, Any]:
        """
        审核付款

        Args:
            payment_id: 付款单号
            amount: 付款金额
            category: 费用类别
            payee: 收款方
            supporting_docs: 附件清单
            auto_decision: 是否自动决策（仅低风险）

        Returns:
            审核结果
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="audit_payment",
            parameters={"payment_id": payment_id, "amount": amount, "payee": payee},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason}

        supporting_docs = supporting_docs or []

        # 调用财务API
        result = await self._api.audit_payment(
            payment_id=payment_id,
            amount=amount,
            category=category,
            payee=payee,
            supporting_docs=supporting_docs,
        )

        if not result["success"]:
            return result

        audit = result["data"]

        # 需要人工审批的情况
        if audit["decision"] in ("need_review", "escalate", "need_document"):
            hitl_result = await self._hitl.request_approval(
                agent_name=self.agent_id,
                action="audit_payment",
                parameters={
                    "payment_id": payment_id,
                    "amount": amount,
                    "payee": payee,
                    "category": category,
                },
                requested_by=self.user_id,
                description=f"付款审核: {payee} ¥{amount}",
            )

            audit["decision"] = "approved" if hitl_result.approved else "rejected"
            audit["approved_by"] = hitl_result.approved_by
            audit["comments"] = hitl_result.comments
            audit["human_approved"] = True
        else:
            audit["human_approved"] = False

        # 审计日志
        await self._audit.log(
            event_type=EventType.HUMAN_APPROVAL if audit.get("human_approved") else EventType.AGENT_CALL,
            action="audit_payment",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            actor_role=self.user_role,
            input_data={
                "payment_id": payment_id,
                "amount": amount,
                "category": category,
                "payee": payee,
            },
            output_data=audit,
            level=LogLevel.WARNING if amount > 10000 else LogLevel.INFO,
            risk_score=audit["risk_score"],
        )

        return {
            **result,
            "data": {
                **audit,
                "alerts": self._generate_payment_alerts(audit),
                "summary": self._summarize_audit(audit),
            }
        }

    @traced(agent_name="finance_agent", action="financial_reporting")
    async def financial_reporting(
        self,
        department: str,
        report_type: str = "expense",
        period: str = "month",
    ) -> FinancialReport:
        """生成财务报表"""
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="financial_reporting",
            parameters={"department": department, "report_type": report_type},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return FinancialReport(
                report_type=report_type,
                period=period,
                generated_at=datetime.now().isoformat(),
                summary={"error": decision.reason},
                details=[],
                comparisons={},
            )

        if report_type == "expense":
            result = await self._api.get_expense_report(department, period)
        else:
            result = await self._api.get_budget(department)

        budget_info = await self.query_budget(department)

        return FinancialReport(
            report_type=report_type,
            period=period,
            generated_at=datetime.now().isoformat(),
            summary={
                "department": department,
                "total_budget": budget_info.total_budget,
                "total_spent": budget_info.spent,
                "utilization": budget_info.utilization_rate,
                "status": budget_info.status,
            },
            details=result.get("data", {}).get("details", []) if result.get("success") else [],
            comparisons={
                "vs_budget": {
                    "variance": budget_info.total_budget - budget_info.spent,
                    "variance_rate": round(
                        (budget_info.total_budget - budget_info.spent) / budget_info.total_budget * 100, 2
                    ),
                }
            },
        )

    def _generate_payment_alerts(self, audit: dict) -> list[str]:
        alerts = []
        if audit["risk_score"] > 0.5:
            alerts.append(f"⚠️ 中高风险付款（评分{audit['risk_score']:.2f}），已人工审批")
        for rule in audit.get("audit_rules", []):
            if rule.startswith("⚠️"):
                alerts.append(rule)
        return alerts

    def _summarize_audit(self, audit: dict) -> dict[str, Any]:
        return {
            "verdict": "通过" if audit["decision"] == "approved" else "拒绝",
            "risk_level": "高" if audit["risk_score"] > 0.5 else "中" if audit["risk_score"] > 0.3 else "低",
            "action_required": "人工审批" if audit.get("human_approved") else "自动通过",
        }


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def demo():
        print("=" * 60)
        print("  财务智能体演示")
        print("=" * 60)

        agent = FinanceAgent(user_role="finance_manager")

        # 预算查询
        print("\n[1] 查询研发部预算")
        budget = await agent.query_budget(department="研发部")
        print(f"  年度预算: ¥{budget.total_budget:,.0f}")
        print(f"  已支出: ¥{budget.spent:,.0f}")
        print(f"  可用: ¥{budget.available:,.0f}")
        print(f"  执行率: {budget.utilization_rate}%")
        print(f"  状态: {budget.status}")

        # 付款审核
        print("\n[2] 审核付款申请（¥8000，小额）")
        result = await agent.audit_payment(
            payment_id="PAY20240415001",
            amount=8000,
            category="原材料",
            payee="华东轴承有限公司",
            supporting_docs=["invoice_001.pdf", "po_approved.pdf"],
        )
        audit = result["data"]
        print(f"  决策: {audit['decision']}")
        print(f"  风险评分: {audit['risk_score']:.2f}")
        print(f"  审核规则: {audit['audit_rules']}")
        print(f"  告警: {result['data']['alerts']}")

        # 财务报表
        print("\n[3] 生成费用报表")
        report = await agent.financial_reporting(department="生产部", period="month")
        print(f"  部门: {report.summary['department']}")
        print(f"  预算: ¥{report.summary['total_budget']:,.0f}")
        print(f"  执行率: {report.summary['utilization']}%")
        for item in report.details[:3]:
            print(f"    {item['category']}: ¥{item['actual']:,.0f} "
                  f"(预算¥{item['budget']:,.0f}, 差异¥{item['variance']:,.0f})")

    asyncio.run(demo())
