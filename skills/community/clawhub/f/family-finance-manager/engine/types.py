"""Family Finance Manager - Type Definitions"""

from typing import Optional, List, Literal

# 操作类型
ActionType = Literal["analyze", "goal-plan", "insurance", "risk-warning", "health-report"]

# 收入稳定性
IncomeStability = Literal["high", "medium", "low"]

# 风险偏好
RiskProfile = Literal["conservative", "moderate", "aggressive"]

# 财务等级
ScoreGrade = Literal["excellent", "good", "fair", "poor"]

# 风险级别
RiskLevel = Literal["low", "medium", "high", "critical"]


class FamilyMember:
    def __init__(self, name: str, age: int, role: str, income: float = 0):
        self.name = name
        self.age = age
        self.role = role  # "self", "spouse", "child", "parent"
        self.income = income


class FinancialGoal:
    def __init__(self, name: str, amount: float, years: int, priority: str = "medium"):
        self.name = name
        self.amount = amount
        self.years = years
        self.priority = priority  # "high", "medium", "low"


class FamilyFinanceRequest:
    def __init__(self, data: dict):
        self.action = data.get("action", "analyze")
        self.family = data.get("family", {})
        self.assets = data.get("assets", {})
        self.liabilities = data.get("liabilities", {})
        self.monthly_expenses = data.get("monthlyExpenses", {})
        self.goals = data.get("goals", [])
        self.insurance = data.get("insurance", {})
        self.risk_profile = data.get("riskProfile", "moderate")

        # Parse family members
        self.members = [
            FamilyMember(
                name=m.get("name", ""),
                age=m.get("age", 0),
                role=m.get("role", "self"),
                income=m.get("income", 0)
            )
            for m in self.family.get("members", [])
        ]

        # Parse financial goals
        self.goals = [
            FinancialGoal(
                name=g.get("name", ""),
                amount=g.get("amount", 0),
                years=g.get("years", 1),
                priority=g.get("priority", "medium")
            )
            for g in data.get("goals", [])
        ]

    @property
    def monthly_income(self) -> float:
        return self.family.get("monthlyIncome", 0)

    @property
    def income_stability(self) -> IncomeStability:
        return self.family.get("incomeStability", "medium")

    def get_total_assets(self) -> float:
        return (
            self.assets.get("liquid", 0) +
            self.assets.get("investments", 0) +
            self.assets.get("property", 0) +
            self.assets.get("other", 0)
        )

    def get_total_liabilities(self) -> float:
        return (
            self.liabilities.get("mortgage", 0) +
            self.liabilities.get("loans", 0) +
            self.liabilities.get("creditCards", 0)
        )

    def get_total_monthly_expenses(self) -> float:
        return sum(self.monthly_expenses.values())

    def get_net_worth(self) -> float:
        return self.get_total_assets() - self.get_total_liabilities()


class FinancialAnalysisReport:
    def __init__(self):
        self.income_expense = {}
        self.net_worth = {}
        self.ratios = {}
        self.suggestions = []

    def to_dict(self) -> dict:
        return {
            "incomeExpense": self.income_expense,
            "netWorth": self.net_worth,
            "ratios": self.ratios,
            "suggestions": self.suggestions
        }


class SavingsGoalPlan:
    def __init__(self, goal: FinancialGoal):
        self.goal = goal
        self.monthly_required = 0.0
        self.yearly_required = 0.0
        self.current_progress = 0.0
        self.completion_percentage = 0.0
        self.milestones = []
        self.investment_advice = []
        self.risk_assessment = ""

    def to_dict(self) -> dict:
        return {
            "goal": {
                "name": self.goal.name,
                "amount": self.goal.amount,
                "years": self.goal.years,
                "priority": self.goal.priority
            },
            "monthlyRequired": self.monthly_required,
            "yearlyRequired": self.yearly_required,
            "currentProgress": self.current_progress,
            "completionPercentage": self.completion_percentage,
            "milestones": self.milestones,
            "investmentAdvice": self.investment_advice,
            "riskAssessment": self.risk_assessment
        }


class InsuranceRecommendation:
    def __init__(self):
        self.coverage_gaps = {"life": 0, "health": 0, "disability": 0, "criticalIllness": 0}
        self.recommendations = []
        self.total_recommended_coverage = 0
        self.budget_considerations = []

    def to_dict(self) -> dict:
        return {
            "coverageGaps": self.coverage_gaps,
            "recommendations": self.recommendations,
            "totalRecommendedCoverage": self.total_recommended_coverage,
            "budgetConsiderations": self.budget_considerations
        }


class RiskWarningReport:
    def __init__(self):
        self.overall_risk_level: RiskLevel = "low"
        self.risk_factors = []
        self.immediate_actions = []
        self.warning_signs = []

    def to_dict(self) -> dict:
        return {
            "overallRiskLevel": self.overall_risk_level,
            "riskFactors": self.risk_factors,
            "immediateActions": self.immediate_actions,
            "warningSigns": self.warning_signs
        }


class FinancialHealthReport:
    def __init__(self):
        self.overall_score = 0
        self.score_grade: ScoreGrade = "fair"
        self.dimensions = {
            "budgeting": 0,
            "saving": 0,
            "investing": 0,
            "debt": 0,
            "protection": 0,
            "planning": 0
        }
        self.summary = ""
        self.top_strengths = []
        self.top_concerns = []
        self.action_plan = []

    def to_dict(self) -> dict:
        return {
            "overallScore": self.overall_score,
            "scoreGrade": self.score_grade,
            "dimensions": self.dimensions,
            "summary": self.summary,
            "topStrengths": self.top_strengths,
            "topConcerns": self.top_concerns,
            "actionPlan": self.action_plan
        }
