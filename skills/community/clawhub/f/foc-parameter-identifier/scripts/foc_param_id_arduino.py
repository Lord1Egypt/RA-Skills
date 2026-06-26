#!/usr/bin/env python3
"""
FOC 电机参数辨识 - 阶跃响应实测数据处理脚本
用于从示波器导出的 CSV 数据中提取电机参数

用法：
  python foc_param_id_arduino.py --mode step_response --file voltage_current.csv
  python foc_param_id_arduino.py --mode back_emf --file emf_data.csv
  python foc_param_id_arduino.py --mode report --R 1.23 --L 5.6 --Ke 0.082 --np 4
"""

import argparse
import math
import sys
from pathlib import Path

try:
    import numpy as np
    from scipy.optimize import curve_fit
    from scipy.signal import find_peaks
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ============================================================
# 阶跃响应分析 - 电感提取
# ============================================================

def extract_inductance_step(time, current, voltage_step, R_shunt,
                            L_guess=5e-3, R_guess=1.0):
    """
    从阶跃响应提取电感 L 和电阻 R

    原理：LR 电路阶跃响应
    I(t) = V/R * (1 - exp(-t * R/L))

    参数:
        time: 时间数组 (s)
        current: 电流数组 (A) = V_sense / R_shunt
        voltage_step: 阶跃电压幅值 (V)
        R_shunt: 采样电阻 (Ω)
        L_guess, R_guess: 拟合初始猜测值
    """
    if not HAS_SCIPY:
        print("[ERROR] 需要 scipy: pip install scipy")
        return None

    current = np.array(current)
    time = np.array(time)

    # 动态确定稳态电流
    I_ss = np.mean(current[-len(current)//10:])  # 最后10%取平均
    if I_ss < 0.01:
        print("[ERROR] 电流信号太弱，请检查接线")
        return None

    # 归一化电流 (0 → 1)
    i_norm = current / I_ss

    # 指数上升模型: 1 - exp(-t/tau)
    def exp_model(t, tau):
        return 1 - np.exp(-t / tau)

    # 找到电流从0.1到0.9的时间点
    try:
        # 取指数上升段 (10%~80%)
        mask = (i_norm > 0.1) & (i_norm < 0.8)
        t_fit = time[mask] - time[mask][0]
        i_fit = i_norm[mask]

        # 拟合时间常数 tau
        popt, _ = curve_fit(exp_model, t_fit, i_fit, p0=[L_guess/R_guess])
        tau = popt[0]

        # 计算参数
        R_measured = voltage_step / I_ss
        L_measured = tau * R_measured

        # 验证：计算 R²
        i_pred = exp_model(t_fit, tau)
        ss_res = np.sum((i_fit - i_pred)**2)
        ss_tot = np.sum((i_fit - np.mean(i_fit))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"\n===== 阶跃响应分析结果 =====")
        print(f"阶跃电压: {voltage_step} V")
        print(f"采样电阻: {R_shunt} Ω")
        print(f"稳态电流: {I_ss:.4f} A")
        print(f"回路电阻: {R_measured:.4f} Ω")
        print(f"时间常数 τ: {tau*1000:.2f} ms")
        print(f"电感 L: {L_measured*1000:.2f} mH")
        print(f"拟合 R²: {r_squared:.4f}")
        print(f"⚠️  如 R² < 0.95，请检查示波器数据质量")

        return {
            'R_ohm': R_measured,
            'L_H': L_measured,
            'tau_s': tau,
            'r_squared': r_squared,
            'I_ss_A': I_ss,
        }
    except Exception as e:
        print(f"[ERROR] 拟合失败: {e}")
        print("[提示] 请确保电压阶跃已稳定，电流已充分上升")
        return None


# ============================================================
# 反电动势分析 - 磁链常数提取
# ============================================================

def extract_ke_back_emf(time, voltage, speed_rpm, pole_pairs,
                         R_phase=None, I_phase=None):
    """
    从反电动势波形提取 Ke 和 Kt

    参数:
        time: 时间数组 (s)
        voltage: 线间电压数组 (V)
        speed_rpm: 电机转速 (rpm)
        pole_pairs: 极对数
        R_phase: 相电阻 (Ω)，用于补偿 IR 压降
        I_phase: 相电流 (A)，如已知可补偿更精确
    """
    voltage = np.array(voltage)
    time = np.array(time)

    # 计算电气角速度
    omega_e = 2 * math.pi * speed_rpm * pole_pairs / 60  # rad/s
    f_elec = speed_rpm * pole_pairs / 60  # Hz

    # 找到电压峰值（反电动势幅值）
    V_peak = np.max(np.abs(voltage))
    V_rms_measured = np.sqrt(np.mean(voltage**2))

    # 正弦波峰值与有效值关系：V_peak = V_rms * sqrt(2)
    # 但线间电压需考虑整流和波形的因素
    V_phase_peak = V_peak / 2  # 近似相电压峰值（线电压/2）
    V_phase_rms = V_phase_peak / math.sqrt(2)

    # 反电动势常数（线间有效值）
    # E_line_rms = Ke * n * np / 60
    # 所以 Ke = E_line_rms * 60 / (n * np)
    # 其中 E_line_rms = V_rms（开路时电压即反电动势）

    E_line_rms = V_rms_measured
    Ke = E_line_rms * 60 / (speed_rpm * pole_pairs)  # V/(rad/s)

    # 磁链
    Psi_m = Ke / omega_e  # Wb

    # 转矩常数
    Kt = 1.5 * pole_pairs * Psi_m  # Nm/A

    # 补偿 IR 压降（如提供电阻和电流）
    if R_phase and I_phase:
        V_IR = R_phase * I_phase
        E_line_rms_comp = math.sqrt(max(V_rms_measured**2 - V_IR**2, 0))
        Ke_comp = E_line_rms_comp * 60 / (speed_rpm * pole_pairs)
        Psi_m_comp = Ke_comp / omega_e
        Kt_comp = 1.5 * pole_pairs * Psi_m_comp
        print(f"\n===== 反电动势分析结果（含IR补偿）=====")
        print(f"转速: {speed_rpm} rpm")
        print(f"极对数: {pole_pairs}")
        print(f"电气频率: {f_elec:.1f} Hz")
        print(f"线电压有效值: {V_rms_measured:.2f} V")
        print(f"IR补偿电压: {V_IR:.2f} V")
        print(f"反电动势常数 Ke: {Ke_comp:.4f} V/(rad/s)")
        print(f"磁链常数 Ψm: {Psi_m_comp:.5f} Wb")
        print(f"转矩常数 Kt: {Kt_comp:.4f} Nm/A")
        return {'Ke': Ke_comp, 'Psi_m': Psi_m_comp, 'Kt': Kt_comp,
                'V_rms': E_line_rms_comp}
    else:
        print(f"\n===== 反电动势分析结果 =====")
        print(f"转速: {speed_rpm} rpm")
        print(f"极对数: {pole_pairs}")
        print(f"电气频率: {f_elec:.1f} Hz")
        print(f"线电压有效值（≈反电动势）: {V_rms_measured:.2f} V")
        print(f"反电动势常数 Ke: {Ke:.4f} V/(rad/s)")
        print(f"磁链常数 Ψm: {Psi_m:.5f} Wb")
        print(f"转矩常数 Kt: {Kt:.4f} Nm/A")
        print(f"⚠️  如需IR补偿，请提供 --R 和 --I 参数")
        return {'Ke': Ke, 'Psi_m': Psi_m, 'Kt': Kt,
                'V_rms': V_rms_measured}


# ============================================================
# 极对数判断
# ============================================================

def identify_pole_pairs_from_hall(hall_transitions, mechanical_rotation_time):
    """
    从 Hall 传感器信号判断极对数

    参数:
        hall_transitions: Hall 状态变化次数（手动旋转一圈计数）
        mechanical_rotation_time: 旋转一圈的时间 (s)
    """
    # Hall 每极对变化2次（上升沿+下降沿）
    # 所以 np = hall_transitions / 2
    np_identified = hall_transitions / 2

    print(f"\n===== 极对数判断 =====")
    print(f"Hall 变化次数: {hall_transitions}")
    print(f"判断极对数: {np_identified:.0f}")
    return {'pole_pairs': np_identified}


# ============================================================
# 完整参数报告生成
# ============================================================

def generate_foc_config_report(R, L, Ke, np, Vdc=48, Idc=10,
                                n_rated=3000, T_rated=0.64):
    """生成 FOC 控制器配置参数报告"""

    # 温度修正（铜温漂 +0.4%/℃）
    T_work = 75  # 工作温度 ℃
    R_75 = R * (1 + 0.004 * (T_work - 20))

    # 派生参数
    omega_e = 2 * math.pi * n_rated * np / 60
    Psi_m = Ke / omega_e if Ke else 0
    Kt = 1.5 * np * Psi_m

    # 电流环带宽
    bw_current = R / (L * 1e-3) / (2 * math.pi)  # Hz

    # 速度环带宽
    bw_speed = bw_current / 10  # Hz

    # 电气时间常数
    tau_e = L / R * 1000  # ms

    # 电压裕量
    V_phase_peak = Vdc / math.sqrt(2)
    V_line_rms = V_phase_peak * math.sqrt(2) / math.sqrt(3)
    E_line = Ke * n_rated * np / 60
    v_margin = V_line_rms - E_line

    report = f"""
================================================================
                 FOC 电机参数完整报告
================================================================

【基本参数】
  极对数 np              = {np}
  额定电压 Vdc           = {Vdc} V
  额定电流 Idc          = {Idc} A
  额定转速 nr           = {n_rated} rpm
  额定转矩 T_rated      = {T_rated:.3f} Nm

【测量参数 @ 20℃】
  相电阻 R_20℃         = {R:.4f} Ω
  相电感 L              = {L:.2f} mH
  反电动势常数 Ke       = {Ke:.4f} V/(rad/s)
  磁链常数 Ψm           = {Psi_m:.5f} Wb
  转矩常数 Kt           = {Kt:.4f} Nm/A

【温度修正 @ {T_work}℃】
  相电阻 R_{T_work}℃    = {R_75:.4f} Ω（增大 {((R_75/R)-1)*100:.1f}%）

【控制器建议参数】
  电流环带宽            ≈ {bw_current:.1f} Hz
  速度环带宽            ≈ {bw_speed:.1f} Hz
  电气时间常数 τe       = {tau_e:.2f} ms

【电压裕量评估 @ {n_rated}rpm】
  额定相电压峰值        ≈ {V_phase_peak:.1f} V
  额定反电动势          ≈ {E_line:.1f} V
  电压裕量              ≈ {v_margin:.1f} V
  {'✅ 裕量充足' if v_margin > 20 else '⚠️ 电压裕量偏小，建议提高Vdc或降低转速'}

================================================================
              STM32 FOC 参数配置代码
================================================================

// motor_params.h
#define POLE_PAIR_NUM    {np}
#define RS               {R:.4f}f    // Ω @ 20℃
#define RS_75            {R_75:.4f}f  // Ω @ 75℃
#define LD               {L:.2f}e-3f  // H
#define LQ               {L:.2f}e-3f  // H（表贴式电机 Ld=Lq）
#define KE               {Ke:.4f}f    // V/(rad/s)
#define KT               {Kt:.4f}f    // Nm/A
#define FLUX_LINKAGE     {Psi_m:.5f}f // Wb

// 电流环 PI 参数（典型值，建议根据带宽调整）
#define CURRENT_KP       {R:.4f}f     // Kp ≈ R
#define CURRENT_KI       {R/L:.2f}f   // Ki ≈ R/L（需×Ts积分）

// 速度环 PI 参数
#define SPEED_KP         {bw_speed:.1f}f
#define SPEED_KI         {bw_speed/10:.1f}f

================================================================
              Arduino (SimpleFOC) 参数配置
================================================================

// simplefoc_config.ino
motor.controller = MotionControlType::torque;

motor.pole_pairs = {np};
motor.phase_resistance = {R};  // Ω
motor KV = {1/Ke:.2f};        // KV值（rpm/V）

// 电流限幅
motor.current_limit = {Idc};  // A

// 速度环
motor.velocity_limit = {n_rated};  // rpm

// PI 参数（自动整定后的初始值）
motor.PID_velocity.P = {bw_speed * 0.5:.2f};
motor.PID_velocity.I = {bw_speed * 0.1:.2f};

================================================================
"""
    return report


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='FOC 参数辨识工具')
    parser.add_argument('--mode', required=True,
                        choices=['step_response', 'back_emf', 'hall_method',
                                 'report', 'all'])
    # 阶跃响应参数
    parser.add_argument('--file', help='CSV 数据文件路径')
    parser.add_argument('--V', type=float, help='阶跃电压幅值 (V)')
    parser.add_argument('--R_shunt', type=float, default=0.1,
                        help='采样电阻 (Ω)')
    # 反电动势参数
    parser.add_argument('--speed', type=float, help='转速 (rpm)')
    parser.add_argument('--np', type=int, help='极对数')
    parser.add_argument('--R', type=float, help='相电阻 (Ω)，用于IR补偿')
    parser.add_argument('--I', type=float, help='相电流 (A)，用于IR补偿')
    # 通用参数
    parser.add_argument('--Vdc', type=float, default=48, help='母线电压 (V)')
    parser.add_argument('--Idc', type=float, default=10, help='额定电流 (A)')
    parser.add_argument('--n_rated', type=float, default=3000, help='额定转速 (rpm)')

    args = parser.parse_args()

    if args.mode == 'step_response':
        if not args.file:
            # 演示阶跃响应数据
            print("[INFO] 无数据文件，使用演示数据")
            np.random.seed(42)
            t = np.linspace(0, 0.05, 500)
            V = 12.0
            R = 1.0
            L = 5.6e-3
            tau = L / R
            I_ss = V / R
            current = I_ss * (1 - np.exp(-t / tau)) + 0.01 * np.random.randn(500)
            extract_inductance_step(t, current, V, args.R_shunt)
        else:
            print(f"[INFO] 从 {args.file} 读取数据（请实现 CSV 解析）")
            print("[提示] 期望格式: time(s), voltage_sense(V)")

    elif args.mode == 'back_emf':
        np = args.np or 4
        speed = args.speed or 3000
        if not args.file:
            # 演示反电动势数据
            print("[INFO] 无数据文件，使用演示数据")
            np.random.seed(42)
            f = speed * np / 60
            t = np.linspace(0, 0.1, 1000)
            voltage = 48 * np.sin(2 * np.pi * f * t) + 2 * np.random.randn(1000)
            extract_ke_back_emf(t, voltage, speed, np,
                                R_phase=args.R, I_phase=args.I)
        else:
            print(f"[INFO] 从 {args.file} 读取数据（请实现 CSV 解析）")

    elif args.mode == 'hall_method':
        print("请手动旋转电机一圈，记录 Hall 信号变化次数")
        print("极对数 = Hall变化次数 / 2")

    elif args.mode == 'report':
        R = args.R or 1.23
        L = args.L if hasattr(args, 'L') else 5.6
        Ke = args.Ke if hasattr(args, 'Ke') else 0.082
        np = args.np or 4
        print(generate_foc_config_report(R, L, Ke, np,
                                        Vdc=args.Vdc, Idc=args.Idc,
                                        n_rated=args.n_rated))

    elif args.mode == 'all':
        print("===== 完整参数辨识演示 =====")
        # 模拟完整辨识流程
        R_measured = 1.23
        L_measured = 5.6
        Ke_measured = 0.082
        np_measured = 4

        np.random.seed(42)
        f = 3000 * np_measured / 60
        t = np.linspace(0, 0.1, 1000)
        voltage = 48 * np.sin(2 * np.pi * f * t)

        print("\n[1/3] 电阻测量（万用表法）")
        print(f"  R_phase = {R_measured} Ω")

        print("\n[2/3] 电感测量（阶跃响应法）")
        extract_inductance_step(t,
                                5.6 * (1 - np.exp(-t / (5.6e-3/1.23))),
                                12, 0.1)

        print("\n[3/3] 反电动势法测 Ke")
        extract_ke_back_emf(t, voltage, 3000, np_measured)

        print(generate_foc_config_report(R_measured, L_measured, Ke_measured,
                                        np_measured, Vdc=args.Vdc, Idc=args.Idc,
                                        n_rated=args.n_rated))


if __name__ == '__main__':
    main()
