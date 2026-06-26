# 跨交易所资金费率套利算法详解

## 核心原理

永续合约通过资金费率（Funding Rate）锚定现货价格。不同交易所的费率由各自市场供需决定，经常出现显著差异。本策略利用这个差异：

```
策略 = 在费率低的交易所做多 + 在费率高的交易所做空
净收益 = (short_rate − long_rate) × 3次/天 × 365天 × 名义价值 − 往返成本
```

## 1. 机会扫描

### VarFunding API

VarFunding（varfunding.xyz）是第三方服务，预计算各交易所间的套利机会：

```
GET /api/funding?exchanges=hyperliquid,binance
```

返回的每个 market 包含：
- `baseAsset`：币种（如 FET, RENDER）
- `variational.rate`：参考交易所的费率
- `comparisons[].rate`：对比交易所的费率
- `arbitrageOpportunity`：计算好的方向、spread、估计 APR、置信度

### 过滤规则

```python
if estimated_apr >= min_apr_pct          # 默认 10%
   and confidence >= min_confidence:     # 默认 medium
    # 保留这个机会
```

## 2. 稳定性验证

防止瞬时费率异常导致错误开仓。

### 快照积累

每个 tick 记录 Top 5 机会的快照到 state.rate_snapshots（最多保留 20 条）：

```json
{
  "ts": "2026-03-25T10:00:00Z",
  "coin": "FET",
  "spread": 0.0006,
  "estimated_apr": 66.5,
  "long_exchange": "hyperliquid",
  "short_exchange": "binance"
}
```

### 稳定性检查

按币种分组后，对同一币种的所有快照：

```python
count = len(snapshots)        # 需要 >= stability_snapshots (3)
spreads = [s["spread"] for s in snapshots]
avg = mean(spreads)
std = stdev(spreads)
std_ratio = std / abs(avg)    # 需要 < stability_max_std_ratio (0.3)
```

含义：费率差在多个 tick 间保持稳定（变异系数 < 30%），不是偶发异常。

## 3. 深度验证

VarFunding 数据可能滞后，需要独立验证。

### 实时费率

分别从 HL 和 Binance 获取实时 funding rate 和 mid price：

```python
hl_rate = hl_client.get_funding_rate("FET")    # 8h 费率
bn_rate = bn_client.get_funding_rate("FET")
hl_price = hl_client.get_mid_price("FET")
bn_price = bn_client.get_mid_price("FET")
```

### 计算

```python
# 实际 spread（做空方费率 − 做多方费率）
actual_spread = rate_map[short_exchange] - rate_map[long_exchange]

# 年化 APR
gross_annual = actual_spread × 3 × 365 × 100    # 8h 费率 × 3次/天 × 365天

# 价格差异（影响 delta 中性）
price_basis_pct = |hl_price - bn_price| / avg_price × 100

# 净 APR
net_apr = gross_annual - round_trip_cost_pct     # 默认扣 0.12%
```

### 拒绝条件

- `actual_spread <= 0` → 方向反转
- `price_basis_pct > 0.5%` → 两所价格差异过大
- `net_apr < 10%` → 扣成本后不够

## 4. 仓位计算

### Size 计算

```python
budget = min(hl_budget, bn_budget)
conservative = budget × 0.5          # 保守系数 50%（HL 分级保证金对小币要求高）
effective = conservative × 0.95       # 预留 5% 手续费
raw_size = effective × leverage / price

# 两所分别按精度向下取整，取较小值
hl_rounded = hl.round_size(coin, raw_size)
bn_rounded = bn.round_size(coin, raw_size)
final_size = min(hl_rounded, bn_rounded)
```

### 为什么保守系数 50%？

HL 的分级保证金对小币（如 FET, RENDER）要求远高于标准保证金。
budget $300 × leverage 3 = $900 名义，但 HL 可能只允许 $400-500 名义。
预留 50% 安全余量，失败后自动减半重试。

## 5. 原子开仓

### 执行顺序

```
1. HL 设杠杆（cross margin）
2. Binance 设杠杆
3. HL 下单（LIMIT IOC, 滑点 0.1%）
   └→ Insufficient margin? → size ÷ 2，重试（最多 3 次）
4. 等待 1s（防止 rate limit）
5. Binance 下单（LIMIT IOC, 滑点 0.1%）
   └→ 失败? → 回滚 HL（close_position）
```

### 为什么先 HL？

- HL 分级保证金限制更严，更容易失败
- HL 失败时还没开 Binance，损失仅手续费（~$0.05）
- 反过来：先 Binance 成功后 HL 失败，需要平 Binance 多花一次手续费

### 滑点为什么是 0.1%？

套利策略对成本极度敏感。常规交易 5% 滑点在这里会吞噬大部分利润。
0.1% 在流动性好的币上足够成交，同时保护利润。

## 6. PnL 计算

### 基于实际余额

```python
entry_total = entry_hl_balance + entry_bn_balance    # 开仓时总余额
current_total = current_hl_balance + current_bn_balance

pnl = current_total - entry_total
roi_pct = pnl / entry_total × 100

# 年化
hours_held = (now - entry_time).total_seconds() / 3600
annualized_roi = roi_pct / hours_held × 24 × 365
```

这种方式包含了所有因素：funding 收入、手续费、资金冻结、标记价变动。

## 7. 健康检查

每个 tick 对持仓进行三重检查：

| 检查 | 指标 | 阈值 | 触发动作 |
|------|------|------|----------|
| Delta | `abs(long_size - short_size) / avg_size` | > 20% | 告警 |
| Spread | `short_rate - long_rate` | < 0.005% | 平仓 |
| 双腿 | `long_size > 0 and short_size > 0` | 任一为 0 | 平仓 |

## 8. 切仓逻辑

```python
# 1. 不健康 → 平仓
if not spread_favorable:
    close_position()

if not has_both_legs:
    close_position()

# 2. 平仓后下一 tick → 自动扫描新机会
# （state 清空 → tick 进入"无持仓"分支 → 重新扫描）
```

## 常见问题

### Q: 两所资金不平衡怎么办？

A: Size 用 `min(两所)` 计算，较大一侧的多余资金闲置。建议保持 HL:BN ≈ 2:3（HL 需要更少保证金因为 cross margin）。

### Q: 费率突然反转怎么办？

A: 每个 tick 检查 spread。反转后 spread < threshold → 自动平仓。最大损失 = 反转 tick 的 funding（5 分钟内的 funding 约 0.0001% 级别，忽略不计）+ 往返手续费。

### Q: Agent Wallet 是什么？

A: HL 支持通过主账户创建子密钥（Agent Wallet），可以下单但不能转账。策略代码自动检测并路由到正确地址。

### Q: Binance 时间戳报错？

A: 客户端内置自动时间同步。首次请求和 -1021 错误时自动校准。
