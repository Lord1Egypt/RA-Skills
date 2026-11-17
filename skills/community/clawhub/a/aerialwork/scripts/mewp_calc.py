#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEWP 工程计算工具(高空作业平台) —— 确定性工程初算 CLI

子命令:
  tipping-check    整机稳定性初算(稳定力矩 / 倾翻力矩比)
  wind-load        风载荷(GB 50009 基本风压与风作用力)
  motor-check      电机功率校核(扭矩法, 含效率与裕量)
  hydraulic-check  油缸出力与泵/马达系统功率校核
  cylinder-size    油缸缸径/杆径选型与压杆稳定校核

说明:
  1. 本工具输出均为工程初算值, 用于方案筛选与快速校核;
     安全攸关结论(稳定性、结构强度、安全回路)必须按
     GB/T 25849-2010 / EN 280 等标准原文复核, 并由具备资质机构评审。
  2. 脚本内默认的安全系数、载荷组合、风荷载体型系数等均为提示值,
     标书 / 鉴定用途必须按标准条款核定。
"""

import argparse
import math
import sys

G = 9.81  # 重力加速度 m/s^2


def _print_formula(lines):
    print("--- 计算过程 ---")
    for ln in lines:
        print("  " + ln)
    print("--- 结果 ---")


def _fmt(x, nd=3):
    return f"{x:.{nd}f}"


# ---------------------------------------------------------------- 稳定性
def cmd_tipping_check(a):
    lines = []
    m_self = a.mass
    F_self = m_self * G
    arm = a.cg_arm if a.cg_arm is not None else a.span / 2.0
    lines.append(f"整机重力 F1 = m*g = {_fmt(m_self)} kg x {G} m/s^2 = {_fmt(F_self)} N")
    lines.append(f"稳定力臂 Ls = {_fmt(arm)} m (cg_arm 或 span/2)")
    M_stab = F_self * arm
    lines.append(f"稳定力矩 Ms = F1*Ls = {_fmt(M_stab)} N*m")

    M_tip = 0.0
    if a.load and a.reach:
        F_p = a.load * G
        M_load = F_p * a.reach
        M_tip += M_load
        lines.append(
            f"平台额定载荷 F2 = {_fmt(a.load)} kg x {G} = {_fmt(F_p)} N; "
            f"幅度 Lr = {_fmt(a.reach)} m"
        )
        lines.append(f"载荷倾翻力矩 Ml = F2*Lr = {_fmt(M_load)} N*m")

    if a.wind_speed and a.wind_height and a.area:
        # 基本风压 w0 = v^2/1600 (kPa, GB 50009), 风作用力 F = w0*A*coef
        w0_kpa = a.wind_speed ** 2 / 1600.0
        q_pa = 0.5 * 1.2 * a.wind_speed ** 2  # 动压 1/2*rho*v^2, rho=1.2 kg/m^3
        F_w = w0_kpa * 1000.0 * a.area * a.coef
        M_w = F_w * a.wind_height
        M_tip += M_w
        lines.append(
            f"基本风压 w0 = v^2/1600 = {_fmt(a.wind_speed)}^2/1600 = {_fmt(w0_kpa, 4)} kPa "
            f"(动压 1/2*rho*v^2 = {_fmt(q_pa)} Pa, rho=1.2)"
        )
        lines.append(
            f"风作用力 Fw = w0*A*coef = {_fmt(w0_kpa, 4)} kPa x {_fmt(a.area)} m^2 x "
            f"{_fmt(a.coef, 2)} = {_fmt(F_w / 1000.0)} kN"
        )
        lines.append(f"风载力矩 Mw = Fw*h = {_fmt(F_w / 1000.0)} kN x {_fmt(a.wind_height)} m = {_fmt(M_w / 1000.0)} kN*m")

    if a.extra_moment:
        M_tip += a.extra_moment * 1000.0
        lines.append(f"附加力矩 Me = {_fmt(a.extra_moment)} kN*m")

    lines.append(f"总倾翻力矩 Mt = {_fmt(M_tip / 1000.0)} kN*m")

    if M_tip <= 0:
        print("错误: 未提供 --load/--reach 或 --wind 等倾翻输入, 无法计算倾翻力矩。")
        sys.exit(2)

    k = M_stab / M_tip
    lines.append(f"稳定系数 K = Ms/Mt = {_fmt(k)}")
    verdict = "满足(初算)" if k >= a.sf else "不满足(初算)"
    lines.append(f"判定: K={_fmt(k)} vs 要求系数 {_fmt(a.sf)} -> {verdict}")

    print("=== MEWP 整机稳定性初算(提示性) ===")
    _print_formula(lines)
    print(f"  稳定力矩 Ms = {_fmt(M_stab / 1000.0)} kN*m")
    print(f"  倾翻力矩 Mt = {_fmt(M_tip / 1000.0)} kN*m")
    print(f"  稳定系数 K  = {_fmt(k)}  (要求 >= {_fmt(a.sf)}, 该系数为提示值, 须按标准条款核定)")
    print(f"  结论       = {verdict}")
    if k < a.sf:
        print("  提示: 可增大支承跨距(支腿/履带跨距)、后移配重或降低额定载荷/幅度后重算。")


# ---------------------------------------------------------------- 风载
def cmd_wind_load(a):
    lines = []
    w0_kpa = a.speed ** 2 / 1600.0
    q_pa = 0.5 * 1.2 * a.speed ** 2
    F_n = w0_kpa * 1000.0 * a.area * a.coef
    lines.append(f"基本风压 w0 = v^2/1600 = {_fmt(a.speed)}^2 / 1600 = {_fmt(w0_kpa, 5)} kPa (GB 50009 式, v 为基本风速 m/s)")
    lines.append(f"动压校核 q = 1/2*rho*v^2 = 0.5 x 1.2 x {_fmt(a.speed)}^2 = {_fmt(q_pa)} Pa (rho=1.2 kg/m^3)")
    lines.append(f"风作用力 F = w0 * A * coef = {_fmt(w0_kpa, 5)} kPa x {_fmt(a.area)} m^2 x {_fmt(a.coef, 2)}")
    print("=== 风载荷计算 ===")
    _print_formula(lines)
    print(f"  基本风压 w0 = {_fmt(w0_kpa, 5)} kPa = {_fmt(w0_kpa * 1000.0)} Pa")
    print(f"  风作用力 F  = {_fmt(F_n / 1000.0)} kN (面积 {_fmt(a.area)} m^2, 体型系数 {_fmt(a.coef, 2)} 为提示值)")
    if a.wind_height:
        print(f"  对平台/臂架取力臂 h={_fmt(a.wind_height)} m 时, 风载力矩 M = {_fmt(F_n * a.wind_height / 1000.0)} kN*m")
    print("  参考: MEWP 工作状态设计风速通常取 12.5 m/s(约6级风), 以标准原文与机器铭牌为准。")


# ---------------------------------------------------------------- 电机
def cmd_motor_check(a):
    lines = []
    omega = 2 * math.pi * a.speed / 60.0
    p_out = a.torque * omega
    p_in = p_out / a.efficiency
    lines.append(f"角速度 omega = 2*pi*n/60 = {_fmt(a.speed)} rpm -> {_fmt(omega, 4)} rad/s")
    lines.append(f"轴功率 P_out = T*omega = {_fmt(a.torque)} N*m x {_fmt(omega, 4)} = {_fmt(p_out / 1000.0)} kW")
    lines.append(f"输入功率 P_in = P_out/eta = {_fmt(p_out / 1000.0)} / {_fmt(a.efficiency, 2)} = {_fmt(p_in / 1000.0)} kW")
    print("=== 电机功率校核(扭矩法) ===")
    _print_formula(lines)
    p_out_kw = p_out / 1000.0
    p_in_kw = p_in / 1000.0
    if a.rated:
        margin = (a.rated - p_in_kw) / a.rated * 100.0
        lines2 = f"额定功率 Pr = {_fmt(a.rated)} kW; 裕量 = (Pr-P_in)/Pr = {_fmt(margin, 1)}%"
        print("--- 校核 ---")
        print("  " + lines2)
        verdict = "通过(初算)" if margin > 0 else "不通过(初算)"
        print(f"  轴功率 P_out = {_fmt(p_out_kw)} kW; 输入功率 P_in = {_fmt(p_in_kw)} kW")
        print(f"  结论 = {verdict} (裕量 {_fmt(margin, 1)}%, 空载/瞬时按工作制另行核算)")
    else:
        print(f"  轴功率 P_out = {_fmt(p_out_kw)} kW; 输入功率 P_in = {_fmt(p_in_kw)} kW (未提供 --rated, 仅需求功率)")
    if a.duty:
        print(f"  工作制: {a.duty} —— 启动/制动/间歇载荷须按等效法校核温升与过载能力。")


# ---------------------------------------------------------------- 液压
def cmd_hydraulic_check(a):
    lines = []
    p_pa = a.pressure * 1e6
    d = a.bore / 1000.0
    rod = a.rod / 1000.0
    area_ext = math.pi * d ** 2 / 4.0
    area_ret = math.pi * (d ** 2 - rod ** 2) / 4.0
    f_ext = p_pa * area_ext
    f_ret = p_pa * area_ret
    lines.append(f"无杆腔面积 Ae = pi*D^2/4 = 3.1416 x {_fmt(d)}^2/4 = {_fmt(area_ext * 1e6, 1)} mm^2")
    lines.append(f"有杆腔面积 Ar = pi*(D^2-d^2)/4 = {_fmt(area_ret * 1e6, 1)} mm^2")
    lines.append(f"伸出推力 F_ext = p*Ae = {_fmt(a.pressure)} MPa x {_fmt(area_ext * 1e6, 1)} mm^2 = {_fmt(f_ext / 1000.0)} kN")
    lines.append(f"缩回拉力 F_ret = p*Ar = {_fmt(f_ret / 1000.0)} kN")
    v_ext = a.flow * 1e6 / 60.0 / (area_ext * 1e6)  # mm/s
    v_ret = a.flow * 1e6 / 60.0 / (area_ret * 1e6)
    lines.append(f"伸出速度 v = Q/Ae = {_fmt(a.flow)} L/min / {_fmt(area_ext * 1e6, 1)} mm^2 = {_fmt(v_ext, 2)} mm/s")
    lines.append(f"缩回速度 v = Q/Ar = {_fmt(v_ret, 2)} mm/s")
    p_hyd = p_pa * (a.flow / 1000.0 / 60.0) / a.efficiency
    lines.append(f"系统功率 P = p*Q/eta = {_fmt(a.pressure)} MPa x {_fmt(a.flow)} L/min / {_fmt(a.efficiency, 2)} = {_fmt(p_hyd / 1000.0)} kW")
    print("=== 液压油缸出力与泵系统校核 ===")
    _print_formula(lines)
    print(f"  伸出推力 F_ext = {_fmt(f_ext / 1000.0)} kN; 缩回拉力 F_ret = {_fmt(f_ret / 1000.0)} kN")
    print(f"  伸出速度 {_fmt(v_ext, 2)} mm/s; 缩回速度 {_fmt(v_ret, 2)} mm/s")
    print(f"  泵系统功率 = {_fmt(p_hyd / 1000.0)} kW(含效率 {_fmt(a.efficiency, 2)} 提示值)")
    print("  提示: 背压、冲击压力与保持回路(平衡阀/液控单向阀)按标准与详细设计核算。")


# ---------------------------------------------------------------- 油缸选型
def cmd_cylinder_size(a):
    lines = []
    f_load = a.load * 1000.0
    p_pa = a.pressure * 1e6
    d = math.sqrt(4.0 * f_load / (math.pi * p_pa * a.efficiency))
    rod = d * a.rod_ratio
    lines.append(f"所需缸径 D = sqrt(4*F/(pi*p*eta)) = sqrt(4 x {_fmt(f_load)} N / (3.1416 x {_fmt(a.pressure)} MPa x {_fmt(a.efficiency, 2)})) = {_fmt(d * 1000.0, 1)} mm")
    lines.append(f"杆径 d = {_fmt(a.rod_ratio, 2)} * D = {_fmt(rod * 1000.0, 1)} mm (杆径比 0.5-0.7 常规)")
    print("=== 油缸缸径选型 ===")
    _print_formula(lines)
    print(f"  理论缸径 D = {_fmt(d * 1000.0, 1)} mm -> 圆整取标准缸径")
    print(f"  杆径 d   = {_fmt(rod * 1000.0, 1)} mm")
    # 压杆稳定: 分别校核缸筒与活塞杆, 取临界力较小者为控制件
    e_gpa = 210.0
    mu = {"fixed": 0.65, "pinned": 1.0, "cantilever": 2.0}[a.mount]
    l_eff = mu * (a.stroke / 1000.0)
    lines2 = []
    lines2.append(f"长度系数 mu = {a.mount} -> {_fmt(mu, 2)}; 有效长度 L = mu*行程 = {_fmt(l_eff, 3)} m")
    lines2.append("欧拉临界力 Pcr = pi^2*E*I / L^2, E=210 GPa; 杆/筒均按同长度系数简化(提示值)")
    # 缸筒: 内径近似取杆径(真实内孔一般略大于杆径, 该近似偏不安全, 须按样本壁厚复核)
    i_bar = math.pi * (d ** 4 - rod ** 4) / 64.0
    a_bar = math.pi * (d ** 2 - rod ** 2) / 4.0
    k_bar = math.sqrt(i_bar / a_bar)
    lam_bar = l_eff / k_bar
    pcr_bar = math.pi ** 2 * e_gpa * 1e9 * i_bar / l_eff ** 2
    lines2.append(
        f"[缸筒] I = pi*(D^4-d^4)/64 = {_fmt(i_bar * 1e12, 1)} mm^4, A = {_fmt(a_bar * 1e6, 1)} mm^2, "
        f"k = sqrt(I/A) = {_fmt(k_bar * 1000.0, 2)} mm, lambda = {_fmt(lam_bar, 1)}"
    )
    lines2.append(f"[缸筒] Pcr = {_fmt(pcr_bar / 1000.0)} kN")
    # 活塞杆: 按实心杆近似
    i_rod_only = math.pi * rod ** 4 / 64.0
    a_rod_only = math.pi * rod ** 2 / 4.0
    k_rod = math.sqrt(i_rod_only / a_rod_only)
    lam_rod = l_eff / k_rod
    pcr_rod = math.pi ** 2 * e_gpa * 1e9 * i_rod_only / l_eff ** 2
    lines2.append(
        f"[活塞杆] I = pi*d^4/64 = {_fmt(i_rod_only * 1e12, 1)} mm^4, A = {_fmt(a_rod_only * 1e6, 1)} mm^2, "
        f"k = d/4 = {_fmt(k_rod * 1000.0, 2)} mm, lambda = {_fmt(lam_rod, 1)}"
    )
    lines2.append(f"[活塞杆] Pcr = {_fmt(pcr_rod / 1000.0)} kN")
    pcr_kN = min(pcr_bar, pcr_rod) / 1000.0
    crit_name = "缸筒" if pcr_bar <= pcr_rod else "活塞杆"
    n_buckle = pcr_kN / a.load
    lines2.append(f"控制件 = {crit_name}; 临界力 Pcr = {_fmt(pcr_kN)} kN")
    lines2.append(f"稳定安全系数 n = Pcr/F = {_fmt(pcr_kN)} / {_fmt(a.load)} = {_fmt(n_buckle, 2)}")
    verdict = "满足(初算)" if n_buckle >= a.n_min else "不满足(初算)"
    print("--- 压杆稳定校核(缸筒与活塞杆, E=210 GPa) ---")
    for ln in lines2:
        print("  " + ln)
    print(f"  稳定系数 n = {_fmt(n_buckle, 2)} vs 要求 {_fmt(a.n_min, 2)} -> {verdict}")
    if verdict.startswith("不"):
        print("  提示: 提高缸径/加大杆径比、增设导向套或中间支承可提高稳定性。")


def build_parser():
    p = argparse.ArgumentParser(
        prog="mewp_calc.py",
        description="MEWP 高空作业平台工程初算工具(安全攸关结论须按标准复核)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("tipping-check", help="整机稳定性初算")
    s.add_argument("--mass", type=float, required=True, help="整机质量 kg(含空平台)")
    s.add_argument("--span", type=float, required=True, help="支承横向跨距 m(轮距/履带距/支腿中心距)")
    s.add_argument("--cg-arm", type=float, default=None, help="重心到倾翻侧支点距离 m, 缺省= span/2")
    s.add_argument("--load", type=float, default=0.0, help="平台额定载荷 kg")
    s.add_argument("--reach", type=float, default=0.0, help="最大幅度 m(支点至载荷重心水平距)")
    s.add_argument("--wind-speed", type=float, default=None, help="工作风速 m/s(可选)")
    s.add_argument("--area", type=float, default=None, help="受风面积 m^2(可选)")
    s.add_argument("--wind-height", type=float, default=None, help="风力作用点高度 m(可选)")
    s.add_argument("--coef", type=float, default=1.3, help="风荷载体型系数(提示值 1.3)")
    s.add_argument("--extra-moment", type=float, default=0.0, help="附加倾翻力矩 kN*m(如惯性载荷)")
    s.add_argument("--sf", type=float, default=1.5, help="要求的稳定系数(提示值 1.5, 须按标准核定)")
    s.set_defaults(func=cmd_tipping_check)

    s = sub.add_parser("wind-load", help="风载荷(基本风压与风作用力)")
    s.add_argument("--speed", type=float, required=True, help="基本风速 m/s(如 12.5)")
    s.add_argument("--area", type=float, required=True, help="受风面积 m^2")
    s.add_argument("--coef", type=float, default=1.3, help="体型系数(提示值 1.3)")
    s.add_argument("--wind-height", type=float, default=None, help="力臂高度 m(可选, 用于风载力矩)")
    s.set_defaults(func=cmd_wind_load)

    s = sub.add_parser("motor-check", help="电机功率校核(扭矩法)")
    s.add_argument("--torque", type=float, required=True, help="负载扭矩 N*m")
    s.add_argument("--speed", type=float, required=True, help="转速 rpm")
    s.add_argument("--rated", type=float, default=None, help="电机额定功率 kW(可选, 用于裕量校核)")
    s.add_argument("--efficiency", type=float, default=0.9, help="传动/电机总效率(提示值 0.9)")
    s.add_argument("--duty", type=str, default=None, help="工作制, 如 S2-30min / S3-25%(可选)")
    s.set_defaults(func=cmd_motor_check)

    s = sub.add_parser("hydraulic-check", help="油缸出力与泵系统校核")
    s.add_argument("--pressure", type=float, required=True, help="系统压力 MPa")
    s.add_argument("--bore", type=float, required=True, help="缸径 mm")
    s.add_argument("--rod", type=float, required=True, help="杆径 mm")
    s.add_argument("--flow", type=float, required=True, help="泵流量 L/min")
    s.add_argument("--efficiency", type=float, default=0.85, help="总效率(提示值 0.85)")
    s.set_defaults(func=cmd_hydraulic_check)

    s = sub.add_parser("cylinder-size", help="油缸缸径选型与压杆稳定校核")
    s.add_argument("--load", type=float, required=True, help="轴向负载 kN")
    s.add_argument("--pressure", type=float, required=True, help="工作压力 MPa")
    s.add_argument("--stroke", type=float, required=True, help="行程 mm")
    s.add_argument("--mount", choices=["fixed", "pinned", "cantilever"], default="pinned", help="安装形式(长度系数)")
    s.add_argument("--rod-ratio", type=float, default=0.6, help="杆径/缸径比, 常规 0.5-0.7")
    s.add_argument("--efficiency", type=float, default=0.9, help="机械效率(提示值 0.9)")
    s.add_argument("--n-min", type=float, default=2.5, help="稳定安全系数下限(经验 2.5-3.5, 提示值)")
    s.set_defaults(func=cmd_cylinder_size)
    return p


def main():
    parser = build_parser()
    a = parser.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
