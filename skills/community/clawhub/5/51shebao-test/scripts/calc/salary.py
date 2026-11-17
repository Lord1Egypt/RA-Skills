"""工资个税计算器（累计预扣预缴法）。
移植自 hr-tool：SalaryServiceImpl + CalculatorUtil + PersonIncomeTaxEnum。
五险一金由原保险中台 Feign 改为用户手动传入月度个人缴纳额。
"""
from decimal import Decimal

from .constants import SALARY_TAX_LEVELS, THRESHOLD
from .util import r2

D = Decimal


def get_level(taxable: Decimal):
    """累计应纳税所得额定档 → (预扣率, 速算扣除数)。
    档位语义与 PersonIncomeTaxEnum.getLevel 一致：(min, max] 右闭。"""
    for upper, rate, quick in SALARY_TAX_LEVELS:
        if upper is None or taxable <= upper:
            return rate, quick
    raise AssertionError("unreachable")


def _cumulative_tax(taxable: Decimal) -> Decimal:
    """累计应纳税额 = 所得额 * 税率 - 速算扣除数，下限 0"""
    rate, quick = get_level(taxable)
    tax = taxable * rate - quick
    return tax if tax > 0 else D("0.00")


def _paid_tax_before(before_tax: Decimal, periods: int, social_ee: Decimal,
                     fund_ee: Decimal, five_monthly: Decimal) -> Decimal:
    """前 (periods-1) 月累计已缴税额（CalculatorUtil.beforePersonIncomeTax）。
    与原实现一致：此处不扣除个人养老金。"""
    if periods <= 1:
        return D("0.00")
    n = D(periods - 1)
    taxable = (r2(before_tax * n) - r2(THRESHOLD * n) - r2(five_monthly * n)
               - r2(fund_ee * n) - r2(social_ee * n))
    if taxable < 0:
        taxable = D("0.00")
    return _cumulative_tax(taxable)


def salary_calculation(before_tax: Decimal, periods: int = 1,
                       social_ee: Decimal = D("0"), fund_ee: Decimal = D("0"),
                       child_edu: Decimal = D("0"), continue_edu: Decimal = D("0"),
                       serious_medical: Decimal = D("0"), house: Decimal = D("0"),
                       elder: Decimal = D("0"), infant_care: Decimal = D("0"),
                       personal_pension: Decimal = D("0")) -> dict:
    """工资个税正算：输入月度税前收入与扣除项，返回当期结果 dict（金额字段为 str）。"""
    n = D(periods)
    cumulative_income = r2(before_tax * n)
    cumulative_deduction = r2(THRESHOLD * n)
    five_monthly = r2(child_edu + continue_edu + serious_medical + house + elder + infant_care)
    five_total = r2(five_monthly * n)
    fund_total = r2(fund_ee * n)
    social_total = r2(social_ee * n)
    pension_total = r2(r2(personal_pension) * n)

    taxable = (cumulative_income - cumulative_deduction - five_total
               - fund_total - social_total - pension_total)
    if taxable < 0:
        taxable = D("0.00")

    rate, quick = get_level(taxable)
    paid_before = _paid_tax_before(before_tax, periods, social_ee, fund_ee, five_monthly)
    tax = taxable * rate - quick - paid_before          # 保持未舍入（与原实现一致）
    after = before_tax - tax - fund_ee - social_ee      # 到手用未舍入税额，最后舍入
    tax_rate_pct = str((rate * D("100.00")).quantize(D("1")))

    return {
        "before_tax_income": str(r2(before_tax)),
        "after_tax_income": str(r2(after)),
        "personal_income_tax": str(r2(tax)),
        "taxable_income": str(r2(taxable)),
        "tax_rate": tax_rate_pct,
        "quick_deduction": str(quick),
        "threshold": str(THRESHOLD),
        "social_ee_sum": str(r2(social_ee)),
        "fund_ee_amount": str(r2(fund_ee)),
        "five_deduction": {
            "child_edu": str(child_edu),
            "continue_edu": str(continue_edu),
            "serious_medical": str(serious_medical),
            "house": str(house),
            "elder": str(elder),
            "infant_care": str(infant_care),
            "monthly_total": str(five_monthly),
            "total": str(five_total),
        },
        "personal_pension_total": str(pension_total),
        "periods_count": str(periods),
    }


def reverse_salary_calculation(after_tax: Decimal, periods: int = 1, **kwargs) -> dict:
    """到手反推税前：二分查找（对应 SalaryServiceImpl.searchBeforeTaxIncome）。
    初始区间 [after, 2*after]，到手误差 ±1 元内收敛；不收敛返回 0.00。"""
    start, end = r2(after_tax), r2(after_tax * D("2"))
    found = D("0.00")
    while start < end:
        mid = r2((start + end) / D("2.00"))
        est_after = D(salary_calculation(mid, periods, **kwargs)["after_tax_income"])
        diff = est_after - after_tax
        if D("-1.00") <= diff <= D("1.00"):
            found = mid
            break
        if est_after < after_tax:
            start = mid
        else:
            end = mid
    result = salary_calculation(found, periods, **kwargs)
    result["before_tax_income"] = str(r2(found))
    result["after_tax_income"] = str(r2(after_tax))
    return result
