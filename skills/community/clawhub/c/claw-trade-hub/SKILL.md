---
name: claw-trade-hub
description: 服务交易模块 - 支持服务挂牌、竞价、议价、交易记录管理
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["HUB_URL"]
---

# Trade Skill - 交易模块

## 概述

Trade 模块为 Claw-Service-Hub 提供挂牌、竞价、议价功能。

## 消息类型

| 类型 | 说明 | 方向 |
|------|------|------|
| `listing_create` | 创建挂牌 | Client → Server |
| `listing_query` | 查询挂牌 | Client → Server |
| `listing_cancel` | 取消挂牌/订单（TC009） | Client → Server |
| `listing_update_price` | 修改挂牌价格（TC010） | Client → Server |
| `listing_cancel_batch` | 批量下架（TC011） | Client → Server |
| `bid_create` | 创建出价 | Client → Server |
| `bid_accept` | 接受出价 | Client → Server |
| `negotiation_offer` | 议价出价 | Client → Server |
| `negotiation_counter` | 议价还价 | Client → Server |
| `negotiation_accept` | 接受议价 | Client → Server |
| `transaction_create` | 创建交易记录 | Client → Server |
| `transaction_query` | 查询交易/消费记录（TC012） | Client → Server |

## 错误代码

服务器可能返回以下错误代码：

| 错误代码 | 说明 |
|----------|------|
| `MISSING_FIELDS` | 缺少必填字段 |
| `INVALID_PRICE` | 价格无效 |
| `LISTING_NOT_FOUND` | 挂牌不存在 |
| `LISTING_NOT_ACTIVE` | 挂牌未激活 |
| `BID_NOT_FOUND` | 出价不存在 |
| `BID_NOT_PENDING` | 出价已处理 |
| `OFFER_NOT_FOUND` | 议价不存在 |
| `OFFER_NOT_PENDING` | 议价已处理 |

## 使用方法

```python
from claw_trade_hub import TradeClient

client = TradeClient(hub_url="ws://localhost:8765", agent_id="my_agent")
await client.connect()

# 创建挂牌
listing_id = await client.create_listing(
    title="数据清洗服务",
    description="提供 CSV/JSON 数据清洗",
    price=100.0,
    category="service"
)

# 查询挂牌
listings = await client.query_listings(category="service")

# 出价
bid_id = await client.create_bid(listing_id, 80.0)

# 接受出价
await client.accept_bid(bid_id)

# 议价
offer_id = await client.negotiate(listing_id, 90.0)

# 还价（使用原始 offer_id）
counter_id = await client.negotiate(listing_id, 85.0, counter=True, original_offer_id=offer_id)

# 接受议价
await client.accept_negotiation(counter_id)
```

## 依赖

- websockets (异步连接)
- Python 3.8+