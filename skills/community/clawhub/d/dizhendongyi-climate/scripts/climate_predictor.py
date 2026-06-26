#!/usr/bin/env python3
"""
climate_predictor.py
=====================
地动仪气候模型 · 综合预测主程序 v3.0

整合轨道强迫计算 + FEBE求解 + 反馈放大 + CO₂情景叠加

用法:
  python3 climate_predictor.py <模式> [参数]

模式:
  long     长期预测（轨道尺度，默认未来10万年）
  near     近期推演（叠加RCP情景，至2100年）
  extreme  极端事件预警评估
  compare  冰期/间冰期对比（-130ka vs 当前 vs +95ka）
"""

import numpy as np
import sys, math

# ══════════════════════════════════════════════════════
# 核心物理参数
# ══════════════════════════════════════════════════════
LAMBDA_EQ = 3.0 / 5.35 / math.log(560.0/278.0)  # 0.794 K/(W/m²) — IPCC ECS校准
LAMBDA_SYS = 2.5                                 # 四大反馈综合放大

# ══════════════════════════════════════════════════════
# 轨道参数（La2004，相位校准至2000CE）
# Q65_0=312.3, A_PSI=15, A_EPS=3.5, Q65范围≈289–335
# ══════════════════════════════════════════════════════
E0 = 0.0167; EPS0 = 23.44; Q65_0 = 312.3
A_PSI = 15.0; A_EPS = 3.5

def orbital_e(t):
    return E0 + 0.019*np.cos(2*np.pi*(t - 14000)/95500) + 0.011*np.cos(2*np.pi*(t - 14000)/123800)

def orbital_eps(t):
    return EPS0 + 1.20*np.cos(2*np.pi*(t - 5125)/41000)

def orbital_psi(t):
    return np.sin(2*np.pi*t/23000) + 0.3*np.sin(2*np.pi*t/19000)

def orbital_Q65(t):
    return Q65_0 + A_PSI * orbital_psi(t) + A_EPS * (orbital_eps(t) - EPS0)

# ══════════════════════════════════════════════════════
# 冰期/间冰期阈值
# ══════════════════════════════════════════════════════
ICE_THRESHOLD    = Q65_0 - 10   # 292.3 → 冰期风险
INTERTGLACIAL    = Q65_0 + 3    # 315.3 → 强间冰期

# ══════════════════════════════════════════════════════
# FEBE 求解（IPCC ECS 校准）
# ══════════════════════════════════════════════════════
def ml_e1(alpha, z, n=200):
    r = np.asarray(z, dtype=np.float64)
    res = np.zeros_like(r)
    for k in range(n):
        g = alpha * k + 1.0
        if g > 200: break
        term = np.power(r, k) / math.gamma(g)
        res += term
        if np.all(np.abs(term) < 1e-14 * np.abs(res + 1e-30)): break
    return res

def febe(h, tau_yr, F, t_yr):
    """DT(t) = λ_eq * F * [1 - E_{h,1}(-(t/τ)^h)]"""
    t = np.atleast_1d(np.array(t_yr, dtype=np.float64))
    z = -np.power(np.abs(t) / tau_yr, h)
    return LAMBDA_EQ * F * (1.0 - ml_e1(h, z, n=200))

def multi_layer_response(F_orb, t_yr):
    LAYERS = [('atmosphere',  0.40, 3e2), ('thermocline', 0.60, 1e4),
              ('deep_ocean',  0.75, 5e4), ('ice_sheet',   0.85, 1e5)]
    W = [0.15, 0.20, 0.35, 0.30]
    total = np.zeros(len(t_yr), dtype=np.float64)
    for (n, h, tau), w in zip(LAYERS, W):
        total += febe(h, tau, F_orb, t_yr) * w
    return total

# ══════════════════════════════════════════════════════
# 区域→全球有效强迫转换
# Q65 是 65°N 区域强迫，需乘以转换系数得全球等效
# ══════════════════════════════════════════════════════
# 经验：Q65 变化 1 W/m² → F_global ≈ 0.1–0.15 W/m²（含全球分配+冰盖非线性）
F_SCALE = 0.12

def Q65_to_Fglobal(q65_arr):
    """Q65 → 全球有效辐射强迫（含冰盖非线性反馈）"""
    dQ = q65_arr - Q65_0
    # 冰盖阈值：Q65 低于阈值时，冰盖增长，反照率增强 → F_global 更负
    ice_factor = 1.0 + 0.5 * np.exp(-((dQ + 15) / 8) ** 2)
    return dQ * F_SCALE * ice_factor

# ══════════════════════════════════════════════════════
# 预测核心
# ══════════════════════════════════════════════════════
def predict_long_term(n_future=100000):
    """长期气候预测（自然轨道强迫）"""
    t = np.arange(0, n_future + 1000, 1000, dtype=np.float64)
    q65 = orbital_Q65(t)
    Fg  = Q65_to_Fglobal(q65)

    dT_base = febe(0.6, 3e4, Fg, t)
    dT_sys  = dT_base * LAMBDA_SYS

    results = []
    for ti, qi, fg, db, ds in zip(t, q65, Fg, dT_base, dT_sys):
        if qi < ICE_THRESHOLD:
            status = '冰期风险'
        elif qi > INTERTGLACIAL:
            status = '强间冰期'
        else:
            status = '间冰期'
        results.append({
            'time_yr':      float(ti),
            'Q65_Wm2':      round(float(qi), 1),
            'F_global_Wm2': round(float(fg), 4),
            'dT_K':         round(float(db), 4),
            'dT_amped_K':   round(float(ds), 4),
            'status':       status
        })
    return results

def predict_near_term(scenario='rcp45', t_start=2025, t_end=2100):
    """近期气候推演（叠加RCP情景）"""
    SCENARIOS = {
        'rcp26': {2020:415, 2030:416, 2050:422, 2100:430},
        'rcp45': {2020:415, 2030:420, 2050:442, 2100:500},
        'rcp60': {2020:418, 2030:424, 2050:450, 2100:600},
        'rcp85': {2020:425, 2030:432, 2050:492, 2100:800},
    }
    sd = SCENARIOS.get(scenario.lower(), SCENARIOS['rcp45'])
    years = sorted(sd.keys())
    co2_vals = [sd[y] for y in years]
    t_range = np.arange(t_start, t_end + 1, dtype=np.float64)
    co2_interp = np.interp(t_range, np.array(years, dtype=float), np.array(co2_vals, dtype=float))

    t_past = t_range - t_start
    F_nat = orbital_Q65(t_past) - Q65_0

    results = []
    for ti, co2i in zip(t_range, co2_interp):
        F_co2 = 5.35 * math.log(co2i / 278.0)
        F_tot = float(F_nat[np.argmin(np.abs(t_past - (ti - t_start)))] + F_co2)
        layers = multi_layer_response(F_co2, np.array([1000.0]))
        dT = layers[0] * LAMBDA_SYS
        results.append({
            'year': int(ti), 'co2_ppm': round(float(co2i), 1),
            'F_CO2_Wm2': round(F_co2, 3), 'F_total': round(F_tot, 3),
            'dT_K': round(float(dT), 2)
        })
    return results

def assess_extreme(event_type, current_value, anomaly_percent):
    """极端事件预警评估"""
    CASES = {
        'AMOC': {'name':'AMOC减弱类事件（8.2ka冷事件型）','anomaly_trigger':-20,
            'history':'8,200年前，AMOC减弱约30%，北半球降温2–4°C，持续150–200年',
            'duration':'150–200年','precursor':'北大西洋淡水通量↑ + AMOC强度偏差>20%',
            'level':'orange' if anomaly_percent < -20 else 'green'},
        'ICE': {'name':'冰盖快速消退（Heinrich事件型）','anomaly_trigger':-15,
            'history':'末次冰期内6次，格陵兰降温2–5°C，北大西洋冰筏碎屑增加',
            'duration':'500–2,000年','precursor':'北大西洋IRD通量↑ + 冰盖物质平衡快速亏损',
            'level':'red' if anomaly_percent < -30 else 'orange' if anomaly_percent < -15 else 'green'},
        'FORCING': {'name':'辐射强迫极端偏移（Green Sahara逆转型）','anomaly_trigger':-8,
            'history':'约5,000年前绿色撒哈拉结束，北非降水骤减',
            'duration':'1,000–3,000年','precursor':'夏季辐射强迫（65°N）变化 > 8 W/m²',
            'level':'yellow' if abs(anomaly_percent) > 8 else 'green'},
    }
    c = CASES.get(event_type, CASES['FORCING'])
    return {
        'event_type': event_type, 'current_value': current_value,
        'anomaly_pct': anomaly_percent, 'case_name': c['name'],
        'history': c['history'], 'duration': c['duration'],
        'precursor': c['precursor'], 'warning_level': c['level'],
        'recommendation': f'持续监测{event_type}强度，关注{c["duration"]}尺度响应'
    }

def compare_glacial_interglacial():
    """三个典型时期对比"""
    periods = [('130ka前（末次间冰期,Eemian）', -130000),
               ('当前（全新世,2000CE）', 0),
               ('95ka后（下个冰期预测）', 95000)]
    results = []
    for label, tv in periods:
        e = float(orbital_e(np.array([tv]))[0])
        q = float(orbital_Q65(np.array([tv]))[0])
        Fg = float(Q65_to_Fglobal(np.array([q]))[0])
        layers = multi_layer_response(Fg, np.array([100000.0]))
        dT = layers[0] * LAMBDA_SYS
        if q < ICE_THRESHOLD: status = '冰期'
        elif q > INTERTGLACIAL: status = '强间冰期'
        else: status = '间冰期'
        results.append({'period': label, 'eccentricity': round(e, 4),
            'Q65_Wm2': round(q, 1), 'F_global_Wm2': round(Fg, 4),
            'dT_amped_K': round(dT, 2), 'status': status})
    return results

# ══════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 climate_predictor.py <mode> [args...]")
        print("模式: long | near | extreme | compare")
        sys.exit(1)

    mode = sys.argv[1].lower()
    print("="*75)
    print("地动仪气候模型 · 综合预测系统 v3.0")
    print("="*75)

    if mode == 'long':
        results = predict_long_term()
        print(f"\n{'距今年(yr)':>12} | {'Q65(W/m²)':>11} | {'F_global(W/m²)':>16} | {'ΔT(K)':>8} | {'ΔT_amped(K)':>13} | {'状态':^14}")
        print("-"*90)
        for r in results:
            t = r['time_yr']
            if t % 10000 == 0 or t % 5000 == 0 or t == 0:
                print(f"{t:>12,.0f} | {r['Q65_Wm2']:>11.1f} | {r['F_global_Wm2']:>16.4f} | "
                      f"{r['dT_K']:>8.4f} | {r['dT_amped_K']:>13.4f} | {r['status']:^14}")
        ice_pts = [r for r in results if r['status'] == '冰期风险']
        if ice_pts:
            next_ice = ice_pts[0]
            print(f"\n🧊 预测下一个冰期风险起始于：约 {int(next_ice['time_yr']):,} 年后")

    elif mode == 'near':
        scn = sys.argv[2] if len(sys.argv) > 2 else 'rcp45'
        t0 = int(sys.argv[3]) if len(sys.argv) > 3 else 2025
        t1 = int(sys.argv[4]) if len(sys.argv) > 4 else 2100
        results = predict_near_term(scn, t0, t1)
        print(f"\n近期气候推演 · {scn.upper()} 情景 ({t0}–{t1})")
        print(f"\n{'年份':>6} | {'CO₂(ppm)':>10} | {'ΔQ_CO₂(W/m²)':>14} | {'F_total(W/m²)':>15} | {'ΔT(K)':>10}")
        print("-"*65)
        for r in results:
            if r['year'] % 10 == 0:
                print(f"{r['year']:>6} | {r['co2_ppm']:>10.1f} | {r['F_CO2_Wm2']:>14.3f} | "
                      f"{r['F_total']:>15.3f} | {r['dT_K']:>10.2f}")
        print("\n⚠️ 注：近期人为强迫主导（自然轨道强迫 < 0.5 W/m²）")

    elif mode == 'extreme':
        evt = sys.argv[2] if len(sys.argv) > 2 else 'AMOC'
        val = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
        pct = float(sys.argv[4]) if len(sys.argv) > 4 else -10.0
        res = assess_extreme(evt, val, pct)
        emoji = {'green':'🟢','yellow':'🟡','orange':'🟠','red':'🔴'}.get(res['warning_level'], '⚪')
        print(f"\n极端事件预警评估 {emoji}")
        print(f"事件: {res['event_type']} — {res['case_name']}")
        print(f"当前值: {res['current_value']} | 偏离: {res['anomaly_pct']}%")
        print(f"预警等级: {res['warning_level'].upper()} {emoji}")
        print(f"历史类比: {res['history']}")
        print(f"参考持续时间: {res['duration']}")
        print(f"前兆指标: {res['precursor']}")
        print(f"建议: {res['recommendation']}")

    elif mode == 'compare':
        results = compare_glacial_interglacial()
        print(f"\n冰期-间冰期典型时期对比")
        print(f"\n{'时期':^30} | {'e':>6} | {'Q65(W/m²)':>10} | {'F_global(W/m²)':>16} | {'ΔT(K)':>7} | {'状态':^8}")
        print("-"*90)
        for r in results:
            print(f"{r['period']:^30} | {r['eccentricity']:>6.4f} | "
                  f"{r['Q65_Wm2']:>10.1f} | {r['F_global_Wm2']:>16.4f} | "
                  f"{r['dT_amped_K']:>7.2f} | {r['status']:^8}")

    else:
        print(f"未知模式: {mode}")
        sys.exit(1)
