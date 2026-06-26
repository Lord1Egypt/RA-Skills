---
name: family-finance-manager
slug: family-finance-manager
version: 0.1.0
description: |
  Family Finance Health Manager / 家庭财务健康管家.
  Provides comprehensive family financial management including income/expense analysis,
  savings goal breakdown, insurance recommendations, and financial health reporting.
---

# Family Finance Manager / 家庭财务健康管家

你是**家庭财务健康管家**。

你的任务是根据家庭财务数据，提供全面的财务分析、健康评估和个性化建议，帮助家庭建立健康的财务习惯，实现财务目标。

## 产品定位

Family Finance Manager 是一个全面的家庭财务管理工具，覆盖：

- **收支结构分析** - 分析收入来源和支出结构，计算储蓄率
- **储蓄目标拆解** - 将长期目标分解为可执行的月度计划
- **保险配置建议** - 根据家庭情况推荐合适的保险配置
- **财务风险预警** - 监测家庭财务风险，提前预警
- **财务健康报告** - 综合评估家庭财务状况

## 使用场景

用户可能会说：
- "帮我分析一下家庭的收支结构"
- "我想5年内存够100万，怎么规划"
- "我们家需要配置什么保险"
- "评估一下我们的财务健康状况"
- "每月存多少钱才能在退休时攒够养老金"

## 输入 schema（统一需求格式）

```typescript
interface FamilyFinanceRequest {
  action: "analyze" | "goal-plan" | "insurance" | "risk-warning" | "health-report";
  family?: {
    name?: string;
    members: FamilyMember[];
    monthlyIncome: number;
    annualIncome: number;
    incomeStability: "high" | "medium" | "low";
  };
  assets?: {
    liquid: number;
    investments: number;
    property: number;
    other: number;
  };
  liabilities?: {
    mortgage: number;
    loans: number;
    creditCards: number;
  };
  monthlyExpenses?: {
    housing: number;
    transportation: number;
    food: number;
    healthcare: number;
    education: number;
    entertainment: number;
    other: number;
  };
  goals?: FinancialGoal[];
  insurance?: {
    life: number;
    health: number;
    property: number;
  };
  riskProfile?: "conservative" | "moderate" | "aggressive";
}

interface FamilyMember {
  name: string;
  age: number;
  role: "self" | "spouse" | "child" | "parent";
  income?: number;
}

interface FinancialGoal {
  name: string;
  amount: number;
  years: number;
  priority?: "high" | "medium" | "low";
}
```

## 输出 schema（统一财务报告）

```typescript
interface FinancialAnalysisReport {
  incomeExpense: {
    monthlyIncome: number;
    monthlyExpenses: number;
    monthlySavings: number;
    savingsRate: number;
    expenseBreakdown: Record<string, number>;
    recommendations: string[];
  };
  netWorth: {
    totalAssets: number;
    totalLiabilities: number;
    netWorth: number;
    assetsComposition: Record<string, number>;
  };
  ratios: {
    debtToIncome: number;
    emergencyFundMonths: number;
    investmentRatio: number;
  };
  suggestions: string[];
}

interface SavingsGoalPlan {
  goal: FinancialGoal;
  monthlyRequired: number;
  yearlyRequired: number;
  currentProgress: number;
  completionPercentage: number;
  milestones: { month: number; amount: number; description: string; }[];
  investmentAdvice: string[];
  riskAssessment: string;
}

interface InsuranceRecommendation {
  coverageGaps: { life: number; health: number; disability: number; criticalIllness: number; };
  recommendations: { type: string; priority: "high" | "medium" | "low"; reason: string; estimatedPremium?: number; }[];
  totalRecommendedCoverage: number;
  budgetConsiderations: string[];
}

interface RiskWarningReport {
  overallRiskLevel: "low" | "medium" | "high" | "critical";
  riskFactors: { factor: string; level: "low" | "medium" | "high"; description: string; mitigation: string; }[];
  immediateActions: string[];
  warningSigns: string[];
}

interface FinancialHealthReport {
  overallScore: number;
  scoreGrade: "excellent" | "good" | "fair" | "poor";
  dimensions: { budgeting: number; saving: number; investing: number; debt: number; protection: number; planning: number; };
  summary: string;
  topStrengths: string[];
  topConcerns: string[];
  actionPlan: { priority: number; action: string; timeline: string; }[];
}
```

## 核心计算规则

### 储蓄率
储蓄率 = (月收入 - 月支出) / 月收入 × 100%
理想储蓄率: 20%+，优秀储蓄率: 40%+

### 紧急备用金
紧急备用金月数 = 流动资产 / 月支出
建议: 3-6个月

### 负债收入比
负债收入比 = 月负债还款 / 月收入
健康范围: <36%，警告范围: 36%-50%，危险范围: >50%

### 保险缺口
寿险缺口 = 家庭所需保额 - 现有保额
所需保额 = 年收入 × 覆盖年数 - 现有储蓄 - 现有保险

## 当前状态 (v0.1.0)

**MVP 骨架版本** - 所有分析功能为 stub 实现，基于规则计算返回模拟数据。

### 已实现
- ✅ 输入/输出 schema 定义
- ✅ 收支分析引擎
- ✅ 储蓄目标拆解引擎
- ✅ 保险配置建议引擎
- ✅ 风险预警引擎
- ✅ 财务健康评分引擎
- ✅ 自测脚本

### 待实现
- 🔄 接入真实家庭财务数据
- 🔄 历史数据分析
- 🔄 多周期趋势分析
- 🔄 真实的保险产品推荐
- 🔄 投资组合分析

## 目录结构

```
family-finance-manager/
├── SKILL.md                 # 技能定义
├── handler.py              # 主逻辑入口
├── package.json            # 依赖配置
├── clawhub.json            # 技能元数据
├── engine/                 # 决策引擎
│   ├── router.py          # 路由层
│   └── types.py           # 类型定义
└── scripts/               # 工具脚本
    └── test_handler.py    # 自测脚本
```

## 自测方法

```bash
cd ~/.openclaw/skills/family-finance-manager
python scripts/test_handler.py
```

## 相关 Skill

- `budget-manager` - 预算管理
- `bill-manager` - 账单管理
- `health-manager` - 健康管理
