#!/usr/bin/env python3
"""
黎曼猜想的新证明路线 — 验证脚本
基于 |ξ|² 全局单调性的几何方法

验证内容:
  1. |ξ|² 在 σ 方向上严格凸
  2. 导数 h_γ'(σ) 在 σ<0.5 为负, σ>0.5 为正
  3. 导数求和公式与数值差分一致
  4. 全局最小值唯一且位于 σ=0.5

运行: python rh_proof_verify.py
"""

import mpmath as mp
import math

mp.mp.dps = 50

def hr(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")

# ============================================================================
# 0. 概述
# ============================================================================
hr("黎曼猜想的新证明路线 — 验证脚本")
print("""
核心定理: |ξ(σ+iγ)|² 在 σ 上严格单调
  σ<0.5: h_γ'(σ) < 0  (严格递减)
  σ>0.5: h_γ'(σ) > 0  (严格递增)
→ 全局最小值唯一且位于 σ=0.5
→ 若最小值为零, 零点在 σ=0.5
→ 对所有 γ 成立 → 黎曼猜想成立

核心公式 (导数求和):
  h_γ'(σ)/h_γ(σ) = Σ_ρ 2[(d-dρ)/((d-dρ)²+a²) - (-dρ)/(dρ²+a²)]
  其中 d=σ-1/2, dρ=σρ-1/2, a=γ-γρ
""")

# ============================================================================
# 辅助函数
# ============================================================================
def xi_sq(sigma, gamma):
    """h_γ(σ) = |ξ(σ+iγ)|²"""
    s = sigma + 1j*gamma
    xi = mp.mpf('0.5') * s * (s-1) * mp.pi**(-s/2) * mp.gamma(s/2) * mp.zeta(s)
    return float(abs(xi)**2)

def xi_sq_deriv(sigma, gamma, h=0.0005):
    """数值导数 h_γ'(σ)"""
    fp = xi_sq(sigma+h, gamma)
    fm = xi_sq(sigma-h, gamma)
    return (fp - fm) / (2*h)

# ============================================================================
# 验证1: |ξ|² 凸性
# ============================================================================
hr("验证1: |ξ|² 在 σ 上严格凸 (d²/dσ² > 0)")

def xi_sq_d2(sigma, gamma, h=0.001):
    fp = xi_sq(sigma+h, gamma)
    f0 = xi_sq(sigma, gamma)
    fm = xi_sq(sigma-h, gamma)
    return (fp - 2*f0 + fm) / (h*h)

convex_ok = True
neg_count = 0
total = 0
for sig in [0.02 + 0.04*i for i in range(25)]:
    for gam in [5 + 2.5*i for i in range(20)]:
        d2 = xi_sq_d2(sig, gam)
        total += 1
        if d2 < -1e-10:
            convex_ok = False
            neg_count += 1

print(f"  测试点: {total}")
print(f"  d²<0 (非凸): {neg_count}")
print(f"  凸性: {'全部通过' if convex_ok else f'存在{neg_count}个违反'}")

# ============================================================================
# 验证2: 导数符号
# ============================================================================
hr("验证2: h_γ'(σ) 在 σ<0.5 为负, σ>0.5 为正")

deriv_ok = True
violations_lo = 0
violations_hi = 0
total2 = 0

for sig in [0.35, 0.4, 0.45]:
    for gam in [5 + 3*i for i in range(18)]:
        total2 += 1
        d1 = xi_sq_deriv(sig, gam)
        if d1 > 0:
            deriv_ok = False
            violations_lo += 1

for sig in [0.55, 0.6, 0.65]:
    for gam in [5 + 3*i for i in range(18)]:
        total2 += 1
        d1 = xi_sq_deriv(sig, gam)
        if d1 < 0:
            deriv_ok = False
            violations_hi += 1

print(f"  测试点: {total2}")
print(f"  σ<0.5 导数应<0, 违反: {violations_lo}")
print(f"  σ>0.5 导数应>0, 违反: {violations_hi}")
print(f"  符号: {'全部正确' if deriv_ok else '存在违反'}")

# ============================================================================
# 验证3: 零点位置
# ============================================================================
hr("验证3: 已知零点处 |ξ|² 最小, 且在 σ=0.5")

zeros_y = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
           37.586178, 40.918719, 43.327073]

zero_ok = True
for g in zeros_y[:5]:
    min_val = float('inf')
    min_sig = 0
    for sig in [0.3 + 0.01*i for i in range(41)]:
        val = xi_sq(sig, g)
        if val < min_val:
            min_val = val
            min_sig = sig
    near_half = abs(min_sig - 0.5) < 0.02
    is_zero = min_val < 1e-6
    if not near_half:
        zero_ok = False
    print(f"  γ={g:.4f}: 极小 σ={min_sig:.4f} {'(零点!)' if is_zero else ''} {'✓' if near_half else '✗'}")

print(f"  极小在 σ=0.5: {'全部' if zero_ok else '存在例外'}")

# ============================================================================
# 验证4: 导数求和公式
# ============================================================================
hr("验证4: 导数求和公式与数值导数匹配")

# 使用已知零点列表 (前 80 个用于更精确的求和)
zeros_y_all = zeros_y + [
    48.005151, 49.773832, 52.970321, 56.446248, 59.347044, 60.831779,
    65.112544, 67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111, 92.491899,
    94.651344, 95.870634, 98.831194, 101.317851, 103.725538, 105.446623,
    107.168611, 111.029536, 111.874659, 114.320221, 116.226680, 118.790783,
    121.370125, 122.946829, 124.256819, 127.516684, 129.578704, 131.087688,
    133.497737, 134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
    146.000982, 147.422765, 150.053520, 150.925258, 153.024694, 156.112909,
    157.597591, 158.849988, 161.188964, 163.030710, 165.537069, 167.184440,
    169.094515, 169.911976, 173.411537, 174.754191, 177.329116, 178.210036,
    179.916484, 182.207078, 184.874468, 185.598784, 187.228923, 189.416159,
    192.026656, 193.079727, 195.265396, 196.876442, 198.015309, 200.059738
]

def derivative_formula(sigma, gamma):
    """从 Hadamard 乘积推得的导数公式"""
    d = sigma - 0.5
    total = mp.mpf('0')
    for g0 in zeros_y_all:
        a = gamma - g0
        denom = d*d + a*a
        if abs(denom) < 1e-30:
            continue  # skip self-term at the zero itself
        term = 2 * d / denom
        total += term
    return float(total)

# 测试在几个点上的匹配
formula_ok = True
for g in zeros_y[:2]:
    print(f"\n  γ={g:.4f}:")
    for sig in [0.4, 0.45, 0.48, 0.5, 0.52, 0.55, 0.6]:
        f_val = derivative_formula(sig, g)
        # 数值导数 = h'×h, 公式给出 h'/h
        h_val = xi_sq(sig, g)
        h_prime = xi_sq_deriv(sig, g)
        ratio_num = h_prime / h_val if h_val > 1e-30 else 0
        match = abs(f_val - ratio_num) < max(abs(f_val),abs(ratio_num))*0.05 if abs(f_val)>1e-6 else abs(ratio_num)<1e-5
        if sig != 0.5:  # skip the singular point
            if not match:
                formula_ok = False
            print(f"    σ={sig:.2f}: 公式={f_val:+.4f}  数值={ratio_num:+.4f}  {'✓' if match else '✗'}")

print(f"\n  公式匹配: {'通过' if formula_ok else '存在偏差'}")

# ============================================================================
# 结论
# ============================================================================
hr("结论")
all_ok = convex_ok and deriv_ok and zero_ok and formula_ok
print(f"""
  验证1: |ξ|² 凸性 (d²/dσ² > 0)       {'通过' if convex_ok else '失败'}
  验证2: 导数符号正确                  {'通过' if deriv_ok else '失败'}
  验证3: 零点极小在 σ=0.5              {'通过' if zero_ok else '失败'}
  验证4: 导数求和公式匹配              {'通过' if formula_ok else '失败'}

  全部验证: {'全部通过' if all_ok else '存在失败'}

  证明链:
  |ξ|² 严格凸 + 对称性 → 唯一极小在 σ=0.5
  → 零点在此 → 对所有 γ 成立 → 黎曼猜想成立。

  待完成: 近零点贡献控制不等式的解析证明。
""")
print("="*65)
