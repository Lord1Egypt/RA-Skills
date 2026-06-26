#!/usr/bin/env python3
"""
中国个人所得税计算器 - 2025年版
支持月度工资、年终奖、专项附加扣除、年度汇算清缴、多收入来源计算
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

# ==================== 税率表 ====================

# 综合所得月度税率表（累计预扣法）
MONTHLY_TAX_BRACKETS = [
    (3000, 0.03, 0),
    (12000, 0.10, 210),
    (25000, 0.20, 1410),
    (35000, 0.25, 2660),
    (55000, 0.30, 4410),
    (80000, 0.35, 7160),
    (float('inf'), 0.45, 15160),
]

# 综合所得年度税率表（汇算清缴用）
ANNUAL_TAX_BRACKETS = [
    (36000, 0.03, 0),
    (144000, 0.10, 2520),
    (300000, 0.20, 16920),
    (420000, 0.25, 31920),
    (660000, 0.30, 52920),
    (960000, 0.35, 85920),
    (float('inf'), 0.45, 181920),
]

# 年终奖税率表（按月均额）
BONUS_TAX_BRACKETS = [
    (3000, 0.03, 0),
    (12000, 0.10, 210),
    (25000, 0.20, 1410),
    (35000, 0.25, 2660),
    (55000, 0.30, 4410),
    (80000, 0.35, 7160),
    (float('inf'), 0.45, 15160),
]

# 起征点
THRESHOLD = 5000
ANNUAL_THRESHOLD = 60000


# ==================== 数据类 ====================

@dataclass
class SpecialDeduction:
    """专项附加扣除"""
    children_education: int = 0      # 子女教育（2000元/孩/月）
    infant_care: int = 0             # 3岁以下婴幼儿照护（2000元/孩/月）
    continuing_education: int = 0    # 继续教育（400元/月）
    serious_illness: int = 0         # 大病医疗（年度，最高80000）
    housing_loan: int = 0            # 住房贷款利息（1000元/月）
    housing_rent: int = 0            # 住房租金（800-1500元/月）
    elderly_support: int = 0         # 赡养老人（独生3000，非独生最高1500）

    @property
    def total_monthly(self) -> int:
        """月度专项附加扣除总额"""
        return (
            self.children_education +
            self.infant_care +
            self.continuing_education +
            self.housing_loan +
            self.housing_rent +
            self.elderly_support
        )


@dataclass
class MonthlyTaxResult:
    """月度个税计算结果"""
    month: int
    gross_income: float              # 税前收入
    social_insurance: float          # 五险一金
    special_deduction: float         # 专项附加扣除
    taxable_income: float            # 应纳税所得额
    tax_rate: float                  # 税率
    quick_deduction: float           # 速算扣除数
    monthly_tax: float               # 本月应纳税额
    cumulative_tax: float            # 累计应纳税额
    net_income: float                # 税后收入


@dataclass
class BonusTaxResult:
    """年终奖计税结果"""
    bonus: float                     # 年终奖金额
    method: str                      # 计税方式：separate/combined
    monthly_average: float           # 月均额（单独计税）
    tax_rate: float                  # 税率
    quick_deduction: float           # 速算扣除数
    tax: float                       # 应纳税额
    net_bonus: float                 # 税后年终奖


@dataclass
class IncomeSource:
    """多收入来源"""
    salary: float = 0                # 工资薪金（年度总额）
    labor_income: float = 0          # 劳务报酬（年度总额，扣除20%费用）
    royalty_income: float = 0        # 稿酬（年度总额，扣除20%费用后减按70%）
    franchise_income: float = 0      # 特许权使用费（年度总额，扣除20%费用）
    
    @property
    def total_comprehensive_income(self) -> float:
        """
        计算综合所得总额
        - 工资薪金：全额计入
        - 劳务报酬：收入 × (1 - 20%)
        - 稿酬：收入 × (1 - 20%) × 70%
        - 特许权使用费：收入 × (1 - 20%)
        """
        return (
            self.salary +
            self.labor_income * 0.8 +
            self.royalty_income * 0.8 * 0.7 +
            self.franchise_income * 0.8
        )


@dataclass
class AnnualSettlementResult:
    """年度汇算清缴结果"""
    comprehensive_income: float      # 综合所得总额
    deductions: float                # 各项扣除总额
    taxable_income: float            # 应纳税所得额
    tax_rate: float                  # 税率
    quick_deduction: float           # 速算扣除数
    annual_tax: float                # 年度应纳税额
    prepaid_tax: float               # 已预缴税额
    settlement_amount: float         # 汇算金额（正数=应补缴，负数=应退税）
    
    @property
    def is_refund(self) -> bool:
        """是否退税"""
        return self.settlement_amount < 0
    
    @property
    def status_text(self) -> str:
        """状态文本"""
        if self.settlement_amount > 0:
            return f"应补缴 ¥{self.settlement_amount:,.2f}"
        elif self.settlement_amount < 0:
            return f"应退税 ¥{abs(self.settlement_amount):,.2f}"
        else:
            return "无需补退"


@dataclass
class BonusOptimizationResult:
    """年终奖优化结果"""
    total_bonus: float               # 年终奖总额
    optimal_split: List[Dict]        # 最优分配方案
    total_tax: float                 # 最优方案总税额
    worst_tax: float                 # 最差方案总税额
    savings: float                   # 节省税额


# ==================== 计算函数 ====================

def get_tax_info(taxable: float, brackets: list) -> tuple:
    """根据应纳税所得额获取税率和速算扣除数"""
    for upper, rate, quick_ded in brackets:
        if taxable <= upper:
            return rate, quick_ded
    return 0.45, 15160


def calculate_monthly_tax(
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    month: int = 1,
    cumulative_income: float = 0,
    cumulative_social: float = 0,
    cumulative_deduction: float = 0,
    cumulative_tax_paid: float = 0,
) -> MonthlyTaxResult:
    """
    计算月度个税（累计预扣法）

    Args:
        monthly_salary: 月税前工资
        social_insurance: 月五险一金（个人部分）
        special_deduction: 专项附加扣除
        month: 当前月份（1-12）
        cumulative_income: 累计收入
        cumulative_social: 累计五险一金
        cumulative_deduction: 累计专项附加扣除
        cumulative_tax_paid: 累计已缴税额

    Returns:
        MonthlyTaxResult: 月度个税计算结果
    """
    # 累计值
    cum_income = cumulative_income + monthly_salary
    cum_social = cumulative_social + social_insurance
    cum_deduction = cumulative_deduction + special_deduction.total_monthly

    # 累计应纳税所得额
    cum_taxable = cum_income - cum_social - cum_deduction - THRESHOLD * month
    cum_taxable = max(0, cum_taxable)

    # 获取税率
    tax_rate, quick_ded = get_tax_info(cum_taxable, MONTHLY_TAX_BRACKETS)

    # 累计应纳税额
    cum_tax = cum_taxable * tax_rate - quick_ded

    # 本月应纳税额
    monthly_tax = cum_tax - cumulative_tax_paid
    monthly_tax = max(0, monthly_tax)

    # 本月应纳税所得额
    monthly_taxable = cum_taxable - (cumulative_income - cumulative_social - cumulative_deduction - THRESHOLD * (month - 1))

    return MonthlyTaxResult(
        month=month,
        gross_income=monthly_salary,
        social_insurance=social_insurance,
        special_deduction=special_deduction.total_monthly,
        taxable_income=monthly_taxable,
        tax_rate=tax_rate,
        quick_deduction=quick_ded,
        monthly_tax=monthly_tax,
        cumulative_tax=cum_tax,
        net_income=monthly_salary - social_insurance - monthly_tax,
    )


def calculate_annual_tax(
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    months: int = 12,
) -> List[MonthlyTaxResult]:
    """
    计算全年个税（逐月）

    Args:
        monthly_salary: 月税前工资
        social_insurance: 月五险一金
        special_deduction: 专项附加扣除
        months: 计算月数（默认12）

    Returns:
        List[MonthlyTaxResult]: 每月的个税计算结果
    """
    results = []
    cum_income = 0
    cum_social = 0
    cum_deduction = 0
    cum_tax = 0

    for month in range(1, months + 1):
        result = calculate_monthly_tax(
            monthly_salary=monthly_salary,
            social_insurance=social_insurance,
            special_deduction=special_deduction,
            month=month,
            cumulative_income=cum_income,
            cumulative_social=cum_social,
            cumulative_deduction=cum_deduction,
            cumulative_tax_paid=cum_tax,
        )
        results.append(result)

        # 更新累计值
        cum_income += monthly_salary
        cum_social += social_insurance
        cum_deduction += special_deduction.total_monthly
        cum_tax = result.cumulative_tax

    return results


def calculate_bonus_separate(bonus: float) -> BonusTaxResult:
    """
    年终奖单独计税

    Args:
        bonus: 年终奖金额

    Returns:
        BonusTaxResult: 计税结果
    """
    # 月均额
    monthly_avg = bonus / 12

    # 获取税率
    tax_rate, quick_ded = get_tax_info(monthly_avg, BONUS_TAX_BRACKETS)

    # 应纳税额
    tax = bonus * tax_rate - quick_ded

    return BonusTaxResult(
        bonus=bonus,
        method="separate",
        monthly_average=monthly_avg,
        tax_rate=tax_rate,
        quick_deduction=quick_ded,
        tax=tax,
        net_bonus=bonus - tax,
    )


def calculate_bonus_combined(
    bonus: float,
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> BonusTaxResult:
    """
    年终奖合并计税（并入综合所得）

    Args:
        bonus: 年终奖金额
        monthly_salary: 月工资
        social_insurance: 月五险一金
        special_deduction: 专项附加扣除

    Returns:
        BonusTaxResult: 计税结果
    """
    # 计算不含年终奖的年度个税
    annual_results = calculate_annual_tax(
        monthly_salary=monthly_salary,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    tax_without_bonus = annual_results[-1].cumulative_tax

    # 计算含年终奖的年度个税（假设年终奖在12月发放）
    annual_income = monthly_salary * 12 + bonus
    annual_social = social_insurance * 12
    annual_deduction = special_deduction.total_monthly * 12

    annual_taxable = annual_income - annual_social - annual_deduction - THRESHOLD * 12
    annual_taxable = max(0, annual_taxable)

    tax_rate, quick_ded = get_tax_info(annual_taxable, MONTHLY_TAX_BRACKETS)
    tax_with_bonus = annual_taxable * tax_rate - quick_ded

    # 年终奖部分税额
    bonus_tax = tax_with_bonus - tax_without_bonus

    return BonusTaxResult(
        bonus=bonus,
        method="combined",
        monthly_average=0,
        tax_rate=tax_rate,
        quick_deduction=quick_ded,
        tax=bonus_tax,
        net_bonus=bonus - bonus_tax,
    )


def compare_bonus_methods(
    bonus: float,
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    对比年终奖单独计税和合并计税

    Args:
        bonus: 年终奖金额
        monthly_salary: 月工资
        social_insurance: 月五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 对比结果
    """
    separate = calculate_bonus_separate(bonus)
    combined = calculate_bonus_combined(
        bonus, monthly_salary, social_insurance, special_deduction
    )

    return {
        "separate": separate,
        "combined": combined,
        "recommendation": "separate" if separate.tax <= combined.tax else "combined",
        "savings": abs(separate.tax - combined.tax),
    }


def reverse_gross_from_net(
    target_net: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    max_iterations: int = 100,
) -> float:
    """
    从税后收入反推税前收入

    Args:
        target_net: 目标税后收入
        social_insurance: 五险一金
        special_deduction: 专项附加扣除
        max_iterations: 最大迭代次数

    Returns:
        float: 税前收入
    """
    # 初始估计
    gross = target_net + social_insurance

    for _ in range(max_iterations):
        # 计算当前估计的税后
        result = calculate_monthly_tax(
            monthly_salary=gross,
            social_insurance=social_insurance,
            special_deduction=special_deduction,
        )
        current_net = result.net_income

        # 差值
        diff = target_net - current_net

        # 收敛判断
        if abs(diff) < 0.01:
            return gross

        # 调整估计（考虑税率影响）
        gross += diff / (1 - result.tax_rate) if result.tax_rate < 1 else diff

    return gross


# ==================== 年度汇算清缴 ====================

def calculate_annual_settlement(
    income_sources: IncomeSource,
    annual_social_insurance: float,
    special_deduction: SpecialDeduction,
    other_deductions: float = 0,
    prepaid_tax: float = 0,
) -> AnnualSettlementResult:
    """
    计算年度汇算清缴

    Args:
        income_sources: 多收入来源
        annual_social_insurance: 年度五险一金（个人部分）
        special_deduction: 专项附加扣除
        other_deductions: 其他扣除（企业年金、商业健康保险等）
        prepaid_tax: 已预缴税额

    Returns:
        AnnualSettlementResult: 汇算清缴结果
    """
    # 综合所得总额
    comprehensive_income = income_sources.total_comprehensive_income
    
    # 各项扣除总额
    total_deductions = (
        annual_social_insurance +
        special_deduction.total_monthly * 12 +
        other_deductions +
        ANNUAL_THRESHOLD
    )
    
    # 应纳税所得额
    taxable_income = max(0, comprehensive_income - total_deductions)
    
    # 获取税率
    tax_rate, quick_ded = get_tax_info(taxable_income, ANNUAL_TAX_BRACKETS)
    
    # 年度应纳税额
    annual_tax = taxable_income * tax_rate - quick_ded
    
    # 汇算金额（正数=应补缴，负数=应退税）
    settlement_amount = annual_tax - prepaid_tax
    
    return AnnualSettlementResult(
        comprehensive_income=comprehensive_income,
        deductions=total_deductions,
        taxable_income=taxable_income,
        tax_rate=tax_rate,
        quick_deduction=quick_ded,
        annual_tax=annual_tax,
        prepaid_tax=prepaid_tax,
        settlement_amount=settlement_amount,
    )


# ==================== 年终奖智能优化 ====================

def optimize_bonus_allocation(
    total_bonus: float,
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    max_splits: int = 5,
) -> BonusOptimizationResult:
    """
    年终奖智能优化 - 找到最优的年终奖分配方案
    
    策略：
    1. 部分并入当月工资，部分单独计税
    2. 或分多次发放
    3. 找到总税额最小的方案

    Args:
        total_bonus: 年终奖总额
        monthly_salary: 月工资
        social_insurance: 月五险一金
        special_deduction: 专项附加扣除
        max_splits: 最多分几次发放

    Returns:
        BonusOptimizationResult: 优化结果
    """
    optimal_split = []
    min_tax = float('inf')
    max_tax = 0
    
    # 方案1：全部单独计税
    separate = calculate_bonus_separate(total_bonus)
    if separate.tax < min_tax:
        min_tax = separate.tax
        optimal_split = [{"amount": total_bonus, "method": "单独计税", "tax": separate.tax}]
    max_tax = max(max_tax, separate.tax)
    
    # 方案2：全部合并计税
    combined = calculate_bonus_combined(
        total_bonus, monthly_salary, social_insurance, special_deduction
    )
    if combined.tax < min_tax:
        min_tax = combined.tax
        optimal_split = [{"amount": total_bonus, "method": "合并计税", "tax": combined.tax}]
    max_tax = max(max_tax, combined.tax)
    
    # 方案3：部分单独 + 部分合并（按10%递增测试）
    for split_ratio in range(10, 100, 10):
        bonus1 = total_bonus * split_ratio / 100
        bonus2 = total_bonus - bonus1
        
        # 第一部分单独计税
        part1 = calculate_bonus_separate(bonus1)
        
        # 第二部分合并计税
        part2 = calculate_bonus_combined(
            bonus2, monthly_salary, social_insurance, special_deduction
        )
        
        total_split_tax = part1.tax + part2.tax
        
        if total_split_tax < min_tax:
            min_tax = total_split_tax
            optimal_split = [
                {"amount": bonus1, "method": "单独计税", "tax": part1.tax},
                {"amount": bonus2, "method": "合并计税", "tax": part2.tax},
            ]
        
        max_tax = max(max_tax, total_split_tax)
    
    return BonusOptimizationResult(
        total_bonus=total_bonus,
        optimal_split=optimal_split,
        total_tax=min_tax,
        worst_tax=max_tax,
        savings=max_tax - min_tax,
    )


# ==================== 跳槽薪资谈判 ====================

def calculate_salary_negotiation(
    target_net: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    跳槽薪资谈判助手 - 从税后反推税前

    Args:
        target_net: 目标税后收入
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 谈判建议
    """
    gross = reverse_gross_from_net(target_net, social_insurance, special_deduction)
    
    result = calculate_monthly_tax(
        monthly_salary=gross,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    
    # 建议的谈判范围（税前 ± 5%）
    gross_min = gross * 0.95
    gross_max = gross * 1.05
    
    result_min = calculate_monthly_tax(
        monthly_salary=gross_min,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    
    result_max = calculate_monthly_tax(
        monthly_salary=gross_max,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    
    return {
        "目标税后": target_net,
        "需要税前": gross,
        "五险一金": social_insurance,
        "个税": result.monthly_tax,
        "税率": f"{result.tax_rate*100:.0f}%",
        "谈判范围": {
            "最低": {
                "税前": gross_min,
                "税后": result_min.net_income,
            },
            "最高": {
                "税前": gross_max,
                "税后": result_max.net_income,
            },
        },
        "建议话术": f"考虑到税后到手{target_net:.0f}元，建议谈{gross:.0f}元的税前薪资",
    }


# ==================== 社保公积金计算器 ====================

# 各城市社保公积金比例（2025年）
SOCIAL_INSURANCE_RATES = {
    "北京": {
        "养老": {"个人": 0.08, "公司": 0.16},
        "医疗": {"个人": 0.02, "公司": 0.10},
        "失业": {"个人": 0.005, "公司": 0.005},
        "工伤": {"个人": 0, "公司": 0.004},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.12, "公司": 0.12},
        "基数下限": 6326,
        "基数上限": 33891,
    },
    "上海": {
        "养老": {"个人": 0.08, "公司": 0.16},
        "医疗": {"个人": 0.02, "公司": 0.10},
        "失业": {"个人": 0.005, "公司": 0.005},
        "工伤": {"个人": 0, "公司": 0.0026},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.07, "公司": 0.07},
        "基数下限": 7310,
        "基数上限": 36549,
    },
    "深圳": {
        "养老": {"个人": 0.08, "公司": 0.15},
        "医疗": {"个人": 0.02, "公司": 0.06},
        "失业": {"个人": 0.003, "公司": 0.007},
        "工伤": {"个人": 0, "公司": 0.0014},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.05, "公司": 0.05},
        "基数下限": 2360,
        "基数上限": 38863,
    },
    "广州": {
        "养老": {"个人": 0.08, "公司": 0.15},
        "医疗": {"个人": 0.02, "公司": 0.055},
        "失业": {"个人": 0.005, "公司": 0.005},
        "工伤": {"个人": 0, "公司": 0.0015},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.05, "公司": 0.05},
        "基数下限": 2300,
        "基数上限": 36072,
    },
    "杭州": {
        "养老": {"个人": 0.08, "公司": 0.15},
        "医疗": {"个人": 0.02, "公司": 0.099},
        "失业": {"个人": 0.005, "公司": 0.005},
        "工伤": {"个人": 0, "公司": 0.0025},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.12, "公司": 0.12},
        "基数下限": 3957,
        "基数上限": 22311,
    },
    "成都": {
        "养老": {"个人": 0.08, "公司": 0.16},
        "医疗": {"个人": 0.02, "公司": 0.069},
        "失业": {"个人": 0.004, "公司": 0.006},
        "工伤": {"个人": 0, "公司": 0.0023},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.05, "公司": 0.05},
        "基数下限": 4071,
        "基数上限": 20355,
    },
    "默认": {
        "养老": {"个人": 0.08, "公司": 0.16},
        "医疗": {"个人": 0.02, "公司": 0.08},
        "失业": {"个人": 0.005, "公司": 0.005},
        "工伤": {"个人": 0, "公司": 0.002},
        "生育": {"个人": 0, "公司": 0},
        "公积金": {"个人": 0.12, "公司": 0.12},
        "基数下限": 0,
        "基数上限": 1000000,
    },
}


@dataclass
class SocialInsuranceResult:
    """社保公积金计算结果"""

    # 缴费基数
    base_salary: float
    adjusted_base: float  # 调整后的基数（在上下限之间）

    # 个人缴纳
    pension_personal: float  # 养老保险
    medical_personal: float  # 医疗保险
    unemployment_personal: float  # 失业保险
    housing_fund_personal: float  # 公积金
    total_personal: float  # 个人合计

    # 公司缴纳
    pension_company: float
    medical_company: float
    unemployment_company: float
    work_injury_company: float  # 工伤保险
    maternity_company: float  # 生育保险
    housing_fund_company: float
    total_company: float  # 公司合计

    # 总计
    total_social: float  # 社保总计
    total_all: float  # 全部总计（含公积金）


def calculate_social_insurance(
    salary: float,
    city: str = "默认",
    custom_housing_fund_rate: float = None,
) -> SocialInsuranceResult:
    """
    计算社保公积金

    Args:
        salary: 税前月薪
        city: 城市
        custom_housing_fund_rate: 自定义公积金比例（如 0.12 表示 12%）

    Returns:
        SocialInsuranceResult: 计算结果
    """
    rates = SOCIAL_INSURANCE_RATES.get(city, SOCIAL_INSURANCE_RATES["默认"])

    # 调整缴费基数（在上下限之间）
    adjusted_base = max(rates["基数下限"], min(salary, rates["基数上限"]))

    # 公积金比例
    housing_rate = (
        custom_housing_fund_rate
        if custom_housing_fund_rate
        else rates["公积金"]["个人"]
    )

    # 个人缴纳
    pension_personal = adjusted_base * rates["养老"]["个人"]
    medical_personal = adjusted_base * rates["医疗"]["个人"]
    unemployment_personal = adjusted_base * rates["失业"]["个人"]
    housing_fund_personal = adjusted_base * housing_rate

    total_personal = (
        pension_personal
        + medical_personal
        + unemployment_personal
        + housing_fund_personal
    )

    # 公司缴纳
    pension_company = adjusted_base * rates["养老"]["公司"]
    medical_company = adjusted_base * rates["医疗"]["公司"]
    unemployment_company = adjusted_base * rates["失业"]["公司"]
    work_injury_company = adjusted_base * rates["工伤"]["公司"]
    maternity_company = adjusted_base * rates["生育"]["公司"]
    housing_fund_company = adjusted_base * rates["公积金"]["公司"]

    total_company = (
        pension_company
        + medical_company
        + unemployment_company
        + work_injury_company
        + housing_fund_company
    )

    # 总计
    total_social = total_personal + total_company - housing_fund_personal - housing_fund_company
    total_all = total_personal + total_company

    return SocialInsuranceResult(
        base_salary=salary,
        adjusted_base=adjusted_base,
        pension_personal=pension_personal,
        medical_personal=medical_personal,
        unemployment_personal=unemployment_personal,
        housing_fund_personal=housing_fund_personal,
        total_personal=total_personal,
        pension_company=pension_company,
        medical_company=medical_company,
        unemployment_company=unemployment_company,
        work_injury_company=work_injury_company,
        maternity_company=maternity_company,
        housing_fund_company=housing_fund_company,
        total_company=total_company,
        total_social=total_social,
        total_all=total_all,
    )


def list_supported_cities() -> List[str]:
    """列出支持的城市"""
    return [city for city in SOCIAL_INSURANCE_RATES.keys() if city != "默认"]


# ==================== 可视化图表 ====================

def generate_tax_distribution_chart(
    salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> str:
    """
    生成个税分布图表（文本版）

    Args:
        salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        str: ASCII 图表
    """
    result = calculate_monthly_tax(salary, social_insurance, special_deduction)
    
    # 计算各项占比
    total = salary
    social_pct = social_insurance / total * 100
    tax_pct = result.monthly_tax / total * 100
    deduction_pct = special_deduction.total_monthly / total * 100
    net_pct = result.net_income / total * 100
    
    # 生成文本图表
    chart = f"""
╔══════════════════════════════════════════════════════════╗
║                  工资条可视化分析                          ║
╠══════════════════════════════════════════════════════════╣
║  税前工资：¥{salary:>10,.2f}                              ║
╠══════════════════════════════════════════════════════════╣
║  扣除项：                                                 ║
║  ├─ 五险一金  │{'█' * int(social_pct)} {social_pct:>5.1f}% │ ¥{social_insurance:>8,.2f} ║
║  ├─ 专项扣除  │{'█' * int(deduction_pct)} {deduction_pct:>5.1f}% │ ¥{special_deduction.total_monthly:>8,.2f} ║
║  └─ 个人所得税│{'█' * int(tax_pct)} {tax_pct:>5.1f}% │ ¥{result.monthly_tax:>8,.2f} ║
╠══════════════════════════════════════════════════════════╣
║  税后到手：¥{result.net_income:>10,.2f} ({net_pct:>5.1f}%)                    ║
╚══════════════════════════════════════════════════════════╝
"""
    return chart


def generate_salary_pie_chart(
    salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    生成工资分布饼图数据

    Args:
        salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 饼图数据（可用于前端渲染）
    """
    result = calculate_monthly_tax(salary, social_insurance, special_deduction)
    
    return {
        "labels": ["税后到手", "五险一金", "个人所得税", "专项扣除"],
        "values": [
            result.net_income,
            social_insurance,
            result.monthly_tax,
            special_deduction.total_monthly,
        ],
        "colors": ["#4CAF50", "#FF9800", "#F44336", "#2196F3"],
        "percentages": [
            result.net_income / salary * 100,
            social_insurance / salary * 100,
            result.monthly_tax / salary * 100,
            special_deduction.total_monthly / salary * 100,
        ],
    }


def generate_tax_trend_chart(
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> str:
    """
    生成年度个税趋势图（文本版）

    Args:
        monthly_salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        str: ASCII 图表
    """
    annual = calculate_annual_tax(monthly_salary, social_insurance, special_deduction)
    
    # 找到最大值用于缩放
    max_tax = max(r.monthly_tax for r in annual)
    scale = 40 / max_tax if max_tax > 0 else 1
    
    chart = """
╔════════════════════════════════════════════════════════════╗
║                   年度个税趋势图                            ║
╠════════════════════════════════════════════════════════════╣
"""
    
    for r in annual:
        bar_len = int(r.monthly_tax * scale)
        bar = "█" * bar_len
        chart += f"║ {r.month:>2}月 │{bar:<40} ¥{r.monthly_tax:>6,.0f} ║\n"
    
    chart += """╠════════════════════════════════════════════════════════════╣
║  累计个税：¥{:>10,.2f}                                   ║
╚════════════════════════════════════════════════════════════╝
""".format(
        annual[-1].cumulative_tax
    )
    
    return chart


# ==================== 年终奖规划 ====================

def plan_bonus_thresholds(
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    规划年终奖临界点（找出单独计税更划算的金额区间）

    Args:
        monthly_salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 临界点分析
    """
    # 年终奖税率临界点（单独计税）
    bonus_thresholds = [
        (36000, 0.03, 0),
        (144000, 0.1, 210),
        (300000, 0.2, 1410),
        (420000, 0.25, 2660),
        (660000, 0.3, 4410),
        (960000, 0.35, 7160),
    ]
    
    recommendations = []
    
    for i, (threshold, rate, deduction) in enumerate(bonus_thresholds):
        # 测试临界点前后
        test_amounts = [threshold - 1, threshold, threshold + 10000]
        
        for amount in test_amounts:
            if amount <= 0:
                continue
            
            comparison = compare_bonus_methods(
                bonus=amount,
                monthly_salary=monthly_salary,
                social_insurance=social_insurance,
                special_deduction=special_deduction,
            )
            
            recommendations.append(
                {
                    "金额": amount,
                    "单独计税": comparison["separate"].tax,
                    "合并计税": comparison["combined"].tax,
                    "推荐": comparison["recommendation"],
                    "节省": comparison["savings"],
                }
            )
    
    # 找出最优区间
    optimal_ranges = []
    current_range = None
    
    for rec in recommendations:
        if rec["推荐"] == "separate":
            if current_range is None:
                current_range = {"start": rec["金额"], "end": rec["金额"]}
            else:
                current_range["end"] = rec["金额"]
        else:
            if current_range:
                optimal_ranges.append(current_range)
                current_range = None
    
    if current_range:
        optimal_ranges.append(current_range)
    
    return {
        "临界点": [
            {"金额": t[0], "税率": f"{t[1]*100:.0f}%", "速算扣除": t[2]}
            for t in bonus_thresholds
        ],
        "推荐区间": optimal_ranges,
        "详细分析": recommendations[:10],  # 只返回前10个
        "建议": "年终奖在以下区间时，建议单独计税："
        + "、".join([f"¥{r['start']:,.0f}-¥{r['end']:,.0f}" for r in optimal_ranges])
        if optimal_ranges
        else "当前薪资水平下，合并计税更划算",
    }


def find_optimal_bonus_amount(
    target_tax: float,
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    找出最优年终奖金额（给定目标税额）

    Args:
        target_tax: 目标个税总额
        monthly_salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 最优年终奖金额
    """
    # 计算无年终奖时的个税
    annual = calculate_annual_tax(monthly_salary, social_insurance, special_deduction)
    base_tax = annual[-1].cumulative_tax
    
    # 如果目标税额低于基础个税，无解
    if target_tax < base_tax:
        return {
            "错误": "目标税额低于基础个税，无法实现",
            "基础个税": base_tax,
        }
    
    # 剩余税额
    remaining_tax = target_tax - base_tax
    
    # 尝试不同的年终奖金额
    best_bonus = 0
    best_tax_diff = float("inf")
    
    for bonus in range(10000, 1000000, 10000):
        comparison = compare_bonus_methods(
            bonus=bonus,
            monthly_salary=monthly_salary,
            social_insurance=social_insurance,
            special_deduction=special_deduction,
        )
        
        total_tax = base_tax + comparison[comparison["recommendation"]].tax
        tax_diff = abs(total_tax - target_tax)
        
        if tax_diff < best_tax_diff:
            best_tax_diff = tax_diff
            best_bonus = bonus
    
    return {
        "目标税额": target_tax,
        "最优年终奖": best_bonus,
        "实际税额": base_tax
        + compare_bonus_methods(
            best_bonus, monthly_salary, social_insurance, special_deduction
        )["separate"].tax,
        "差异": best_tax_diff,
    }


# ==================== Excel 导出 ====================

def generate_excel_data(
    salary: float,
    social: float,
    deduction: SpecialDeduction,
    bonus: float = 0,
) -> str:
    """
    生成 Excel 格式数据（CSV 格式）

    Args:
        salary: 月薪
        social: 五险一金
        deduction: 专项附加扣除
        bonus: 年终奖

    Returns:
        str: CSV 格式数据
    """
    # 计算月度个税
    annual = calculate_annual_tax(salary, social, deduction)
    
    # CSV 头
    csv = "月份,税前工资,五险一金,专项扣除,应纳税所得额,税率,本月个税,累计个税,税后工资\n"
    
    # CSV 数据
    for r in annual:
        csv += f"{r.month},{r.gross_income:.2f},{r.social_insurance:.2f},"
        csv += f"{deduction.total_monthly:.2f},{r.taxable_income:.2f},"
        csv += f"{r.tax_rate*100:.0f}%,{r.monthly_tax:.2f},"
        csv += f"{r.cumulative_tax:.2f},{r.net_income:.2f}\n"
    
    # 年度汇总
    csv += "\n年度汇总\n"
    csv += f"税前总收入,{salary * 12 + bonus:.2f}\n"
    csv += f"五险一金,{social * 12:.2f}\n"
    csv += f"专项扣除,{deduction.total_monthly * 12:.2f}\n"
    csv += f"年度个税,{annual[-1].cumulative_tax:.2f}\n"
    csv += f"税后总收入,{salary * 12 - social * 12 - annual[-1].cumulative_tax:.2f}\n"
    
    # 年终奖
    if bonus > 0:
        comparison = compare_bonus_methods(bonus, salary, social, deduction)
        csv += "\n年终奖\n"
        csv += f"金额,{bonus:.2f}\n"
        csv += f"单独计税,{comparison['separate'].tax:.2f}\n"
        csv += f"合并计税,{comparison['combined'].tax:.2f}\n"
        csv += f"推荐,{'单独' if comparison['recommendation'] == 'separate' else '合并'}\n"
    
    return csv


# ==================== 涨薪效果分析 ====================

def calculate_raise_effect(
    current_salary: float,
    raise_percentage: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    计算涨薪效果

    Args:
        current_salary: 当前月薪
        raise_percentage: 涨薪百分比（如 10 表示涨 10%）
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 涨薪效果分析
    """
    # 当前工资计算
    current_result = calculate_monthly_tax(
        monthly_salary=current_salary,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    
    # 涨薪后工资
    new_salary = current_salary * (1 + raise_percentage / 100)
    new_result = calculate_monthly_tax(
        monthly_salary=new_salary,
        social_insurance=social_insurance,
        special_deduction=special_deduction,
    )
    
    # 计算差额
    gross_increase = new_salary - current_salary
    tax_increase = new_result.monthly_tax - current_result.monthly_tax
    net_increase = new_result.net_income - current_result.net_income
    
    # 实际到手比例
    effective_rate = (net_increase / gross_increase * 100) if gross_increase > 0 else 0
    
    return {
        "涨薪前": {
            "税前": current_salary,
            "个税": current_result.monthly_tax,
            "到手": current_result.net_income,
        },
        "涨薪后": {
            "税前": new_salary,
            "个税": new_result.monthly_tax,
            "到手": new_result.net_income,
        },
        "涨薪效果": {
            "税前增加": gross_increase,
            "个税增加": tax_increase,
            "到手增加": net_increase,
            "实际到手比例": f"{effective_rate:.1f}%",
        },
        "年度效果": {
            "税前增加": gross_increase * 12,
            "个税增加": tax_increase * 12,
            "到手增加": net_increase * 12,
        },
        "建议": f"涨薪{raise_percentage}%后，每月多拿¥{net_increase:,.0f}（实际到手{effective_rate:.1f}%），年度多拿¥{net_increase*12:,.0f}",
    }


# ==================== 快速模板 ====================

# 预设场景模板
QUICK_TEMPLATES = {
    "单身青年": SpecialDeduction(
        housing_rent=1500,  # 租房
    ),
    "已婚一孩": SpecialDeduction(
        children_education=2000,  # 1个孩子
        housing_loan=1000,  # 房贷
        elderly_support=1000,  # 赡养老人（非独生）
    ),
    "已婚二孩": SpecialDeduction(
        children_education=4000,  # 2个孩子
        housing_loan=1000,  # 房贷
        elderly_support=1500,  # 赡养老人
    ),
    "有房贷无孩": SpecialDeduction(
        housing_loan=1000,  # 房贷
    ),
    "有娃有房贷": SpecialDeduction(
        children_education=2000,  # 1个孩子
        housing_loan=1000,  # 房贷
    ),
    "独生子女赡养": SpecialDeduction(
        elderly_support=3000,  # 独生子女
    ),
    "继续教育": SpecialDeduction(
        continuing_education=400,  # 学历继续教育
    ),
    "默认": SpecialDeduction(),
}

def get_template(name: str) -> SpecialDeduction:
    """获取预设模板"""
    return QUICK_TEMPLATES.get(name, QUICK_TEMPLATES["默认"])

def list_templates() -> List[str]:
    """列出所有预设模板"""
    return list(QUICK_TEMPLATES.keys())

def quick_calc_with_template(
    salary: float,
    social: float,
    template_name: str,
) -> Dict:
    """
    使用模板快速计算

    Args:
        salary: 月工资
        social: 五险一金
        template_name: 模板名称

    Returns:
        Dict: 计算结果
    """
    deduction = get_template(template_name)
    
    result = calculate_monthly_tax(
        monthly_salary=salary,
        social_insurance=social,
        special_deduction=deduction,
    )
    
    return {
        "模板": template_name,
        "税前": salary,
        "五险一金": social,
        "专项扣除": deduction.total_monthly,
        "个税": result.monthly_tax,
        "到手": result.net_income,
        "税率": f"{result.tax_rate*100:.0f}%",
    }


# ==================== 交互式问答 ====================

def interactive_tax_calculator(answers: Dict) -> Dict:
    """
    交互式个税计算

    Args:
        answers: 用户回答的问题
            - salary: 月薪
            - social: 五险一金
            - children: 子女数量
            - infants: 婴幼儿数量
            - has_loan: 是否有房贷
            - rent: 租房金额
            - elderly_type: 赡养老人类型（独生/非独生/无）
            - education: 是否继续教育
            - bonus: 年终奖（可选）

    Returns:
        Dict: 完整的个税计算结果
    """
    # 构建专项扣除
    deduction = SpecialDeduction(
        children_education=answers.get('children', 0) * 2000,
        infant_care=answers.get('infants', 0) * 2000,
        housing_loan=1000 if answers.get('has_loan', False) else 0,
        housing_rent=answers.get('rent', 0),
        continuing_education=400 if answers.get('education', False) else 0,
        elderly_support={
            '独生': 3000,
            '非独生': 1500,
            '无': 0,
        }.get(answers.get('elderly_type', '无'), 0),
    )
    
    # 计算月度个税
    monthly = calculate_monthly_tax(
        monthly_salary=answers['salary'],
        social_insurance=answers.get('social', 0),
        special_deduction=deduction,
    )
    
    # 计算年度个税
    annual = calculate_annual_tax(
        monthly_salary=answers['salary'],
        social_insurance=answers.get('social', 0),
        special_deduction=deduction,
    )
    
    result = {
        "月度": {
            "税前": answers['salary'],
            "五险一金": answers.get('social', 0),
            "专项扣除": deduction.total_monthly,
            "个税": monthly.monthly_tax,
            "到手": monthly.net_income,
            "税率": f"{monthly.tax_rate*100:.0f}%",
        },
        "年度": {
            "税前": answers['salary'] * 12,
            "五险一金": answers.get('social', 0) * 12,
            "专项扣除": deduction.total_monthly * 12,
            "个税": annual[-1].cumulative_tax,
            "到手": answers['salary'] * 12 - answers.get('social', 0) * 12 - annual[-1].cumulative_tax,
        },
        "专项扣除明细": {
            "子女教育": deduction.children_education,
            "婴幼儿照护": deduction.infant_care,
            "继续教育": deduction.continuing_education,
            "住房贷款利息": deduction.housing_loan,
            "住房租金": deduction.housing_rent,
            "赡养老人": deduction.elderly_support,
        },
    }
    
    # 如果有年终奖
    if answers.get('bonus', 0) > 0:
        bonus_comparison = compare_bonus_methods(
            bonus=answers['bonus'],
            monthly_salary=answers['salary'],
            social_insurance=answers.get('social', 0),
            special_deduction=deduction,
        )
        result["年终奖"] = {
            "金额": answers['bonus'],
            "单独计税": {
                "税额": bonus_comparison['separate'].tax,
                "到手": bonus_comparison['separate'].net_bonus,
            },
            "合并计税": {
                "税额": bonus_comparison['combined'].tax,
                "到手": bonus_comparison['combined'].net_bonus,
            },
            "推荐": bonus_comparison['recommendation'],
            "节省": bonus_comparison['savings'],
        }
    
    return result


# ==================== 飞书文档报告 ====================

def generate_feishu_report(
    salary: float,
    social: float,
    deduction: SpecialDeduction,
    bonus: float = 0,
) -> str:
    """
    生成飞书文档格式的个税报告

    Args:
        salary: 月工资
        social: 五险一金
        deduction: 专项附加扣除
        bonus: 年终奖（可选）

    Returns:
        str: 飞书文档 Markdown 格式
    """
    # 计算结果
    monthly = calculate_monthly_tax(salary, social, deduction)
    annual = calculate_annual_tax(salary, social, deduction)
    
    report = f"""# 📊 个人所得税计算报告

> 生成时间：2025年
> 税率依据：《个人所得税法》（2025年版）

---

## 一、收入概览

| 项目 | 月度 | 年度 |
|------|------|------|
| 税前收入 | ¥{salary:,.2f} | ¥{salary*12:,.2f} |
| 五险一金 | ¥{social:,.2f} | ¥{social*12:,.2f} |
| 专项附加扣除 | ¥{deduction.total_monthly:,.2f} | ¥{deduction.total_monthly*12:,.2f} |
| 应纳税所得额 | ¥{monthly.taxable_income:,.2f} | ¥{annual[-1].taxable_income:,.2f} |
| **个人所得税** | **¥{monthly.monthly_tax:,.2f}** | **¥{annual[-1].cumulative_tax:,.2f}** |
| **税后收入** | **¥{monthly.net_income:,.2f}** | **¥{salary*12-social*12-annual[-1].cumulative_tax:,.2f}** |

---

## 二、专项附加扣除明细

| 扣除项 | 月度金额 | 年度金额 | 条件 |
|--------|----------|----------|------|
| 子女教育 | ¥{deduction.children_education:,.2f} | ¥{deduction.children_education*12:,.2f} | 3岁-博士在读，每孩2000元/月 |
| 婴幼儿照护 | ¥{deduction.infant_care:,.2f} | ¥{deduction.infant_care*12:,.2f} | 0-3岁，每孩2000元/月 |
| 继续教育 | ¥{deduction.continuing_education:,.2f} | ¥{deduction.continuing_education*12:,.2f} | 学历继续教育400元/月 |
| 住房贷款利息 | ¥{deduction.housing_loan:,.2f} | ¥{deduction.housing_loan*12:,.2f} | 首套房贷1000元/月 |
| 住房租金 | ¥{deduction.housing_rent:,.2f} | ¥{deduction.housing_rent*12:,.2f} | 800-1500元/月（按城市） |
| 赡养老人 | ¥{deduction.elderly_support:,.2f} | ¥{deduction.elderly_support*12:,.2f} | 独生3000元/月，非独生最高1500元/月 |
| **合计** | **¥{deduction.total_monthly:,.2f}** | **¥{deduction.total_monthly*12:,.2f}** | - |

---

## 三、适用税率

- **应纳税所得额**：¥{annual[-1].taxable_income:,.2f}/年
- **适用税率**：{annual[-1].tax_rate*100:.0f}%
- **速算扣除数**：¥{annual[-1].quick_deduction:,.2f}

---

## 四、月度个税明细

| 月份 | 税前收入 | 五险一金 | 累计应税所得 | 税率 | 本月个税 | 累计个税 | 税后收入 |
|------|----------|----------|--------------|------|----------|----------|----------|
"""
    
    for r in annual:
        report += f"| {r.month} | ¥{r.gross_income:,.0f} | ¥{r.social_insurance:,.0f} | ¥{r.taxable_income:,.0f} | {r.tax_rate*100:.0f}% | ¥{r.monthly_tax:,.0f} | ¥{r.cumulative_tax:,.0f} | ¥{r.net_income:,.0f} |\n"
    
    # 年终奖对比
    if bonus > 0:
        comparison = compare_bonus_methods(bonus, salary, social, deduction)
        
        report += f"""
---

## 五、年终奖计税对比

**年终奖金额**：¥{bonus:,.2f}

| 计税方式 | 月均额 | 税率 | 应纳税额 | 税后金额 |
|----------|--------|------|----------|----------|
| 单独计税 | ¥{comparison['separate'].monthly_average:,.2f} | {comparison['separate'].tax_rate*100:.0f}% | ¥{comparison['separate'].tax:,.2f} | ¥{comparison['separate'].net_bonus:,.2f} |
| 合并计税 | - | {comparison['combined'].tax_rate*100:.0f}% | ¥{comparison['combined'].tax:,.2f} | ¥{comparison['combined'].net_bonus:,.2f} |

### 📋 推荐

**推荐方式**：{'单独计税' if comparison['recommendation'] == 'separate' else '合并计税'}

**节省税额**：¥{comparison['savings']:,.2f}

---

## 六、年度总收入

| 项目 | 金额 |
|------|------|
| 税前总收入 | ¥{salary*12+bonus:,.2f} |
| 年度个税 | ¥{annual[-1].cumulative_tax + comparison[comparison['recommendation']].tax:,.2f} |
| 年度五险一金 | ¥{social*12:,.2f} |
| **年度税后总收入** | **¥{salary*12+bonus-social*12-annual[-1].cumulative_tax-comparison[comparison['recommendation']].tax:,.2f}** |
"""
    
    report += """
---

## 七、注意事项

1. **累计预扣法**：每月个税按年初累计计算，非简单月度计算
2. **年终奖优惠**：2027年12月31日前，年终奖可选择单独计税
3. **专项扣除**：五险一金中的个人缴纳部分可税前扣除
4. **赡养老人**：仅限生父母、继父母、养父母，不包括岳父岳母/公婆

---

*本报告由「中国个税计算器」自动生成*
"""
    
    return report


def compare_job_offers(
    offers: List[Dict],
    special_deduction: SpecialDeduction = None,
) -> Dict:
    """
    对比多个 Offer

    Args:
        offers: Offer 列表，每个包含 {name, salary, social_insurance, bonus}
        special_deduction: 专项附加扣除

    Returns:
        Dict: 对比结果
    """
    if special_deduction is None:
        special_deduction = SpecialDeduction()
    
    results = []
    
    for offer in offers:
        name = offer.get('name', 'Offer')
        salary = offer.get('salary', 0)
        social = offer.get('social_insurance', 0)
        bonus = offer.get('bonus', 0)
        
        # 计算月度个税
        monthly = calculate_monthly_tax(
            monthly_salary=salary,
            social_insurance=social,
            special_deduction=special_deduction,
        )
        
        # 计算年度个税
        annual = calculate_annual_tax(
            monthly_salary=salary,
            social_insurance=social,
            special_deduction=special_deduction,
        )
        
        # 计算年终奖（默认单独计税）
        bonus_result = None
        if bonus > 0:
            bonus_result = calculate_bonus_separate(bonus)
        
        # 年度总到手
        annual_net = annual[-1].cumulative_tax
        total_annual_gross = salary * 12 + bonus
        total_annual_net = salary * 12 - social * 12 - annual_net
        if bonus_result:
            total_annual_net += bonus_result.net_bonus
        
        results.append({
            "名称": name,
            "月薪": salary,
            "五险一金": social,
            "月个税": monthly.monthly_tax,
            "月到手": monthly.net_income,
            "年终奖": bonus,
            "年终奖个税": bonus_result.tax if bonus_result else 0,
            "年终奖到手": bonus_result.net_bonus if bonus_result else 0,
            "年度总收入": total_annual_gross,
            "年度总到手": total_annual_net,
            "年度总个税": annual_net + (bonus_result.tax if bonus_result else 0),
        })
    
    # 按年度总到手排序
    sorted_results = sorted(results, key=lambda x: x['年度总到手'], reverse=True)
    
    # 添加排名
    for i, r in enumerate(sorted_results):
        r['排名'] = i + 1
    
    return {
        "对比结果": sorted_results,
        "推荐选择": sorted_results[0]['名称'] if sorted_results else None,
        "年度到手差额": sorted_results[0]['年度总到手'] - sorted_results[-1]['年度总到手'] if len(sorted_results) > 1 else 0,
    }


# ==================== 报告生成 ====================

def generate_tax_report(
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    bonus: float = 0,
) -> str:
    """
    生成个税计算报告

    Args:
        monthly_salary: 月工资
        social_insurance: 五险一金
        special_deduction: 专项附加扣除
        bonus: 年终奖（可选）

    Returns:
        str: Markdown 格式的报告
    """
    # 计算年度个税
    annual_results = calculate_annual_tax(
        monthly_salary, social_insurance, special_deduction
    )

    # 统计
    annual_gross = monthly_salary * 12
    annual_social = social_insurance * 12
    annual_deduction = special_deduction.total_monthly * 12
    annual_tax = annual_results[-1].cumulative_tax
    annual_net = annual_gross - annual_social - annual_tax

    # 报告
    report = f"""# 📊 个税计算报告

## 基本信息

| 项目 | 月度 | 年度 |
|------|------|------|
| 税前收入 | ¥{monthly_salary:,.2f} | ¥{annual_gross:,.2f} |
| 五险一金 | ¥{social_insurance:,.2f} | ¥{annual_social:,.2f} |
| 专项附加扣除 | ¥{special_deduction.total_monthly:,.2f} | ¥{annual_deduction:,.2f} |
| 应纳税额 | - | ¥{annual_results[-1].taxable_income:,.2f} |
| 个税 | ¥{annual_tax/12:,.2f} | ¥{annual_tax:,.2f} |
| **税后收入** | **¥{annual_net/12:,.2f}** | **¥{annual_net:,.2f}** |

## 专项附加扣除明细

| 扣除项 | 金额（月） |
|--------|-----------|
| 子女教育 | ¥{special_deduction.children_education:,.2f} |
| 婴幼儿照护 | ¥{special_deduction.infant_care:,.2f} |
| 继续教育 | ¥{special_deduction.continuing_education:,.2f} |
| 住房贷款利息 | ¥{special_deduction.housing_loan:,.2f} |
| 住房租金 | ¥{special_deduction.housing_rent:,.2f} |
| 赡养老人 | ¥{special_deduction.elderly_support:,.2f} |
| **合计** | **¥{special_deduction.total_monthly:,.2f}** |

## 月度个税明细

| 月份 | 税前 | 五险一金 | 累计应税 | 税率 | 本月个税 | 累计个税 | 到手 |
|------|------|----------|----------|------|----------|----------|------|
"""

    for r in annual_results:
        report += f"| {r.month} | ¥{r.gross_income:,.0f} | ¥{r.social_insurance:,.0f} | ¥{r.taxable_income:,.0f} | {r.tax_rate*100:.0f}% | ¥{r.monthly_tax:,.0f} | ¥{r.cumulative_tax:,.0f} | ¥{r.net_income:,.0f} |\n"

    # 年终奖对比
    if bonus > 0:
        comparison = compare_bonus_methods(
            bonus, monthly_salary, social_insurance, special_deduction
        )

        report += f"""
## 年终奖计税对比（¥{bonus:,.0f}）

| 计税方式 | 月均额 | 税率 | 应纳税额 | 税后年终奖 |
|----------|--------|------|----------|-----------|
| 单独计税 | ¥{comparison['separate'].monthly_average:,.0f} | {comparison['separate'].tax_rate*100:.0f}% | ¥{comparison['separate'].tax:,.0f} | ¥{comparison['separate'].net_bonus:,.0f} |
| 合并计税 | - | {comparison['combined'].tax_rate*100:.0f}% | ¥{comparison['combined'].tax:,.0f} | ¥{comparison['combined'].net_bonus:,.0f} |

**推荐**：{'单独计税' if comparison['recommendation'] == 'separate' else '合并计税'}，可节省 ¥{comparison['savings']:,.0f}
"""

    report += f"""
---
*报告生成时间：2025年*
*税率依据：《个人所得税法》（2025年版）*
"""

    return report


# ==================== 快捷函数 ====================

def quick_calc(
    salary: float,
    social: float = 0,
    children: int = 0,
    infants: int = 0,
    education: bool = False,
    loan: bool = False,
    rent: int = 0,
    elderly: int = 0,
) -> Dict:
    """
    快速计算个税（简化版）

    Args:
        salary: 月工资
        social: 五险一金
        children: 子女数量（每人2000）
        infants: 婴幼儿数量（每人2000）
        education: 是否继续教育
        loan: 是否有房贷
        rent: 租房金额
        elderly: 赡养老人扣除额

    Returns:
        Dict: 计算结果
    """
    deduction = SpecialDeduction(
        children_education=children * 2000,
        infant_care=infants * 2000,
        continuing_education=400 if education else 0,
        housing_loan=1000 if loan else 0,
        housing_rent=rent,
        elderly_support=elderly,
    )

    result = calculate_monthly_tax(
        monthly_salary=salary,
        social_insurance=social,
        special_deduction=deduction,
    )

    return {
        "税前": salary,
        "五险一金": social,
        "专项扣除": deduction.total_monthly,
        "个税": result.monthly_tax,
        "到手": result.net_income,
        "税率": f"{result.tax_rate*100:.0f}%",
    }


# ==================== v2.0.0 新功能 ====================

# 历史税率表（用于对比）
HISTORICAL_TAX_BRACKETS = {
    2018: [  # 2018年10月前（旧税法）
        (1500, 0.03, 0),
        (4500, 0.10, 105),
        (9000, 0.20, 555),
        (35000, 0.25, 1005),
        (55000, 0.30, 2755),
        (80000, 0.35, 5505),
        (float('inf'), 0.45, 13505),
    ],
    2019: MONTHLY_TAX_BRACKETS,  # 2019年起实施新税法
    2020: MONTHLY_TAX_BRACKETS,
    2021: MONTHLY_TAX_BRACKETS,
    2022: MONTHLY_TAX_BRACKETS,
    2023: MONTHLY_TAX_BRACKETS,
    2024: MONTHLY_TAX_BRACKETS,
    2025: MONTHLY_TAX_BRACKETS,
}

# 历史起征点
HISTORICAL_THRESHOLD = {
    2018: 3500,  # 2018年10月前
    2019: 5000,  # 2018年10月起
    2020: 5000,
    2021: 5000,
    2022: 5000,
    2023: 5000,
    2024: 5000,
    2025: 5000,
}


def calculate_historical_tax(
    salary: float,
    year: int,
    social_insurance: float,
) -> Dict:
    """
    计算历史税率下的个税

    Args:
        salary: 月薪
        year: 年份
        social_insurance: 五险一金

    Returns:
        Dict: 历史个税计算结果
    """
    brackets = HISTORICAL_TAX_BRACKETS.get(year, MONTHLY_TAX_BRACKETS)
    threshold = HISTORICAL_THRESHOLD.get(year, 5000)

    # 应纳税所得额
    taxable = max(0, salary - social_insurance - threshold)

    # 计算税额
    tax = 0
    for limit, rate, deduction in brackets:
        if taxable <= limit:
            tax = taxable * rate - deduction
            break

    tax = max(0, tax)

    return {
        "年份": year,
        "税前": salary,
        "五险一金": social_insurance,
        "起征点": threshold,
        "应纳税所得额": taxable,
        "个税": tax,
        "到手": salary - social_insurance - tax,
    }


def compare_historical_tax(
    salary: float,
    social_insurance: float,
    years: List[int] = None,
) -> Dict:
    """
    对比历史税率

    Args:
        salary: 月薪
        social_insurance: 五险一金
        years: 对比年份列表

    Returns:
        Dict: 历史税率对比结果
    """
    if years is None:
        years = [2018, 2019, 2025]

    results = []
    for year in years:
        result = calculate_historical_tax(salary, year, social_insurance)
        results.append(result)

    # 找出最优年份
    best_year = min(results, key=lambda x: x["个税"])

    return {
        "对比结果": results,
        "最优年份": best_year["年份"],
        "节省个税": max(r["个税"] for r in results) - best_year["个税"],
        "建议": f"对比{years}，{best_year['年份']}年税负最低，每月节省¥{max(r['个税'] for r in results) - best_year['个税']:,.0f}",
    }


def find_bonus_trap_points() -> List[Dict]:
    """
    找出年终奖临界点（多发1块钱，少拿几千块的陷阱）

    Returns:
        List[Dict]: 临界点列表
    """
    # 年终奖税率临界点
    trap_points = [
        {"金额": 36000, "陷阱": 36001, "说明": "多发1元，多缴税¥2300"},
        {"金额": 144000, "陷阱": 144001, "说明": "多发1元，多缴税¥13000"},
        {"金额": 300000, "陷阱": 300001, "说明": "多发1元，多缴税¥13750"},
        {"金额": 420000, "陷阱": 420001, "说明": "多发1元，多缴税¥13600"},
        {"金额": 660000, "陷阱": 660001, "说明": "多发1元，多缴税¥13000"},
        {"金额": 960000, "陷阱": 960001, "说明": "多发1元，多缴税¥12800"},
    ]

    return trap_points


def check_bonus_trap(bonus: float) -> Dict:
    """
    检查年终奖是否在陷阱区间

    Args:
        bonus: 年终奖金额

    Returns:
        Dict: 检查结果
    """
    trap_points = find_bonus_trap_points()

    for trap in trap_points:
        # 检查是否在陷阱区间内（临界点+1000元内）
        if trap["金额"] < bonus < trap["金额"] + 1000:
            return {
                "状态": "⚠️ 警告",
                "问题": f"年终奖¥{bonus:,.0f}在陷阱区间",
                "建议": f"建议调整为¥{trap['金额']:,.0f}（多发1块钱会少拿几千）",
                "陷阱说明": trap["说明"],
            }

    return {
        "状态": "✅ 安全",
        "问题": "年终奖不在陷阱区间",
        "建议": "当前金额安全",
    }


def optimize_bonus_avoiding_traps(
    target_bonus: float,
    monthly_salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    优化年终奖避免陷阱（找到最近的安全金额）

    Args:
        target_bonus: 目标年终奖
        monthly_salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除

    Returns:
        Dict: 优化结果
    """
    trap_points = find_bonus_trap_points()

    # 找到最近的安全金额
    safe_amounts = []
    for i, trap in enumerate(trap_points):
        # 临界点前1000元
        safe_amounts.append(trap["金额"] - 1000)
        # 临界点后10000元
        if i < len(trap_points) - 1:
            safe_amounts.append(trap["金额"] + 10000)

    # 找到最接近目标的安全金额
    best_amount = min(
        [a for a in safe_amounts if a > 0],
        key=lambda x: abs(x - target_bonus),
    )

    # 计算两个金额的税额
    target_comparison = compare_bonus_methods(
        target_bonus, monthly_salary, social_insurance, special_deduction
    )
    best_comparison = compare_bonus_methods(
        best_amount, monthly_salary, social_insurance, special_deduction
    )

    target_tax = target_comparison['separate'].tax
    best_tax = best_comparison['separate'].tax

    return {
        "目标金额": target_bonus,
        "推荐金额": best_amount,
        "目标税额": target_tax,
        "推荐税额": best_tax,
        "节省税额": target_tax - best_tax,
        "金额差异": abs(best_amount - target_bonus),
        "建议": f"建议调整为¥{best_amount:,.0f}，节省税额¥{target_tax - best_tax:,.0f}",
    }


def batch_calculate_tax(
    employees: List[Dict],
    special_deduction: SpecialDeduction,
) -> Dict:
    """
    批量计算员工个税（HR 模式）

    Args:
        employees: 员工列表，每个员工包含 {name, salary, social_insurance, bonus}
        special_deduction: 专项附加扣除

    Returns:
        Dict: 批量计算结果
    """
    results = []
    total_gross = 0
    total_tax = 0
    total_net = 0

    for emp in employees:
        # 计算月度个税
        monthly = calculate_monthly_tax(
            emp["salary"],
            emp.get("social_insurance", 0),
            special_deduction,
        )

        # 计算年终奖（如果有）
        bonus_tax = 0
        bonus_net = 0
        if emp.get("bonus", 0) > 0:
            comparison = compare_bonus_methods(
                emp["bonus"],
                emp["salary"],
                emp.get("social_insurance", 0),
                special_deduction,
            )
            bonus_tax = comparison[comparison["recommendation"]].tax
            bonus_net = comparison[comparison["recommendation"]].net_bonus

        # 年度总计
        annual_gross = emp["salary"] * 12 + emp.get("bonus", 0)
        annual_tax = monthly.monthly_tax * 12 + bonus_tax
        annual_net = monthly.net_income * 12 + bonus_net

        results.append(
            {
                "姓名": emp["name"],
                "月薪": emp["salary"],
                "年终奖": emp.get("bonus", 0),
                "年度税前": annual_gross,
                "年度个税": annual_tax,
                "年度到手": annual_net,
                "月度个税": monthly.monthly_tax,
                "月度到手": monthly.net_income,
            }
        )

        total_gross += annual_gross
        total_tax += annual_tax
        total_net += annual_net

    return {
        "员工数量": len(employees),
        "年度税前总计": total_gross,
        "年度个税总计": total_tax,
        "年度到手总计": total_net,
        "人均个税": total_tax / len(employees) if employees else 0,
        "人均到手": total_net / len(employees) if employees else 0,
        "员工明细": results,
    }


def generate_tax_optimization_advice(
    salary: float,
    social_insurance: float,
    special_deduction: SpecialDeduction,
    bonus: float = 0,
) -> Dict:
    """
    生成税负优化建议（智能推荐）

    Args:
        salary: 月薪
        social_insurance: 五险一金
        special_deduction: 专项附加扣除
        bonus: 年终奖

    Returns:
        Dict: 优化建议
    """
    advices = []

    # 1. 检查专项扣除是否用足
    available_deductions = {
        "子女教育": 2000,
        "婴幼儿照护": 2000,
        "继续教育": 400,
        "住房贷款利息": 1000,
        "住房租金": 1500,
        "赡养老人": 3000,
    }

    unused = []
    for name, amount in available_deductions.items():
        if getattr(special_deduction, name.replace("子女教育", "children_education")
                                          .replace("婴幼儿照护", "infant_care")
                                          .replace("继续教育", "continuing_education")
                                          .replace("住房贷款利息", "housing_loan")
                                          .replace("住房租金", "housing_rent")
                                          .replace("赡养老人", "elderly_support"), 0) == 0:
            unused.append(name)

    if unused:
        advices.append(
            {
                "类型": "专项扣除",
                "建议": f"未使用的扣除项：{', '.join(unused)}",
                "潜在节省": f"每月最多可节省¥{sum(available_deductions.values()) * 0.2:,.0f}个税",
            }
        )

    # 2. 检查年终奖陷阱
    if bonus > 0:
        trap_check = check_bonus_trap(bonus)
        if "⚠️" in trap_check["状态"]:
            advices.append(
                {
                    "类型": "年终奖陷阱",
                    "建议": trap_check["建议"],
                    "潜在节省": "数千元",
                }
            )

    # 3. 年终奖计税方式
    if bonus > 0:
        comparison = compare_bonus_methods(
            bonus, salary, social_insurance, special_deduction
        )
        if comparison["savings"] > 0:
            advices.append(
                {
                    "类型": "年终奖计税",
                    "建议": f"建议使用{'单独' if comparison['recommendation'] == 'separate' else '合并'}计税",
                    "节省金额": f"¥{comparison['savings']:,.0f}",
                }
            )

    # 4. 社保公积金基数优化
    if social_insurance < salary * 0.2:
        advices.append(
            {
                "类型": "社保公积金",
                "建议": "当前五险一金较低，可考虑提高缴费基数",
                "潜在收益": "退休金增加 + 医保账户增加",
            }
        )

    # 5. 年度汇算清缴提醒
    advices.append(
        {
            "类型": "年度汇算",
            "建议": "每年3-6月进行年度汇算清缴，可能退税",
            "注意事项": "劳务报酬、稿酬等需要汇总计税",
        }
    )

    return {
        "优化建议": advices,
        "总结": f"共{len(advices)}条建议，可有效降低税负",
    }


def generate_batch_excel_data(
    employees: List[Dict],
    special_deduction: SpecialDeduction,
) -> str:
    """
    生成批量计算 Excel 数据（CSV 格式）

    Args:
        employees: 员工列表
        special_deduction: 专项附加扣除

    Returns:
        str: CSV 格式数据
    """
    batch_result = batch_calculate_tax(employees, special_deduction)

    # CSV 头
    csv = "姓名,月薪,年终奖,年度税前,月度个税,月度到手,年度个税,年度到手\n"

    # CSV 数据
    for emp in batch_result["员工明细"]:
        csv += f"{emp['姓名']},{emp['月薪']:.2f},{emp['年终奖']:.2f},"
        csv += f"{emp['年度税前']:.2f},{emp['月度个税']:.2f},"
        csv += f"{emp['月度到手']:.2f},{emp['年度个税']:.2f},"
        csv += f"{emp['年度到手']:.2f}\n"

    # 汇总
    csv += "\n汇总\n"
    csv += f"员工数量,{batch_result['员工数量']}\n"
    csv += f"年度税前总计,{batch_result['年度税前总计']:.2f}\n"
    csv += f"年度个税总计,{batch_result['年度个税总计']:.2f}\n"
    csv += f"年度到手总计,{batch_result['年度到手总计']:.2f}\n"
    csv += f"人均个税,{batch_result['人均个税']:.2f}\n"
    csv += f"人均到手,{batch_result['人均到手']:.2f}\n"

    return csv


if __name__ == "__main__":
    # 测试用例
    print("=" * 60)
    print("中国个税计算器测试 v1.3.0")
    print("=" * 60)

    # 测试1：月度个税
    deduction = SpecialDeduction(
        children_education=2000,
        housing_loan=1000,
        elderly_support=1000,
    )

    result = quick_calc(
        salary=30000,
        social=4500,
        children=1,
        loan=True,
        elderly=1000,
    )

    print("\n测试1：月度个税计算")
    for k, v in result.items():
        print(f"  {k}: {v}")

    # 测试2：年终奖对比
    print("\n测试2：年终奖计税对比")
    comparison = compare_bonus_methods(
        bonus=60000,
        monthly_salary=20000,
        social_insurance=3000,
        special_deduction=deduction,
    )

    print(f"  单独计税: ¥{comparison['separate'].tax:,.0f} (税后 ¥{comparison['separate'].net_bonus:,.0f})")
    print(f"  合并计税: ¥{comparison['combined'].tax:,.0f} (税后 ¥{comparison['combined'].net_bonus:,.0f})")
    print(f"  推荐: {comparison['recommendation']}, 节省 ¥{comparison['savings']:,.0f}")

    # 测试3：反推税前
    print("\n测试3：反推税前工资")
    gross = reverse_gross_from_net(
        target_net=25000,
        social_insurance=4000,
        special_deduction=deduction,
    )
    print(f"  目标到手: ¥25,000")
    print(f"  需要税前: ¥{gross:,.2f}")
    
    # 测试4：年度汇算清缴
    print("\n测试4：年度汇算清缴")
    income = IncomeSource(
        salary=360000,  # 年薪30k*12
        labor_income=20000,  # 劳务报酬
        royalty_income=10000,  # 稿酬
    )
    settlement = calculate_annual_settlement(
        income_sources=income,
        annual_social_insurance=54000,  # 4500*12
        special_deduction=deduction,
        prepaid_tax=25000,  # 已预缴
    )
    print(f"  综合所得: ¥{settlement.comprehensive_income:,.0f}")
    print(f"  应纳税额: ¥{settlement.annual_tax:,.0f}")
    print(f"  已预缴: ¥{settlement.prepaid_tax:,.0f}")
    print(f"  {settlement.status_text}")
    
    # 测试5：年终奖优化
    print("\n测试5：年终奖智能优化")
    optimization = optimize_bonus_allocation(
        total_bonus=100000,
        monthly_salary=20000,
        social_insurance=3000,
        special_deduction=deduction,
    )
    print(f"  年终奖总额: ¥{optimization.total_bonus:,.0f}")
    print(f"  最优方案总税额: ¥{optimization.total_tax:,.0f}")
    print(f"  最差方案总税额: ¥{optimization.worst_tax:,.0f}")
    print(f"  节省: ¥{optimization.savings:,.0f}")
    print(f"  最优分配:")
    for split in optimization.optimal_split:
        print(f"    - ¥{split['amount']:,.0f} ({split['method']}, 税额 ¥{split['tax']:,.0f})")
    
    # 测试6：跳槽薪资谈判
    print("\n测试6：跳槽薪资谈判")
    negotiation = calculate_salary_negotiation(
        target_net=25000,
        social_insurance=4000,
        special_deduction=deduction,
    )
    print(f"  目标税后: ¥{negotiation['目标税后']:,.0f}")
    print(f"  需要税前: ¥{negotiation['需要税前']:,.0f}")
    print(f"  {negotiation['建议话术']}")
    
    # 测试7：Offer对比
    print("\n测试7：Offer对比")
    offers = [
        {"name": "A公司", "salary": 25000, "social_insurance": 4000, "bonus": 50000},
        {"name": "B公司", "salary": 28000, "social_insurance": 4500, "bonus": 30000},
        {"name": "C公司", "salary": 22000, "social_insurance": 3500, "bonus": 80000},
    ]
    comparison = compare_job_offers(offers, deduction)
    print(f"  推荐选择: {comparison['推荐选择']}")
    print(f"  年度到手差额: ¥{comparison['年度到手差额']:,.0f}")
    print("\n  各Offer详情:")
    for r in comparison['对比结果']:
        print(f"    {r['排名']}. {r['名称']}: 月薪¥{r['月薪']:,.0f}, 年度到手¥{r['年度总到手']:,.0f}")
    
    # v1.2.0 新功能测试
    print("\n" + "=" * 60)
    print("v1.2.0 新功能测试")
    print("=" * 60)
    
    print("\n测试8：涨薪效果分析")
    raise_effect = calculate_raise_effect(
        current_salary=20000,
        raise_percentage=20,
        social_insurance=3000,
        special_deduction=deduction,
    )
    print(f"  涨薪前: 税前¥{raise_effect['涨薪前']['税前']:,.0f}, 到手¥{raise_effect['涨薪前']['到手']:,.0f}")
    print(f"  涨薪后: 税前¥{raise_effect['涨薪后']['税前']:,.0f}, 到手¥{raise_effect['涨薪后']['到手']:,.0f}")
    print(f"  {raise_effect['建议']}")
    
    print("\n测试9：快速模板")
    print(f"  可用模板: {', '.join(list_templates())}")
    template_result = quick_calc_with_template(
        salary=25000,
        social=4000,
        template_name="已婚一孩",
    )
    print(f"  模板[{template_result['模板']}]: 税前¥{template_result['税前']:,.0f}, 到手¥{template_result['到手']:,.0f}")
    
    print("\n测试10：交互式问答")
    answers = {
        "salary": 30000,
        "social": 4500,
        "children": 1,
        "has_loan": True,
        "rent": 0,
        "elderly_type": "非独生",
        "education": False,
        "bonus": 60000,
    }
    interactive_result = interactive_tax_calculator(answers)
    print(f"  月度到手: ¥{interactive_result['月度']['到手']:,.0f}")
    print(f"  年度到手: ¥{interactive_result['年度']['到手']:,.0f}")
    print(f"  年终奖推荐: {interactive_result['年终奖']['推荐']}")
    
    print("\n测试11：飞书文档报告")
    feishu_report = generate_feishu_report(
        salary=30000,
        social=4500,
        deduction=deduction,
        bonus=60000,
    )
    # 只打印报告前10行
    report_lines = feishu_report.split('\n')[:10]
    print("  报告预览（前10行）:")
    for line in report_lines:
        print(f"    {line}")
    print("  ... (完整报告已生成)")
    
    # v1.3.0 新功能测试
    print("\n" + "=" * 60)
    print("v1.3.0 新功能测试")
    print("=" * 60)
    
    print("\n测试12：社保公积金计算器")
    print(f"  支持城市: {', '.join(list_supported_cities())}")
    social_result = calculate_social_insurance(
        salary=30000,
        city="北京",
    )
    print(f"  北京月薪30k:")
    print(f"    缴费基数: ¥{social_result.adjusted_base:,.0f}")
    print(f"    个人缴纳: ¥{social_result.total_personal:,.0f}")
    print(f"    公司缴纳: ¥{social_result.total_company:,.0f}")
    
    print("\n测试13：可视化图表")
    chart = generate_tax_distribution_chart(30000, 4500, deduction)
    print(chart)
    
    print("\n测试14：年终奖规划")
    bonus_plan = plan_bonus_thresholds(20000, 3000, deduction)
    print(f"  {bonus_plan['建议']}")
    print(f"  临界点: {len(bonus_plan['临界点'])} 个")
    
    print("\n测试15：Excel 导出")
    excel_data = generate_excel_data(30000, 4500, deduction, 60000)
    print("  Excel 数据已生成（CSV 格式）")
    print(f"  数据行数: {len(excel_data.split(chr(10)))} 行")
    
    # v2.0.0 新功能测试
    print("\n" + "=" * 60)
    print("v2.0.0 新功能测试")
    print("=" * 60)
    
    print("\n测试16：历史税率对比")
    historical = compare_historical_tax(30000, 4500, [2018, 2019, 2025])
    print(f"  {historical['建议']}")
    print(f"  2018年个税: ¥{historical['对比结果'][0]['个税']:,.0f}")
    print(f"  2019年个税: ¥{historical['对比结果'][1]['个税']:,.0f}")
    print(f"  2025年个税: ¥{historical['对比结果'][2]['个税']:,.0f}")
    
    print("\n测试17：年终奖陷阱检查")
    trap = check_bonus_trap(36001)
    print(f"  年终奖36,001元:")
    print(f"    {trap['状态']}: {trap['问题']}")
    print(f"    {trap['建议']}")
    
    trap_safe = check_bonus_trap(36000)
    print(f"  年终奖36,000元:")
    print(f"    {trap_safe['状态']}: {trap_safe['建议']}")
    
    print("\n测试18：年终奖陷阱优化")
    optimization = optimize_bonus_avoiding_traps(36001, 20000, 3000, deduction)
    print(f"  目标: ¥{optimization['目标金额']:,.0f}")
    print(f"  推荐: ¥{optimization['推荐金额']:,.0f}")
    print(f"  {optimization['建议']}")
    
    print("\n测试19：批量计算（HR模式）")
    employees = [
        {"name": "张三", "salary": 30000, "social_insurance": 4500, "bonus": 60000},
        {"name": "李四", "salary": 25000, "social_insurance": 4000, "bonus": 50000},
        {"name": "王五", "salary": 20000, "social_insurance": 3000, "bonus": 30000},
    ]
    batch = batch_calculate_tax(employees, deduction)
    print(f"  员工数量: {batch['员工数量']}")
    print(f"  年度税前总计: ¥{batch['年度税前总计']:,.0f}")
    print(f"  年度个税总计: ¥{batch['年度个税总计']:,.0f}")
    print(f"  年度到手总计: ¥{batch['年度到手总计']:,.0f}")
    print(f"  人均个税: ¥{batch['人均个税']:,.0f}")
    print(f"  人均到手: ¥{batch['人均到手']:,.0f}")
    
    print("\n测试20：税负优化建议")
    advice = generate_tax_optimization_advice(30000, 4500, deduction, 36001)
    print(f"  {advice['总结']}")
    for i, a in enumerate(advice['优化建议'][:3], 1):
        print(f"  {i}. [{a['类型']}] {a['建议']}")
    
    print("\n" + "=" * 60)
    print("所有测试完成！v2.0.0 新功能测试通过")
    print("=" * 60)
