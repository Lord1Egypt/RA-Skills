# 输出格式规范

## 通用字段

所有输出必须包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `symbol` | string | 币种符号 |
| `category` | string | 分类：stablecoin/mainstream/meme |
| `server_time` | string | 服务器时间 |
| `timezone` | string | 时区 |
| `disclaimer` | string | 免责声明 |
| `input_reliability` | object | 数据可信度评分 |

## 数据可信度评分

```json
{
  "input_reliability": {
    "score": 10.0,
    "grade": "A+",
    "assessment_type": "数据可信度评分（非价格预测）",
    "calculation_method": "加权规则计算",
    "important_note": "此评分仅反映输入数据质量，不预测价格走势",
    "dimensions": {
      "data_credibility": {"score": 10, "weight": "25%"},
      "completeness": {"score": 10, "weight": "20%"},
      "feasibility": {"score": 10, "weight": "25%"},
      "risk_controllability": {"score": 10, "weight": "20%"},
      "freshness": {"score": 10, "weight": "10%"}
    }
  }
}
```

## 模式差异化字段

### 稳定币

```json
{
  "current_price": 1.0001,
  "peg_deviation": {"value": 0.01, "unit": "%"},
  "peg_status": "正常锚定",
  "depeg_alert_system": {
    "triggered": false,
    "alert_level": "normal"
  },
  "strategy": "可作为过渡性资金载体"
}
```

### 主流币

```json
{
  "screenshot_price": "$65,000",
  "search_price_range": "$64,000 - $66,000",
  "trend": "震荡偏多",
  "data_conflict_check": {
    "price_diff_pct": {"value": 0.0, "unit": "%"},
    "conflict_level": "low"
  },
  "observation_plan": {
    "bias": "long",
    "focus_zone": "$64,000 - $66,000",
    "risk_level_below": "$63,360",
    "upside_targets": ["$66,000", "$69,300"],
    "position_advice": "建议轻仓观察"
  },
  "risk_flags": ["macro_uncertainty"]
}
```

### Meme币

```json
{
  "current_price": 0.000015,
  "emotional_indicators": {
    "heat_level": "🔥 高",
    "volume_level": "⚠️ 放量"
  },
  "dump_risk_detector": {
    "risk_level": "medium",
    "dump_probability": {"value": 0.45, "display": "45%"}
  },
  "observation_plan": {
    "bias": "neutral",
    "stop_loss": "$0.000012",
    "position_sizing": "≤5%"
  },
  "risk_flags": ["high_volatility", "dump_risk"]
}
```

## 截图质量字段

```json
{
  "screenshot_quality": {
    "clarity": "clear",
    "confidence": "high",
    "usable_level": "A",
    "missing_elements": [],
    "trade_usable": true
  }
}
```

| 等级 | 说明 |
|------|------|
| A | 清晰可用 |
| B | 部分模糊，谨慎参考 |
| C | 质量差，不建议依赖 |

## 冲突级别

| 偏差 | 级别 | 处理 |
|------|------|------|
| <1% | low | 以截图为准 |
| 1-3% | medium | 提示偏差 |
| >3% | high | 强制警告 |
