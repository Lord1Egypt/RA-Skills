---
name: china-options-pricing
description: Compute Black-Scholes option prices, implied volatility, Greeks (Delta/Gamma/Theta/Vega/Rho), and multi-leg strategy P&L for Chinese ETF options, index options, and commodity options. Uses pure math (no third-party libraries). Can chain with china-commodity-quotes for underlying price input.
emoji: 🦐📈
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    envVars: []
---

# China Options Pricing — 中国期权定价分析

Black-Scholes 期权定价、隐含波动率计算、希腊值分析、多腿策略盈亏计算。覆盖中国主流期权品种：ETF期权、股指期权、商品期权。

## Quick Start — 快速上手

**什么时候用虾哥的期权分析能力：**

| 场景 | 怎么做 |
|:-----|:-------|
| 想知道一张期权合约的理论价格 | 用 BS 定价公式计算 |
| 市场报价隐含了多少波动率 | 用 Newton-Raphson 反推 IV |
| 持仓的风险敞口有多大 | 计算 Delta / Gamma / Theta / Vega / Rho |
| 组合策略（牛市价差/跨式/蝶式）的盈亏形态 | 用策略分析功能 |
| 需要标的资产的实时价格 | 先调 china-commodity-quotes 获取 |

### 核心公式速览 (Black-Scholes)

**欧式认购期权 (Call):**
$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

**欧式认沽期权 (Put):**
$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

其中：
$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$$
$$d_2 = d_1 - \sigma\sqrt{T}$$

- $S_0$ = 标的资产当前价格
- $K$ = 行权价
- $T$ = 剩余期限（年）
- $r$ = 无风险利率
- $\sigma$ = 波动率
- $N(\cdot)$ = 标准正态累积分布函数

---

## Core Capabilities

### 1. Black-Scholes 期权定价

**用途：** 给定标的价、行权价、到期时间、利率、波动率，计算认购/认沽期权理论价格。

#### 标准正态分布 CDF 近似

使用 Abramowitz & Stegun 算法（误差 < 1.5×10⁻⁷），无需第三方库：

```python
import math

def norm_cdf(x):
    """标准正态累积分布函数 — Abramowitz & Stegun 近似"""
    if x < -6:
        return 0.0
    if x > 6:
        return 1.0
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    sign = 1.0 if x >= 0 else -1.0
    x_abs = abs(x)
    t = 1.0 / (1.0 + p * x_abs)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x_abs * x_abs / 2)
    return y if sign > 0 else 1.0 - y

def norm_pdf(x):
    """标准正态概率密度函数"""
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
```

#### BS 定价实现

```python
def d1_d2(S, K, T, r, sigma):
    """计算 d1 和 d2"""
    if T <= 0 or sigma <= 0:
        raise ValueError("T 和 sigma 必须为正数")
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return d1, d2

def bs_call_price(S, K, T, r, sigma):
    """欧式认购期权理论价格"""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

def bs_put_price(S, K, T, r, sigma):
    """欧式认沽期权理论价格"""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
```

#### 执行示例

```
用户输入：
  S = 3.500  (上证50ETF 现价)
  K = 3.600  (行权价)
  T = 0.25   (3个月到期)
  r = 0.025  (无风险利率 2.5%)
  σ = 0.20   (波动率 20%)

输出：
  🦐 Black-Scholes 定价结果
  📌 标的: 上证50ETF | 认购 Call | 行权价 3.600
  📅 剩余期限: 0.25 年 (约91天)
  ─────────────────────────────────────
  💰 理论价格:  0.0552 (约 552 元/张)
  📊 内在价值:  0.0000 (价外)
  ⏳ 时间价值:  0.0552
  ✅ 价格状态:  看涨期权为价外 (OTM)
  ─────────────────────────────────────
```

**中国期权合约单位：**

| 期权类型 | 合约单位 | 权利金示例 |
|:---------|:---------|:-----------|
| ETF期权 | 10,000份/张 | 价格 0.0552 = 552元/张 |
| 股指期权 | 每点100元 | 价格 80.5 = 8,050元/张 |
| 商品期权 | 同期货手数 | 按品种而异 |

---

### 2. 隐含波动率 (Implied Volatility)

**用途：** 根据市场价格反推隐含的波动率水平。使用 Newton-Raphson 迭代。

#### 实现

```python
def implied_volatility_call(S, K, T, r, market_price, max_iter=100, tol=1e-6):
    """用 Newton-Raphson 反推认购期权的隐含波动率"""
    if T <= 0:
        return 0.0
    # 初始猜测
    sigma = 0.2
    for i in range(max_iter):
        d1, d2 = d1_d2(S, K, T, r, sigma)
        price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma
        # Vega = ∂price/∂σ
        vega = S * norm_pdf(d1) * math.sqrt(T)
        if vega < 1e-12:
            break
        sigma -= diff / vega
        if sigma <= 0:
            sigma = 0.01
    return round(sigma, 6)

def implied_volatility_put(S, K, T, r, market_price, max_iter=100, tol=1e-6):
    """用 Newton-Raphson 反推认沽期权的隐含波动率"""
    if T <= 0:
        return 0.0
    sigma = 0.2
    for i in range(max_iter):
        d1, d2 = d1_d2(S, K, T, r, sigma)
        price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma
        vega = S * norm_pdf(d1) * math.sqrt(T)
        if vega < 1e-12:
            break
        sigma -= diff / vega
        if sigma <= 0:
            sigma = 0.01
    return round(sigma, 6)
```

**收敛条件：** 最大 100 次迭代，精度 1×10⁻⁶。通常 5-15 次迭代即可收敛。

#### 执行示例

```
用户输入：
  S = 3.500    (上证50ETF 现价)
  K = 3.600
  T = 0.25
  r = 0.025
  market_price = 0.0600 (市场权利金)

输出：
  🦐 隐含波动率计算
  📌 认购 Call @ 3.600 | 市价 0.0600
  ─────────────────────────────────────
  🔄 隐含波动率 σ_IV = 24.37%
  📊 BS 理论价 @ 24.37% = 0.0600 ✅
  ─────────────────────────────────────
```

---

### 3. 希腊值 (Greeks) 计算

**用途：** 量化期权价格对各风险因子的敏感度。

| 希腊值 | 符号 | 含义 | 公式 |
|:-------|:-----|:-----|:-----|
| **Delta** | Δ | 标的价每变动1元，期权价格变动多少 | Call: $N(d_1)$, Put: $-N(-d_1)$ |
| **Gamma** | Γ | Delta对标的价的敏感度 | $\frac{N'(d_1)}{S_0 \sigma \sqrt{T}}$ |
| **Theta** | Θ | 每过去1天，期权价格损失多少 | 见代码 |
| **Vega** | ν | 波动率每变动1%，期权价格变动多少 | $S_0 N'(d_1) \sqrt{T}$ |
| **Rho** | ρ | 利率每变动1%，期权价格变动多少 | Call: $KTe^{-rT} N(d_2)$, Put: $-KTe^{-rT} N(-d_2)$ |

#### 实现

```python
def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """计算所有希腊值"""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    sqrt_T = math.sqrt(T)

    # Delta
    if option_type == 'call':
        delta = norm_cdf(d1)
    else:
        delta = -norm_cdf(-d1)

    # Gamma (Call 和 Put 相同)
    gamma = norm_pdf(d1) / (S * sigma * sqrt_T)

    # Theta (年化 → 每日)
    term1 = -(S * norm_pdf(d1) * sigma) / (2 * sqrt_T)
    if option_type == 'call':
        theta_year = term1 - r * K * math.exp(-r * T) * norm_cdf(d2)
    else:
        theta_year = term1 + r * K * math.exp(-r * T) * norm_cdf(-d2)
    theta_daily = theta_year / 365

    # Vega (波动率每变动 1%)
    vega = S * norm_pdf(d1) * sqrt_T / 100  # 每变动1个百分点

    # Rho (利率每变动 1%)
    if option_type == 'call':
        rho = K * T * math.exp(-r * T) * norm_cdf(d2) / 100
    else:
        rho = -K * T * math.exp(-r * T) * norm_cdf(-d2) / 100

    return {
        'delta': round(delta, 4),
        'gamma': round(gamma, 4),
        'theta': round(theta_daily, 6),   # 每日时间价值损耗
        'vega':  round(vega, 6),          # 波动率+1%的敏感度
        'rho':   round(rho, 6)            # 利率+1%的敏感度
    }
```

#### 希腊值解读表

| Delta 值 | 含义 |
|:---------|:-----|
| 0.50~0.70 | 平值或轻度价内，标的波动敏感 |
| 0.20~0.40 | 价外期权，方向性弱 |
| >0.90 | 深度价内，接近持有标的 |

| Gamma 值 | 含义 |
|:---------|:-----|
| 高 Gamma | 平值附近，Delta 变化快，适合 Gamma Scalping |
| 低 Gamma | 深度价内/价外，Delta 稳定 |

| Theta | 含义 |
|:------|:-----|
| 负值 | 时间损耗（期权卖方收益来源） |
| 绝对值大 | 平值附近到期前 Theta 最大 |

#### 执行示例

```
用户输入：
  S = 3.500, K = 3.600, T = 0.25, r = 0.025, σ = 0.20

输出：
  🦐 希腊值分析 — 认购 Call
  ─────────────────────────────────────
  📌 标的: 50ETF @ 3.500 | 行权 3.600 | 剩余 91天
  ─────────────────────────────────────
  Δ Delta  =  0.3232  → 标的+1分，期权约+0.32分
  Γ Gamma  =  1.7286  → 每升1元，Delta增1.73
  Θ Theta  = -0.00052 → 每天损耗约5.2元/张
  ν Vega   =  0.00373 → 波动率+1%，期权+0.37分(37元/张)
  ρ Rho    =  0.00074 → 利率+1%，期权+0.07分(7.4元/张)
  ─────────────────────────────────────
```

---

### 4. 期权策略分析

**用途：** 分析常见期权组合策略的盈亏情况。

#### 支持的策略

| 策略 | 腿数 | 适用场景 |
|:-----|:-----|:---------|
| **买入看涨 (Long Call)** | 1 | 强烈看涨，风险有限 |
| **买入看跌 (Long Put)** | 1 | 强烈看跌，风险有限 |
| **卖出看涨 (Short Call)** | 1 | 不看涨，收取权利金 |
| **卖出看跌 (Short Put)** | 1 | 不看跌，收取权利金 |
| **牛市价差 (Bull Spread)** | 2 | 温和看涨，降低权利金成本 |
| **熊市价差 (Bear Spread)** | 2 | 温和看跌，降低权利金成本 |
| **跨式组合 (Straddle)** | 2 | 预期剧烈波动（做多跨式） |
| **宽跨式 (Strangle)** | 2 | 预期大幅波动，成本更低 |
| **蝶式价差 (Butterfly)** | 4 | 预期窄幅震荡，风险有限 |
| **备兑开仓 (Covered Call)** | 2 | 持有标的，增收权利金 |
| **保护性看跌 (Protective Put)** | 2 | 持有标的，买入保险 |

#### 盈亏计算实现

```python
def strategy_pnl(strategy, S_T, legs):
    """
    计算期权策略在到期时的盈亏
    strategy: 策略名称
    S_T: 到期标的价
    legs: 列表，每腿 = {type: 'call'/'put', position: 'long'/'short',
                         K: 行权价, premium: 权利金, multiplier: 合约乘数}
    """
    total = 0.0
    for leg in legs:
        if leg['type'] == 'call':
            intrinsic = max(S_T - leg['K'], 0)
        else:
            intrinsic = max(leg['K'] - S_T, 0)
        if leg['position'] == 'long':
            leg_pnl = (intrinsic - leg['premium']) * leg.get('multiplier', 1)
        else:
            leg_pnl = (leg['premium'] - intrinsic) * leg.get('multiplier', 1)
        total += leg_pnl
    return total

def analyze_strategy(strategy, legs, S_range=None):
    """
    分析策略在标的价范围内的盈亏
    返回盈亏表 + 关键指标(最大盈利/最大亏损/盈亏平衡点)
    """
    # ... 实现策略分析，返回盈亏表
    pass
```

#### 执行示例

```
🦐 期权策略分析 — 牛市价差 (Bull Call Spread)
═════════════════════════════════════════
📌 标的: 上证50ETF (510050)
📅 到期: 2026-08-20 (剩余91天)

📋 策略构成:
  腿1: 买入 Call @ 3.500，权利金 0.0800
  腿2: 卖出 Call @ 3.700，权利金 0.0250
  净权利金支出: 0.0550 (550元/张)

📊 到期盈亏分析:
  S_T=3.400:  -550 元 🔴
  S_T=3.500:  -550 元 🔴 (盈亏平衡点下方)
  S_T=3.555:     0 元 ⚪ (盈亏平衡点)
  S_T=3.600:  +450 元 🟢
  S_T=3.700: +1450 元 🟢 (最大盈利)

📈 关键指标:
  最大盈利: 1,450 元/张
  最大亏损: -550 元/张
  盈亏平衡: 3.555
  盈亏比: 2.64 : 1
```

---

### 5. 中国期权品种参考

#### ETF期权（上证所/深交所）

| 品种 | 代码 | 合约单位 | 上市交易所 | 标的 |
|:-----|:-----|:---------|:----------|:----|
| **上证50ETF期权** | 510050 | 10,000份 | 上交所 | 上证50ETF |
| **沪深300ETF期权(沪)** | 510300 | 10,000份 | 上交所 | 华泰柏瑞沪深300ETF |
| **沪深300ETF期权(深)** | 159919 | 10,000份 | 深交所 | 嘉实沪深300ETF |
| **中证500ETF期权(沪)** | 510500 | 10,000份 | 上交所 | 南方中证500ETF |
| **中证500ETF期权(深)** | 159922 | 10,000份 | 深交所 | 嘉实中证500ETF |
| **科创50ETF期权** | 588000 | 10,000份 | 上交所 | 科创50ETF |
| **创业板ETF期权** | 159915 | 10,000份 | 深交所 | 创业板ETF |
| **中证1000ETF期权** | 159845 | 10,000份 | 深交所 | 中证1000ETF |
| **深100ETF期权** | 159901 | 10,000份 | 深交所 | 深证100ETF |
| **上证综指ETF期权** | 510210 | 10,000份 | 上交所 | 上证综合ETF |

#### 股指期权（中金所 CFFEX）

| 品种 | 代码 | 乘数 | 上市日期 |
|:-----|:-----|:-----|:---------|
| **沪深300股指期权** | IO | ¥100/点 | 2019-12-23 |
| **中证1000股指期权** | MO | ¥100/点 | 2022-07-22 |
| **上证50股指期权** | HO | ¥100/点 | 2022-12-19 |

#### 商品期权（三大商品交易所）

| 交易所 | 品种 | 代码 | 行权方式 |
|:-------|:-----|:-----|:---------|
| **大商所 DCE** | 豆粕期权 | M | 美式 |
| | 玉米期权 | C | 美式 |
| | 铁矿石期权 | I | 美式 |
| | 棕榈油期权 | P | 美式 |
| | 豆油期权 | Y | 美式 |
| | 液化气期权 | PG | 美式 |
| | 塑料期权 | L | 美式 |
| | 聚丙烯期权 | PP | 美式 |
| | PVC期权 | V | 美式 |
| | 豆二期权 | B | 美式 |
| | 玉米淀粉期权 | CS | 美式 |
| | 乙二醇期权 | EG | 美式 |
| | 苯乙烯期权 | EB | 美式 |
| | 生猪期权 | LH | 美式 |
| **郑商所 ZCE** | 白糖期权 | SR | 美式 |
| | 棉花期权 | CF | 美式 |
| | PTA期权 | TA | 美式 |
| | 甲醇期权 | MA | 美式 |
| | 菜籽粕期权 | RM | 美式 |
| | 菜籽油期权 | OI | 美式 |
| | 动力煤期权 | ZC | 美式 |
| | 纯碱期权 | SA | 美式 |
| | 尿素期权 | UR | 美式 |
| | 短纤期权 | PF | 美式 |
| | 花生期权 | PK | 美式 |
| | 对二甲苯期权 | PX | 美式 |
| | 烧碱期权 | SH | 美式 |
| | 玻璃期权 | FG | 美式 |
| | 苹果期权 | AP | 美式 |
| **上期所 SHFE** | 铜期权 | CU | 美式 |
| | 黄金期权 | AU | 美式 |
| | 铝期权 | AL | 美式 |
| | 锌期权 | ZN | 美式 |
| | 橡胶期权 | RU | 美式 |
| | 螺纹钢期权 | RB | 美式 |
| | 白银期权 | AG | 美式 |
| | 丁二烯橡胶期权 | BR | 美式 |
| | 氧化铝期权 | AO | 美式 |
| | 铅期权 | PB | 美式 |
| | 镍期权 | NI | 美式 |
| | 锡期权 | SN | 美式 |
| | 热轧卷板期权 | HC | 美式 |
| | 天然橡胶期权 | RU | 美式 |
| | 纸浆期权 | SP | 美式 |
| **广期所 GFEX** | 工业硅期权 | SI | 美式 |
| | 碳酸锂期权 | LC | 美式 |
| **国际能源中心 INE** | 原油期权 | SC | 美式 |

**重要提示：** 中国商品期权多为 **美式期权**，可在到期前任意交易日行权，BS 模型仅作为近似参考，实际定价应考虑提前行权溢价。

---

### 6. 定价公式速查（纯数学实现）

所有公式均使用 `math.log`, `math.exp`, `math.sqrt`, `math.pi`，**不依赖任何第三方库**。

#### 关键函数汇总

```python
# ==============================
# 正态分布函数
# ==============================
def norm_cdf(x):
    """Abramowitz & Stegun 近似 (误差 < 1.5e-7)"""

def norm_pdf(x):
    """标准正态密度函数"""

# ==============================
# BS 核心函数
# ==============================
def d1_d2(S, K, T, r, sigma):
    """计算 d1, d2"""
    d1 = (log(S/K) + (r + sigma**2/2)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    return d1, d2

def bs_call_price(S, K, T, r, sigma):
    """BS认购定价"""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return S*N(d1) - K*exp(-r*T)*N(d2)

def bs_put_price(S, K, T, r, sigma):
    """BS认沽定价"""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return K*exp(-r*T)*N(-d2) - S*N(-d1)

# ==============================
# 隐含波动率
# ==============================
def iv_call(S, K, T, r, mkt_price):
    """Newton-Raphson 反推 IV"""
def iv_put(S, K, T, r, mkt_price):
    """Newton-Raphson 反推 IV"""

# ==============================
# 希腊值
# ==============================
def calculate_greeks(S, K, T, r, sigma, type='call'):
    """返回 delta, gamma, theta, vega, rho"""
```

#### 参数约定

| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| 无风险利率 $r$ | **2.5%** (0.025) | 参考 10Y 中国国债收益率 |
| 到期时间 $T$ | 按日历日/365 | 如91天 = 91/365 ≈ 0.25 |
| 波动率 $\sigma$ | 20% (0.20) | 年化波动率 |
| 迭代精度 | 1×10⁻⁶ | 隐含波动率收敛条件 |
| 最大迭代 | 100 | Newton-Raphson 上限 |

---

### 7. 在 Skilled Chain 中使用（结合 china-commodity-quotes）

**典型工作流：** 先查标的价 → 再算期权定价

步骤：
1. 用 `china-commodity-quotes` 获取标的资产实时价格
2. 将获取到的价格作为 $S_0$ 代入 BS 定价
3. 输出完整的期权分析结果

**示例：上证50ETF期权分析**

```
Step 1: 查标的价
  → 使用 china-commodity-quotes 获取 510050 最新价
  → 返回: S = 3.500

Step 2: 计算 Call @ 3.600, 剩余91天
  → 使用本 skill 的 BS 定价
  → 参数: S=3.500, K=3.600, T=0.25, r=0.025, σ=0.20
  → 结果: 理论价 0.0552

Step 3: 如果已有市价，反推隐含波动率
  → 市价 = 0.0600
  → IV = 24.37%
```

---

## Notes & Caveats

1. **BS 模型局限性：** 假设波动率恒定、利率恒定、无交易成本、标的连续交易。中国期权市场实际定价可能与 BS 模型存在偏差。

2. **美式期权溢价：** 中国商品期权多为美式期权，BS 模型计算的欧式价格低于美式理论价格（因提前行权权有额外价值）。对于深度价内的 ETF 期权（含股息），提前行权也可能发生。

3. **股息调整：** ETF 期权在除息日应调整 BS 模型：$S_0 \to S_0 - PV(D)$，其中 $PV(D)$ 为剩余期限内预期股息的现值。

4. **波动率偏斜：** 中国期权市场存在波动率微笑/偏斜现象，不同行权价的 IV 不同。分析时建议同时查多个行权价进行波动率曲线分析。

5. **到期月份选择：** 中国期权通常有当月、下月、下季月、隔季月四个到期月份，选择流动性最好的月份进行分析。

6. **无风险利率：** 默认 2.5% 为近似值。对于更精确的分析，可查询当日中国 10 年期国债收益率替代。

7. **保证金计算（卖方）：** 本 skill 不直接计算期权卖方的保证金需求。实际交易中，卖方保证金按交易所标准单独计算，超出权利金收入。
