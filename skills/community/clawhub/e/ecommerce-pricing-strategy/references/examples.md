# 示例 - ecommerce-pricing-strategy

> 来源: SKILL.md(ecommerce-pricing-strategy) + 01手册§七(定价策略)

> 电商定价策略生成器的输入输出示例。

## 示例1: 新品定价策略

### 输入
```json
{
  "cost": 30,
  "competitor_prices": "35,40,45,50",
  "platform": "taobao",
  "action": "strategy"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "suggested_price": 42.5,
    "profit_margin": "29.4%",
    "strategy": "竞争导向法(竞品均价42.5)+淘宝搜索权重定价(成本×1.8-3.0=54-90,取竞品均价平衡)+毛利率目标>=30%",
    "promotion_plan": {
      "model": "竞争导向法",
      "competitor_avg": 42.5,
      "cost_plus_price": 48.0,
      "platform_range": "54-90",
      "final_price": 42.5,
      "margin": "29.4%"
    }
  },
  "error": null,
  "code": null
}
```

## 示例2: 大促定价方案

### 输入
```json
{
  "cost": 30,
  "competitor_prices": "35,40,45",
  "platform": "taobao",
  "action": "promotion"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "suggested_price": 42.5,
    "profit_margin": "29.4%",
    "strategy": "大促定价方案",
    "promotion_plan": {
      "original_price": 42.5,
      "discount_rate": 0.7,
      "platform_coupon": "满300减50",
      "store_coupon": "店铺券减10",
      "final_price": 42.5,
      "presale_deposit": 4.25,
      "deposit_doubled": 8.5,
      "price_protection_days": 15
    }
  },
  "error": null,
  "code": null
}
```

## 示例3: 捆绑销售方案

### 输入
```json
{
  "cost": 30,
  "competitor_prices": "35,40",
  "platform": "taobao",
  "action": "bundle"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "suggested_price": 42.5,
    "profit_margin": "29.4%",
    "strategy": "捆绑销售+满减策略",
    "promotion_plan": {
      "bundle_a_plus_b": 0.85,
      "tiered_discount": [
        {"threshold": 99, "discount": 10},
        {"threshold": 199, "discount": 30},
        {"threshold": 299, "discount": 60}
      ],
      "second_half_price": 0.75
    }
  },
  "error": null,
  "code": null
}
```
