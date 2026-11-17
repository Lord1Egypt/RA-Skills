#!/usr/bin/env python3
"""嵌入式时序计算器：一次算出 + 公式回显 + 合法性判定（带依据）。"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

__version__ = "1.1.2"

HERE = os.path.dirname(os.path.abspath(__file__))
TH = os.path.join(os.path.dirname(HERE), "assets", "thresholds.json")

I2C_BUS = {
    # (tr_max ns, Cb_max pF, rate, Rp_max 系数 k, 来源)
    # std/fast/fm+ 都用同一条单调 RC 上升沿公式 Rp(max)=tr/(0.8473×Cb)（UM10204 §7.1，TI SLVA689）
    "std":    (1000, 400, 100e3, 0.8473, "I2C-bus spec UM10204 Rev7.0 标准模式 100kHz：tr<=1000ns、Cb<=400pF，Rp(max)=tr/(0.8473×Cb)（0.8473=ln(0.7/0.3)，TI SLVA689 同式）"),
    "fast":   (300, 400, 400e3, 0.8473, "I2C-bus spec UM10204 Rev7.0 快速模式 400kHz：tr<=300ns、Cb<=400pF，Rp(max)=tr/(0.8473×Cb)；速率上限由 tr 收紧而不是换系数（TI SLVA689）"),
    "fmplus": (120, 550, 1e6, 0.8473, "I2C-bus spec UM10204 Rev7.0 快速+ 1MHz：tr<=120ns、Cb<=550pF，Rp(max)=tr/(0.8473×Cb)；tr/Cb 收紧后自然比 fast 更严（TI SLVA689）"),
    "hs":     (40, 100, 3.4e6, None, "I2C-bus spec UM10204 Rev7.0 高速模式 3.4MHz：上拉为电流源结构，不能用无源 Rp(max)=tr/(0.8473×Cb) 公式，需按 Hs-mode 章节人工核对"),
}


class CalcError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def load_th():
    if not os.path.isfile(TH):
        raise CalcError("E_DATA_MISSING", "找不到阈值库 assets/thresholds.json")
    with open(TH, encoding="utf-8") as fh:
        return {t["id"]: t for t in json.load(fh)["thresholds"]}


def verdict(ok, why=""):
    return ("PASS 合法" if ok else "FAIL 不合法") + (("：" + why) if why else "")


def calc_uart(pclk, baud, osr=16):
    if pclk <= 0 or baud <= 0:
        raise CalcError("E_ARG", "pclk/baud 必须为正数")
    if osr not in (8, 16):
        raise CalcError("E_ARG", "--os 过采样只支持 8 或 16")
    brr = round(pclk / (osr * baud))
    if brr == 0:
        raise CalcError("E_RANGE", "BRR=0：波特率太高或主频太低")
    if brr > 65535:
        raise CalcError("E_RANGE", "BRR=%d 超 16 位：波特率太低" % brr)
    actual = pclk / (osr * brr)
    err = abs(actual - baud) / baud * 100
    th = load_th()["uart-baud-error"]
    ok = err <= th["value"]
    return ok, [
        "BRR（分频值）= %d" % brr,
        "实际波特率 = %.2f（期望 %d）" % (actual, baud),
        "误差 = %.3f%%（上限 %.1f%%）" % (err, th["value"]),
        "公式：BRR = round(PCLK/(%d×Baud))；Actual = PCLK/(%d×BRR)" % (osr, osr),
        "依据：%s（%s）" % (th["label"], th["source"]),
        verdict(ok, "误差 %.3f%% %s 2%%——%s" % (
            err, "<=" if ok else ">",
            "可用" if ok else "会误码：换 HSE/晶振、降波特率或选可整除主频")),
    ]


def calc_timer(pclk, freq=None, psc=None, arr=None):
    if pclk <= 0:
        raise CalcError("E_ARG", "pclk 必须为正数")
    if freq is not None and psc is None and arr is None:
        if freq <= 0:
            raise CalcError("E_ARG", "freq 必须为正数")
        div_total = pclk / freq
        if div_total < 1:
            raise CalcError("E_RANGE", "目标频率 %gHz 高于时钟 %gHz" % (freq, pclk))
        recs = []
        for psc_c in [0, 1, 7, 15, 31, 63, 71, 99, 127, 255, 719, 999, 1439, 7199, 35999, 65535]:
            arr_c = round(div_total / (psc_c + 1)) - 1
            if 0 <= arr_c <= 65535:
                actual = pclk / ((psc_c + 1) * (arr_c + 1))
                err = abs(actual - freq) / freq * 100
                recs.append((psc_c, arr_c, actual, err))
        if not recs:
            raise CalcError("E_RANGE", "PCLK=%g 无法用 16 位 PSC/ARR 近似 %gHz" % (pclk, freq))
        recs.sort(key=lambda r: (r[3], -r[0]))
        lines = ["推荐组合（误差升序，前 5 组）："]
        for psc_c, arr_c, actual, err in recs[:5]:
            lines.append("  PSC=%-6d ARR=%-6d 实际=%.4f Hz 误差=%.4f%%" % (psc_c, arr_c, actual, err))
        lines += [
            "公式：F = PCLK/((PSC+1)×(ARR+1))",
            "提示：APB 分频>1 时定时器时钟 = PCLK×2（别拿 APB 外设时钟直接算）",
            "提示：改 ARR 后新周期下个更新事件才生效（软触发 EGR 立即同步）",
            "依据：通用定时器时基单元（STM32 RM0090/RM0440）",
        ]
        return True, lines
    if psc is not None and arr is not None:
        if psc < 0 or arr < 0 or psc > 65535 or arr > 65535:
            raise CalcError("E_RANGE", "PSC/ARR 均 0-65535")
        f = pclk / ((psc + 1) * (arr + 1))
        return True, [
            "输出频率 = %.4f Hz，周期 = %.6g s" % (f, 1 / f if f else float("inf")),
            "公式：F = PCLK/((PSC+1)×(ARR+1)) = %g/(%d×%d)" % (pclk, psc + 1, arr + 1),
        ]
    raise CalcError("E_ARG", "反向用 --freq；正向用 --psc --arr")


def calc_i2c_rp(bus, cb, vdd=3.3):
    if bus not in I2C_BUS:
        raise CalcError("E_ARG", "bus 取值：%s" % ", ".join(I2C_BUS))
    tr_max, cb_max, _rate, k, src = I2C_BUS[bus]
    if k is None:
        raise CalcError(
            "E_UNSUPPORTED",
            "Hs-mode（3.4MHz）为电流源上拉，不能用无源上拉公式 Rp(max)=tr/(0.8473×Cb) 判定；"
            "请按 I2C-bus spec UM10204 Hs-mode 章节核对电流源、Rp 与 Cb 要求（本工具不自动计算该模式）")
    if cb <= 0:
        raise CalcError("E_ARG", "cb（总线电容 pF）必须为正数")
    if cb > cb_max:
        return False, [
            "FAIL 总线电容 %gpF 超出上限 %dpF" % (cb, cb_max),
            "依据：%s" % src,
            "对策：缩短走线/减少挂载/降速率——电容超标时任何上拉都救不回来",
        ]
    rp_max = tr_max * 1e-9 / (k * cb * 1e-12)
    rp_min = (vdd - 0.4) / 0.003
    std_vals = [1000, 1500, 2200, 3300, 4700, 6800, 10000]
    recs = [v for v in std_vals if rp_min <= v <= rp_max]
    return bool(recs), [
        "Rp_max = tr/(k×Cb) = %dns/(%.4g×%gpF) = %.2f kΩ" % (tr_max, k, cb, rp_max / 1000),
        "Rp_min = (VDD-0.4V)/3mA = %.0f Ω（VDD=%gV）" % (rp_min, vdd),
        "合法区间：%.0f Ω ~ %.2f kΩ" % (rp_min, rp_max / 1000),
        "推荐标准阻值：%s" % ("、".join("%gk" % (v / 1000) for v in recs) if recs else "无（区间过窄）"),
        "公式：Rp_max = tr_max/(0.8473×Cb)（std/fast/fm+ 同一 RC 上升沿式；hs 为电流源上拉，本工具抛 E_UNSUPPORTED）",
        "依据：%s" % src,
        verdict(bool(recs), "区间%s" % ("存在标准阻值可选" if recs else "过窄")),
    ]


def calc_can(clk, baud, sp=87.5, family="bxcan"):
    if clk <= 0 or baud <= 0:
        raise CalcError("E_ARG", "clk/baud 必须为正数")
    # 家族口径：bxCAN（F1/F4/F0/G0/L 经典）每位最多 25 TQ（TSEG1<=16/TSEG2<=8）；
    # FDCAN（G4/H7 等）宽得多（TSEG1<=256/TSEG2<=128）。
    if family == "fdcan":
        tq_max, seg1_max, seg2_max, warn = 385, 256, 128, None
    else:
        tq_max, seg1_max, seg2_max = 25, 16, 8
        warn = ("提示 按 bxCAN 口径（每位最多 25 TQ，TSEG1<=16/TSEG2<=8）；"
                "G4/H7 等 FDCAN 可到 385 TQ——用 --family fdcan 解锁宽口径")
    tq_total = round(clk / baud)
    if tq_total < 8:
        raise CalcError("E_RANGE", "每位仅 %d TQ（CAN 需 ≥8）" % tq_total)
    if tq_total > 512:
        raise CalcError("E_RANGE", "每位 %d TQ 过大（>512）" % tq_total)
    # 正解：遍历 BRP 找"波特率精确整数解"的 TQ 总数 t，再对每个 t 枚举全部
    # 合法 (seg1, seg2)，优先落在 75-87.5% 窗内且最接近目标，否则取最接近的合法点。
    lo = load_th()["can-sp-low"]["value"]
    hi = load_th()["can-sp-high"]["value"]
    candidates = []  # (窗内?, 与目标偏差, brp, t, seg1, seg2, 实际采样点)
    for brp in range(1, 256):
        tq_f = clk / (brp * baud)
        if abs(tq_f - round(tq_f)) > 1e-9:
            continue
        t = int(round(tq_f))
        if not 8 <= t <= tq_max:
            continue
        for seg1 in range(1, min(seg1_max, t - 2) + 1):
            seg2 = t - 1 - seg1
            if not 1 <= seg2 <= seg2_max:
                continue
            actual_sp = (1 + seg1) / t * 100
            in_window = lo <= actual_sp <= hi
            candidates.append((0 if in_window else 1, abs(actual_sp - sp),
                               brp, t, seg1, seg2, actual_sp))
    if not candidates:
        hint = ("（bxCAN 每位最多 25 TQ——若用 G4/H7 等 FDCAN，加 --family fdcan 重试）"
                if family != "fdcan" else "（FDCAN 口径下仍无解）")
        raise CalcError("E_RANGE",
                        "1-256 分频内找不到波特率整数解且满足 TQ<=%d/seg1<=%d/seg2<=%d 的分配 %s"
                        % (tq_max, seg1_max, seg2_max, hint))
    _, _, brp, t, seg1, seg2, actual_sp = min(candidates, key=lambda c: (c[0], c[1]))
    actual_baud = clk / (brp * t)
    baud_err = abs(actual_baud - baud) / baud * 100
    th = load_th()
    ok_sp = lo <= actual_sp <= hi
    ok_baud = baud_err <= 2.0
    lines = [
        "TQ 总数 = %d（BRP=%d）→ 实际波特率 %.4f（期望 %d，误差 %.4f%%）" % (t, brp, actual_baud, baud, baud_err),
        "段分配：SYNC=1、Prop+Ph1=%d、Ph2=%d（TQ<=%d、TSEG1<=%d、TSEG2<=%d）"
        % (seg1, seg2, tq_max, seg1_max, seg2_max),
        "采样点 = %.1f%%（目标 %.1f%%，合法窗 %.0f-%.1f%%）" % (actual_sp, sp, lo, hi),
        "公式：SamplePoint=(1+TSEG1)/TQ_total×100%；F_baud=CLK/(BRP×TQ_total)",
        "依据：%s" % th["can-sp-low"]["source"],
    ]
    if warn:
        lines.append(warn)
    if not ok_sp:
        lines.append("说明：在 %s 段约束下已取最接近目标的合法点；再提高采样点需换 FDCAN（--family fdcan）或调整主频/波特率"
                     % family)
    lines.append(verdict(ok_sp and ok_baud, "采样点%s、波特率误差%s" % (
        "在窗内" if ok_sp else "出窗", " ≤2%" if ok_baud else " >2%")))
    return ok_sp and ok_baud, lines


def calc_adc_rad(ts, fadc, nbits=12, cs_pf=8.0, radc_ohm=0.0):
    if ts <= 0 or fadc <= 0:
        raise CalcError("E_ARG", "ts/fadc 必须为正数")
    if not 6 <= nbits <= 24:
        raise CalcError("E_ARG", "nbits 6-24")
    if cs_pf <= 0 or radc_ohm < 0:
        raise CalcError("E_ARG", "cs 必须为正、radc 不能为负")
    ts_sec = ts / fadc
    # ST datasheet 口径：Rsrc_max = ts/(Cadc×ln(2^(N+2))) − Radc（整定到 1/4 LSB）
    k = math.log(2 ** (nbits + 2))
    r_no_radc = ts_sec / ((cs_pf * 1e-12) * k)
    r_max = r_no_radc - radc_ohm
    if radc_ohm > 0:
        radc_line = "已扣片内 Radc = %.0f Ω：Rsrc_max = %.1f kΩ − %.1f kΩ = %.1f kΩ（负值按 0 处理）" % (
            radc_ohm, r_no_radc / 1000, radc_ohm / 1000, max(r_max, 0.0) / 1000)
    else:
        radc_line = "未扣 Radc：Rsrc_max = %.1f kΩ（片内 RADC 未计入，用 --radc 可按目标芯片 datasheet 扣减）" % (r_no_radc / 1000)
    return True, [
        "采样时间 = %g cycles / %g Hz = %.1f ns" % (ts, fadc, ts_sec * 1e9),
        "建立系数 k = ln(2^(N+2)) = %.2f（%d 位整定到 1/4 LSB，ST datasheet 口径）" % (k, nbits),
        radc_line,
        "公式：Rsrc_max = ts/(Cs×ln(2^(N+2))) − Radc，Cs 按 %gpF" % cs_pf,
        "依据：%s" % load_th()["adc-fs-clamp"]["source"],
        "提示：源阻抗超限时——加运放缓冲/增大 ts/降 ADC 时钟；具体 Cs 与 Radc 以目标芯片 datasheet 为准",
    ]


def calc_rc(r=None, c=None, fc=None):
    if r is not None and c is not None:
        return True, [
            "截止频率 fc = %.6g Hz" % (1 / (2 * math.pi * r * c)),
            "公式：fc = 1/(2πRC)，R=%g C=%g" % (r, c),
            "依据：一阶 RC 低通 -3dB 定义",
        ]
    if fc is not None and c is not None:
        r = 1 / (2 * math.pi * fc * c)
        return True, [
            "电阻 R = %.6g Ω" % r,
            "公式：R = 1/(2π×fc×C)，fc=%g C=%g" % (fc, c),
            "依据：一阶 RC 低通 -3dB 定义",
            "提示：用 E24 标称值就近取后反算实际 fc",
        ]
    raise CalcError("E_ARG", "用 --r --c 算 fc，或 --fc --c 反推 R")


def calc_spi(fclk, div):
    if div <= 0:
        raise CalcError("E_ARG", "div 必须为正")
    div_i = int(round(div))
    f = fclk / div_i
    lines = ["SCK = %.6g Hz" % f, "公式：SCK = FCLK/%d" % div_i]
    if not (float(div).is_integer() and div_i & (div_i - 1) == 0):
        lines.append("FAIL %g 不是 2 的幂——多数 SPI 只支持 2^n 分频（2/4/.../256）" % div)
        return False, lines
    lines.append("PASS 2^n 分频合法")
    return True, lines


def calc_nyquist(fs, fbw):
    if fs <= 0 or fbw <= 0:
        raise CalcError("E_ARG", "fs/fbw 必须为正数")
    ratio = fs / fbw
    ok = ratio >= 2.0
    return ok, [
        "fs/fbw = %.2f 倍" % ratio,
        "Nyquist 要求：fs ≥ 2×fbw = %g Hz" % (2 * fbw),
        "工程建议 5-10 倍（抗混叠+重建质量）",
        "依据：%s" % load_th()["nyquist-margin"]["source"],
        verdict(ok, "%.2f 倍%s" % (ratio, "，过 Nyquist" if ok else "，必混叠")),
    ]


def calc_i2c_time(bus, nbytes):
    if bus not in I2C_BUS:
        raise CalcError("E_ARG", "bus 取值：%s" % ", ".join(I2C_BUS))
    if nbytes <= 0:
        raise CalcError("E_ARG", "bytes 必须为正数")
    rate = I2C_BUS[bus][2]
    bits = (nbytes + 1) * 9 + 2
    t = bits / rate
    return True, [
        "传输耗时 ≈ %.2f µs（%s，%d 数据字节+地址+启停）" % (t * 1e6, bus, nbytes),
        "公式：t = ((n+1)×9+2)/f_bus，f_bus=%g" % rate,
        "依据：I2C-bus spec Rev7.0 帧结构（每字节 9 位含 ACK）",
        "提示：多从机轮询时用此值估算实时性余量",
    ]


def calc_deadtime(fsw, dt):
    if fsw <= 0 or dt <= 0:
        raise CalcError("E_ARG", "fsw/dt 必须为正数")
    period = 1 / fsw
    ratio = dt / period * 100
    th = load_th()["deadtime-ratio"]
    ok = ratio <= th["value"]
    return ok, [
        "开关周期 = %.2f µs，死区占比 = %.2f%%（提示级阈值 %.0f%%）" % (period * 1e6, ratio, th["value"]),
        "有效占空比压缩：每边损失 %.2f%%" % (ratio / 2),
        "公式：ratio = dt/(1/fsw)×100%%",
        "依据：%s" % th["source"],
        verdict(ok, "占比 %.2f%%" % ratio)
        + "；死区与 SVPWM/有效矢量时间的深水区配合 → 转电机控制专家",
    ]


def calc_fpga_uart(clk, baud):
    if clk <= 0 or baud <= 0:
        raise CalcError("E_ARG", "clk/baud 必须为正数")
    div = clk / baud
    n = round(div)
    if n == 0:
        raise CalcError("E_RANGE", "分频值=0：波特率过高")
    actual = clk / n
    err = abs(actual - baud) / baud * 100
    th = load_th()["uart-baud-error"]
    ok = err <= th["value"]
    frac = div - int(div)
    lines = [
        "整数分频 N = %d（理想 %.4f）" % (n, div),
        "实际波特率 = %.2f，误差 = %.3f%%" % (actual, err),
        "公式：N = round(CLK/Baud)；Baud = CLK/N",
    ]
    if abs(frac) > 1e-9:
        lines.append("提示：理想分频 %.4f 非整数，小数部分 %.3f——整数分频有固有误差" % (div, frac))
        if abs(frac) > 0.02:
            lines.append("提示：可考虑分数分频（小数控分频）或换时钟频率让 N 整除")
    lines += [
        "依据：%s" % th["source"],
        verdict(ok, "误差 %.3f%%" % err),
    ]
    return ok, lines


def calc_fpga_slack(tclk, tco, tlogic, troute, tsu):
    period = tclk
    total = tco + tlogic + troute + tsu
    slack = period - total
    th = load_th()
    ok = slack >= th["fpga-slack-ok"]["value"]
    fmax = 1000.0 / total if total > 0 else float("inf")
    lines = [
        "数据路径总延时 = Tco+Tlogic+Troute+Tsu = %.2f ns" % total,
        "Slack = Tclk - 总延时 = %.2f - %.2f = %.2f ns" % (period, total, slack),
        "理论 Fmax = %.1f MHz（1/总延时）" % fmax,
        "公式：slack = Tclk - (Tco+Tlogic+Troute+Tsu)",
        "依据：%s" % th["fpga-slack-ok"]["source"],
    ]
    if ok and slack < th["fpga-slack-warn"]["value"]:
        lines.append("WARN 裕量 <%.1f ns：PVT 跨角漂移风险，建议关键路径加约束/流水" % th["fpga-slack-warn"]["value"])
    lines.append(verdict(ok, "slack %.2f ns" % slack))
    return ok, lines


def calc_fpga_pwm(clk, fpwm):
    if clk <= 0 or fpwm <= 0:
        raise CalcError("E_ARG", "clk/fpwm 必须为正数")
    counts = clk / fpwm
    bits = math.log2(counts) if counts > 0 else 0
    ok = counts >= 256
    lines = [
        "每 PWM 周期计数 = %.1f（CLK/%g）" % (counts, fpwm),
        "理论位深 = %.2f 位（2^%.2f）" % (bits, bits),
        "公式：counts = CLK/fpwm；bits = log2(counts)",
    ]
    if ok:
        lines.append("PASS ≥8 位（256 级）：占空比分辨率可接受")
    else:
        lines.append("FAIL <8 位：占空比只有 %d 级，会出现台阶/啸叫——降 fpwm 或升 clk" % int(counts))
    lines.append("提示：电机用中心对齐（计数上下）时有效位深再除 2，深度配合转电机专家")
    return ok, lines


def calc_wdg(clk, presc, reload):
    """看门狗超时：Tout = (presc × reload) / clk（IWDG 口径）"""
    if clk <= 0 or presc <= 0 or reload <= 0:
        raise CalcError("E_ARG", "clk/presc/reload 必须为正数")
    tout = presc * reload / clk
    lines = [
        "超时时间 = %.3f s（%.1f ms）" % (tout, tout * 1000),
        "公式：Tout = Presc × Reload / Clk = %g × %d / %g" % (presc, reload, clk),
        "提示：喂狗周期必须 < 超时的 60%%（留双倍裕量防任务抖动）；喂狗点放在主循环，别放定时器中断（中断卡死时看门狗救不了）",
        "提示：窗口看门狗（WWDG）还需计数窗口下限，避开喂太早复位",
        "依据：IWDG 通式（STM32 RM0090/RM0440，LSI 40kHz 口径）",
    ]
    return True, lines


def calc_pll(clkin, m, n, p, vcomin=100e6, vcomax=200e6):
    """PLL 输出：f_vco = clkin/m×n；f_out = f_vco/p（STM32 主 PLL 口径）"""
    if clkin <= 0 or m <= 0 or n <= 0 or p <= 0:
        raise CalcError("E_ARG", "参数必须为正数")
    fvco = clkin / m * n
    fout = fvco / p
    ok_vco = vcomin <= fvco <= vcomax
    lines = [
        "VCO = Clkin/M×N = %g/%d×%d = %.3f MHz" % (clkin / 1e6, m, n, fvco / 1e6),
        "输出 = VCO/P = %.3f MHz（P=%d）" % (fout / 1e6, p),
        "VCO 合法窗：%.0f ~ %.0f MHz" % (vcomin / 1e6, vcomax / 1e6),
        "公式：f_VCO = Clkin/M×N；f_out = f_VCO/P",
        "提示：M 取值让 Clkin/M 落在 1~2MHz（spec 推荐输入范围）；P 从 {2,4,6,8} 里选（部分家族支持奇数）",
        "依据：STM32 RM0090（F4）/RM0440（G4）主 PLL 通式，VCO 窗以目标芯片 datasheet 为准",
        verdict(ok_vco, "VCO %.1f MHz %s 窗" % (fvco / 1e6, "在" if ok_vco else "出")),
    ]
    return ok_vco, lines


E24_VALUES = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
              3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def e24_nearest(value):
    """任意数量级就近取 E24 标称值。"""
    if value <= 0:
        return value
    mag = 10 ** math.floor(math.log10(value))
    return min(E24_VALUES, key=lambda v: abs(v * mag - value)) * mag


def calc_divider(vin, vout, current_ua=None):
    """分压电阻：无电流时 R2=10k 基准；给电流时 R_total=Vin/I、R1/R2 分别由电流定。"""
    if vin <= 0 or vout <= 0:
        raise CalcError("E_ARG", "vin/vout 必须为正数")
    if vout >= vin:
        raise CalcError("E_ARG", "vout 必须 < vin（分压只会降压）")
    if current_ua is not None and current_ua <= 0:
        raise CalcError("E_ARG", "分压电流必须为正数")
    ratio = vout / vin
    lines = ["分压比 = Vout/Vin = %.4f（%.1f%%）" % (ratio, ratio * 100)]
    if current_ua:
        i_a = current_ua * 1e-6
        r_total = vin / i_a
        r1 = (vin - vout) / i_a
        r2 = vout / i_a
        r1_std = e24_nearest(r1)
        r2_std = e24_nearest(r2)
        vout_std = vin * r2_std / (r1_std + r2_std)
        err = abs(vout_std - vout) / vout * 100
        i_std = vin / (r1_std + r2_std) * 1e6
        lines += [
            "给定电流 %gµA：R_total = Vin/I = %.1f kΩ；R1 = (Vin-Vout)/I = %.1f kΩ；R2 = Vout/I = %.1f kΩ"
            % (current_ua, r_total / 1000, r1 / 1000, r2 / 1000),
            "E24 就近：R1 = %.1f kΩ、R2 = %.1f kΩ（各自取标称后复算）" % (r1_std / 1000, r2_std / 1000),
            "用标称值复算：Vout' = %.4f V（误差 %.2f%%），分压电流 ≈ %.1f µA" % (vout_std, err, i_std),
            "公式：R_total=Vin/I；R2=Vout/I；R1=(Vin-Vout)/I",
        ]
    else:
        # 未给电流：R2=10k 基准，R1=R2×(Vin-Vout)/Vout
        r2 = 10000.0
        r1 = r2 * (vin - vout) / vout
        r1_std = e24_nearest(r1)
        vout_std = vin * r2 / (r1_std + r2)
        err = abs(vout_std - vout) / vout * 100
        lines += [
            "未给分压电流，按 R2=10k 基准：R1 = R2×(Vin-Vout)/Vout = %.1f Ω → E24 就近 %.1f kΩ"
            % (r1, r1_std / 1000),
            "用标称值复算：Vout' = %.4f V（误差 %.2f%%）" % (vout_std, err),
            "公式：Vout = Vin×R2/(R1+R2)；R1 = R2×(Vin-Vout)/Vout",
        ]
    lines += [
        "提示：高阻分压省电但噪声大，ADC 采样口记得核对源阻抗（用 adc-rad）；采样保持电流会让高阻分压读数偏低",
        "依据：电阻分压通式 + E24 标称系列",
    ]
    return True, lines


def calc_ntc(r25, beta, temp_c):
    """NTC 测温：Beta 公式双向。给 temp → 阻值；电阻对温度校准用"""
    if r25 <= 0 or beta <= 0:
        raise CalcError("E_ARG", "r25/beta 必须为正数")
    t0 = 298.15  # 25°C
    t = temp_c + 273.15
    r = r25 * math.exp(beta * (1 / t - 1 / t0))
    lines = [
        "%g°C 时 NTC 阻值 = %.1f Ω（R25=%g，Beta=%g）" % (temp_c, r, r25, beta),
        "公式：R(T) = R25 × exp(Beta×(1/T − 1/T0))，T 开尔文",
        "提示：Beta 公式 ±1°C 量级精度；要 ±0.1°C 用 Steinhart-Hart 三系数",
        "提示：ADC 分压采样建议 NTC 放下臂（R25 与固定电阻分压），高温段分辨率更好；配合 adc-rad 查源阻抗",
        "依据：Beta（两参数）模型， datasheet 通常给 25/50/85°C 两点 Beta",
    ]
    return True, lines


def calc_rc_settle(r, c, nbits=10):
    """RC 建立时间：到 n 位精度需 ~0.693×(n+1)×RC（2^-n 残差口径 0.693×n×RC，取保守）"""
    if r <= 0 or c <= 0:
        raise CalcError("E_ARG", "r/c 必须为正数")
    tau = r * c
    t = math.log(2 ** nbits) * tau  # n bits → ln(2^n) τ
    lines = [
        "τ = RC = %.3g s（%.3g µs）" % (tau, tau * 1e6),
        "到 %d 位精度（残差 2^-%d）需 t ≈ %.2f τ = %.3g s（%.3g µs）" % (nbits, nbits, math.log(2**nbits), t, t * 1e6),
        "公式：t_settle = ln(2^nbits) × RC",
        "提示：采样链路（分压+RC+ADC）要保证采样窗 ≥ 此值的 5 倍；与 adc-rad 联查源阻抗",
        "依据：RC 阶跃响应 e^(-t/RC) 通式",
    ]
    return True, lines


def calc_ppm(base_hz, ppm):
    """晶振频率漂移与波特率影响"""
    if base_hz <= 0:
        raise CalcError("E_ARG", "base_hz 必须为正数")
    drift = base_hz * ppm / 1e6
    lines = [
        "漂移 = ±%g Hz（%g MHz × %g ppm）" % (drift, base_hz / 1e6, ppm),
        "对波特率的影响：同数量级 %g ppm → UART 误差 ±%.4f%%" % (ppm, ppm / 1e4),
        "公式：Δf = f × ppm/1e6",
        "提示：双端通信两端各 ±ppm，最坏叠加 2×ppm——HSI ±1%%=10000ppm 直接爆 UART 2%% 限（呼应 pitfalls rcc-hsi-uart）",
        "提示：常见晶振 ±20ppm，TCXO ±2ppm，HSI/RCO ±0.5%%~1%%",
        "依据：频率漂移通式；UART 2%% 上限见 uart 计算器",
    ]
    return True, lines


def calc_fpga_i2c(clk_mhz, clk_div, i2c_rate=100e3):
    """FPGA 行为级 I2C：CLK(MHz) 与半位分频数 → SCL 频率（每半位计 clk_div 个时钟）"""
    if clk_mhz <= 0 or clk_div <= 0:
        raise CalcError("E_ARG", "clk_mhz/clk_div 必须为正数")
    scl = clk_mhz * 1e6 / (clk_div * 2)
    err = abs(scl - i2c_rate) / i2c_rate * 100
    half_us = clk_div / (clk_mhz * 1e6) * 1e6
    ok = err <= 10.0  # I2C 同步协议时钟容忍度高，10% 提示线
    return ok, [
        "SCL = CLK/(clk_div×2) = %g MHz/(%g×2) = %.4g Hz（目标 %.4g，误差 %.1f%%）"
        % (clk_mhz, clk_div, scl, i2c_rate, err),
        "半位时间 = %.2f µs（高/低各半）" % half_us,
        "公式：SCL = CLK/(clk_div×2)；行为级实现每半位计数 clk_div",
        "提示：行为级仿真够用，上板要顾 SCL 上升沿（开漏+上拉，RC 由 i2c-rp 算）",
        "依据：I2C 协议时钟由主控产生、误差容忍度高于 UART（同步位采样）",
        verdict(ok, "SCL 误差 %.1f%%" % err),
    ]


def calc_fpga_debounce(clk, ms, stages=2):
    """按键/信号消抖：移位寄存器级数与计数器宽度两种实现"""
    if clk <= 0 or ms <= 0:
        raise CalcError("E_ARG", "clk/ms 必须为正数")
    cycles = clk * ms / 1000.0
    cnt_bits = math.ceil(math.log2(cycles + 1)) if cycles > 1 else 1
    lines = [
        "消抖窗口 %g ms = %g 个时钟周期" % (ms, cycles),
        "实现一（计数器）：%d 位计数器 + 采样标志" % cnt_bits,
        "实现二（移位寄存器）：连续 %d 个采样一致才翻转——要覆盖 %g ms 需 %d 级（1 级 1 采样，采样率=CLK）" % (stages, ms, int(cycles)),
        "公式：cycles = CLK × T_debounce",
        "提示：机械按键典型 5-20ms；移位寄存器法面积大但无计数器进位时序压力",
        "依据：同步消抖通式（采样须先过 2 级触发器防亚稳态——这个坑在 pitfalls fpga 类）",
    ]
    return True, lines


def calc_fpga_cdc(toggle_rate_mhz=100):
    """跨时钟域检查单：数据宽度 vs 同步器需求（提示级，配 pitfalls fpga 类）"""
    lines = [
        "CDC（跨时钟域）检查单：",
        "1. 单 bit 控制信号 → 2 级触发器同步器（防亚稳态）；快→慢域用打拍+边沿检测",
        "2. 多 bit 数据总线 → 禁止直接同步！用握手（req/ack）或异步 FIFO（格雷码指针）",
        "3. 计数器跨域 → 格雷码（相邻只变 1 位）",
        "4. 复位：每个时钟域独立异步复位、同步释放（async assert, sync de-assert）",
        "5. 门控时钟/行波计数器 → CDC 工具（如 Vivado report_cdc）必查",
        "公式：无统一公式，纪律清单——MTBF ∝ e^(t_meta/τ)，两级同步器够用绝大多数场景",
        "依据：CDC 设计通则（Cummings 经典论文系列：Clock Domain Crossing）",
    ]
    return True, lines


def calc_fpga_uart_fifo(tx_rate_bps, read_rate_bps, burst_bytes, fifo_depth):
    """FPGA UART 收包 FIFO 溢出检查：突发写入 vs 下游读速"""
    if tx_rate_bps <= 0 or fifo_depth <= 0:
        raise CalcError("E_ARG", "tx_rate_bps/fifo_depth 必须为正数")
    # 下游每秒读走 read_rate_bps/10 字节；突发 burst_bytes 写入需要排空时间
    in_rate = tx_rate_bps / 10.0
    out_rate = read_rate_bps / 10.0
    if out_rate >= in_rate:
        steady_ok = True
        steady = "稳态不积压（读速 ≥ 写速）"
    else:
        steady_ok = False
        steady = "稳态积压 %.0f 字节/秒——FIFO 深度再大也会溢出，必须提读速或流控" % (in_rate - out_rate)
    drain = burst_bytes / out_rate if out_rate else float("inf")
    ok = steady_ok and burst_bytes <= fifo_depth
    return ok, [
        "写入速率 = %.0f 字节/s，读出速率 = %.0f 字节/s" % (in_rate, out_rate),
        "稳态：%s" % steady,
        "突发 %d 字节：排空需 %.2f ms；FIFO 深度 %d %s"
        % (burst_bytes, drain * 1000, fifo_depth, "够" if burst_bytes <= fifo_depth else "不够（突发即溢出）"),
        "公式：稳态条件 out_rate ≥ in_rate；突发条件 burst ≤ depth；排空 t = burst/out_rate",
        "提示：FIFO 读空/写满标志要跨时钟域时用格雷码指针（CDC 纪律，见 fpga-cdc）",
        "依据：异步 FIFO 容量设计通式（Cummings：Simulation and Synthesis Techniques for Asynchronous FIFO）",
        verdict(ok, "FIFO 容量与速率匹配"),
    ]


def calc_esp32_clk(div=None, target=None):
    """ESP32 外设时钟速查：APB 80MHz 起步，分频得目标"""
    apb = 80e6
    th = load_th()["esp32-apb-clk"]
    lines = ["ESP32 经典款 APB 外设时钟 = 80 MHz（SDK 常量，多数外设按此推导）"]
    if target is not None and target > 0:
        div = apb / target
        lines.append("目标 %g Hz → 分频系数 = 80M/target = %.4f" % (target, div))
        if abs(div - round(div)) < 1e-6:
            n = int(round(div))
            lines.append("PASS 整除：分频 %d，实际 %.6g Hz（零误差）" % (n, apb / n))
            return True, lines
        n = round(div)
        actual = apb / n
        err = abs(actual - target) / target * 100
        lines.append("非整除：最近整数分频 %d → 实际 %.6g Hz，误差 %.3f%%" % (n, actual, err))
        lines.append("提示：ESP32 外设时钟多路可选（80/160/240MHz CPU 分频），换时钟源可能整除——此处仅按 80M APB 口径")
        lines.append("依据：%s" % th["source"])
        return True, lines
    if div is not None and div > 0:
        f = apb / div
        lines.append("分频 %g → %.6g Hz" % (div, f))
        return True, lines
    lines.append("速查：80M/1=80M（默认）、/2=40M、/4=20M、/5=16M、/8=10M、/10=8M、/16=5M、/20=4M、/40=2M、/80=1M")
    lines.append("依据：%s" % th["source"])
    return True, lines


def calc_rp2040_uart(clk_peri, baud):
    """RP2040 UART divider：BAUDDIV = clk_peri/(16×baud)，IBRD 16 位整数 + FBRD 6 位小数（1/64 步进）。"""
    if clk_peri <= 0 or baud <= 0:
        raise CalcError("E_ARG", "clk_peri/baud 必须为正数")
    div_ideal = clk_peri / (16 * baud)
    ibrd = int(div_ideal)
    frac = div_ideal - ibrd
    fbrd = int(round(frac * 64))
    carry = fbrd == 64
    if carry:
        # FBRD 只有 6 位（0-63）：四舍五入到 64 时向 IBRD 进位
        ibrd += 1
        fbrd = 0
    if ibrd > 0xFFFF:
        raise CalcError("E_RANGE", "IBRD=%d 超 16 位（clk_peri 过高或 baud 过低）" % ibrd)
    div_used = ibrd + fbrd / 64.0
    if div_used <= 0:
        raise CalcError("E_RANGE", "BAUDDIV=0：波特率过高")
    actual = clk_peri / (16 * div_used)
    err = abs(actual - baud) / baud * 100
    th = load_th()["uart-baud-error"]
    ok = err <= th["value"]
    lines = [
        "BAUDDIV 理想 = %.4f（整数部分 %d，小数 %.4f）" % (div_ideal, int(div_ideal), frac),
        "FBRD = round(小数×64) = %d%s → IBRD=%d、FBRD=%d、实际分频 %.4f"
        % (fbrd, "（四舍五入到 64，已向 IBRD 进位）" if carry else "", ibrd, fbrd, div_used),
        "实际波特率 = %.2f（期望 %g，误差 %.3f%%）" % (actual, baud, err),
        "公式：BAUDDIV = clk_peri/(16×baud) = IBRD + FBRD/64；IBRD 16 位整数、FBRD 6 位小数（0-63）",
        "依据：%s（%s）" % (th["label"], th["source"]),
        verdict(ok, "误差 %.3f%% %s 2%%" % (err, "<=" if ok else ">")),
    ]
    return ok, lines


def calc_pwm_dim(clk, fpwm):
    """PWM 调光分辨率：counts 与位深，<8 位判不合法（可见台阶）"""
    if clk <= 0 or fpwm <= 0:
        raise CalcError("E_ARG", "clk/fpwm 必须为正数")
    counts = clk / fpwm
    bits = math.log2(counts) if counts > 0 else 0
    th = load_th()["pwm-resolution-min"]
    ok = bits >= th["value"]
    return ok, [
        "每周期计数 = %.0f，分辨率 = %.2f 位（%d 级）" % (counts, bits, int(2 ** bits) if bits < 20 else 10 ** 6),
        "公式：bits = log2(CLK/fpwm)",
        "依据：%s（%s）" % (th["label"], th["source"]),
        verdict(ok, "%.2f 位 %s %d 位下限%s" % (
            bits, ">=" if ok else "<", int(th["value"]),
            "，呼吸灯/调光平滑" if ok else "——可见台阶：升 CLK 或降 fpwm")),
    ]


def calc_ws2812(t0h, t1h, t0l=None, t1l=None):
    """WS2812 位时序：高电平必查（T0H≈300ns/T1H≈800ns），低电平给了才查。"""
    th = load_th()["ws2812-timing-tolerance"]
    tol = th["value"]
    ok0 = abs(t0h - 300) <= tol
    ok1 = abs(t1h - 800) <= tol
    ok = ok0 and ok1
    lines = [
        "T0H = %g ns（标称 300 ±%g）→ %s" % (t0h, tol, "PASS" if ok0 else "FAIL"),
        "T1H = %g ns（标称 800 ±%g）→ %s" % (t1h, tol, "PASS" if ok1 else "FAIL"),
    ]
    if t0l is not None:
        ok0l = abs(t0l - 850) <= tol
        ok = ok and ok0l
        lines.append("T0L = %g ns（WS2812B 典型 850 ±%g）→ %s" % (t0l, tol, "PASS" if ok0l else "FAIL"))
    if t1l is not None:
        ok1l = abs(t1l - 450) <= tol
        ok = ok and ok1l
        lines.append("T1L = %g ns（WS2812B 典型 450 ±%g）→ %s" % (t1l, tol, "PASS" if ok1l else "FAIL"))
    lines += [
        "公式：位由高电平宽度区分（T0H≈300ns / T1H≈800ns）；低电平标称随型号变（WS2812B T0L≈850ns / T1L≈450ns）",
        "依据：%s（%s）" % (th["label"], th["source"]),
    ]
    if t0l is None or t1l is None:
        lines.append("未覆盖：低电平脉宽（可选 --t0l/--t1l）、复位低电平 >50µs 与具体型号差异（WS2812B-V5/SK6812 等以各自 datasheet 为准）")
    if not ok0:
        lines.append("对策 T0H：%s——FPGA/PIO 按时钟数核对（如 8MHz 下 300ns≈2.4 拍，取 2-3 拍实测校准）" % ("偏短会判 0 失败" if t0h < 150 else "偏长会被并成 1"))
    if not ok1:
        lines.append("对策 T1H：%s" % ("偏短会判 0" if t1h < 650 else "偏长占带宽且可能触发复位"))
    lines.append(verdict(ok, "WS2812 高/低电平脉宽"))
    return ok, lines


def calc_servo(pulse_us=None, angle=None, range_deg=180.0):
    """舵机：50Hz 标准，0.5-2.5ms ↔ 0-180°"""
    th = load_th()["servo-pwm"]
    if pulse_us is not None:
        if not 500 <= pulse_us <= 2500:
            return False, [
                "脉宽 %g µs 超出舵机标准行程 500-2500 µs" % pulse_us,
                "依据：%s（%s）" % (th["label"], th["source"]),
                "提示：超出范围的脉宽部分舵机不打（机械限位），强行给可能堵转发热",
            ]
        angle = (pulse_us - 500) / 2000.0 * range_deg
        return True, [
            "脉宽 %g µs → 角度 %.1f°（行程 %g°）" % (pulse_us, angle, range_deg),
            "公式：angle = (pulse-500)/2000 × range",
            "依据：%s（%s）" % (th["label"], th["source"]),
        ]
    if angle is not None:
        if not 0 <= angle <= range_deg:
            raise CalcError("E_RANGE", "角度 0-%g°" % range_deg)
        pulse = 500 + angle / range_deg * 2000
        return True, [
            "角度 %.1f° → 脉宽 %.0f µs" % (angle, pulse),
            "公式：pulse = 500 + angle/range × 2000（50Hz，周期 20ms）",
            "依据：%s（%s）" % (th["label"], th["source"]),
            "提示：定时器配 50Hz 用 timer 计算器；分辨率 1µs ≈ 0.09°（180° 行程）",
        ]
    raise CalcError("E_ARG", "用 --pulse-us（正向）或 --angle（反向）")


def calc_stepper(pulse_us=None, step_deg=1.8, microstep=16, rpm=None, pclk=None):
    """步进：STEP 脉宽检查 / 转速↔STEP 频率 / 定时器分频"""
    th = load_th()["stepper-pulse-min"]
    steps_per_rev = 360.0 / step_deg * microstep
    lines = ["每转步数 = 360/%g × %d 细分 = %g 步" % (step_deg, microstep, steps_per_rev)]
    ok = True
    if pulse_us is not None:
        ok_p = pulse_us >= th["value"]
        ok = ok and ok_p
        lines.append("STEP 脉宽 %g µs（最小 %g µs）→ %s" % (pulse_us, th["value"], "PASS" if ok_p else "FAIL 会丢步"))
    if rpm is not None:
        if rpm <= 0:
            raise CalcError("E_ARG", "rpm 必须为正数")
        step_hz = steps_per_rev * rpm / 60.0
        lines.append("%g rpm → STEP 频率 = %.0f Hz（%.1f kHz）" % (rpm, step_hz, step_hz / 1000))
        if pclk:
            div = pclk / step_hz
            lines.append("定时器（%g Hz）分频 = %.1f → PSC/ARR 组合用 timer 计算器反查" % (pclk, div))
    lines += [
        "公式：STEP_freq = (360/step_deg) × microstep × rpm/60",
        "依据：%s（%s）；转速上限还受驱动电流/力矩曲线限制——失步先降速再查脉宽" % (th["label"], th["source"]),
    ]
    return ok, lines


SERIAL_BAUD_DB = {
    "gps":        ("GPS/NMEA（ublox 等）", 9600, "可配至 115200+；NMEA 默认 9600"),
    "bluetooth":  ("蓝牙 AT 模式（HC-05 等）", 9600, "AT 模式 9600，透传模式多跟随配对配置"),
    "esp-at":     ("ESP32 AT 固件", 115200, "AT 口 115200"),
    "debug":      ("调试串口通用", 115200, "事实标准"),
    "esp32-rom":  ("ESP32 ROM loader 打印", 74880, "上电 boot log 专用，易误认为乱码"),
    "stm32-bl":   ("STM32 系统Bootloader", 115200, "AN2606 各系列不同，常用 115200"),
}


def calc_serial_baud(module=None):
    th = load_th()["stepper-serial-baud"]
    lines = ["常用串口默认波特率速查："]
    for key, (name, baud, note) in sorted(SERIAL_BAUD_DB.items()):
        if module and module != key:
            continue
        lines.append("  %-12s %-24s %d bps  —— %s" % (key, name, baud, note))
    if module and module not in SERIAL_BAUD_DB:
        raise CalcError("E_ARG", "module 取值：%s" % ", ".join(SERIAL_BAUD_DB))
    lines.append("提示：'乱码'先查两端波特率与字长/校验（pitfalls uart 类）；loader 打印波特率与工作波特率不同是高频误会")
    lines.append("依据：%s（%s）" % (th["label"], th["source"]))
    return True, lines


def calc_rtc_drift(ppm, days=1.0):
    """32.768kHz 晶振精度 → RTC 日走时误差（ppm 允许负值=走慢）"""
    if days <= 0:
        raise CalcError("E_ARG", "days 必须为正数")
    sec_per_day = 86400.0
    err_per_day = sec_per_day * abs(ppm) / 1e6
    total = err_per_day * days
    sign = "快" if ppm > 0 else ("慢" if ppm < 0 else "不漂")
    lines = [
        "%+g ppm → 每日误差 ±%.2f s（%s）" % (ppm, err_per_day, sign),
        "%g 天累计误差 ±%.2f s（%.1f 分钟）" % (days, total, total / 60),
        "公式：日误差 = 86400 × |ppm|/1e6；符号：正=走快、负=走慢",
        "依据：%s（%s）" % (load_th()["rtc-crystal-ppm"]["label"], load_th()["rtc-crystal-ppm"]["source"]),
        "提示：常年走时的 RTC 要么选 ±5ppm 晶振+定期校准，要么软件补偿（对 32768 计数做加减校准寄存器）",
    ]
    return True, lines


def calc_usb_clk(fclk, divisor_desc):
    """USB 48MHz 推导链检查：fclk 与分频描述→是否精确 48M"""
    th = load_th()["usb-48m"]
    # divisor_desc 例："pllq=/4"（自定义解析）或直接给数值
    # 简化：用户直接传分频后频率用 --fusb；此处用 fclk 与整数分频试探
    found = []
    for d in range(1, 33):
        f = fclk / d
        if abs(f - th["value"]) < 1.0:
            found.append((d, f))
    # 半整数分频（STM32 PLLQ 不支持，但 RCC 有 USBPRE /1.5）
    f15 = fclk / 1.5
    has15 = abs(f15 - th["value"]) < 1.0
    lines = [
        "要求：USB 时钟精确 48 MHz（0% 容差，FS=12M×4 过采样）",
        "依据：%s（%s）" % (th["label"], th["source"]),
    ]
    if found:
        for d, f in found:
            lines.append("PASS %g Hz / %d = %.0f MHz ✓" % (fclk, d, f / 1e6))
    if has15:
        lines.append("PASS %g Hz / 1.5 = 48.0 MHz ✓（RCC USBPRE=1.5 分频口径）" % fclk)
    if not found and not has15:
        near = min(range(1, 33), key=lambda d: abs(fclk / d - th["value"]))
        lines += [
            "FAIL %g Hz 无整数分频可得 48M（最近 /%d = %.2f MHz）" % (fclk, near, fclk / near / 1e6),
            "对策：换 USB 可整除的主频（72/48/96/168 等常见 USB-friendly 频率）或用独立 USB PLL",
        ]
        return False, lines
    lines.append("注意：整数可分 ≠ RCC 实际支持该分频——PLLQ/USBPRE 的可用档位以目标芯片 RCC 章节为准（如 PLLQ 常见 2-15），本检查只验证算术可除性")
    lines.append("提示：USB 时钟错→枚举失败/CRC 错（trees usb 树）；上板前先算这条链")
    return True, lines


def calc_battery(mah, current_ma, derate=True, days_per_charge=None):
    """电池续航：mAh / 平均电流，默认打 8 折"""
    if mah <= 0 or current_ma <= 0:
        raise CalcError("E_ARG", "mah/current_ma 必须为正数")
    th = load_th()["battery-endurance"]
    factor = (th["value"] / 100.0) if derate else 1.0
    hours = mah * factor / current_ma
    lines = [
        "续航 = %g mAh × %s / %g mA = %.1f 小时（%.1f 天）"
        % (mah, ("0.8 折减" if derate else "不打折"), current_ma, hours, hours / 24),
        "公式：hours = mAh × 0.8 / I_avg（折减含低温/老化/放电平台）",
        "依据：%s（%s）" % (th["label"], th["source"]),
    ]
    if days_per_charge:
        need = hours / 24 / days_per_charge
        lines.append("目标 %g 天一充 → 平均电流需 ≤ %.2f mA（当前 %g mA %s）"
                     % (days_per_charge, mah * factor / 24 / days_per_charge,
                        current_ma, "达标" if current_ma <= mah * factor / 24 / days_per_charge else "超标"))
    lines.append("提示：平均电流 = Σ(各状态电流×占空比)——睡眠 µA 级 vs 工作 mA 级的占空比是 IoT 续航第一杠杆（pwr 树）")
    return True, lines


def calc_modbus_silence(baud):
    """Modbus RTU 帧间隔：3.5 字符 = 3.5×11 bit / baud"""
    if baud <= 0:
        raise CalcError("E_ARG", "baud 必须为正数")
    th = load_th()["modbus-silence-35"]
    bits = 11  # 8N1+起停=10，Modbus 常按 11 位（含校验）口径
    silence = th["value"] * bits / baud
    lines = [
        "%d bps 下帧间隔 = 3.5×%d/%d = %.3f ms" % (baud, bits, baud, silence * 1000),
        "公式：silence = 3.5 字符 × 11 bit / baud（RTU）",
        "依据：%s（%s）" % (th["label"], th["source"]),
        "提示：发送方帧内字节间隔必须 < 此值（否则被当帧结束拆包）；帧间必须 ≥ 此值（9600 时 4ms——定时器/RTOS 调度抖动易踩）",
        "提示：>19200 bps 时 spec 建议固定 1.75ms",
    ]
    return True, lines


def calc_flash_wear(page_bytes=None, freq_per_hour=None, capacity_cycles=10000.0,
                    pages=1, record_bytes=None):
    """片内 Flash 擦写寿命：写入频率 → 擦除次数 → 可用年数。

    --record 给定时按页擦除核算：erases/year = writes/year × record_bytes/page_bytes；
    未给 --record 时按"一次写入=一次擦除"的保守口径。
    """
    if freq_per_hour is None or freq_per_hour <= 0 or capacity_cycles <= 0 or pages <= 0:
        raise CalcError("E_ARG", "freq/cycles/pages 必须为正数")
    if page_bytes is not None and page_bytes <= 0:
        raise CalcError("E_ARG", "page 必须为正数")
    if record_bytes is not None:
        if page_bytes is None:
            raise CalcError("E_ARG", "给 --record 时必须同时给 --page（记录字节需按页折算擦除次数）")
        if record_bytes <= 0:
            raise CalcError("E_ARG", "record 必须为正数")
    th = load_th()["flash-endurance"]
    writes_per_year = freq_per_hour * 24 * 365
    if record_bytes is not None:
        erases_per_year = writes_per_year * record_bytes / page_bytes
        basis = ("按页擦除口径：erases/year = writes/year × record/page = %.0f × %g/%g = %.0f 次/年"
                 % (writes_per_year, record_bytes, page_bytes, erases_per_year))
    else:
        erases_per_year = writes_per_year
        basis = ("未给 --record：按一次写入=一次擦除的保守口径（page 不参与计算；"
                 "实际按页擦除寿命通常更长，补 --page 与 --record 可精确核算）")
    # wear-leveling 轮换 pages 页
    cycles_per_page = erases_per_year / pages
    life_years = capacity_cycles / cycles_per_page
    ok = life_years >= 5.0
    return ok, [
        "写入频率 %g 次/小时 × 8760h = %.0f 次/年" % (freq_per_hour, writes_per_year),
        basis,
        "%d 页轮换 → 单页 %.0f 次擦除/年 → 寿命 %.3g 年（寿命阈值 %g cycles，实测以目标芯片 datasheet 为准）"
        % (pages, cycles_per_page, life_years, th["value"]),
        "公式：life = endurance × pages / erases_per_year",
        "依据：%s（%s）" % (th["label"], th["source"]),
        verdict(ok, "寿命 %.3g 年" % life_years)
        + ("" if ok else "——对策：加页轮换/降频/RAM 缓存批量写/外挂 EEPROM 或 FRAM"),
    ]


def calc_spi_time(nbytes, sck_hz):
    """SPI 传输耗时（全双工按同时收发，只算位数）"""
    if nbytes <= 0 or sck_hz <= 0:
        raise CalcError("E_ARG", "nbytes/sck_hz 必须为正数")
    bits = nbytes * 8
    t = bits / sck_hz
    overhead_cs = 2.0  # 片选建立+保持典型 2µs（量级提示）
    return True, [
        "传输 %.1f µs（%d 字节 @ %.4g Hz，纯移位时间）" % (t * 1e6, nbytes, sck_hz),
        "加片选建立/保持 ≈ %.1f µs → 实际 %.1f µs" % (overhead_cs, (t + overhead_cs * 1e-6) * 1e6),
        "公式：t = bytes×8/SCK",
        "提示：与 i2c-time 对比选总线——SPI 相同字节快 8-40 倍（无地址/ACK 开销）；CS 频繁切换时开销不可忽略",
        "依据：SPI 协议位传输通式",
    ]


def calc_sensor_lsb(raw, fsr, nbits=16, unipolar=False):
    """传感器分辨率换算：双极性满量程为 ±FSR（跨度 2×FSR），单极性才按 FSR 跨度。"""
    if fsr <= 0 or nbits <= 0:
        raise CalcError("E_ARG", "fsr/nbits 必须为正数")
    span = fsr if unipolar else 2 * fsr
    mode = "单极性（0~FSR）" if unipolar else "双极性（±FSR，跨度 2×FSR）"
    lsb = span / (2 ** nbits)
    value = raw * lsb
    return True, [
        "量程口径：%s" % mode,
        "LSB = %s/2^nbits = %g / 2^%d = %.6g（每 LSB 对应物理量）"
        % ("FSR" if unipolar else "2×FSR", span, nbits, lsb),
        "raw %g → 物理量 %.6g" % (raw, value),
        "公式：value = raw × span/2^nbits；双极性 span=2×FSR，单极性 span=FSR（accel ±2g 档 = 16384 LSB/g）",
        "依据：%s（%s）" % (load_th()["sensor-lsb-typical"]["label"], load_th()["sensor-lsb-typical"]["source"]),
        "提示：量程档位与分辨率是跷跷板——要小信号分辨率就降 FSR，够不到量程就升；别用错档位系数（高频错误）",
    ]


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        prog="timing.py", description="嵌入式时序计算器",
        epilog="""示例:
  python timing.py uart --pclk 72000000 --baud 115200     UART 波特率/BRR
  python timing.py timer --pclk 72000000 --freq 1000      反向推荐 PSC/ARR
  python timing.py i2c-rp --bus fast --cb 100             I2C 上拉电阻
  python timing.py can-bit --clk 42000000 --baud 500000   CAN 位时序
  python timing.py fpga-slack --tclk 10 --tco 2.5 --tlogic 3.2 --troute 3.1 --tsu 0.8
  python timing.py demo                                   自检（已知答案回归）
零依赖、离线；每个结果带公式、合法性判定与依据。--format json 需放子命令前。""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--format", choices=("text", "json"), default="text",
                        help="输出格式（放在子命令前，如 timing.py --format json uart ...）")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("uart", help="UART 波特率/BRR")
    p.add_argument("--pclk", type=float, required=True)
    p.add_argument("--baud", type=float, required=True)
    p.add_argument("--os", type=int, default=16, choices=(8, 16))

    p = sub.add_parser("timer", help="定时器 PWM")
    p.add_argument("--pclk", type=float, required=True)
    p.add_argument("--freq", type=float)
    p.add_argument("--psc", type=int)
    p.add_argument("--arr", type=int)

    p = sub.add_parser("i2c-rp", help="I2C 上拉电阻")
    p.add_argument("--bus", required=True, choices=tuple(I2C_BUS))
    p.add_argument("--cb", type=float, required=True, help="总线电容 pF")
    p.add_argument("--vdd", type=float, default=3.3)

    p = sub.add_parser("i2c-time", help="I2C 传输耗时")
    p.add_argument("--bus", required=True, choices=tuple(I2C_BUS))
    p.add_argument("--bytes", type=int, required=True, dest="nbytes")

    p = sub.add_parser("can-bit", help="CAN 位时序")
    p.add_argument("--clk", type=float, required=True)
    p.add_argument("--baud", type=float, required=True)
    p.add_argument("--sp", type=float, default=87.5)
    p.add_argument("--family", choices=("bxcan", "fdcan"), default="bxcan",
                   help="芯片族：bxCAN（F1/F4 经典，25TQ 上限）或 FDCAN（G4/H7，385TQ）")

    p = sub.add_parser("adc-rad", help="ADC 最大源阻抗")
    p.add_argument("--ts", type=float, required=True, help="采样周期数 cycles")
    p.add_argument("--fadc", type=float, required=True)
    p.add_argument("--nbits", type=int, default=12)
    p.add_argument("--cs", type=float, default=8.0, help="采样电容 pF")
    p.add_argument("--radc", type=float, default=0.0, help="片内 ADC 采样开关电阻 Ω（可选，从结果中扣减）")

    p = sub.add_parser("rc", help="RC 截止频率")
    p.add_argument("--r", type=float)
    p.add_argument("--c", type=float)
    p.add_argument("--fc", type=float)

    p = sub.add_parser("spi", help="SPI 分频")
    p.add_argument("--fclk", type=float, required=True)
    p.add_argument("--div", type=float, required=True)

    p = sub.add_parser("nyquist", help="采样定理检查")
    p.add_argument("--fs", type=float, required=True)
    p.add_argument("--fbw", type=float, required=True)

    p = sub.add_parser("deadtime", help="死区占比")
    p.add_argument("--fsw", type=float, required=True)
    p.add_argument("--dt", type=float, required=True)

    p = sub.add_parser("fpga-uart", help="FPGA UART 整数分频")
    p.add_argument("--clk", type=float, required=True)
    p.add_argument("--baud", type=float, required=True)

    p = sub.add_parser("fpga-slack", help="FPGA 静态时序 slack")
    p.add_argument("--tclk", type=float, required=True, help="时钟周期 ns")
    p.add_argument("--tco", type=float, required=True)
    p.add_argument("--tlogic", type=float, required=True)
    p.add_argument("--troute", type=float, required=True)
    p.add_argument("--tsu", type=float, required=True)

    p = sub.add_parser("fpga-pwm", help="FPGA PWM 位深")
    p.add_argument("--clk", type=float, required=True)
    p.add_argument("--fpwm", type=float, required=True)

    p = sub.add_parser("wdg", help="看门狗超时")
    p.add_argument("--clk", type=float, required=True, help="看门狗时钟（如 LSI 40000）")
    p.add_argument("--presc", type=float, required=True, help="预分频（4/8/16/.../256）")
    p.add_argument("--reload", type=float, required=True, help="重装值")

    p = sub.add_parser("pll", help="PLL 输出与 VCO 窗")
    p.add_argument("--clkin", type=float, required=True)
    p.add_argument("--m", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--p", type=int, required=True)
    p.add_argument("--vcomin", type=float, default=100e6)
    p.add_argument("--vcomax", type=float, default=200e6)

    p = sub.add_parser("divider", help="分压电阻")
    p.add_argument("--vin", type=float, required=True)
    p.add_argument("--vout", type=float, required=True)
    p.add_argument("--iua", type=float, dest="current_ua", help="分压电流 µA（可选；给定后 R_total/R1/R2 全由电流定）")

    p = sub.add_parser("ntc", help="NTC 阻值（Beta 公式）")
    p.add_argument("--r25", type=float, required=True)
    p.add_argument("--beta", type=float, required=True)
    p.add_argument("--temp", type=float, required=True, help="目标温度 °C")

    p = sub.add_parser("rc-settle", help="RC 建立时间")
    p.add_argument("--r", type=float, required=True)
    p.add_argument("--c", type=float, required=True)
    p.add_argument("--nbits", type=int, default=10)

    p = sub.add_parser("ppm", help="晶振 ppm 漂移")
    p.add_argument("--base", type=float, required=True, help="标称频率 Hz")
    p.add_argument("--ppm", type=float, required=True)

    p = sub.add_parser("esp32-clk", help="ESP32 外设时钟速查与分频")
    p.add_argument("--div", type=float, help="APB 80MHz 的分频（可选）")
    p.add_argument("--target", type=float, help="目标频率 Hz（可选）")

    p = sub.add_parser("rp2040-uart", help="RP2040 UART divider（IBRD 16 位 + FBRD 6 位）")
    p.add_argument("--clk-peri", type=float, required=True, help="clk_peri Hz")
    p.add_argument("--baud", type=float, required=True)

    p = sub.add_parser("pwm-dim", help="PWM 调光分辨率检查")
    p.add_argument("--clk", type=float, required=True)
    p.add_argument("--fpwm", type=float, required=True)

    p = sub.add_parser("ws2812", help="WS2812 高/低电平脉宽检查")
    p.add_argument("--t0h", type=float, required=True, help="T0H 实测 ns")
    p.add_argument("--t1h", type=float, required=True, help="T1H 实测 ns")
    p.add_argument("--t0l", type=float, help="T0L 实测 ns（可选，给了才判）")
    p.add_argument("--t1l", type=float, help="T1L 实测 ns（可选，给了才判）")

    p = sub.add_parser("servo", help="舵机脉宽↔角度")
    p.add_argument("--pulse-us", type=float, help="脉宽 µs（正向求角度）")
    p.add_argument("--angle", type=float, help="角度（反向求脉宽）")
    p.add_argument("--range", type=float, default=180.0, help="行程角（默认 180）")

    p = sub.add_parser("stepper", help="步进电机参数")
    p.add_argument("--pulse-us", type=float, help="STEP 脉宽 µs（检查）")
    p.add_argument("--step-deg", type=float, default=1.8, help="步距角")
    p.add_argument("--microstep", type=int, default=16)
    p.add_argument("--rpm", type=float, help="目标转速")
    p.add_argument("--pclk", type=float, help="定时器时钟（算 STEP 频率分频）")

    p = sub.add_parser("serial-baud", help="常用模块默认波特率速查")
    p.add_argument("--module", help="gps/bluetooth/esp-at/debug（可省略=全表）")

    p = sub.add_parser("rtc-drift", help="RTC 晶振误差→日走时")
    p.add_argument("--ppm", type=float, required=True, help="晶振精度（带符号）")
    p.add_argument("--days", type=float, default=1.0)

    p = sub.add_parser("usb-clk", help="USB 48MHz 推导链检查")
    p.add_argument("--fclk", type=float, required=True, help="待分频时钟 Hz")

    p = sub.add_parser("battery", help="电池续航估算")
    p.add_argument("--mah", type=float, required=True)
    p.add_argument("--i", type=float, required=True, dest="current_ma", help="平均电流 mA")
    p.add_argument("--no-derate", action="store_true", help="不打 8 折")
    p.add_argument("--days", type=float, dest="days_per_charge", help="目标续航天数（校核）")

    p = sub.add_parser("modbus-silence", help="Modbus RTU 帧间隔")
    p.add_argument("--baud", type=float, required=True)

    p = sub.add_parser("flash-wear", help="Flash 擦写寿命")
    p.add_argument("--page", type=float, help="页字节（可选；与 --record 同给时按页擦除核算）")
    p.add_argument("--record", type=float, dest="record_bytes", help="单条记录字节（可选；缺省按一次写入=一次擦除）")
    p.add_argument("--freq", type=float, required=True, help="写入频率 次/小时")
    p.add_argument("--cycles", type=float, default=10000.0, help="擦写寿命")
    p.add_argument("--pages", type=int, default=1, help="轮换页数")

    p = sub.add_parser("spi-time", help="SPI 传输耗时")
    p.add_argument("--bytes", type=int, required=True, dest="nbytes")
    p.add_argument("--sck", type=float, required=True)

    p = sub.add_parser("sensor-lsb", help="传感器分辨率换算")
    p.add_argument("--raw", type=float, required=True)
    p.add_argument("--fsr", type=float, required=True, help="满量程（如 accel ±2g 档=2）")
    p.add_argument("--nbits", type=int, default=16)
    p.add_argument("--unipolar", action="store_true", help="单极性 0~FSR（默认双极性 ±FSR，跨度 2×FSR）")

    p = sub.add_parser("fpga-i2c", help="FPGA 行为级 I2C 分频")
    p.add_argument("--clk", type=float, required=True, help="FPGA 时钟 MHz")
    p.add_argument("--clk-div", type=float, required=True, help="半位分频数")
    p.add_argument("--rate", type=float, default=100e3, help="目标 SCL Hz")

    p = sub.add_parser("fpga-debounce", help="FPGA 消抖窗口")
    p.add_argument("--clk", type=float, required=True, help="采样时钟 Hz")
    p.add_argument("--ms", type=float, required=True, help="消抖窗口 ms")
    p.add_argument("--stages", type=int, default=2, help="移位寄存器已用级数")

    sub.add_parser("fpga-cdc", help="跨时钟域（CDC）检查单")

    p = sub.add_parser("fpga-fifo", help="FPGA 异步 FIFO 溢出检查")
    p.add_argument("--tx-bps", type=float, required=True, help="写入侧波特率（UART 口径）")
    p.add_argument("--read-bps", type=float, required=True, help="读出侧波特率")
    p.add_argument("--burst", type=int, required=True, help="突发字节数")
    p.add_argument("--depth", type=int, required=True, help="FIFO 深度")

    sub.add_parser("list", help="列出全部计算器")
    sub.add_parser("demo", help="自检：已知答案回归")

    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        return 0

    try:
        if args.cmd == "list":
            names = ["uart", "timer", "i2c-rp", "i2c-time", "can-bit", "adc-rad", "rc",
                     "spi", "spi-time", "nyquist", "deadtime", "fpga-uart", "fpga-slack", "fpga-pwm",
                     "wdg", "pll", "divider", "ntc", "rc-settle", "ppm",
                     "fpga-i2c", "fpga-debounce", "fpga-cdc", "fpga-fifo",
                     "esp32-clk", "rp2040-uart", "pwm-dim", "ws2812", "servo", "stepper", "serial-baud",
                     "rtc-drift", "usb-clk", "battery", "modbus-silence", "flash-wear", "sensor-lsb"]
            print("共 %d 个计算器：\n" % len(names))
            print("\n".join("- " + n for n in names))
            return 0
        if args.cmd == "demo":
            cases = [
                ("uart 72M@115200", lambda: calc_uart(72e6, 115200), True),
                ("uart 8M@921600", lambda: calc_uart(8e6, 921600), False),
                ("timer 72M@1k", lambda: calc_timer(72e6, freq=1000), True),
                ("i2c-rp fast 100pF", lambda: calc_i2c_rp("fast", 100), True),
                ("i2c-rp fast 500pF", lambda: calc_i2c_rp("fast", 500), False),
                ("can 42M@500k@87.5", lambda: calc_can(42e6, 500e3, 87.5), True),
                ("nyquist 1k/100", lambda: calc_nyquist(1000, 100), True),
                ("nyquist 150/100", lambda: calc_nyquist(150, 100), False),
                ("fpga-uart 50M@115200", lambda: calc_fpga_uart(50e6, 115200), True),
                ("fpga-slack 10/2.5/3.2/3.1/0.8", lambda: calc_fpga_slack(10, 2.5, 3.2, 3.1, 0.8), True),
                ("fpga-slack 9/2.5/3.2/3.1/0.8", lambda: calc_fpga_slack(9, 2.5, 3.2, 3.1, 0.8), False),
                ("fpga-pwm 50M@20k", lambda: calc_fpga_pwm(50e6, 20e3), True),
                ("wdg 40k/256/625 ≈4s", lambda: calc_wdg(40000, 256, 625), True),
                ("pll 8M/4/80/2=80M", lambda: calc_pll(8e6, 4, 80, 2), True),
                ("pll 8M/1/168/2 VCO 超窗", lambda: calc_pll(8e6, 1, 168, 2), False),
                ("divider 12V→3.3V", lambda: calc_divider(12.0, 3.3), True),
                ("ntc 10k B3950@50°C", lambda: calc_ntc(10000, 3950, 50), True),
                ("rc-settle 10k/100n/10bit", lambda: calc_rc_settle(10000, 100e-9, 10), True),
                ("ppm 8M ±20", lambda: calc_ppm(8e6, 20), True),
                ("fpga-i2c 50M/250@100k", lambda: calc_fpga_i2c(50, 250), True),
                ("fpga-i2c 50M/250@400k", lambda: calc_fpga_i2c(50, 250, 400e3), False),
                ("fpga-fifo 稳态不积压", lambda: calc_fpga_uart_fifo(115200, 230400, 64, 128), True),
                ("fpga-fifo 稳态积压", lambda: calc_fpga_uart_fifo(230400, 115200, 64, 128), False),
                ("rp2040-uart 125M@115200", lambda: calc_rp2040_uart(125e6, 115200), True),
                ("pwm-dim 72M@1k 16位", lambda: calc_pwm_dim(72e6, 1000), True),
                ("pwm-dim 8M@40k 不足8位", lambda: calc_pwm_dim(8e6, 40e3), False),
                ("ws2812 标称", lambda: calc_ws2812(300, 800), True),
                ("ws2812 T1H 偏短", lambda: calc_ws2812(300, 400), False),
                ("servo 1500µs", lambda: calc_servo(pulse_us=1500), True),
                ("servo 超程", lambda: calc_servo(pulse_us=3000), False),
                ("stepper 脉宽合规", lambda: calc_stepper(pulse_us=5), True),
                ("stepper 脉宽丢步", lambda: calc_stepper(pulse_us=1), False),
                ("rtc-drift 20ppm", lambda: calc_rtc_drift(20, 30), True),
                ("usb-clk 72M", lambda: calc_usb_clk(72e6, ""), True),
                ("usb-clk 66M", lambda: calc_usb_clk(66e6, ""), False),
                ("modbus 9600", lambda: calc_modbus_silence(9600), True),
                ("flash-wear 5年", lambda: calc_flash_wear(64, 2, 10000, 16), True),
                ("flash-wear 不足", lambda: calc_flash_wear(64, 1000, 10000, 1), False),
                ("sensor-lsb accel 2g", lambda: calc_sensor_lsb(8192, 2.0, 16), True),
            ]
            failed = []
            for name, fn, expect in cases:
                ok, _ = fn()
                status = "PASS" if ok == expect else "FAIL"
                if ok != expect:
                    failed.append(name)
                print("%-32s expect=%-5s got=%-5s %s" % (name, expect, ok, status))
            if failed:
                print("\n回归失败：%s" % ", ".join(failed))
                return 1
            print("\n自检通过：%d 个已知答案全部命中。" % len(cases))
            return 0

        funcs = {
            "uart": lambda: calc_uart(args.pclk, args.baud, args.os),
            "timer": lambda: calc_timer(args.pclk, getattr(args, "freq", None),
                                        getattr(args, "psc", None), getattr(args, "arr", None)),
            "i2c-rp": lambda: calc_i2c_rp(args.bus, args.cb, args.vdd),
            "i2c-time": lambda: calc_i2c_time(args.bus, args.nbytes),
            "can-bit": lambda: calc_can(args.clk, args.baud, args.sp, args.family),
            "adc-rad": lambda: calc_adc_rad(args.ts, args.fadc,
                                            getattr(args, "nbits", 12), getattr(args, "cs", 8.0),
                                            getattr(args, "radc", 0.0)),
            "rc": lambda: calc_rc(getattr(args, "r", None), getattr(args, "c", None),
                                  getattr(args, "fc", None)),
            "spi": lambda: calc_spi(args.fclk, args.div),
            "nyquist": lambda: calc_nyquist(args.fs, args.fbw),
            "deadtime": lambda: calc_deadtime(args.fsw, args.dt),
            "fpga-uart": lambda: calc_fpga_uart(args.clk, args.baud),
            "fpga-slack": lambda: calc_fpga_slack(args.tclk, args.tco, args.tlogic, args.troute, args.tsu),
            "fpga-pwm": lambda: calc_fpga_pwm(args.clk, args.fpwm),
            "wdg": lambda: calc_wdg(args.clk, args.presc, args.reload),
            "pll": lambda: calc_pll(args.clkin, args.m, args.n, args.p,
                                    getattr(args, "vcomin", 100e6), getattr(args, "vcomax", 200e6)),
            "divider": lambda: calc_divider(args.vin, args.vout,
                                            getattr(args, "current_ua", None)),
            "ntc": lambda: calc_ntc(args.r25, args.beta, args.temp),
            "rc-settle": lambda: calc_rc_settle(args.r, args.c,
                                                getattr(args, "nbits", 10)),
            "ppm": lambda: calc_ppm(args.base, args.ppm),
            "fpga-i2c": lambda: calc_fpga_i2c(args.clk, args.clk_div,
                                              getattr(args, "rate", 100e3)),
            "fpga-debounce": lambda: calc_fpga_debounce(args.clk, args.ms,
                                                        getattr(args, "stages", 2)),
            "fpga-cdc": lambda: calc_fpga_cdc(),
            "fpga-fifo": lambda: calc_fpga_uart_fifo(getattr(args, "tx_bps", 0),
                                                     getattr(args, "read_bps", 1),
                                                     getattr(args, "burst", 0),
                                                     getattr(args, "depth", 0)),
            "esp32-clk": lambda: calc_esp32_clk(getattr(args, "div", None),
                                                getattr(args, "target", None)),
            "rp2040-uart": lambda: calc_rp2040_uart(args.clk_peri, args.baud),
            "pwm-dim": lambda: calc_pwm_dim(args.clk, args.fpwm),
            "ws2812": lambda: calc_ws2812(args.t0h, args.t1h,
                                          getattr(args, "t0l", None), getattr(args, "t1l", None)),
            "servo": lambda: calc_servo(getattr(args, "pulse_us", None),
                                        getattr(args, "angle", None),
                                        getattr(args, "range", 180.0)),
            "stepper": lambda: calc_stepper(getattr(args, "pulse_us", None),
                                            getattr(args, "step_deg", 1.8),
                                            getattr(args, "microstep", 16),
                                            getattr(args, "rpm", None),
                                            getattr(args, "pclk", None)),
            "serial-baud": lambda: calc_serial_baud(getattr(args, "module", None)),
            "rtc-drift": lambda: calc_rtc_drift(args.ppm, getattr(args, "days", 1.0)),
            "usb-clk": lambda: calc_usb_clk(args.fclk, ""),
            "battery": lambda: calc_battery(args.mah, args.current_ma,
                                            not getattr(args, "no_derate", False),
                                            getattr(args, "days_per_charge", None)),
            "modbus-silence": lambda: calc_modbus_silence(args.baud),
            "flash-wear": lambda: calc_flash_wear(getattr(args, "page", None), args.freq,
                                                  getattr(args, "cycles", 10000.0),
                                                  getattr(args, "pages", 1),
                                                  getattr(args, "record_bytes", None)),
            "spi-time": lambda: calc_spi_time(args.nbytes, args.sck),
            "sensor-lsb": lambda: calc_sensor_lsb(args.raw, args.fsr,
                                                  getattr(args, "nbits", 16),
                                                  getattr(args, "unipolar", False)),
        }
        if args.cmd not in funcs:
            parser.print_help()
            return 2
        ok, lines = funcs[args.cmd]()
        if args.format == "json":
            print(json.dumps({"tool": "embedded-timing-calc", "version": __version__,
                              "calc": args.cmd, "pass": ok, "lines": lines},
                             ensure_ascii=False, indent=2))
        else:
            print("\n".join(lines))
        return 0 if ok else 1
    except CalcError as exc:
        msg = "%s：%s" % (exc.code, exc)
        if args.format == "json":
            print(json.dumps({"tool": "embedded-timing-calc", "version": __version__,
                              "calc": getattr(args, "cmd", "?"), "pass": False,
                              "error": msg}, ensure_ascii=False, indent=2))
        else:
            print(msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
