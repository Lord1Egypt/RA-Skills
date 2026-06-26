# 输出格式规范（三模差异化版 + 交易决策系统）

## 目录

1. [核心升级概览](#核心升级概览)
2. [搜索返回格式（五要素强制）](#搜索返回格式五要素强制)
3. [截图分析格式 - 稳定币模式](#截图分析格式---稳定币模式)
4. [截图分析格式 - 主流币模式](#截图分析格式---主流币模式)
5. [截图分析格式 - Meme币模式](#截图分析格式---meme币模式)
6. [双源融合结构（混合查询）](#双源融合结构混合查询)
7. [冲突处理机制](#冲突处理机制)
8. [复合查询输出格式](#复合查询输出格式)
9. [截图质量与降级处理](#截图质量与降级处理)
10. [搜索可用性状态](#搜索可用性状态)
11. [币种分类判断规则](#币种分类判断规则)
12. [币种别名完整映射表](#币种别名完整映射表)
13. [风险提示模板](#风险提示模板)
14. [交易指令拒绝模板](#交易指令拒绝模板)

---

## 核心升级概览

本规范从「分析工具层」进化到「交易决策系统」，核心升级：

| 升级项 | 关键字段 | 价值 |
|--------|---------|------|
| **双源融合** | `analysis_source`, `data_fusion` | 统一搜索+截图，避免数据冲突 |
| **冲突处理** | `data_conflict_check` | 明确截图vs搜索价格偏差处理 |
| **交易结构** | `market_structure` | HH/HL/流动性区/订单块，交易员语言 |
| **崩盘识别** | `dump_risk_detector` | Meme币出货检测 |
| **极端事件** | `depeg_alert_system` | 稳定币紧急模式 |
| **交易可用性** | `trade_usable`, `usable_level` | A/B/C分级，直接决策参考 |
| **策略标准化** | `observation_plan` | 入场/止损/止盈/R比，仅供参考不做交易决策 |
| **数据可信度** | `data_quality` | tier1/tier2/tier3分级 |
| **智能风险** | `risk_flags` | 自动组合风险标签 |
| **咪呀评分** | `lobster_score` | 7.5分/B+，综合评级 |

---

## 搜索返回格式（五要素强制）

所有联网搜索返回必须包含以下五个要素：

| 要素 | 字段名 | 说明 | 示例值 |
|------|--------|------|--------|
| 【数据】 | `data` | 核心数据体 | - |
| 【来源】 | `source` | 数据来源说明 | "联网搜索聚合（Tavily/Bing）" |
| 【时间】 | `server_time` + `timezone` | 服务器时间+时区 | "2026-05-04 08:30:00", "北京时间 (UTC+8)" |
| 【延迟】 | `delay_note` | 数据延迟说明 | "搜索聚合行情，延迟约1-5分钟" |
| 【边界】 | `boundary` | 能力边界说明 | "仅信息搜索与截图分析，不支持直接交易" |
| 【免责】 | `disclaimer` | 必填免责声明 | "仅信息整理与技术分析，不构成投资建议" |

### 数据可信度分级（新增）

```json
{
  "data_quality": {
    "source_tier": "tier1",
    "confidence": "high",
    "cross_verified": true,
    "tier_explanation": "tier1=官方/ETF/链上，tier2=媒体，tier3=社交"
  }
}
```

| 等级 | 来源示例 | 可信度 |
|------|---------|--------|
| **tier1** | ETF官网、链上浏览器、交易所公告 | 高 |
| **tier2** | 金色财经、CoinDesk、彭博 | 中 |
| **tier3** | Twitter/X、Telegram、论坛 | 低 |

### JSON 结构

```json
{
  "source": "联网搜索聚合",
  "data": {
    "symbol": "BTC",
    "symbol_cn": "比特币",
    "category": "mainstream",
    "price_range": "约 $77,800 - $78,200",
    "change_24h": "+1.2%",
    "market_summary": "近期在77K-80K区间震荡，ETF持续净流入",
    "key_news": ["ETF净流入5亿美元", "美联储官员讲话偏鹰"],
    "search_time": "2026-05-04 08:30:00"
  },
  "freshness_check": {
    "is_fresh": true,
    "search_time": "2026-05-04 08:30:00",
    "note": "基于联网搜索，非交易所原生实时撮合数据"
  },
  "search_availability": {
    "status": "search_ok",
    "detail": "搜索服务正常"
  },
  "data_quality": {
    "source_tier": "tier1",
    "confidence": "high",
    "cross_verified": true
  },
  "server_time": "2026-05-04 08:30:00",
  "timezone": "北京时间 (UTC+8)",
  "delay_note": "搜索聚合行情，延迟约 1-5 分钟（非交易所原生毫秒级数据）",
  "boundary": "仅信息搜索与截图分析，不支持直接交易/下单/合约操作",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。",
  "screenshot_prompt": "如需精准技术分析，请发送交易所APP实时K线截图"
}
```

### 价格单位（强制）

- 所有价格必须标注单位：`$` 表示 USD
- 示例：`$78,146`（正确），`78146`（错误，缺单位）
- 价格精度自适应：
  - ≥ $10,000：保留 0 位小数，如 `$78,146`
  - $1,000 - $9,999：保留 2 位小数，如 `$2,350.50`
  - $100 - $999：保留 4 位小数，如 `$84.3250`
  - $1 - $100：保留 4 位小数，如 `$84.3250`
  - $0.1 - $1：保留 6 位小数，如 `$0.623450`
  - $0.01 - $0.1：保留 6 位小数，如 `$0.045600`
  - < $0.01（Meme币常见）：保留 8 位小数，如 `$0.00000845`

---

## 截图分析格式 - 稳定币模式

当 `category == "stable"` 时使用此模板。

### 时效性阈值

稳定币对时效性要求较低，锚定状态变化较慢：
- **过期阈值**：60分钟
- **字段说明**：`freshness_check.note` 应包含"稳定币过期阈值为60分钟"

### JSON 结构（含新增字段）

```json
{
  "source": "用户截图图像分析",
  "category": "stablecoin",
  "symbol": "USDT",
  "symbol_cn": "泰达币",
  "analysis_mode": "长线基本面",
  "analysis_source": ["screenshot", "search"],
  "data_fusion": true,
  "data": {
    "current_price": 1.001,
    "price_currency": "USD",
    "peg_deviation": {
      "value": 0.1,
      "unit": "%",
      "display": "+0.1%"
    },
    "peg_status": "正常锚定",
    "peg_safe_range": "0.998 - 1.002",
    "reserve_audit": {
      "latest_report": "2026年Q1 德勤审计通过",
      "report_date": "2026-03-15",
      "source_freshness": "2026-05-04搜索确认"
    },
    "market_cap_trend": {
      "value": 2.3,
      "unit": "%",
      "period": "30天",
      "display": "+2.3%（30天）"
    },
    "regulatory_risk": "低（近期无重大监管动作）",
    "usage_scene": "交易所储备占比 62%，DeFi 锁仓 $85亿"
  },
  "freshness_check": {
    "is_fresh": true,
    "screenshot_time": "2026-05-04 08:25:00",
    "expiration_threshold_minutes": 60,
    "note": "稳定币过期阈值为60分钟，当前截图在有效期内"
  },
  "screenshot_check": {
    "price_in_range": true,
    "price_warning": null
  },
  "screenshot_quality": {
    "clarity": "clear",
    "missing_elements": [],
    "confidence": "high",
    "trade_usable": true,
    "usable_level": "A"
  },
  "search_availability": {
    "status": "search_ok",
    "detail": "搜索服务正常"
  },
  "depeg_alert_system": {
    "triggered": false,
    "alert_level": "normal",
    "historical_reference": "2023年3月USDC脱钩事件（硅谷银行倒闭）",
    "market_spread": "Binance vs Coinbase 价差 0.03%",
    "reserve_concern": "无"
  },
  "lobster_view": "健康",
  "lobster_logic": "锚定稳、储备透明、市值增长、无监管利空",
  "lobster_score": {
    "score": 8.5,
    "grade": "A",
    "dimensions": {
      "peg_stability": 9,
      "reserve_transparency": 8,
      "regulatory_risk": 8,
      "market_adoption": 9
    }
  },
  "risk_flags": ["low_risk"],
  "strategy": "可作为过渡性资金载体，大额建议分散至USDT/USDC",
  "server_time": "2026-05-04 08:30:00",
  "timezone": "北京时间 (UTC+8)",
  "delay_note": "基于搜索数据+截图价格的综合分析",
  "boundary": "仅稳定币健康度评估，不构成投资建议",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。"
}
```

### 极端事件开关（depeg_alert_system）

当稳定币触发脱钩警报时，进入紧急模式：

```json
{
  "depeg_alert_system": {
    "triggered": true,
    "alert_level": "critical",
    "current_price": 0.97,
    "peg_deviation": {
      "value": -3.0,
      "unit": "%",
      "display": "-3.0%"
    },
    "historical_reference": "类似2023年3月USDC脱钩事件",
    "market_spread": "Binance vs Coinbase 价差 2.1%（异常）",
    "reserve_concern": "大规模赎回迹象，储备透明度存疑",
    "recommended_action": "立即减仓，换仓至其他稳定币或法币"
  },
  "lobster_view": "🚨 紧急脱钩",
  "risk_flags": ["critical_depeg", "liquidity_crisis", "reserve_concern"]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `current_price` | ✅ | 截图显示的价格 |
| `peg_deviation` | ✅ | 与 $1.00 的偏离度（数值+单位结构：value/unit/display） |
| `peg_status` | ✅ | 正常锚定/轻度偏离/严重脱钩 |
| `reserve_audit.latest_report` | 条件 | 最新储备审计情况 |
| `reserve_audit.report_date` | 条件 | 审计报告日期 |
| `reserve_audit.source_freshness` | ✅ | 搜索确认时间 |
| `market_cap_trend` | ✅ | 流通市值变化趋势（数值+单位结构：value/unit/period/display） |
| `depeg_alert_system` | ✅ | 极端事件检测系统 |
| `depeg_alert_system.triggered` | ✅ | 是否触发警报 |
| `screenshot_quality.trade_usable` | ✅ | 是否可用于交易决策 |
| `screenshot_quality.usable_level` | ✅ | A/B/C分级 |
| `lobster_score.score` | ✅ | 0-10分综合评分 |
| `lobster_score.grade` | ✅ | A+/A/B+/B/C/D评级 |
| `risk_flags` | ✅ | 风险标签数组 |

### 脱钩警报规则

| 偏离度 | 状态 | alert_level | 输出 |
|--------|------|-------------|------|
| ±0.1% 以内 | ✅ 正常 | normal | "锚定正常" |
| ±0.1% - ±1% | ⚠️ 轻度偏离 | warning | "轻度偏离，建议关注" |
| ±1% - ±2% | 🔴 危险 | danger | "严重脱钩风险，建议减配" |
| > ±2% | 🚨 紧急 | critical | "严重脱钩警报：建议立即避险换仓" |

---

## 截图分析格式 - 主流币模式

当 `category == "mainstream"` 时使用此模板。

### 时效性阈值

主流币对时效性要求中等，技术形态变化较快：
- **过期阈值**：15-30分钟（视时间周期而定）
- **1小时/4小时线**：30分钟
- **日线**：60分钟
- **字段说明**：`freshness_check.note` 应包含具体时间周期和过期阈值

### JSON 结构（含新增字段）

```json
{
  "source": "用户截图图像分析",
  "category": "mainstream",
  "symbol": "BTC",
  "symbol_cn": "比特币",
  "analysis_mode": "中线技术面+宏观",
  "analysis_source": ["screenshot", "search"],
  "data_fusion": true,
  "data": {
    "screenshot_price": "$78,146",
    "search_price_range": "$77,800 - $78,200",
    "price_currency": "USD",
    "timeframe": "4小时",
    "timeframe_note": "适合中线分析（日线/4h）",
    "trend": "震荡偏多",
    "trend_explanation": "价格在EMA20上方运行，高点抬高",
    "market_structure": {
      "structure_type": "HH/HL（多头结构）",
      "break_of_structure": false,
      "liquidity_zone": "$76,800 下方存在流动性真空区",
      "order_block": "$77,200 - $77,500（需求区）",
      "equal_highs": "$80,000（流动性狩猎目标）"
    },
    "support": "$77,000",
    "support_logic": "前低+EMA20重合位",
    "resistance": "$80,000",
    "resistance_logic": "整数关口+前高压力",
    "pattern": "上升三角形整理末端",
    "pattern_explanation": "高点水平，低点抬高，成交量萎缩",
    "volume_analysis": "缩量回调，未放量跌破支撑",
    "indicators": {
      "macd": "零轴上方粘合等待金叉",
      "rsi": "58 中性区",
      "ema": "价格在EMA20上方"
    },
    "macro_search": "ETF近5日净流入 $1.2亿（搜索来源）",
    "onchain_hint": "交易所净流出 5000 BTC（惜售信号，搜索验证）",
    "sentiment_override": "市场情绪中性偏乐观（恐惧贪婪指数 65）"
  },
  "freshness_check": {
    "is_fresh": true,
    "screenshot_time": "2026-05-04 08:25:00",
    "expiration_threshold_minutes": 30,
    "note": "4小时线过期阈值为30分钟，当前截图在有效期内"
  },
  "data_conflict_check": {
    "price_diff_pct": {
      "value": 0.58,
      "unit": "%",
      "display": "0.58%"
    },
    "conflict_level": "low",
    "resolution": "以截图价格为准（更实时）",
    "note": "搜索行情存在延迟，截图$78,146 vs 搜索$77,800-$78,200"
  },
  "screenshot_check": {
    "price_in_range": true,
    "price_warning": null
  },
  "screenshot_quality": {
    "clarity": "clear",
    "missing_elements": [],
    "confidence": "high",
    "trade_usable": true,
    "usable_level": "A"
  },
  "search_availability": {
    "status": "search_ok",
    "detail": "搜索服务正常"
  },
  "lobster_view": "偏多",
  "lobster_logic": "三角整理末端+ETF持续流入+链上流出，突破80K概率增大",
  "lobster_score": {
    "score": 7.5,
    "grade": "B+",
    "dimensions": {
      "trend": 8,
      "volume": 7,
      "macro": 8,
      "risk": 6
    }
  },
  "risk_flags": ["macro_uncertainty", "key_resistance_nearby"],
  "observation_plan": {
    "bias": "long",
    "focus_zone": "$77,800 - $78,200（关注区间）",
    "risk_level_below": "$76,900（跌破需警惕）",
    "upside_targets": ["$80,000", "$82,500（潜在目标位）"],
    "risk_reward_estimate": "约 1:2（估算）",
    "position_advice": "建议轻仓观察，勿重仓",
    "timeframe_expectation": "1-2周内观察"
  },
  "server_time": "2026-05-04 08:35:00",
  "timezone": "北京时间 (UTC+8)",
  "delay_note": "基于用户截图时间点的技术分析+搜索宏观数据",
  "boundary": "仅技术分析参考，不构成买卖建议",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。"
}
```

### 交易结构层级（market_structure）

```json
{
  "market_structure": {
    "structure_type": "HH/HL（多头结构）| LH/LL（空头结构）| 震荡区间",
    "break_of_structure": false,
    "break_direction": null,
    "liquidity_zone": "$76,800 下方存在流动性真空区",
    "order_block": "$77,200 - $77,500（需求区，前支撑转阻力/支撑）",
    "equal_highs": "$80,000（流动性狩猎目标，止损密集区）",
    "fair_value_gap": "$77,800 - $78,000（价格可能回补的缺口）"
  }
}
```

### 策略标准化输出（observation_plan）

```json
{
  "observation_plan": {
    "bias": "long|short|neutral",
    "focus_zone": "$77,800 - $78,200（关注区间）",
    "risk_level_below": "$76,900（跌破需警惕）",
    "upside_targets": ["$80,000", "$82,500（潜在目标位）"],
    "risk_reward_estimate": "约 1:2（估算）",
    "position_advice": "建议轻仓观察，勿重仓",
    "timeframe_expectation": "1-2周内观察",
    "invalidation_condition": "跌破$76,800且4小时收线低于此位（结构破坏信号）"
  }
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `timeframe` | ✅ | 时间周期 |
| `market_structure` | ✅ | 交易结构（HH/HL/流动性区/订单块） |
| `market_structure.structure_type` | ✅ | 多头/空头/震荡结构 |
| `market_structure.liquidity_zone` | ✅ | 流动性区域 |
| `market_structure.order_block` | ✅ | 订单块/供需区 |
| `data_conflict_check` | 条件 | 截图与搜索价格冲突检测 |
| `data_conflict_check.price_diff_pct` | 条件 | 价格偏差百分比（数值+单位结构：value/unit/display） |
| `data_conflict_check.conflict_level` | 条件 | low/medium/high |
| `screenshot_quality.trade_usable` | ✅ | 是否可用于交易 |
| `screenshot_quality.usable_level` | ✅ | A/B/C |
| `lobster_score.score` | ✅ | 0-10分 |
| `lobster_score.grade` | ✅ | A+/A/B+/B/C/D |
| `observation_plan` | ✅ | 标准化观察计划（仅供参考不做交易决策） |
| `observation_plan.bias` | ✅ | 方向偏好（long/short/neutral） |
| `observation_plan.focus_zone` | ✅ | 关注区间（模糊化表述，非入场指令） |
| `observation_plan.risk_level_below` | ✅ | 跌破需警惕价位（非止损指令） |
| `observation_plan.upside_targets` | ✅ | 潜在上行目标位（非止盈指令） |
| `observation_plan.risk_reward_estimate` | ✅ | 风险回报估算（约 1:X，非精确R比） |
| `observation_plan.position_advice` | ✅ | 仓位建议（模糊化，如"轻仓观察"） |
| `risk_flags` | ✅ | 风险标签数组 |

### 冲突分级处理

| 偏差 | conflict_level | 处理 |
|------|----------------|------|
| <1% | low | 正常，以截图价格为准 |
| 1%-3% | medium | 提醒用户"价格存在偏差，建议核实" |
| >3% | high | ⚠️ 警告"数据异常，请重新截图或检查交易所" |

---

## 截图分析格式 - Meme币模式

当 `category == "meme"` 时使用此模板。

### 时效性阈值

Meme币对时效性要求极高，情绪变化快：
- **过期阈值**：5-10分钟
- **字段说明**：`freshness_check.note` 应包含"Meme币过期阈值为10分钟"

### JSON 结构（含新增字段）

```json
{
  "source": "用户截图图像分析",
  "category": "meme",
  "symbol": "DOGE",
  "symbol_cn": "狗狗币",
  "analysis_mode": "短线情绪面",
  "analysis_source": ["screenshot", "search"],
  "data_fusion": true,
  "data": {
    "current_price": 0.1623,
    "price_currency": "USD",
    "timeframe": "1小时",
    "timeframe_note": "Meme币只看超短周期（15min/1h）",
    "social_heat": "X提及量 +45%（24h），马斯克昨日发帖提及",
    "whale_move": "前10地址增持 0.8%（轻度吸筹）",
    "volume_surge": {
      "value": 2.8,
      "unit": "x",
      "comparison": "24h vs 7日均量",
      "status": "接近异常",
      "display": "2.8倍"
    },
    "exchange_news": "无新上线/下架公告",
    "exchange_news_source": "search",
    "kline_status": "垂直拉升后缩量横盘",
    "sentiment": "FOMO升温"
  },
  "freshness_check": {
    "is_fresh": true,
    "screenshot_time": "2026-05-04 08:25:00",
    "expiration_threshold_minutes": 10,
    "note": "Meme币过期阈值为10分钟，当前截图在有效期内"
  },
  "data_conflict_check": {
    "price_diff_pct": {
      "value": 0.12,
      "unit": "%",
      "display": "0.12%"
    },
    "conflict_level": "low",
    "resolution": "以截图价格为准",
    "note": "截图与搜索价格基本一致"
  },
  "screenshot_check": {
    "price_in_range": true,
    "price_warning": null
  },
  "screenshot_quality": {
    "clarity": "clear",
    "missing_elements": [],
    "confidence": "high",
    "trade_usable": true,
    "usable_level": "B"
  },
  "emotional_indicators": {
    "heat_level": "🔥 高",
    "volume_level": "⚠️ 放量（2.8倍均量）",
    "whale_level": "✅ 轻度吸筹",
    "overall": "狂热期边缘"
  },
  "classification_logic": {
    "stage": "狂热期边缘",
    "trigger_conditions": {
      "volume_surge": 2.8,
      "volume_threshold_met": true,
      "social_heat_change": "+45%",
      "social_threshold_met": true,
      "whale_status": "轻度吸筹",
      "price_trend": "持续上涨+30%"
    },
    "risk_signals": ["已涨30%", "接近历史高位", "FOMO升温"]
  },
  "dump_risk_detector": {
    "smart_money_outflow": "疑似（交易所净流入+12%）",
    "volume_price_divergence": true,
    "top_signal": "高位放量滞涨",
    "risk_level": "high",
    "dump_probability": {
      "value": 0.65,
      "unit": "probability",
      "display": "65%"
    },
    "warning_signals": ["大额转账至交易所", "鲸鱼地址减持", "热度降温迹象"]
  },
  "search_availability": {
    "status": "search_ok",
    "detail": "搜索服务正常"
  },
  "lobster_view": "狂热期边缘",
  "lobster_logic": "热度上升+放量拉盘+名人提及，但已涨30%，追高风险大",
  "lobster_score": {
    "score": 5.5,
    "grade": "C+",
    "dimensions": {
      "momentum": 7,
      "risk": 3,
      "timing": 6,
      "fundamentals": 1
    }
  },
  "risk_flags": ["high_volatility", "meme_coin_no_fundamentals", "dump_risk_high", "fomo_zone"],
  "observation_plan": {
    "bias": "neutral",
    "focus_zone": "$0.14 - $0.15 附近可观察",
    "risk_level_below": "$0.13（跌破需警惕）",
    "upside_targets": ["$0.18", "$0.20（潜在目标位）"],
    "risk_reward_estimate": "约 1:1.5（估算）",
    "position_advice": "Meme币风险极高，建议极小仓位或观望",
    "timeframe_expectation": "3-7天内观察"
  },
  "server_time": "2026-05-04 08:35:00",
  "timezone": "北京时间 (UTC+8)",
  "delay_note": "基于搜索情绪数据+截图技术形态的综合分析",
  "boundary": "仅情绪博弈分析，不构成投资建议",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。"
}
```

### 崩盘识别器（dump_risk_detector）

```json
{
  "dump_risk_detector": {
    "smart_money_outflow": "疑似（交易所净流入+12%，前10地址减持2%）",
    "volume_price_divergence": true,
    "top_signal": "高位放量滞涨（成交量新高但价格未突破）",
    "risk_level": "high",
    "dump_probability": {
      "value": 0.65,
      "unit": "probability",
      "display": "65%"
    },
    "warning_signals": [
      "大额转账至交易所（监测到3笔超1000万DOGE）",
      "鲸鱼地址减持（前10地址24h减持2%）",
      "热度降温迹象（社交媒体提及量下降15%）"
    ],
    "recommended_action": "立即减仓或离场，不参与追高"
  }
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `timeframe` | ✅ | 必须为 15分钟 或 1小时 |
| `social_heat` | 条件 | 社交媒体热度 |
| `whale_move` | 条件 | 鲸鱼地址动向 |
| `volume_surge` | ✅ | 成交量异常倍数（数值+单位结构：value/unit/display） |
| `exchange_news` | 条件 | 交易所动态（新上线/下架/合约开通） |
| `exchange_news_source` | 条件 | 新闻来源标识（search/user_input） |
| `emotional_indicators` | ✅ | 情绪指标汇总 |
| `classification_logic` | ✅ | 情绪阶段判断逻辑 |
| `dump_risk_detector` | ✅ | 崩盘/出货风险检测 |
| `dump_risk_detector.risk_level` | ✅ | low/medium/high/critical |
| `dump_risk_detector.dump_probability` | ✅ | 崩盘概率（数值+单位结构：value=0-1概率值/unit=probability/display=百分比） |
| `screenshot_quality.trade_usable` | ✅ | Meme币通常≤B级 |
| `screenshot_quality.usable_level` | ✅ | A/B/C |
| `lobster_score.score` | ✅ | Meme币通常≤7分 |
| `observation_plan` | ✅ | 标准化观察计划（仅供参考不做交易决策） |
| `risk_flags` | ✅ | 风险标签数组 |

### Meme币情绪周期（量化边界）

| 阶段 | 量化阈值 | lobster_view | 策略 |
|------|---------|--------------|------|
| **冷却期** | volume_surge < 1.5x 且 social_heat < 20% | 等待启动 | 不介入 |
| **启动期** | volume_surge 1.5-2x 且 social_heat 20-50% | 关注 | 小仓位试多 |
| **狂热期** | volume_surge > 2x 且 social_heat > 50% 且 价格上涨 | 警惕见顶 | 不追高，持仓止盈 |
| **出货期** | volume_surge > 2x 但 价格滞涨/下跌 | 风险极高 | 立即离场 |

---

## 双源融合结构（混合查询）

当用户同时使用搜索和截图（如"BTC现在多少？顺便看看我这张图"），采用**双源融合结构**：

```json
{
  "query_type": "fusion",
  "analysis_source": ["screenshot", "search"],
  "data_fusion": true,
  "fusion_logic": "价格以截图为准（更实时），宏观/链上以搜索为准",
  "server_time": "2026-05-04 08:30:00",
  "timezone": "北京时间 (UTC+8)",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。",
  
  "search_data": {
    "source": "联网搜索聚合",
    "price_range": "$77,800 - $78,200",
    "macro": "ETF近5日净流入 $1.2亿",
    "onchain": "交易所净流出 5000 BTC",
    "freshness_check": {
      "is_fresh": true,
      "search_time": "2026-05-04 08:28:00"
    }
  },
  
  "screenshot_data": {
    "source": "用户截图图像分析",
    "screenshot_price": "$78,146",
    "timeframe": "4小时",
    "trend": "震荡偏多",
    "pattern": "上升三角形",
    "freshness_check": {
      "is_fresh": true,
      "screenshot_time": "2026-05-04 08:25:00"
    },
    "screenshot_quality": {
      "trade_usable": true,
      "usable_level": "A"
    }
  },
  
  "data_conflict_check": {
    "price_diff_pct": {
      "value": 0.58,
      "unit": "%",
      "display": "0.58%"
    },
    "conflict_level": "low",
    "resolution": "以截图价格为准（更实时）",
    "note": "搜索存在1-5分钟延迟"
  },
  
  "fused_output": {
    "symbol": "BTC",
    "final_price": "$78,146",
    "final_price_source": "screenshot",
    "trend": "震荡偏多",
    "macro_context": "ETF持续流入利好",
    "technical_setup": "三角整理末端，等待突破",
    "lobster_view": "偏多",
    "lobster_score": {
      "score": 7.5,
      "grade": "B+"
    },
    "observation_plan": {
      "focus_zone": "$77,800 - $78,200（关注区间）",
      "risk_level_below": "$76,900（跌破需警惕）",
      "upside_targets": ["$80,000（潜在目标位）"]
    },
    "risk_flags": ["key_resistance_nearby"]
  }
}
```

### 数据源优先级

| 数据类型 | 优先来源 | 说明 |
|---------|---------|------|
| **价格** | screenshot | 截图更实时 |
| **技术形态** | screenshot | K线形态、支撑压力 |
| **宏观** | search | ETF、政策、新闻 |
| **链上** | search | 交易所流向、大额转账 |
| **情绪** | search | 社交媒体热度 |
| **时间戳** | screenshot | 截图自带时间 |

---

## 冲突处理机制

### 冲突检测逻辑

```python
def detect_conflict(screenshot_price, search_price_range):
    """检测截图与搜索价格是否存在冲突"""
    search_mid = (search_price_range[0] + search_price_range[1]) / 2
    diff_pct = abs(screenshot_price - search_mid) / search_mid * 100
    
    if diff_pct < 1:
        return {"level": "low", "action": "accept"}
    elif diff_pct < 3:
        return {"level": "medium", "action": "warn"}
    else:
        return {"level": "high", "action": "reject"}
```

### 冲突分级处理

| 偏差 | conflict_level | 处理策略 | 用户提示 |
|------|----------------|---------|---------|
| <1% | low | 接受，以截图为准 | 正常，不提示 |
| 1%-3% | medium | 接受，但提醒用户 | "价格存在轻微偏差，建议核实" |
| >3% | high | 拒绝，要求重新截图 | "⚠️ 数据异常：截图与搜索价格偏差过大，请重新截图或检查交易所" |

### 冲突处理示例（medium级别）

```json
{
  "data_conflict_check": {
    "screenshot_price": "$78,500",
    "search_price_range": "$76,000 - $76,800",
    "price_diff_pct": {
      "value": 2.75,
      "unit": "%",
      "display": "2.75%"
    },
    "conflict_level": "medium",
    "resolution": "接受截图价格，但提醒用户核实",
    "note": "搜索行情存在延迟，截图可能更实时，但建议确认交易所实际价格",
    "user_prompt": "截图显示$78,500，但搜索聚合价为$76,000-$76,800，存在偏差。请以您交易所APP显示价格为准。"
  }
}
```

---

## 复合查询输出格式

当用户一次提及多个币种时，采用**包裹结构**：

```json
{
  "query_type": "multi_coin",
  "server_time": "2026-05-04 08:30:00",
  "timezone": "北京时间 (UTC+8)",
  "delay_note": "多币种批量分析",
  "boundary": "仅信息搜索与截图分析，不支持直接交易",
  "disclaimer": "仅信息整理与技术分析，不构成投资建议。",
  
  "coins": [
    {
      "symbol": "BTC",
      "category": "mainstream",
      "lobster_view": "偏多",
      "lobster_score": {"score": 7.5, "grade": "B+"},
      "observation_plan": {"bias": "long", "focus_zone": "$77,800 - $78,200（关注区间）"}
    },
    {
      "symbol": "USDT",
      "category": "stablecoin",
      "lobster_view": "健康",
      "lobster_score": {"score": 8.5, "grade": "A"}
    }
  ]
}
```

---

## 截图质量与降级处理

### 截图质量分级

```json
{
  "screenshot_quality": {
    "clarity": "clear|blurry|partial",
    "missing_elements": ["volume", "indicators", "timeframe", "price"],
    "confidence": "high|medium|low",
    "trade_usable": true,
    "usable_level": "A|B|C",
    "assessment": "截图质量良好，所有要素清晰可辨"
  }
}
```

### 可用性等级标准

| 等级 | clarity | confidence | trade_usable | 含义 |
|------|---------|-----------|--------------|------|
| **A** | clear | high | ✅ | 可直接给策略 |
| **B** | partial | medium | ✅ | 可参考，需结合搜索 |
| **C** | blurry | low | ❌ | 仅观察，不交易 |

### 降级分析示例

```json
{
  "screenshot_quality": {
    "clarity": "partial",
    "missing_elements": ["volume", "indicators"],
    "confidence": "medium",
    "trade_usable": true,
    "usable_level": "B",
    "assessment": "K线和价格清晰，但成交量和指标区域被截断"
  },
  "lobster_view": "数据不完整，分析仅供参考（B级）",
  "risk_flags": ["incomplete_data", "medium_confidence"]
}
```

---

## 搜索可用性状态

### 正常态
```json
{
  "search_availability": {
    "status": "search_ok",
    "detail": "搜索服务正常",
    "fallback_used": false,
    "affected_fields": []
  }
}
```

### 搜索失败态（错误处理）
```json
{
  "analysis_source": ["screenshot"],
  "search_availability": {
    "status": "search_failed",
    "detail": "搜索服务暂时不可用",
    "fallback_used": false,
    "affected_fields": ["macro", "onchain", "sentiment"]
  },
  "data": {
    "screenshot_price": "$78,146",
    "timeframe": "4小时",
    "trend": "震荡偏多"
  },
  "error": "搜索服务不可用，仅基于截图分析",
  "screenshot_only_mode": true,
  "note": "宏观/链上/情绪数据缺失，分析完整度受限"
}
```

---

## 币种分类判断规则

```python
def classify_coin(symbol_or_name, price=None):
    """
    币种自动分类，price 为截图识别到的价格（可选）
    使用精确匹配避免子串误判（如"busdt"不会被误判为稳定币）
    """
    name_upper = symbol_or_name.upper().strip()
    
    # 稳定币（精确匹配）
    stable_exact = {'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'UST', 'USDD'}
    if name_upper in stable_exact or name_upper in {'稳定币', '稳定'}:
        return 'stable'
    
    # Meme币（精确匹配）
    meme_exact = {'DOGE', 'SHIB', 'PEPE', 'WIF', 'BONK', 'FLOKI', 'MEME', 'DOGECHAIN'}
    if name_upper in meme_exact:
        return 'meme'
    
    # 价格辅助判断
    if price is not None:
        if 0.95 <= price <= 1.05:
            return 'stable'  # 价格≈1，稳定币
        if price < 0.01:
            return 'meme'    # 价格<0.01，Meme币
    
    # 默认主流币
    return 'mainstream'
```

---

## 币种别名完整映射表

| 中文名 | 英文名 | 别名 | 分类 |
|--------|--------|------|------|
| 比特币 | BTC | 大饼、Bitcoin | 主流币 |
| 以太坊 | ETH | 二饼、Ethereum、以太币 | 主流币 |
| 泰达币 | USDT | Tether、U、稳定币 | 稳定币 |
| 美元币 | USDC | USD Coin | 稳定币 |
| 戴 | DAI | MakerDAO、稳定币 | 稳定币 |
| 瑞波币 | XRP | Ripple | 主流币 |
| 索拉纳 | SOL | Solana、太阳币 | 主流币 |
| 币安币 | BNB | Binance Coin | 主流币 |
| 狗狗币 | DOGE | Dogecoin、狗币 | Meme币 |
| 柴犬币 | SHIB | Shiba Inu | Meme币 |
| 佩佩 | PEPE | Pepe Coin | Meme币 |
| 狗帽 | WIF | Dogwifhat | Meme币 |
| 莱特币 | LTC | Litecoin、辣条 | 主流币 |
| 比特现金 | BCH | Bitcoin Cash | 主流币 |
| 阿普托斯 | APT | Aptos | 主流币 |
| 隋 | SUI | Sui | 主流币 |
| 仲裁 | ARB | Arbitrum | 主流币 |

---

## 风险提示模板

### 智能风险标签（risk_flags）

| 标签 | 含义 | 适用场景 |
|------|------|---------|
| `low_risk` | 低风险 | 稳定币正常锚定 |
| `medium_risk` | 中风险 | 主流币震荡期 |
| `high_volatility` | 高波动 | 价格剧烈波动 |
| `critical_depeg` | 严重脱钩 | 稳定币偏离>2% |
| `liquidity_crisis` | 流动性危机 | 大额赎回/抛压 |
| `macro_uncertainty` | 宏观不确定 | 政策/战争/ETF |
| `key_resistance_nearby` | 关键阻力临近 | 价格接近前高 |
| `meme_coin_no_fundamentals` | Meme币无基本面 | 所有Meme币 |
| `dump_risk_high` | 崩盘风险高 | Meme币出货期 |
| `fomo_zone` | FOMO区域 | 狂热期追高 |
| `incomplete_data` | 数据不完整 | 截图质量差 |
| `medium_confidence` | 置信度中等 | 截图部分缺失 |

### 风险提示示例

```json
{
  "risk_flags": ["high_volatility", "macro_uncertainty", "key_resistance_nearby"],
  "risk_summary": "⚠️ 高波动+宏观不确定+关键阻力，建议降低仓位或观望"
}
```

---

## 交易指令拒绝模板

当检测到交易操作意图时，强制拒绝：

```json
{
  "action": "rejected",
  "action_type": "trade_request|withdrawal_request|account_access|leverage_request",
  "reason": "咪呀不支持直接交易/提现/账户操作/杠杆操作",
  "user_message": "咪呀仅提供分析协助，不代操作、不执行交易、不触碰用户账户。如需交易，请使用您自己的交易所APP。",
  "alternative": "请发送截图，我可以基于截图做技术分析",
  "safety_note": "任何索要密码、助记词、要求转账的行为都是诈骗"
}
```

### 触发关键词

| 意图类型 | 触发词 |
|---------|--------|
| **trade_request** | "帮我买", "帮我卖", "下单", "开多", "开空", "平仓" |
| **withdrawal_request** | "提现", "转出", "提币" |
| **account_access** | "密码", "助记词", "私钥", "登录", "帮我操作" |
| **leverage_request** | "加杠杆", "合约", "开100倍" |
