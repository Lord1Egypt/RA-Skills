# {{product_name}} - API 设计 PRD

> **文档状态**: {{status|default('草稿')}}  
> **版本**: {{version|default('v0.1')}}  
> **创建日期**: {{created_date}}  
> **最后更新**: {{updated_date}}  
> **作者**: {{author}}  
> **技术负责人**: {{tech_lead|default('待指定')}}  
> **评审人**: {{reviewers|default('待指定')}}

---

## 1. 文档概述

### 1.1 文档目的
本文档定义 {{product_name}} 的 API 接口规范，为前后端开发、第三方集成提供统一的技术契约。

### 1.2 适用范围
- 内部微服务间通信
- 前端与后端交互
- 第三方开发者接入
- 移动端 API 调用

### 1.3 术语与规范

| 术语 | 定义 |
|------|------|
| {{term_1|default('REST')}} | {{def_1|default('Representational State Transfer，表征状态转移')}} |
| {{term_2|default('RPC')}} | {{def_2|default('Remote Procedure Call，远程过程调用')}} |
| {{term_3|default('Idempotency')}} | {{def_3|default('幂等性，同一请求多次执行结果一致')}} |

### 1.4 参考规范
- RESTful API 设计规范: {{rest_spec|default('Google API Design Guide / Microsoft REST API Guidelines')}}
- 数据格式: {{data_format|default('JSON (RFC 8259) / Protocol Buffers (gRPC)')}}
- 认证标准: {{auth_std|default('OAuth 2.0 / JWT (RFC 7519) / API Key')}}

---

## 2. 架构设计

### 2.1 API 架构风格

**选定架构**: {{api_style|default('REST + gRPC 混合')}}

| 场景 | 协议 | 理由 |
|------|------|------|
| {{scene_1|default('外部开放 API')}} | {{proto_1|default('REST/HTTP')}} | {{reason_1|default('通用性强，易于接入')}} |
| {{scene_2|default('内部微服务')}} | {{proto_2|default('gRPC')}} | {{reason_2|default('高性能，强类型')}} |
| {{scene_3|default('实时通信')}} | {{proto_3|default('WebSocket')}} | {{reason_3|default('双向实时推送')}} |

### 2.2 系统架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              客户端层                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Web App    │  │  Mobile App  │  │  第三方应用   │  │  内部服务    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
└─────────┼─────────────────┼─────────────────┼─────────────────┼────────────┘
          │                 │                 │                 │
          └─────────────────┴─────────┬───────┴─────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              网关层 (API Gateway)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   认证鉴权   │  │   限流熔断   │  │   协议转换   │  │   日志监控   │    │
│  │   (Auth)     │  │  (Rate Limit)│  │ (REST/gRPC)  │  │ (Observability)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│    服务 A          │     │    服务 B          │     │    服务 C          │
│  ({{service_a}})   │     │  ({{service_b}})   │     │  ({{service_c}})   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

### 2.3 环境划分

| 环境 | 域名 | 用途 | 稳定性 |
|------|------|------|--------|
| {{env_prod|default('生产')}} | {{domain_prod|default('api.example.com')}} | {{use_prod|default('线上正式服务')}} | {{stab_prod|default('99.99%')}} |
| {{env_staging|default('预发')}} | {{domain_staging|default('api-staging.example.com')}} | {{use_staging|default('上线前验证')}} | {{stab_staging|default('99.9%')}} |
| {{env_test|default('测试')}} | {{domain_test|default('api-test.example.com')}} | {{use_test|default('集成测试')}} | {{stab_test|default('不保证')}} |

---

## 3. 通用规范

### 3.1 通信协议

#### 3.1.1 HTTP/REST 规范
- **协议**: {{http_proto|default('HTTPS only')}}
- **端口**: {{http_port|default('443')}}
- **编码**: {{http_encoding|default('UTF-8')}}
- **内容类型**: {{http_content_type|default('application/json')}}

#### 3.1.2 gRPC 规范
- **协议**: {{grpc_proto|default('HTTP/2 + TLS')}}
- **端口**: {{grpc_port|default('50051')}}
- **序列化**: {{grpc_serialization|default('Protocol Buffers v3')}}

### 3.2 URL 设计

#### 3.2.1 基础 URL 格式
```
{{base_url|default('https://api.example.com/v{version}/{resource}/{action}')}}
```

#### 3.2.2 URL 结构规范

| 组件 | 规范 | 示例 |
|------|------|------|
| 版本号 | {{ver_rule|default('v + 主版本号')}} | {{ver_ex|default('/v1/')}} |
| 资源名 | {{res_rule|default('名词复数，小写，连字符分隔')}} | {{res_ex|default('/user-profiles/')}} |
| 动作 | {{action_rule|default('HTTP 方法表示，避免动词路径')}} | {{action_ex|default('POST /orders (创建订单)'}} |
| 参数 | {{param_rule|default('查询参数使用 camelCase')}} | {{param_ex|default('?pageSize=20&sortBy=name'}} |

### 3.3 HTTP 方法使用

| 方法 | 用途 | 幂等性 | 示例 |
|------|------|--------|------|
| GET | 获取资源 | ✅ | {{get_ex|default('GET /users/123')}} |
| POST | 创建资源 | ❌ | {{post_ex|default('POST /users')}} |
| PUT | 全量更新 | ✅ | {{put_ex|default('PUT /users/123')}} |
| PATCH | 部分更新 | ✅ | {{patch_ex|default('PATCH /users/123')}} |
| DELETE | 删除资源 | ✅ | {{delete_ex|default('DELETE /users/123')}} |

### 3.4 状态码规范

#### 3.4.1 标准 HTTP 状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | {{code_200|default('请求成功')}} |
| 201 | Created | {{code_201|default('资源创建成功')}} |
| 204 | No Content | {{code_204|default('删除成功，无返回体')}} |
| 400 | Bad Request | {{code_400|default('请求参数错误')}} |
| 401 | Unauthorized | {{code_401|default('未认证')}} |
| 403 | Forbidden | {{code_403|default('无权限')}} |
| 404 | Not Found | {{code_404|default('资源不存在')}} |
| 409 | Conflict | {{code_409|default('资源冲突')}} |
| 429 | Too Many Requests | {{code_429|default('请求频率超限')}} |
| 500 | Internal Error | {{code_500|default('服务器内部错误')}} |
| 503 | Service Unavailable | {{code_503|default('服务暂时不可用')}} |

#### 3.4.2 自定义业务码

| 业务码 | 状态码 | 含义 | 说明 |
|--------|--------|------|------|
| {{biz_code_1|default('10001')}} | 400 | {{biz_msg_1|default('参数缺失')}} | {{biz_desc_1|default('必填参数未提供')}} |
| {{biz_code_2|default('10002')}} | 400 | {{biz_msg_2|default('参数格式错误')}} | {{biz_desc_2|default('参数类型或格式不符合要求')}} |
| {{biz_code_3|default('20001')}} | 401 | {{biz_msg_3|default('Token 过期')}} | {{biz_desc_3|default('需要重新登录')}} |
| {{biz_code_4|default('30001')}} | 403 | {{biz_msg_4|default('权限不足')}} | {{biz_desc_4|default('当前用户无此操作权限')}} |

### 3.5 请求/响应格式

#### 3.5.1 请求规范

**请求头 (Headers)**
```json
{
  "Content-Type": "{{req_content_type|default('application/json')}}",
  "Authorization": "{{req_auth|default('Bearer {access_token}')}}",
  "X-Request-ID": "{{req_id|default('{uuid}')}}",
  "X-Idempotency-Key": "{{req_idem|default('{uuid} 用于幂等控制')}}"
}
```

**请求体 (Body)**
```json
{
  "fieldName": "value",
  "nestedObject": {
    "subField": "value"
  },
  "arrayField": ["item1", "item2"]
}
```

#### 3.5.2 响应规范

**成功响应**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "12345",
    "name": "example"
  },
  "requestId": "req-uuid-123",
  "timestamp": "2026-04-19T17:16:00Z"
}
```

**错误响应**
```json
{
  "code": {{err_code|default('10001')}},
  "message": "{{err_msg|default('参数错误')}}",
  "details": {
    "field": "username",
    "issue": "cannot be empty"
  },
  "requestId": "req-uuid-123",
  "timestamp": "2026-04-19T17:16:00Z"
}
```

#### 3.5.3 分页响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {"id": "1", "name": "item1"},
      {"id": "2", "name": "item2"}
    ],
    "pagination": {
      "page": {{page|default('1')}},
      "pageSize": {{page_size|default('20')}},
      "total": {{total|default('100')}},
      "totalPages": {{total_pages|default('5')}},
      "hasNext": {{has_next|default('true')}},
      "hasPrev": {{has_prev|default('false')}}
    }
  }
}
```

### 3.6 认证与授权

#### 3.6.1 认证方式

| 方式 | 适用场景 | 说明 |
|------|----------|------|
| {{auth_type_1|default('OAuth 2.0')}} | {{auth_scene_1|default('第三方应用接入')}} | {{auth_desc_1|default('标准 OAuth 流程，支持 Authorization Code 模式')}} |
| {{auth_type_2|default('JWT')}} | {{auth_scene_2|default('内部服务/前端应用')}} | {{auth_desc_2|default('Access Token + Refresh Token 机制')}} |
| {{auth_type_3|default('API Key')}} | {{auth_scene_3|default('服务器间调用')}} | {{auth_desc_3|default('Header 中携带 X-API-Key')}} |

#### 3.6.2 JWT Token 规范

**Token 结构**
```json
// Header
{
  "alg": "{{jwt_alg|default('RS256')}}",
  "typ": "JWT"
}

// Payload
{
  "iss": "{{jwt_iss|default('api.example.com')}}",
  "sub": "{{jwt_sub|default('user_id')}}",
  "aud": "{{jwt_aud|default('app_name')}}",
  "exp": {{jwt_exp|default('过期时间戳')}},
  "iat": {{jwt_iat|default('签发时间戳')}},
  "jti": "{{jwt_jti|default('唯一标识')}}",
  "scope": "{{jwt_scope|default('read write')}}"
}
```

**Token 有效期**
- Access Token: {{access_token_ttl|default('2 小时')}}
- Refresh Token: {{refresh_token_ttl|default('7 天')}}

### 3.7 限流与熔断

#### 3.7.1 限流策略

| 维度 | 限制 | 说明 |
|------|------|------|
| {{limit_dim_1|default('全局 QPS')}} | {{limit_val_1|default('10000/s')}} | {{limit_desc_1|default('整个 API 集群总限流')}} |
| {{limit_dim_2|default('单 IP')}} | {{limit_val_2|default('100/min')}} | {{limit_desc_2|default('防止单 IP 攻击')}} |
| {{limit_dim_3|default('单用户')}} | {{limit_val_3|default('1000/min')}} | {{limit_desc_3|default('按用户 ID 限流')}} |
| {{limit_dim_4|default('单 API')}} | {{limit_val_4|default('按接口配置')}} | {{limit_desc_4|default('不同接口不同阈值')}} |

#### 3.7.2 限流响应

```json
{
  "code": 429,
  "message": "Rate limit exceeded",
  "details": {
    "limit": 100,
    "remaining": 0,
    "resetTime": "2026-04-19T17:17:00Z"
  }
}
```

---

## 4. 接口定义

### 4.1 资源列表

| 资源名 | 路径 | 描述 | 所属服务 |
|--------|------|------|----------|
| {{res_1|default('用户')}} | {{res_1_path|default('/users')}} | {{res_1_desc|default('用户管理')}} | {{res_1_svc|default('user-service')}} |
| {{res_2|default('订单')}} | {{res_2_path|default('/orders')}} | {{res_2_desc|default('订单管理')}} | {{res_2_svc|default('order-service')}} |
| {{res_3|default('商品')}} | {{res_3_path|default('/products')}} | {{res_3_desc|default('商品管理')}} | {{res_3_svc|default('product-service')}} |

### 4.2 用户模块 API

#### 4.2.1 创建用户

**接口信息**
- **方法**: POST
- **路径**: `/v1/users`
- **描述**: {{create_user_desc|default('创建新用户')}}
- **幂等性**: ✅ (通过 X-Idempotency-Key)

**请求参数**

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| username | string | ✅ | {{field_username|default('用户名，3-20字符')}} | "john_doe" |
| email | string | ✅ | {{field_email|default('邮箱地址')}} | "john@example.com" |
| phone | string | ❌ | {{field_phone|default('手机号')}} | "+86-13800138000" |
| password | string | ✅ | {{field_password|default('密码，8-32字符')}} | "***" |
| profile | object | ❌ | {{field_profile|default('用户资料')}} | {...} |

**请求示例**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+86-13800138000",
  "password": "SecurePass123!",
  "profile": {
    "nickname": "John",
    "avatar": "https://cdn.example.com/avatar.jpg",
    "bio": "Hello world"
  }
}
```

**响应示例**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "usr_123456789",
    "username": "john_doe",
    "email": "john@example.com",
    "status": "active",
    "createdAt": "2026-04-19T17:16:00Z",
    "updatedAt": "2026-04-19T17:16:00Z"
  }
}
```

**错误码**

| 错误码 | 说明 |
|--------|------|
| {{err_1|default('10001')}} | {{err_1_desc|default('用户名已存在')}} |
| {{err_2|default('10002')}} | {{err_2_desc|default('邮箱格式错误')}} |
| {{err_3|default('10003')}} | {{err_3_desc|default('密码强度不足')}} |

#### 4.2.2 获取用户详情

**接口信息**
- **方法**: GET
- **路径**: `/v1/users/{userId}`
- **描述**: {{get_user_desc|default('获取指定用户详细信息')}}

**路径参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | string | ✅ | {{path_user_id|default('用户唯一标识')}} |

**查询参数**

| 字段 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| include | string | ❌ | {{query_include|default('附加字段，逗号分隔')}} | - |

**响应示例**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "usr_123456789",
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "+86-13800138000",
    "status": "active",
    "profile": {
      "nickname": "John",
      "avatar": "https://cdn.example.com/avatar.jpg",
      "bio": "Hello world"
    },
    "stats": {
      "orderCount": 42,
      "totalSpent": 12580.50
    },
    "createdAt": "2026-01-15T08:30:00Z",
    "updatedAt": "2026-04-19T17:16:00Z"
  }
}
```

#### 4.2.3 更新用户

**接口信息**
- **方法**: PATCH
- **路径**: `/v1/users/{userId}`
- **描述**: {{update_user_desc|default('部分更新用户信息')}}

**请求示例**
```json
{
  "profile": {
    "nickname": "Johnny",
    "bio": "Updated bio"
  }
}
```

#### 4.2.4 删除用户

**接口信息**
- **方法**: DELETE
- **路径**: `/v1/users/{userId}`
- **描述**: {{delete_user_desc|default('删除用户（软删除）')}}

### 4.3 订单模块 API

#### 4.3.1 创建订单

**接口信息**
- **方法**: POST
- **路径**: `/v1/orders`
- **描述**: {{create_order_desc|default('创建新订单')}}

**请求参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| items | array | ✅ | {{field_items|default('订单商品列表')}} |
| items[].productId | string | ✅ | {{field_product_id|default('商品ID')}} |
| items[].quantity | integer | ✅ | {{field_quantity|default('数量，最小1')}} |
| items[].skuId | string | ❌ | {{field_sku_id|default('SKU ID')}} |
| shippingAddress | object | ✅ | {{field_shipping|default('收货地址')}} |
| paymentMethod | string | ✅ | {{field_payment|default('支付方式')}} |
| couponCode | string | ❌ | {{field_coupon|default('优惠券码')}} |

**请求示例**
```json
{
  "items": [
    {
      "productId": "prod_123",
      "skuId": "sku_456",
      "quantity": 2
    }
  ],
  "shippingAddress": {
    "name": "John Doe",
    "phone": "+86-13800138000",
    "province": "北京市",
    "city": "北京市",
    "district": "朝阳区",
    "address": "xx街道xx号",
    "zipCode": "100000"
  },
  "paymentMethod": "alipay",
  "couponCode": "SAVE20"
}
```

**响应示例**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "orderId": "ord_789012345",
    "status": "pending_payment",
    "totalAmount": 1999.00,
    "discountAmount": 200.00,
    "payableAmount": 1799.00,
    "currency": "CNY",
    "createdAt": "2026-04-19T17:16:00Z",
    "expireAt": "2026-04-19T17:46:00Z",
    "paymentUrl": "https://pay.example.com/ord_789012345"
  }
}
```

#### 4.3.2 查询订单列表

**接口信息**
- **方法**: GET
- **路径**: `/v1/orders`
- **描述**: {{list_orders_desc|default('分页查询用户订单列表')}}

**查询参数**

| 字段 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| status | string | ❌ | {{query_status|default('订单状态过滤')}} | all |
| startDate | string | ❌ | {{query_start|default('开始日期 (ISO 8601)')}} | - |
| endDate | string | ❌ | {{query_end|default('结束日期 (ISO 8601)')}} | - |
| page | integer | ❌ | {{query_page|default('页码，从1开始')}} | 1 |
| pageSize | integer | ❌ | {{query_page_size|default('每页数量，最大100')}} | 20 |
| sortBy | string | ❌ | {{query_sort|default('排序字段')}} | createdAt |
| sortOrder | string | ❌ | {{query_order|default('排序方向: asc/desc')}} | desc |

### 4.4 WebSocket 实时接口 (如适用)

#### 4.4.1 连接建立
- **URL**: `wss://{{ws_url|default('ws.example.com/v1/realtime')}}`
- **认证**: {{ws_auth|default('连接时通过 query param 携带 token')}} 

#### 4.4.2 消息格式
```json
{
  "type": "{{msg_type|default('event_type')}}",
  "timestamp": "2026-04-19T17:16:00Z",
  "payload": {
    // 消息内容
  }
}
```

#### 4.4.3 事件类型

| 事件类型 | 方向 | 说明 |
|----------|------|------|
| {{event_type_1|default('order.update')}} | Server → Client | {{event_desc_1|default('订单状态变更通知')}} |
| {{event_type_2|default('message.new')}} | Server → Client | {{event_desc_2|default('新消息通知')}} |
| {{event_type_3|default('ping')}} | Client → Server | {{event_desc_3|default('心跳检测')}} |

---

## 5. 错误处理

### 5.1 错误分类

| 类别 | 说明 | 处理建议 |
|------|------|----------|
| {{err_cat_1|default('客户端错误 (4xx)')}} | {{err_cat_1_desc|default('请求参数或权限问题')}} | {{err_cat_1_handle|default('检查请求参数，修正后重试')}} |
| {{err_cat_2|default('服务端错误 (5xx)')}} | {{err_cat_2_desc|default('服务器内部错误')}} | {{err_cat_2_handle|default('记录错误，稍后重试，联系支持')}} |
| {{err_cat_3|default('网络错误')}} | {{err_cat_3_desc|default('连接超时或中断')}} | {{err_cat_3_handle|default('检查网络，指数退避重试')}} |

### 5.2 重试策略

| 错误码 | 可重试 | 重试策略 |
|--------|--------|----------|
| 429 | ✅ | {{retry_429|default('等待 Retry-After 时间后重试')}} |
| 500 | ✅ | {{retry_500|default('指数退避，最多3次')}} |
| 502/503 | ✅ | {{retry_503|default('立即重试，最多5次')}} |
| 400/401/403/404 | ❌ | {{retry_4xx|default('不重试，修正请求')}} |

### 5.3 错误日志规范

所有错误响应应包含 `requestId`，用于问题追踪：
```
请求失败: {message}
Request ID: {requestId}
时间: {timestamp}
```

---

## 6. 版本管理

### 6.1 版本策略

| 版本类型 | 说明 | 兼容性 |
|----------|------|--------|
| {{ver_type_1|default('Major (v1 → v2)')}} | {{ver_type_1_desc|default('不兼容变更')}} | {{ver_compat_1|default('不兼容')}} |
| {{ver_type_2|default('Minor (v1.1 → v1.2)')}} | {{ver_type_2_desc|default('新增功能，向下兼容')}} | {{ver_compat_2|default('兼容')}} |
| {{ver_type_3|default('Patch (v1.1.1 → v1.1.2)')}} | {{ver_type_3_desc|default('Bug 修复')}} | {{ver_compat_3|default('兼容')}} |

### 6.2 版本兼容性

- 新版本发布时，旧版本保持可用至少 {{version_ttl|default('6 个月')}}
- 废弃 API 提前 {{deprecation_notice|default('3 个月')}} 通知
- 通过 `X-API-Version` 或 URL 路径指定版本

### 6.3 变更日志

| 版本 | 日期 | 变更内容 | 兼容性 |
|------|------|----------|--------|
| {{api_ver_1|default('v1.0.0')}} | {{api_date_1|default('2026-04-01')}} | {{api_change_1|default('初始版本')}} | {{api_compat_1|default('-')}} |
| {{api_ver_2|default('v1.1.0')}} | {{api_date_2|default('2026-04-15')}} | {{api_change_2|default('新增订单批量查询')}} | {{api_compat_2|default('兼容')}} |

---

## 7. SDK 与工具

### 7.1 官方 SDK

| 语言 | 包名 | 版本 | 安装命令 |
|------|------|------|----------|
| {{sdk_lang_1|default('JavaScript')}} | {{sdk_pkg_1|default('@example/api-sdk')}} | {{sdk_ver_1|default('^1.0.0')}} | {{sdk_install_1|default('npm install @example/api-sdk')}} |
| {{sdk_lang_2|default('Python')}} | {{sdk_pkg_2|default('example-api-sdk')}} | {{sdk_ver_2|default('^1.0.0')}} | {{sdk_install_2|default('pip install example-api-sdk')}} |
| {{sdk_lang_3|default('Go')}} | {{sdk_pkg_3|default('github.com/example/api-sdk-go')}} | {{sdk_ver_3|default('v1.0.0')}} | {{sdk_install_3|default('go get github.com/example/api-sdk-go')}} |

### 7.2 SDK 使用示例

**JavaScript**
```javascript
import { ExampleClient } from '@example/api-sdk';

const client = new ExampleClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.example.com/v1'
});

const user = await client.users.create({
  username: 'john_doe',
  email: 'john@example.com'
});
```

**Python**
```python
from example_api_sdk import ExampleClient

client = ExampleClient(api_key='your-api-key')

user = client.users.create(
    username='john_doe',
    email='john@example.com'
)
```

---

## 8. 附录

### 8.1 OpenAPI 规范
完整 OpenAPI/Swagger 文档: {{openapi_url|default('https://api.example.com/docs/openapi.json')}}

### 8.2 Postman 集合
Postman Collection: {{postman_url|default('https://api.example.com/docs/postman.json')}}

### 8.3 参考文档
- {{api_ref_1|default('[OAuth 2.0 授权流程](链接)')}} - {{api_ref_1_desc|default('第三方接入指南')}}
- {{api_ref_2|default('[Webhook 配置说明](链接)')}} - {{api_ref_2_desc|default('事件订阅文档')}}
- {{api_ref_3|default('[错误码速查表](链接)')}} - {{api_ref_3_desc|default('完整错误码列表')}}

### 8.4 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| {{version|default('v0.1')}} | {{created_date}} | 初稿创建 | {{author}} |

---

## 9. 评审记录

| 评审轮次 | 日期 | 评审人 | 结论 | 备注 |
|----------|------|--------|------|------|
| 技术评审 | {{tech_review_date|default('-')}} | {{tech_reviewer|default('-')}} | {{tech_result|default('待评审')}} | {{tech_note|default('-')}} |
| 架构评审 | {{arch_review_date|default('-')}} | {{arch_reviewer|default('-')}} | {{arch_result|default('待评审')}} | {{arch_note|default('-')}} |
