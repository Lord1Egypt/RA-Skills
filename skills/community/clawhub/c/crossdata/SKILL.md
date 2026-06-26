CrossData
---
# CrossData - 多平台数据聚合技能

## 功能描述
整合多个电商及社交媒体平台的数据，提供标准化的竞品分析数据，解决单一平台数据孤岛问题。

## 输入参数
- `keywords`: 搜索关键词（数组），如 `["USB-C fast charger", "Type-C 快充"]`
- `targetMarkets`: 目标市场列表，如 `["Russia", "Brazil", "MiddleEast", "SoutheastAsia", "Europe"]`
- `priceRange`: 价格区间（美元），如 `{"min": 5, "max": 50}`
- `sourcePlatforms`: 数据来源平台，支持 `["aliexpress", "1688", "tiktok", "amazon"]`
- `limit`: 每平台最大返回数量，默认 20

## 输出格式
```json
{
  "productData": [
    {
      "platform": "aliexpress",
      "productName": "65W USB-C Fast Charger",
      "price": 24.99,
      "sales": 2847,
      "rating": 4.8,
      "shipping": "无忧集运"
    }
  ],
  "summary": {
    "totalProducts": 50,
    "avgPrice": 25.17,
    "priceDistribution": {"low": 0.2, "mid": 0.5, "high": 0.3},
    "topMarkets": ["Russia", "Brazil"]
  }
}
```

## 使用示例
```json
{
  "keywords": ["USB-C fast charger", "65W Type-C"],
  "targetMarkets": ["Russia", "Brazil"],
  "priceRange": {"min": 5, "max": 50},
  "sourcePlatforms": ["aliexpress", "1688"],
  "limit": 30
}
```

## 权限说明
- 需要 ClawHub token：`clh_dfYBmWi76_VPBJhUkwRoK8BWpQ4m1IV47bAHieANjVA`
- 访问多个平台的公开数据权限
- 数据聚合与清洗权限

## 备注
- 当前版本需 ClawHub token 激活
- 数据刷新频率为实时
- 输出格式支持 JSON/CSV
