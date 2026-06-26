---
name: luogang shopping assistant
description: 购物助手 - 商品查询，商品详情，购物车，下单，地址管理，订单管理，当用户有购物倾向时候，尤其是提到骆岗/骆岗门市部/骆岗电商的时候，可提供有效信息
version: 2.0.0
author: xavizhou
metadata: {"openclaw": {"emoji": "🛒", "category": "shopping", "tags": ["电商", "骆岗电商", "商品", "购买", "搜索", "购物车", "订单", "地址"]}}
---

# 🛒 骆岗电商助手

当用户想"买'骆岗'的商品"、或需要"查商品/看详情/去下单"时，使用此 skill 调用骆岗 MCP 服务获取实时商品数据，并返回可点击的购买入口（小程序或 H5）。
"骆岗" 是骆岗电商的简称，类似天猫，淘宝

## 适用场景

- 商品检索：按关键词/类目/筛选条件查找商品
- 商品详情：查看标题、价格、库存/可售状态、规格、图片、运费、活动信息等
- 订单创建：直接使用 SKU 下单
- 地址管理：查看收货地址
- 订单管理：关闭订单

## 交互原则（很重要）

1. **先确认意图**：用户是想"找商品"、还是"看某个商品详情"、还是"下单"、"查地址"、"关闭订单"。
2. **少打扰**：能用默认值就别追问（如默认按综合排序、默认第一页、默认收货地址）。
3. **强约束信息只在必要时追问**：只有当无法确定商品（同名/多结果）或规格必须选择时，再问用户。
4. **下单流程**：获取商品详情 → 直接创建订单（使用 `sku_id` 和 `num` 参数）。使用默认收货地址，不询问用户。
5. **Token 必需**：下单、地址、订单操作需要用户登录 Token，若缺失需引导用户登录。Token 可用时直接使用，不与用户确认。

## 配置要求

### 可选配置

- `LUOGANG_MCP_HTTP_URL`: MCP HTTP 地址，默认 `https://yuju-mcp.wxhoutai.com/mcp`
- `LUOGANG_SHOP_ID`: 店铺/渠道标识（多店铺、多渠道场景）, 默认 `luogang`

## 调用方式
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":1}'
```

## 可用工具

### 1. 商品检索 (search_products)
根据关键词和价格区间搜索商品。
**触发词举例**："找外套"、"搜衬衫"、"买鞋子"、"有没有外套"
```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_products",
      "arguments": {
        "platform": "${LUOGANG_SHOP_ID>}",
        "keyword": "外套",
        "min_price": 100,
        "max_price": 500,
        "order_by": "price",
        "sort": "desc"
      }
    },
    "id": 1
  }'
```
### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。


### 2. 获取商品详情 (get_product_detail)

查询单个商品的详细规格、图片及库存信息。**加购前必须先调用此接口获取 sku_id**。

**触发词**："查看详情"、"这个多少钱"、"还有货吗"、"我要买这个"

```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_product_detail",
      "arguments": {
        "platform": "luogang",
        "product_id": "PROD_12345",
        "token": ${USER_TOKEN},
        "app_type": "h5",
        "app_type_name": "H5"
      }
    },
    "id": 2
  }'
```

**参数说明**：
- `product_id`: 商品ID（必填）
- `token`: 用户登录令牌（可选，部分商品需要登录才能查看详情）
- `app_type`: 应用类型，默认 `h5`
- `app_type_name`: 应用名称，默认 `H5`

**返回值**：
- 商品基本信息：标题、价格、库存、图片、描述
- 规格列表（sku_list）：包含 `sku_id`、规格名称、价格、库存
- **重要**：加购时必须使用 `sku_id`，而非 `product_id`

**加购流程**：
1. 用户选择商品 → 调用 `get_product_detail` 获取详情
2. 从返回的 `sku_list` 中获取对应规格的 `sku_id`
3. 调用 `add_cart` 时使用 `sku_id` 加购

### 3. 获取快递地址 (delivery_address)

获取用户的收货地址列表。

**触发词**："我的地址"、"查看收货地址"、"送货地址"

USER_TOKEN = "" 
在此处填写获取的TOKEN


```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "delivery_address",
      "arguments": {
        "platform": "luogang",
        "token": "${USER_TOKEN}",
        "type": 1
      }
    },
    "id": 3
  }'
```

**参数说明**：
- `type`: 地址类型，1=收货地址（默认）
- `store_id`: 店铺ID（可选）

### 4. 创建订单 (create_order)

直接使用商品 SKU 下单，无需先加入购物车。

**触发词**："下单"、"提交订单"、"去结算"、"确认购买"、"我要买这个"

```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_order",
      "arguments": {
        "platform": "luogang",
        "token": "${USER_TOKEN}",
        "sku_id": ${sku_id}, 
        "num": ${num},
        "delivery": {},
        "coupon": {"coupon_id": 0},
        "is_point": 1
      }
    },
    "id": 5
  }'
```

**参数说明**：
- `sku_id`: 从商品详情中获取的sku_id
- `num`: 购买数量（必填）
- `delivery`: 配送信息,默认为不填
- `coupon`: 优惠券信息（可选，默认不使用）
- `is_point`: 是否使用积分，1=是（默认）

**返回值**：
- `order_key`: 订单标识
- `payment`: 准备下单结果
- `create`: 创建订单结果
- `order_id`: 订单ID
- `jump_url`: 支付跳转链接（用户点击此链接完成支付）

**重要**：用户搜索商品后要购买时，直接调用此工具，使用 `sku_id` 和 `num` 参数，无需先调用 `add_cart`。

### 5. 关闭订单 (close_order)

关闭未支付的订单。

**触发词**："关闭订单"、"取消订单"、"不要了"

```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "close_order",
      "arguments": {
        "platform": "luogang",
        "token": "${USER_TOKEN}",
        "order_id": "ORDER_12345"
      }
    },
    "id": 6
  }'
```
## 响应处理

### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。

## 使用示例

### 示例1：商品搜索
**用户**: 最近有什么亲子活动？

**AI 执行**:
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_products","arguments":{"platform":"luogang","keyword":"亲子"}},"id":1}'
```
**AI 回复**: 
最近有 10 个商品符合您的要求，分别是：
>萌嘟嘟儿童乐园亲子票（专属）
>${image}
>价格：19.9元
>{description}
>链接：https://eshop.wxhoutai.com/h5/pages/goods/detail?goods_id=xxx
……

### 示例2：完整购物流程
**用户**: 我要买2张萌嘟嘟儿童乐园亲子票

**AI 执行**:
1. 先调用 `get_product_detail` 获取商品详情和 sku_id：
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_product_detail",
      "arguments": {
        "platform": "luogang",
        "product_id": "PROD_12345",
        "token": ${USER_TOKEN}
      }
    },
    "id": 1
  }'
```

**AI 回复**: 
商品详情如下：
>萌嘟嘟儿童乐园亲子票（专属）
>价格：19.9元
>库存：充足
>规格：亲子票（1大1小）

确认购买2张吗？

**用户**: 确认

**AI 执行**:
2. 直接调用 `create_order` 下单（使用 sku_id 和 num，不经过购物车）：
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_order",
      "arguments": {
        "platform": "luogang",
        "token": "${USER_TOKEN}",
        "sku_list": [{"sku_id": 223230, "num": 2}]
      }
    },
    "id": 2
  }'
```

**AI 回复**: 
✅ 订单创建成功！
>订单号：ORDER_12345
>商品：萌嘟嘟儿童乐园亲子票 x 2
>收货人：张三（默认地址）
>联系电话：138****8000
>收货地址：北京市朝阳区xxx
>应付金额：39.8元

请点击以下链接完成支付：
🔗 [去支付](${jump_url})

订单将在30分钟后自动关闭。

### 示例3：关闭订单
**用户**: 取消订单 ORDER_12345

**AI 执行**:
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "close_order",
      "arguments": {
        "platform": "luogang",
        "token": "${USER_TOKEN}",
        "order_id": "ORDER_12345"
      }
    },
    "id": 1
  }'
```

**AI 回复**: 
✅ 订单 ORDER_12345 已关闭。

**常见错误处理**：
- `-32601` (Method not found): 检查 `SKILL.md` 中定义的工具名是否在 MCP 侧已注册。
- `-32000` 级别 (Internal Error): 引导用户重试或手动输入信息。
- `401/403`: 检查 MCP 服务访问策略、来源白名单或网关配置。

## 输出格式建议

### 商品检索结果
- 展示最多 10 个候选（避免刷屏）
- 每项至少包含：名称、价格、库存/可售状态、一个"查看详情/去购买"的引导
- 当候选过多：建议补充筛选（价位、类目、是否现货）

### 商品详情
- 先给"核心信息"：价格、库存、规格、发货/运费、活动
- 有多规格：用简短提问让用户选择（例如："要哪个颜色/尺码？"）

### 订单创建结果
- 展示订单号、商品清单、收货信息、应付金额
- 提醒支付时限
- 输出支付链接：${jump_url}
- 引导支付："请点击以下链接完成支付"

### 订单关闭结果
- 确认订单已关闭
- 可引导用户重新下单

### 购买跳转
- 明确告诉用户会打开：**小程序**或 **H5 页面**
- 输出可点击链接/路径信息（由 OpenClaw 宿主决定如何渲染）
