# 示例

## 示例1：BTC 主流币分析

**输入**：
```bash
python scripts/crypto_advisor.py analyze \
  --symbol BTC \
  --screenshot-price 65000 \
  --search-min 64000 \
  --search-max 66000
```

**输出（JSON）**：
```json
{
  "symbol": "BTC",
  "category": "mainstream",
  "screenshot_price": "$65,000",
  "search_price_range": "$64,000 - $66,000",
  "trend": "震荡偏多",
  "data_conflict_check": {
    "price_diff_pct": {"value": 0.0, "unit": "%"},
    "conflict_level": "low"
  },
  "input_reliability": {
    "score": 10.0,
    "grade": "A+",
    "assessment_type": "数据可信度评分（非价格预测）"
  },
  "observation_plan": {
    "bias": "long",
    "focus_zone": "$64,000 - $66,000",
    "risk_level_below": "$63,360",
    "upside_targets": ["$66,000", "$69,300"],
    "position_advice": "建议轻仓观察，等待放量突破后加仓"
  },
  "risk_flags": ["macro_uncertainty"]
}
```

---

## 示例2：USDT 稳定币分析

**输入**：
```bash
python scripts/crypto_advisor.py analyze --symbol USDT --search-min 0.999 --search-max 1.001
```

**输出（JSON）**：
```json
{
  "symbol": "USDT",
  "category": "stablecoin",
  "current_price": 1.0001,
  "peg_deviation": {"value": 0.01, "unit": "%"},
  "peg_status": "正常锚定",
  "depeg_alert_system": {
    "triggered": false,
    "alert_level": "normal"
  },
  "input_reliability": {
    "score": 8.5,
    "grade": "A"
  },
  "strategy": "可作为过渡性资金载体"
}
```

---

## 示例3：PEPE Meme 币分析

**输入**：
```bash
python scripts/crypto_advisor.py analyze \
  --symbol PEPE \
  --search-min 0.000014 \
  --search-max 0.000016
```

**输出（JSON）**：
```json
{
  "symbol": "PEPE",
  "category": "meme",
  "current_price": 0.000015,
  "dump_risk_detector": {
    "risk_level": "high",
    "dump_probability": {"value": 0.65, "display": "65%"}
  },
  "input_reliability": {
    "score": 5.1,
    "grade": "C+",
    "important_note": "Meme币高波动，谨慎参考"
  },
  "risk_flags": ["high_volatility", "dump_risk"]
}
```

---

## 示例4：价格冲突警告

**场景**：截图 $70,000 vs 搜索 $67,000（偏差 4.3%）

**输入**：
```bash
python scripts/crypto_advisor.py conflict \
  --screenshot-price 70000 \
  --search-min 67000 \
  --search-max 67500
```

**输出（JSON）**：
```json
{
  "data_conflict_check": {
    "price_diff_pct": {"value": 4.3, "unit": "%"},
    "conflict_level": "high",
    "resolution": "价格偏差超过3%，建议核实数据源",
    "note": "截图 $70,000 vs 搜索 $67,000"
  },
  "input_reliability": {
    "score": 6.2,
    "grade": "B",
    "calculation_details": ["价格冲突HIGH，可信度扣3分"]
  }
}
```

---

## 示例5：币种分类

```bash
# 主流币
python scripts/crypto_advisor.py classify --symbol BTC
# {"symbol": "BTC", "category": "mainstream", "type_cn": "主流币"}

# Meme 币
python scripts/crypto_advisor.py classify --symbol DOGE
# {"symbol": "DOGE", "category": "meme", "type_cn": "Meme币"}

# 稳定币
python scripts/crypto_advisor.py classify --symbol USDT
# {"symbol": "USDT", "category": "stable", "type_cn": "稳定币"}

# 未知币种（默认归为山寨币）
python scripts/crypto_advisor.py classify --symbol XYZ
# {"symbol": "XYZ", "category": "altcoin", "type_cn": "山寨币/概念币"}
```
