#!/usr/bin/env python3
"""
FOC 电机参数辨识流程脚本
用于记录和管理电机参数辨识结果

用法：
  python parameter_id_flow.py --mode interactive
  python parameter_id_flow.py --mode report --R 1.23 --L 5.6 --Ke 0.082 --np 4
"""

import argparse
import math


def calculate_from_measured(R_phase, L_phase, Ke_line, np, Vdc=48, Idc=10, n_rated=3000):
    """根据测量参数计算 FOC 控制器所需参数"""

    # 1. 转矩常数
    Kt = Ke_line / (2 * math.pi * np / 60)  # Ke_rpm → Kt_NmA
    # 或直接：Kt = 1.5 * np * Ψm（需反算 Ψm）

    # Ψm 反算（线间有效值 Ke → 磁链）
    # E_line_rms = Ke_line × n × np / (60 × √2) × 2π/√3
    # 简化：
    omega_e = 2 * math.pi * n_rated * np / 60  # rad/s
    Psi_m = Ke_line / (omega_e / math.sqrt(3))  # Wb（粗略）
    Kt_exact = 1.5 * np * Psi_m  # Nm/A

    # 2. 电流环带宽（建议值）
    bw_current = R_phase / L_phase * 1e-3  # rad/s → kHz
    bw_current_Hz = bw_current / (2 * math.pi)  # Hz

    # 3. 速度环带宽（建议值）
    bw_speed = bw_current_Hz / 10  # Hz

    # 4. 电气时间常数
    tau_e = L_phase / R_phase * 1000  # ms

    # 5. 机械时间常数（需 J）
    # tau_m = J / B（需输入转动惯量）

    # 6. 额定转速对应电压估算
    V_phase_rms = Vdc / math.sqrt(2)  # SVPWM 最大相电压幅值
    V_line_rms = V_phase_rms * math.sqrt(3)
    E_line_rms_at_n = Ke_line * n_rated * np / 60
    voltage_headroom = V_line_rms - E_line_rms_at_n

    # 7. 铜损估算
    I_rms = Idc * 0.707  # 假设方波驱动
    P_cu = 3 * (I_rms ** 2) * R_phase  # W

    result = {
        'R_phase_Ohm': R_phase,
        'L_phase_mH': L_phase,
        'Ke_line_V_rms': Ke_line,
        'np': np,
        'tau_e_ms': round(tau_e, 2),
        'bw_current_Hz': round(bw_current_Hz, 1),
        'bw_speed_Hz': round(bw_speed, 1),
        'Psi_m_Wb': round(Psi_m, 5),
        'Kt_Nm_A': round(Kt_exact, 4),
        'V_line_rms_V': round(V_line_rms, 1),
        'E_line_rms_at_rated_V': round(E_line_rms_at_n, 1),
        'voltage_headroom_V': round(voltage_headroom, 1),
        'P_cu_W': round(P_cu, 2),
    }

    return result


def format_report(params):
    """生成参数报告"""
    p = params
    return f"""
==========================================
       FOC 电机参数辨识报告
==========================================

【电机基本参数】
  极对数 np         = {p['np']}
  额定电压 Vdc      = {p.get('Vdc', 48)} V
  额定电流 Idc      = {p.get('Idc', 10)} A
  额定转速 nr       = {p.get('n_rated', 3000)} rpm

【测量参数】
  相电阻 R          = {p['R_phase_Ohm']} Ω
  相电感 L          = {p['L_phase_mH']} mH
  反电动势常数 Ke   = {p['Ke_line_V_rms']} V（线间有效值 @ 60Hz基准）

【派生参数】
  磁链常数 Ψm      = {p['Psi_m_Wb']} Wb
  转矩常数 Kt       = {p['Kt_Nm_A']} Nm/A
  电气时间常数 τe   = {p['tau_e_ms']} ms

【控制器建议参数】
  电流环带宽        ≈ {p['bw_current_Hz']} Hz
  速度环带宽        ≈ {p['bw_speed_Hz']} Hz
  （注：带宽需根据负载惯量调整）

【电气评估】
  额定相电压峰值    = {p['V_line_rms_V']} V
  额定反电动势      = {p['E_line_rms_at_rated_V']} V
  电压裕量          = {p['voltage_headroom_V']} V
  铜损估算          = {p['P_cu_W']} W

【FOC控制器配置建议】
  // 电机参数定义
  #define POLE_PAIR_NUM    {p['np']}
  #define RS               {p['R_phase_Ohm']}f    // Ω
  #define LD               {p['L_phase_mH']}e-3f  // H
  #define LQ               {p['L_phase_mH']}e-3f  // H
  #define KE               {p['Ke_line_V_rms']}f  // V/Hz
  #define KT               {p['Kt_Nm_A']}f       // Nm/A

==========================================
"""


def main():
    parser = argparse.ArgumentParser(description='FOC 参数辨识计算工具')
    parser.add_argument('--mode', default='interactive', choices=['interactive', 'report'])
    parser.add_argument('--R', type=float, help='相电阻 (Ω)')
    parser.add_argument('--L', type=float, help='相电感 (mH)')
    parser.add_argument('--Ke', type=float, help='线间反电动势常数 (Vrms)')
    parser.add_argument('--np', type=int, help='极对数')
    parser.add_argument('--Vdc', type=float, default=48, help='母线电压 (V)')
    parser.add_argument('--Idc', type=float, default=10, help='额定电流 (A)')
    parser.add_argument('--n_rated', type=float, default=3000, help='额定转速 (rpm)')

    args = parser.parse_args()

    if args.mode == 'interactive':
        print("=== FOC 参数辨识计算器 ===")
        print("（使用 --R --L --Ke --np 参数直接输出报告）")
        print()
        # 演示数据
        demo = calculate_from_measured(
            R_phase=1.23, L_phase=5.6, Ke_line=0.082, np=4,
            Vdc=args.Vdc, Idc=args.Idc, n_rated=args.n_rated
        )
        print("演示参数（请用命令行参数替换）：")
        print(format_report(demo))
    else:
        if not all([args.R, args.L, args.Ke, args.np]):
            print("错误：请提供完整参数 --R --L --Ke --np")
            return
        result = calculate_from_measured(
            R_phase=args.R, L_phase=args.L, Ke_line=args.Ke, np=args.np,
            Vdc=args.Vdc, Idc=args.Idc, n_rated=args.n_rated
        )
        print(format_report(result))


if __name__ == "__main__":
    main()
