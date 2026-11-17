# 双币赢分析 (BTCETH DualWin Engine)

## 功能描述
专业 BTC 与 ETH 双币赢（Dual-Win）理财决策助手。当用户询问 BTC/ETH 买入卖出时机、期权策略或需要双币理财建议时触发。通过实时监控波动率曲面与技术指标，自动识别期权费最高且安全边际最大的申购方案，助你实现低价抄底或高位止盈。

## 使用方式
用户说"双币赢分析"即可自动获取数据

## 核心决策逻辑

### 第一层：确定方向（买低还是高卖）

**核心指标**：RSI + 25 Delta Skew

| 条件 | 方向 | 策略 |
|------|------|------|
| RSI < 40 且 Skew < 0 | Buy Low（低吸） | 卖出 Put，收取权利金最高 |
| RSI > 60 且 Skew > 0 | Sell High（高抛） | 卖出 Call，收益最肥 |

### 第二层：品种性价比（BTC vs ETH）

**核心指标**：IVP (IV Percentile)

- 比较 BTC 和 ETH 的 IVP
- **优先选择 IVP 更高的品种**
- 理由：IVP 高 = 期权费处于历史高位，卖出性价比高

### 第三层：胜率预测（1-3天）

**核心指标**：DVOL + IVK

- DVOL 高（>60）→ 年化收益可观
- IVK 高 → 极端行情预期 → 赢率打折
- 挂单价在 1.5×DVOL 波动区间外 → 赢率极高

## 指标速查表

| 指标 | 监控维度 | 触发条件 | 影响 |
|------|----------|----------|------|
| DVOL | 整体波动水位 | > 60 | 年化收益加成 |
| IVP | 性价比 | > 70% | 强烈申购信号 |
| 25 Delta Skew | 偏向性 | 正且拉升 | 高卖 (Sell High) |
| IVK | 尾部风险 | 异常升高 | 风险预警，调低赢率 |
| RSI | 动能 | > 70 或 < 30 | 确认极值点 |

## 进阶优化

1. **轮询频率**：每小时轮询 DVOL，捕捉 IV 突发飙升
2. **RV 对比**：若 IV - RV > 10%，最佳"卖保险"时机
3. **风险提示**：IVK 暴涨 → 输出 "⚠️ 检测到肥尾效应，建议观望，防止穿仓。"

## 输出格式

```
📊 双币赢实操建议 | [时间]

---

📈 市场数据
BTC: $xxx | DVOL xx% | IVP xx% | RSI xx | Skew xx
ETH: $xxx | DVOL xx% | IVP xx% | RSI xx | Skew xx
恐慌指数: xx [emoji]

---

💡 决策分析
- BTC: DVOL=xx%, 5日均值=xx%, 动量Z=xx, 扩张=XX
- ETH: DVOL=xx%, 5日均值=xx%, 动量Z=xx, 扩张=XX
- ETH/BTC Ratio=xx, Z-score=xx

[结论]

---

1. 推荐品种：[BTC/ETH]
- 理由：xxx

2. 推荐方向：[高卖/低买]

3. 操作建议

🎯 1天期
激进 CALL $xx (+x%) 胜率xx%
稳健 CALL $xx (+x%) 胜率xx%
平衡 CALL $xx (+x%) 胜率xx%
保守 CALL $xx (+x%) 胜率xx%

🎯 2天期
激进 CALL $xx (+x%) 胜率xx%
稳健 CALL $xx (+x%) 胜率xx%
平衡 CALL $xx (+x%) 胜率xx%
保守 CALL $xx (+x%) 胜率xx%

🎯 3天期
激进 CALL $xx (+x%) 胜率xx%
稳健 CALL $xx (+x%) 胜率xx%
平衡 CALL $xx (+x%) 胜率xx%
保守 CALL $xx (+x%) 胜率xx%

---

⚠️ 风险提示
```

## 注意事项

⚠️ 本工具仅供参考，不构成投资建议
⚠️ 期权交易有风险，请谨慎操作
