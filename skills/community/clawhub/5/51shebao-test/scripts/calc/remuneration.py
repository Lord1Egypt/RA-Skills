"""劳务报酬 / 稿酬 / 特许权使用费 / 解除劳动合同一次性补偿金计算器。
移植自 hr-tool：RemunerationServiceImpl + laborRemuneration-*.ql +
AuthorRemunConstant + PersonalPrivilegeFeeConstant。
注意：原 Java 劳务报酬实现执行 incomeTax.ql 时误传 context（疑似 bug），
此处按正确逻辑实现，由教科书测试用例锁定（见 test_calc.TestLabor）。
"""
from decimal import Decimal

from .constants import (DEDUCTION_800, LABOR_08, LABOR_800, LABOR_TAX_LEVELS,
                        RATE_20, RATIO_70, RATIO_80, SCOPE_TWO_MIN)
from .salary import get_level
from .util import r2

D = Decimal


def _labor_tax(taxable: Decimal):
    """劳务报酬预扣税额 → (税额(2位), 速算扣除数str, 预扣率str)"""
    for upper, rate, quick in LABOR_TAX_LEVELS:
        if upper is None or taxable <= upper:
            return r2(taxable * rate - quick), str(quick), f"{int(rate * 100)}%"
    raise AssertionError("unreachable")


def labor_calculate(before_tax: Decimal) -> dict:
    """劳务报酬正算（laborRemuneration-taxableIncome.ql + incomeTax.ql）"""
    if before_tax is None or before_tax <= 0:
        raise ValueError("税前收入必须大于 0")
    before = r2(before_tax)
    if before <= LABOR_800:
        taxable = D("0")
        formula = "免税"
    elif before <= D("4000"):
        taxable = r2(before - LABOR_800)
        formula = f"税前收入({before}) - 800.00"
    else:
        taxable = r2(before * LABOR_08)
        formula = f"税前收入({before}) * (1-20%)"

    if taxable <= 0:
        return {
            "before_tax_income": str(before),
            "after_tax_income": str(before),
            "income_tax": "0",
            "taxable_income": "0",
            "taxable_income_formula": formula,
            "quick_calc_deduction": "",
            "withholding_rate": "",
        }
    tax, quick, rate = _labor_tax(taxable)
    return {
        "before_tax_income": str(before),
        "after_tax_income": str(before - tax),
        "income_tax": str(tax),
        "taxable_income": str(taxable),
        "taxable_income_formula": formula,
        "quick_calc_deduction": quick,
        "withholding_rate": rate,
    }


def reverse_labor_calculate(after_tax: Decimal) -> dict:
    """劳务报酬反推（laborRemuneration-beforeTaxIncome.ql 分段公式，再走正算）"""
    after = after_tax
    if after < D("800"):
        before = after
    elif after < D("3360"):
        before = (after - D("160")) / D("0.8")
    elif after < D("21000"):
        before = after / D("0.84")
    elif after < D("49500"):
        before = (after - D("2000")) / D("0.76")
    else:
        before = (after - D("7000")) / D("0.68")
    return labor_calculate(r2(before))


def author_calculate(before_tax: Decimal) -> dict:
    """稿酬正算：所得额 (收入-800)*70% 或 收入*80%*70%；税 = 所得额*20%"""
    before = before_tax
    if D("0") < before <= SCOPE_TWO_MIN:
        taxable = r2((before - DEDUCTION_800) * RATIO_70)
        formula = f"[税前收入({before}) - 800] * 70% "
    else:
        taxable = r2(before * RATIO_80 * RATIO_70)
        formula = f"税前收入({before}) * (1-20%) * 70%"
    tax = r2(taxable * RATE_20)
    return {
        "before_tax_income": str(r2(before)),
        "after_tax_income": str(r2(before - tax)),
        "income_tax": str(tax),
        "taxable_income": str(taxable),
        "taxable_income_formula": formula,
        "quick_calc_deduction": "0.00",
        "withholding_rate": "20%",
    }


def privilege_calculate(before_tax: Decimal) -> dict:
    """特许权使用费正算：所得额 收入-800 或 收入*80%；税 = 所得额*20%"""
    before = before_tax
    if D("0") < before <= SCOPE_TWO_MIN:
        taxable = r2(before - DEDUCTION_800)
        formula = f"税前收入({before}) - 800.00 "
    else:
        taxable = r2(before * RATIO_80)
        formula = f"税前收入({before}) * (1-20%)"
    tax = r2(taxable * RATE_20)
    return {
        "before_tax_income": str(r2(before)),
        "after_tax_income": str(r2(before - tax)),
        "income_tax": str(tax),
        "taxable_income": str(taxable),
        "taxable_income_formula": formula,
        "quick_calc_deduction": "0.00",
        "withholding_rate": "20%",
    }


def reverse_privilege_calculate(after_tax: Decimal) -> dict:
    """特许权使用费反推（与原实现一致的双候选分支判断）"""
    after = after_tax
    one = r2((after - D("160")) / D("0.8"))
    two = r2(after / D("0.84"))
    if D("0") < one <= SCOPE_TWO_MIN:
        before = one
        taxable = r2(before - DEDUCTION_800)
        formula = f"税前收入({before}) - 800 "
    else:
        before = two
        taxable = r2(before * RATIO_80)
        formula = f"税前收入({before}) * (1-20%)"
    tax = r2(taxable * RATE_20)
    return {
        "before_tax_income": str(r2(before)),
        "after_tax_income": str(r2(before - tax)),
        "income_tax": str(tax),
        "taxable_income": str(taxable),
        "taxable_income_formula": formula,
        "quick_calc_deduction": "0.00",
        "withholding_rate": "20%",
    }


def compensation_calculate(before_tax: Decimal, avg_salary: Decimal) -> dict:
    """解除劳动合同一次性补偿金：免税额 = 上年月平均工资 * 12 * 3，
    超出部分按综合所得年度 7 级税率表计税（RemunerationServiceImpl.calculLumpNumCompensation）。"""
    before = before_tax
    tax_free = avg_salary * D("12") * D("3")
    result = {
        "before_tax_income": str(r2(before)),
        "after_tax_income": "0.00",
        "income_tax": "0.00",
        "taxable_income": "0.00",
        "taxable_income_formula": "",
        "quick_calc_deduction": "0.00",
        "withholding_rate": "0%",
        "last_year_city_avg_salary": str(r2(avg_salary)),
    }
    if before <= tax_free:
        result["after_tax_income"] = str(r2(before))
        return result
    taxable = before - tax_free
    rate, quick = get_level(taxable)
    tax = r2(taxable * rate - quick)
    result.update({
        "after_tax_income": str(r2(before - tax)),
        "income_tax": str(tax),
        "taxable_income": str(r2(taxable)),
        "taxable_income_formula":
            f"[一次性补偿收入({before}) - 上年月平均({avg_salary}) * 12 * 3)]",
        "quick_calc_deduction": str(quick),
        "withholding_rate": f"{int(rate * 100)}%",
    })
    return result
