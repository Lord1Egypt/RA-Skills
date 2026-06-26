# AliMerce MCP Tools

OpenClaw AI 助手调用 AliMerce 商城后台的 MCP 工具集。

## 工具列表

### Product Tools

#### `product_create`
创建商品。

**必填参数：** `title` (JSON), `slug`, `price`, `category`

**可选：** `description` (JSON), `inventory`, `status`

**示例：**
```
product_create --title='{"zh":"T恤","en":"T-Shirt"}' --slug=t-shirt-001 --price=99 --category=cat_xxx
```

#### `product_list`
列出商品。

**可选：** `status`, `category`, `limit`, `page`

#### `product_get`
获取商品详情。

**必填：** `id`

#### `product_update`
更新商品。

**必填：** `id`
**可选：** `title`, `price`, `inventory`, `status`

#### `product_delete`
删除商品（高风险，需审核）。

**必填：** `id`

---

### User Tools

#### `user_list`
列出用户。

**可选：** `role`, `limit`, `page`

#### `user_get`
获取用户详情。

**必填：** `id`

#### `user_update`
更新用户。

**必填：** `id`
**可选：** `name`, `role`

---

### Order Tools

#### `order_list`
列出订单。

**可选：** `status`, `customer`, `limit`, `page`

#### `order_get`
获取订单详情。

**必填：** `id`

#### `order_update`
更新订单（高风险操作需审核）。

**必填：** `id`
**可选：** `status` (pending|processing|shipped|delivered)

---

### Customer Memory Tools

#### `customer_preferences_get`
获取客户偏好。

**必填：** `customerId`

#### `customer_preferences_update`
更新客户偏好。

**必填：** `customerId`, `preferences` (object)

---

## 高风险操作

以下操作需要人工审核后才能执行：
- `product_delete`
- `order_update` (status → shipped/delivered)
- `user_update` (role → admin)

审核结果通过飞书/邮件通知管理员。

## 认证

通过环境变量配置：
- `ALIMERCE_API_TOKEN` — API 认证 Token
- `ALIMERCE_API_URL` — API 地址（默认 http://localhost:3000/api）
