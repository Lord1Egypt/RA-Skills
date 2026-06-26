#!/usr/bin/env python3
"""
febe_solver.py
===============
分数阶能量平衡方程（FEBE）求解器。

方程:  _0^C D_t^h DT(t) = -DT(t)/tau + F(t)/C
解（瞬态）:  DT(t) = DT_eq * [1 - E_{h,1}(-(t/tau)^h)]

其中 DT_eq = lambda_eq * F，lambda_eq 通过 IPCC ECS 校准。

用法:
  python3 febe_solver.py [h [tau_yr [F_Wm2 [t_end_yr]]]]
"""

import numpy as np
import json, sys, math

# ── IPCC ECS 校准 ──
# ECS_1xCO2 ≈ 3°C, F_1xCO2 = 5.35*ln(560/278) ≈ 3.78 W/m²
# lambda_eq = ECS/F = 3.0/3.78 = 0.794 K/(W/m²)
LAMBDA_EQ = 3.0 / 5.35 / math.log(560.0/278.0)  # ≈ 0.794

def mittag_leffler(alpha, beta, z, n_terms=200):
    """E_{α,β}(z) = Σ z^k / Γ(αk + β)"""
    z = np.asarray(z, dtype=np.float64)
    result = np.zeros_like(z)
    for k in range(n_terms):
        gamma_arg = alpha * k + beta
        if gamma_arg > 200: break
        term = np.power(z, k) / math.gamma(gamma_arg)
        result += term
        if np.all(np.abs(term) < 1e-15 * np.abs(result)): break
    return result if result.shape else float(result)

def E_h_1(alpha, z, n_terms=200):
    return mittag_leffler(alpha, 1.0, z, n_terms)

def febe_solution(h, tau_yr, F_orb, t_yr):
    """
    FEBE 瞬态求解。

    DT(t) = lambda_eq * F * [1 - E_{h,1}(-(t/τ)^h)]

    t → ∞ 时 DT → λ_eq * F（平衡值）
    """
    if np.isscalar(F_orb):
        F_arr = np.full_like(t_yr, F_orb)
    else:
        F_arr = np.asarray(F_orb)

    z = -np.power(np.abs(t_yr) / tau_yr, h)
    ml_term = E_h_1(h, z)

    return LAMBDA_EQ * F_arr * (1.0 - ml_term)

def sensitivity_factor(h, tau_yr, F_orb, t_target):
    delta_T = febe_solution(h, tau_yr, F_orb, np.array([t_target]))
    return float(delta_T[0] / F_orb) if F_orb != 0 else 0.0

def multi_layer_response(F_orb, t_yr):
    """多圈层耦合的温度响应"""
    LAYERS = [
        ('atmosphere',  0.40, 3e2,   0.15),
        ('thermocline', 0.60, 1e4,   0.20),
        ('deep_ocean',  0.75, 5e4,   0.35),
        ('ice_sheet',   0.85, 1e5,   0.30),
    ]
    results = {}
    total = np.zeros_like(t_yr)
    for name, h, tau, w in LAYERS:
        dT = febe_solution(h, tau, F_orb, t_yr) * w
        results[name] = dT
        total += dT
    results['total'] = total
    return results

if __name__ == '__main__':
    h, tau, F0, t_end = 0.6, 3e4, 30.0, 1e5
    if len(sys.argv) >= 2: h     = float(sys.argv[1])
    if len(sys.argv) >= 3: tau    = float(sys.argv[2])
    if len(sys.argv) >= 4: F0     = float(sys.argv[3])
    if len(sys.argv) >= 5: t_end  = float(sys.argv[4])

    t_yr  = np.linspace(0, t_end, 1001)
    dT    = febe_solution(h, tau, F0, t_yr)
    dT_amp = dT * 2.5  # 含反馈

    key_times = [1000, 5000, 10000, 23000, 41000, 100000]
    key_idx   = [np.argmin(np.abs(t_yr - tt)) for tt in key_times]

    print("="*62)
    print("地动仪模型 · FEBE方程求解结果（IPCC ECS校准）")
    print("="*62)
    print(f"参数: h={h}, τ₀={tau:.0e} yr, F={F0} W/m²")
    print(f"ECS校准: λ_eq = {LAMBDA_EQ:.4f} K/(W/m²)")
    print(f"DT_eq (基础) = {LAMBDA_EQ*F0:.2f} K")
    print(f"DT_eq (含反馈×2.5) = {LAMBDA_EQ*F0*2.5:.2f} K")
    print()
    print(f"{'时间(yr)':>12} | {'ΔT基础(K)':>12} | {'ΔT放大(K)':>12} | {'说明'}")
    print("-"*62)
    labels = {1000:'千年', 5000:'5千年', 10000:'1万年', 23000:'2.3万年', 41000:'4.1万年', 100000:'10万年'}
    for tt, idx in zip(key_times, key_idx):
        lbl = labels.get(tt, '')
        print(f"{tt:>12,.0f} | {dT[idx]:>12.3f} | {dT_amp[idx]:>12.3f} | {lbl}")

    ECS = sensitivity_factor(h, tau, F0, 100000)
    print(f"\n平衡气候敏感度（@100kyr）: {ECS:.4f} K/(W/m²) * {F0} W/m² = {ECS*F0:.2f} K")
    print(f"含反馈平衡敏感度          : {ECS*F0*2.5:.2f} K")

    out = {
        't_yr': t_yr.tolist(), 'dT_base': dT.tolist(), 'dT_amped': dT_amp.tolist(),
        'params': {'h': h, 'tau_yr': tau, 'F_Wm2': F0, 'lambda_eq': LAMBDA_EQ, 'lambda_sys': 2.5},
        'key_points': {str(tt): float(dT[idx]) for tt, idx in zip(key_times, key_idx)},
        'ECS_amped': float(ECS*F0*2.5)
    }
    with open('/tmp/febe_results.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n数据已存: /tmp/febe_results.json")
