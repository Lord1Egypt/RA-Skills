# 蛋叔商城 API 接口文档

## 协议信息

- **端点**：`POST https://www.dangaoss.com/dsapi/workbuddy/mcp_server`
- **协议**：JSON-RPC 2.0
- **请求格式**：`{"jsonrpc":"2.0","method":"tools/call","params":{"name":"接口名","arguments":{参数对象}},"id":1}`
- **返回格式**：`{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"{业务JSON}"}]}}`
- **业务JSON**：`{"code":200,"data":...,"msg":"..."}`
- **成功状态码**：`code: 200`

---

## 接口列表

### 1. getAddrList — 获取地址列表

**用途**：获取用户在指定城市已保存的收货地址

**arguments 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_token` | string | 是 | 用户 token |
| `city_name` | string | 是 | 城市名（规范到市一级，如"深圳市"） |

**curl 示例**：
```bash
curl -s -X POST "https://www.dangaoss.com/dsapi/workbuddy/mcp_server" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"getAddrList","arguments":{"user_token":"TOKEN","city_name":"北京市"}},"id":1}'
```

**返回值**：
```json
{"code":200,"msg":"获取成功","data":[{"id":"10806796","name":"dd","province":"北京市","city":"北京市","area":"海淀区","addr":"嘉豪国际中心-C座"}]}
```

> 地址 `id` 在后续接口中以 `aid` 参数名传入。

---

### 2. addAddrList — 添加地址

**用途**：添加新的收货地址

**arguments 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_token` | string | 是 | 用户 token |
| `province` | string | 是 | 省份（如"广东省"） |
| `city` | string | 是 | 城市（规范到市一级） |
| `area` | string | 是 | 区县（字段名是 `area`，不是 `district`） |
| `addr` | string | 是 | 详细地址（字段名是 `addr`，不是 `detail`） |
| `name` | string | 是 | 收货人姓名 |
| `phone` | string | 是 | 11位手机号（1[3-9]开头） |

**curl 示例**：
```bash
curl -s -X POST "https://www.dangaoss.com/dsapi/workbuddy/mcp_server" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"addAddrList","arguments":{"user_token":"TOKEN","province":"北京市","city":"北京市","area":"海淀区","addr":"嘉豪国际中心-C座","name":"dd","phone":"13800138000"}},"id":1}'
```

**返回值**：
```json
{"code":200,"msg":"添加成功","data":[{"id":"13","name":"dd","province":"北京市","city":"北京市","area":"海淀区","addr":"嘉豪国际中心-C座"}]}
```

> 取 `data[0].id` 作为后续接口的 `aid` 使用。

---

### 3. sweets_lst — 商品搜索

**用途**：根据地址 ID 和关键词搜索可配送商品

**arguments 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_token` | string | 是 | 用户 token |
| `aid` | string/int | 是 | 地址 ID（用于确定配送城市范围） |
| `keyword` | string | 是 | 搜索关键词 |
| `page` | int | 否 | 页码，默认 1 |

**curl 示例**：
```bash
curl -s -X POST "https://www.dangaoss.com/dsapi/workbuddy/mcp_server" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"sweets_lst","arguments":{"user_token":"TOKEN","aid":"10806796","keyword":"蛋糕","page":1}},"id":1}'
```

**返回值**：
```json
{"code":200,"msg":"获取成功","data":[{"规格ID":1,"商品名称":"草莓奶油蛋糕","规格价格":19900,"规格名称":"6寸","规格描述":"2-3人吃"}]}
```

> 价格单位为**分**，展示时除以 100。`规格ID` 即为 `spec_id`。

---

### 4. getOrderaddr — 生成下单链接

**用途**：根据商品规格和地址生成下单链接

**arguments 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_token` | string | 是 | 用户 token |
| `aid` | string/int | 是 | 地址 ID（字段名是 `aid`，不是 `addr_id`） |
| `spec_id` | string/int | 是 | 商品规格 ID |
| `city_name` | string | 是 | 城市名（规范到市一级） |

**curl 示例**：
```bash
curl -s -X POST "https://www.dangaoss.com/dsapi/workbuddy/mcp_server" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"getOrderaddr","arguments":{"user_token":"TOKEN","aid":"10806796","spec_id":"1","city_name":"北京市"}},"id":1}'
```

**返回值**：
```json
{"code":200,"msg":"下单url获取成功","data":"https://www.dangaoss.com/web/wb_order.html?scene=112"}
```

> `data` 字段直接是 URL 字符串（不是对象），可直接展示给用户。URL 中的 `scene` 参数用于后续订单查询。

---

### 5. getOrderStatus — 订单状态查询

**用途**：根据 scene 查询订单状态

**arguments 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_token` | string | 是 | 用户 token |
| `scene` | string | 是 | 下单链接中的 scene 参数（如 `3881514438313`） |

**curl 示例**：
```bash
curl -s -X POST "https://www.dangaoss.com/dsapi/workbuddy/mcp_server" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"getOrderStatus","arguments":{"user_token":"TOKEN","scene":"3881514438313"}},"id":1}'
```

**返回值**：
```json
{"code":200,"msg":"获取成功","data":{"scene":"3881514438313","status_name":"订单未支付"}}
```

> 返回 `scene` 和 `status_name` 字段，需展示给用户。

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 401 | 缺少规格（getOrderaddr） |
| 402 | 缺少配送地址（getOrderaddr） |
| 403 | 规格不存在或已下架（getOrderaddr） |
| 405 | 商品暂时无法配送（getOrderaddr） |
| 4013 | 缺少授权信息（getOrderaddr） |
| 4024 | 缺少城市名称（getAddrList/getOrderaddr） |
| 4026 | 城市未开通 / 缺少必填字段 |

---

## 参数快速对照（易错点）

| 概念 | 正确字段名 | 错误写法 |
|------|-----------|---------|
| 区县 | `area` | ~~`district`~~ |
| 详细地址 | `addr` | ~~`detail`~~ |
| 地址 ID | `aid` | ~~`addr_id`~~ |
| 成功状态码 | `200` | ~~`0`~~ |
| 下单返回 URL | `data`（字符串） | ~~`data.order_url`~~ |
