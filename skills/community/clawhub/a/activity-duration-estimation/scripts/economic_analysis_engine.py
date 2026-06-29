"""
economic_analysis_engine — 经济效益分析引擎

支持：ROI（静态/加权）、PBP（静态/动态）、NPV、IRR（插值）、BCR
多折现率对比，逐年现金流分析。
验证基准：小作坊例子（初始100万，年维护5万，年收益12万，5年，终值200万）
"""
import math


# ═══════════════════════════════════════════════════════
# 核心参数类
# ═══════════════════════════════════════════════════════

class EconomicParams:
    """经济效益分析输入参数"""
    def __init__(
        self,
        initial_investment: float,
        annual_revenue: float,
        annual_cost: float,
        periods: int,
        terminal_value: float = 0,
        discount_rate: float = 10.0,
        currency: str = "¥",
        name: str = "未命名项目",
    ):
        self.initial_investment = initial_investment
        self.annual_revenue = annual_revenue
        self.annual_cost = annual_cost
        self.periods = periods
        self.terminal_value = terminal_value
        self.discount_rate = discount_rate
        self.currency = currency
        self.name = name

    @property
    def annual_net(self) -> float:
        return self.annual_revenue - self.annual_cost


# ═══════════════════════════════════════════════════════
# 计算结果
# ═══════════════════════════════════════════════════════

class EconomicResult:
    """封装的完整计算结果"""
    def __init__(self):
        # 基础参数
        self.initial_investment: float = 0
        self.annual_revenue: float = 0
        self.annual_cost: float = 0
        self.periods: int = 0
        self.terminal_value: float = 0
        self.discount_rate: float = 10.0
        self.currency: str = "¥"
        self.project_name: str = ""

        # 静态指标
        self.roi_static: float = 0.0       # 年利润率
        self.roi_weighted: float = 0.0     # 加权ROI（含终值）
        self.pbp_static: float = 0.0       # 静态回收期

        # 动态指标
        self.npv: float = 0.0
        self.irr: float = 0.0
        self.bcr: float = 0.0
        self.pbp_dynamic: float = 0.0

        # 逐年现金流明细
        self.cashflows: list[dict] = []

        # 多折现率对比
        self.discount_comparison: dict = {}

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "currency": self.currency,
            "initial_investment": self.initial_investment,
            "annual_revenue": self.annual_revenue,
            "annual_cost": self.annual_cost,
            "annual_net": self.annual_revenue - self.annual_cost,
            "periods": self.periods,
            "terminal_value": self.terminal_value,
            "discount_rate": self.discount_rate,
            "roi_static": round(self.roi_static, 2),
            "roi_weighted": round(self.roi_weighted, 2),
            "npv": round(self.npv, 2),
            "irr": round(self.irr, 2),
            "bcr": round(self.bcr, 4),
            "pbp_static": round(self.pbp_static, 2),
            "pbp_dynamic": round(self.pbp_dynamic, 2),
            "cashflows": self.cashflows,
            "discount_comparison": self.discount_comparison,
        }


# ═══════════════════════════════════════════════════════
# 核心计算方法
# ═══════════════════════════════════════════════════════

def _discount_factor(rate: float, period: int) -> float:
    """折现因子 1/(1+r)^n"""
    return 1.0 / ((1 + rate / 100.0) ** period)


def calc_pbp_static(params: EconomicParams) -> float:
    """静态投资回收期"""
    annual = params.annual_net
    # 每年回报相同的情况
    if annual > 0 and params.initial_investment > 0:
        simple_pbp = params.initial_investment / annual
    else:
        simple_pbp = float("inf")

    # 计算考虑终值的精确回收期
    cum = -params.initial_investment
    for y in range(1, params.periods + 1):
        cf = annual
        if y == params.periods:
            cf += params.terminal_value
        cum += cf
        if cum >= 0:
            prev_cum = cum - cf
            pbp = y - 1 + abs(prev_cum) / cf
            return pbp

    return simple_pbp


def calc_npv(params: EconomicParams) -> float:
    """净现值 NPV = Σ(净现金流折现) - 初始投资"""
    total_discounted = 0.0
    for y in range(1, params.periods + 1):
        cf = params.annual_net
        if y == params.periods:
            cf += params.terminal_value
        total_discounted += cf * _discount_factor(params.discount_rate, y)
    return total_discounted - params.initial_investment


def calc_npv_with_rate(params: EconomicParams, rate: float) -> tuple[float, float]:
    """
    指定折现率计算NPV
    返回: (npv, total_discounted_revenue)
    """
    total_discounted = 0.0
    for y in range(1, params.periods + 1):
        cf = params.annual_net
        if y == params.periods:
            cf += params.terminal_value
        total_discounted += cf * _discount_factor(rate, y)
    npv = total_discounted - params.initial_investment
    return npv, total_discounted


def calc_irr(params: EconomicParams) -> float:
    """内部收益率（插值法）"""
    # 找两个边界值：NPV为正的利率和NPV为负的利率
    low_rate, high_rate = 0.0, 100.0
    low_npv, _ = calc_npv_with_rate(params, low_rate)
    high_npv, _ = calc_npv_with_rate(params, high_rate)

    # 如果两端同号，放宽边界
    if low_npv * high_npv >= 0:
        max_iter = 50
        while low_npv > 0 and max_iter > 0:
            high_rate *= 2
            high_npv, _ = calc_npv_with_rate(params, high_rate)
            max_iter -= 1
        while high_npv < 0 and max_iter > 0:
            low_rate /= 2
            low_npv, _ = calc_npv_with_rate(params, low_rate)
            max_iter -= 1
        if low_npv * high_npv >= 0:
            return 0.0  # 无法确定IRR

    # 二分法求IRR
    for _ in range(50):
        mid = (low_rate + high_rate) / 2
        mid_npv, _ = calc_npv_with_rate(params, mid)
        if abs(mid_npv) < 1e-6:
            return mid
        if mid_npv * low_npv > 0:
            low_rate = mid
            low_npv = mid_npv
        else:
            high_rate = mid
            high_npv = mid_npv

    return (low_rate + high_rate) / 2


def calc_bcr(params: EconomicParams) -> float:
    """
    效益成本比 BCR = Σ净现金流折现 / Σ折现成本
    其中折现成本 = 初始投资折现 + Σ年支出折现（用户表格约定）
    """
    total_net_discounted = 0.0
    total_cost_discounted = 0.0

    for y in range(1, params.periods + 1):
        df = _discount_factor(params.discount_rate, y)
        # 净现金流折现 = (年收益 - 年支出) × 折现因子
        net_cf = params.annual_revenue - params.annual_cost
        if y == params.periods:
            net_cf += params.terminal_value
        total_net_discounted += net_cf * df

        # 折现成本 = 初始投资（折现到第1年）+ 年支出折现
        cost_cf = (params.initial_investment if y == 1 else 0) + params.annual_cost
        total_cost_discounted += cost_cf * df

    return total_net_discounted / total_cost_discounted if total_cost_discounted != 0 else 0


def calc_pbp_dynamic(params: EconomicParams) -> float:
    """动态投资回收期"""
    annual = params.annual_net
    cum_discounted = -params.initial_investment
    prev_cum = cum_discounted

    for y in range(1, params.periods + 1):
        cf = annual
        if y == params.periods:
            cf += params.terminal_value
        disc_cf = cf * _discount_factor(params.discount_rate, y)
        cum_discounted += disc_cf
        if cum_discounted >= 0:
            pbp = y - 1 + abs(prev_cum) / disc_cf
            return pbp
        prev_cum = cum_discounted

    return float(params.periods + 1)


def calc_roi_static(params: EconomicParams) -> float:
    """静态 ROI（年利润率）"""
    if params.initial_investment == 0:
        return 0.0
    return (params.annual_net / params.initial_investment) * 100


def calc_roi_weighted(params: EconomicParams) -> float:
    """
    加权 ROI（考虑终值）
    公式: (年净利×(n-1) + (第n年净现金流含终值-初始投资)/n) / 初始投资 × 100%
    """
    if params.initial_investment == 0:
        return 0.0
    annual_net = params.annual_net
    n = params.periods
    # 第n年总净现金流
    final_cf = annual_net + params.terminal_value
    numerator = annual_net * (n - 1) + (final_cf - params.initial_investment) / n
    return (numerator / params.initial_investment) * 100


# ═══════════════════════════════════════════════════════
# 逐年现金流计算
# ═══════════════════════════════════════════════════════

def calc_cashflows(params: EconomicParams) -> list[dict]:
    """计算逐年现金流明细"""
    cfs = []
    for y in range(1, params.periods + 1):
        revenue = params.annual_revenue
        cost = params.annual_cost
        net = revenue - cost
        if y == params.periods:
            net += params.terminal_value
        df = _discount_factor(params.discount_rate, y)
        disc_net = net * df
        # 折现成本 = 折现的年成本 + 初始投资的分摊
        disc_cost = (params.initial_investment * _discount_factor(params.discount_rate, y)
                     if y == 1 else 0) + params.annual_cost * df
        cfs.append({
            "year": y,
            "revenue": revenue,
            "cost": cost,
            "net_cashflow": net,
            "net_discounted": round(disc_net, 2),
            "discounted_cost": round(disc_cost, 2) if y == 1
                               else round(params.annual_cost * df, 2),
        })
    return cfs


def calc_discount_comparison(params: EconomicParams, rates: list[float] = None) -> dict:
    """多折现率对比分析"""
    if rates is None:
        rates = [5, 8, 10, 12, 15, 18, 20, 25, 30]

    results = {}
    for r in rates:
        p = EconomicParams(
            params.initial_investment, params.annual_revenue,
            params.annual_cost, params.periods,
            params.terminal_value, r, params.currency, params.name
        )
        npv = calc_npv_with_rate(p, r)[0]
        bcr = calc_bcr(p)
        results[str(r)] = {
            "rate": r,
            "npv": round(npv, 2),
            "bcr": round(bcr, 4),
            "pbp_dynamic": round(calc_pbp_dynamic(p), 2),
        }

    return results


# ═══════════════════════════════════════════════════════
# 综合计算入口
# ═══════════════════════════════════════════════════════

def run_analysis(params: EconomicParams) -> EconomicResult:
    """一次性完成全部经济效益分析计算"""
    result = EconomicResult()

    # 基础参数
    result.project_name = params.name
    result.initial_investment = params.initial_investment
    result.annual_revenue = params.annual_revenue
    result.annual_cost = params.annual_cost
    result.periods = params.periods
    result.terminal_value = params.terminal_value
    result.discount_rate = params.discount_rate
    result.currency = params.currency

    # 静态指标
    result.roi_static = calc_roi_static(params)
    result.roi_weighted = calc_roi_weighted(params)
    result.pbp_static = calc_pbp_static(params)

    # 动态指标
    result.npv = calc_npv(params)
    result.irr = calc_irr(params)
    result.bcr = calc_bcr(params)
    result.pbp_dynamic = calc_pbp_dynamic(params)

    # 现金流明细
    result.cashflows = calc_cashflows(params)

    # 多折现率对比
    result.discount_comparison = calc_discount_comparison(params)

    return result


# ═══════════════════════════════════════════════════════
# 验证：小作坊例子
# ═══════════════════════════════════════════════════════

def verify_example():
    """验证小作坊例子的计算结果"""
    params = EconomicParams(
        initial_investment=100,
        annual_revenue=12,
        annual_cost=5,
        periods=5,
        terminal_value=200,
        discount_rate=10,
        name="小作坊",
    )
    r = run_analysis(params)

    print("═" * 50)
    print(f"验证：小作坊例子")
    print(f"  ROI(静态) = {r.roi_static:.2f}%  (预期 7.00%)")
    print(f"  ROI(加权) = {r.roi_weighted:.2f}%  (预期 49.40%)")
    print(f"  PBP(静态) = {r.pbp_static:.2f}年 (预期 4.33年)")
    print(f"  NPV(i=10%) = {r.npv:.2f}    (预期 50.72)")
    print(f"  BCR(i=10%) = {r.bcr:.4f}   (预期 1.37)")
    print(f"  IRR       = {r.irr:.2f}%  (预期 20.39%)")
    print(f"  PBP(动态) = {r.pbp_dynamic:.2f}年 (预期 4.61年)")
    print()

    # 逐年验证
    print("  逐年现金流:")
    for cf in r.cashflows:
        print(f"    第{cf['year']}年: 净={cf['net_cashflow']}, "
              f"折现={cf['net_discounted']}, 折现成本={cf['discounted_cost']}")

    print()
    print("  多折现率对比:")
    for rate, data in sorted(r.discount_comparison.items(), key=lambda x: float(x[0])):
        print(f"    i={rate}%: NPV={data['npv']}, BCR={data['bcr']}, "
              f"PBP(动)={data['pbp_dynamic']}")

    print("═" * 50)


if __name__ == "__main__":
    verify_example()
