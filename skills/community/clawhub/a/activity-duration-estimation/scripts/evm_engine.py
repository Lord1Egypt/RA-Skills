"""
evm_engine — 挣值管理分析引擎

支持：EV/PV/AC 基础指标、SV/SPI/CV/CPI 偏差分析、
BAC/EAC/ETC/VAC 完工预测（修正/不修正两模式）。
验证基准：用户提供的 A-F 阶段实例（D 阶段分析）
"""
import json
import math


# ═══════════════════════════════════════════════════════
# 单阶段参数
# ═══════════════════════════════════════════════════════

class EvmPhase:
    """挣值分析单阶段参数"""
    def __init__(self, name: str, cumulative_days: float,
                 pv: float, ac: float = None,
                 plan_progress: float = None, actual_progress: float = None):
        self.name = name
        self.cumulative_days = cumulative_days
        self.pv = pv                # 该时点的累计计划成本
        self.ac = ac                # 该时点的累计实际成本
        self.plan_progress = plan_progress   # 累计计划进度(%)
        self.actual_progress = actual_progress  # 累计实际进度(%)


# ═══════════════════════════════════════════════════════
# 计算结果
# ═══════════════════════════════════════════════════════

class EvmResult:
    """封装的完整挣值分析结果"""
    def __init__(self):
        self.project_name: str = ""
        self.bac: float = 0.0           # 总预算
        self.total_plan_duration: float = 0.0
        self.analysis_period: str = ""

        # 分析时点的关键数据
        self.pv: float = 0.0
        self.ev: float = 0.0
        self.ac: float = 0.0
        self.plan_progress: float = 0.0
        self.actual_progress: float = 0.0

        # 偏差指标
        self.sv: float = 0.0
        self.spi: float = 0.0
        self.cv: float = 0.0
        self.cpi: float = 0.0

        # 完工预测
        self.eac_uncorrected: float = 0.0
        self.eac_corrected: float = 0.0
        self.etc_uncorrected: float = 0.0
        self.etc_corrected: float = 0.0
        self.vac_uncorrected: float = 0.0
        self.vac_corrected: float = 0.0

        # 各阶段明细
        self.phases: list[dict] = []

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "bac": self.bac,
            "total_plan_duration": self.total_plan_duration,
            "analysis_period": self.analysis_period,
            "plan_progress": self.plan_progress,
            "actual_progress": self.actual_progress,
            "ev": round(self.ev, 2),
            "pv": round(self.pv, 2),
            "ac": round(self.ac, 2),
            "sv": round(self.sv, 2),
            "spi": round(self.spi, 4),
            "cv": round(self.cv, 2),
            "cpi": round(self.cpi, 4),
            "eac_uncorrected": round(self.eac_uncorrected, 2),
            "eac_corrected": round(self.eac_corrected, 2),
            "etc_uncorrected": round(self.etc_uncorrected, 2),
            "etc_corrected": round(self.etc_corrected, 2),
            "vac_uncorrected": round(self.vac_uncorrected, 2),
            "vac_corrected": round(self.vac_corrected, 2),
            "phases": self.phases,
        }


# ═══════════════════════════════════════════════════════
# 核心计算函数
# ═══════════════════════════════════════════════════════

def calc_ev(pv: float, actual_progress: float, plan_progress: float) -> float:
    """
    挣值 EV = PV × (实际进度 / 计划进度)
    当 PV 为 0 时返回 0
    """
    if plan_progress == 0 or pv == 0:
        return 0.0
    return pv * (actual_progress / plan_progress)


def calc_sv(ev: float, pv: float) -> float:
    """进度偏差 SV = EV - PV"""
    return ev - pv


def calc_spi(ev: float, pv: float) -> float:
    """进度绩效指数 SPI = EV / PV"""
    return ev / pv if pv != 0 else 0.0


def calc_cv(ev: float, ac: float) -> float:
    """成本偏差 CV = EV - AC"""
    return ev - ac


def calc_cpi(ev: float, ac: float) -> float:
    """成本绩效指数 CPI = EV / AC"""
    return ev / ac if ac != 0 else 0.0


def calc_eac_uncorrected(bac: float, cpi: float) -> float:
    """完工估算（不修正，后续绩效与当前一致） EAC = BAC / CPI"""
    return bac / cpi if cpi != 0 else bac


def calc_eac_corrected(ac: float, bac: float, ev: float) -> float:
    """完工估算（修正，后续按计划执行） EAC = AC + (BAC - EV)"""
    return ac + (bac - ev)


def calc_etc_uncorrected(eac: float, ac: float) -> float:
    """剩余成本估算（不修正） ETC = EAC - AC"""
    return eac - ac


def calc_etc_corrected(eac_corrected: float, ev: float) -> float:
    """剩余成本估算（修正） ETC = EAC_corrected - EV"""
    return eac_corrected - ev


def calc_vac(bac: float, eac: float) -> float:
    """预算偏差 VAC = BAC - EAC"""
    return bac - eac


# ═══════════════════════════════════════════════════════
# 综合计算入口
# ═══════════════════════════════════════════════════════

def run_evm(phases: list, bac: float = None, name: str = "未命名项目",
            analysis_at: str = None) -> EvmResult:
    """
    阶段性数据进行挣值分析

    参数:
        phases: 各阶段数据列表，每个元素包含
                {name, cumulative_days, pv, ac, plan_progress, actual_progress}
        bac: 总预算（不传则取最后一个阶段的PV）
        name: 项目名称
        analysis_at: 分析时点名称（如 "D 阶段"）
    """
    result = EvmResult()
    result.project_name = name

    # 确定分析时点和BAC
    total_days = max(p["cumulative_days"] for p in phases)
    if bac is None:
        bac = max(p["pv"] for p in phases)
    result.bac = bac
    result.total_plan_duration = total_days

    # 找到分析时点（最后一个有实际数据的阶段）
    target = None
    for p in reversed(phases):
        if p.get("ac") is not None or p.get("actual_progress") is not None:
            target = p
            break

    if target is None:
        return result

    analysis_period = analysis_at or target["name"]
    result.analysis_period = analysis_period

    pv = target["pv"]
    ac = target.get("ac", 0)
    plan_progress = target.get("plan_progress", 100)
    actual_progress = target.get("actual_progress", 0)
    ev = calc_ev(pv, actual_progress, plan_progress)

    result.pv = pv
    result.ac = ac
    result.ev = ev
    result.plan_progress = plan_progress
    result.actual_progress = actual_progress

    # 偏差指标
    result.sv = calc_sv(ev, pv)
    result.spi = calc_spi(ev, pv)
    result.cv = calc_cv(ev, ac)
    result.cpi = calc_cpi(ev, ac)

    # 完工预测
    result.eac_uncorrected = calc_eac_uncorrected(bac, result.cpi)
    result.eac_corrected = calc_eac_corrected(ac, bac, ev)
    result.etc_uncorrected = calc_etc_uncorrected(result.eac_uncorrected, ac)
    result.etc_corrected = calc_etc_corrected(result.eac_corrected, ev)
    result.vac_uncorrected = calc_vac(bac, result.eac_uncorrected)
    result.vac_corrected = calc_vac(bac, result.eac_corrected)

    # 各阶段明细（含各阶段自己的EV）
    result.phases = []
    for p in phases:
        ph_pv = p["pv"]
        ph_plan = p.get("plan_progress", 100)
        ph_actual = p.get("actual_progress", 0)
        ph_ev = calc_ev(ph_pv, ph_actual, ph_plan)
        result.phases.append({
            "phase_name": p["name"],
            "cumulative_days": p["cumulative_days"],
            "pv": ph_pv,
            "ac": p.get("ac"),
            "plan_progress": ph_plan,
            "actual_progress": ph_actual,
            "ev": round(ph_ev, 2),
        })

    return result


# ═══════════════════════════════════════════════════════
# 验证：用户提供的 D 阶段实例
# ═══════════════════════════════════════════════════════

def verify_example():
    """验证 D 阶段计算"""
    phases = [
        {"name": "A", "cumulative_days": 20,  "pv": 100, "ac": 120, "plan_progress": 5,  "actual_progress": 6},
        {"name": "B", "cumulative_days": 60,  "pv": 150, "ac": 150, "plan_progress": 20, "actual_progress": 15},
        {"name": "C", "cumulative_days": 100, "pv": 250, "ac": 276, "plan_progress": 60, "actual_progress": 57},
        {"name": "D", "cumulative_days": 200, "pv": 316, "ac": 300, "plan_progress": 74, "actual_progress": 75},
    ]

    r = run_evm(phases, bac=400, name="示例项目", analysis_at="D 阶段")
    d = r.to_dict()

    print("═" * 50)
    print(f"验证：D 阶段挣值分析")
    print(f"  EV = {d['ev']}     (预期 320.27)")
    print(f"  SV = {d['sv']}     (预期 4.27)")
    print(f"  SPI= {d['spi']}    (预期 1.01)")
    print(f"  CV = {d['cv']}     (预期 20.27)")
    print(f"  CPI= {d['cpi']}    (预期 1.07)")
    print(f"  EAC(不修正)= {d['eac_uncorrected']}  (预期 373.83)")
    print(f"  EAC(修正)= {d['eac_corrected']}     (预期 379.73)")
    print(f"  ETC(不修正)= {d['etc_uncorrected']}   (预期 73.83)")
    print(f"  ETC(修正)= {d['etc_corrected']}     (预期 59.46)")
    print(f"  VAC(不修正)= {d['vac_uncorrected']}   (预期 26.17)")
    print(f"  VAC(修正)= {d['vac_corrected']}     (预期 20.27)")
    print("═" * 50)


if __name__ == "__main__":
    verify_example()
