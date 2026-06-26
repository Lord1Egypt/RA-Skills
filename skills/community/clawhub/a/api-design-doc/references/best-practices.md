# API设计最佳实践

本文档提供了API设计的最佳实践指南，帮助开发者设计出高质量、易用、可维护的API接口。

## RESTful设计原则

### 资源导向

API应该围绕资源进行设计，每个资源都有唯一的标识符。

```
✅ 正确：
GET /api/users/{id}
POST /api/users
PUT /api/users/{id}
DELETE /api/users/{id}

❌ 错误：
GET /api/getUserById
POST /api/createUser
PUT /api/updateUser
DELETE /api/deleteUser
```

### 使用正确的HTTP方法

- `GET` - 获取资源（幂等）
- `POST` - 创建资源
- `PUT` - 完整更新资源（幂等）
- `PATCH` - 部分更新资源
- `DELETE` - 删除资源（幂等）

### 状态码使用

- `200 OK` - 请求成功
- `201 Created` - 资源创建成功
- `204 No Content` - 请求成功但无返回内容（如DELETE）
- `400 Bad Request` - 请求参数错误
- `401 Unauthorized` - 未认证
- `403 Forbidden` - 无权限
- `404 Not Found` - 资源不存在
- `500 Internal Server Error` - 服务器内部错误

## 请求设计

### 统一的请求格式

所有POST/PUT/PATCH请求使用JSON格式：

```json
{
  "userName": "test",
  "userAge": 25,
  "isActive": true
}
```

### 分页参数

使用标准的分页参数：

```
GET /api/users?page_num=1&page_size=10
```

响应格式：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [...],
    "total": 100,
    "pageNum": 1,
    "pageSize": 10
  }
}
```

### 排序参数

```
GET /api/users?sort_by=create_time&sort_order=desc
```

### 过滤参数

```
GET /api/users?status=active&age_gt=18
```

## 响应设计

### 统一的响应格式

所有接口使用统一的响应格式：

```json
{
  "code": 0,
  "message": "success",
  "data": {...}
}
```

- `code`: 状态码（0表示成功，非0表示失败）
- `message`: 响应消息
- `data`: 响应数据（成功时返回业务数据，失败时为null）

### 错误响应

```json
{
  "code": 20101,
  "message": "参数缺失",
  "data": null
}
```

### 时间格式

使用ISO 8601格式：

```json
{
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T12:00:00Z"
}
```

## 安全性

### 认证

使用Token进行认证：

```
Authorization: Bearer {token}
```

### HTTPS

所有API必须使用HTTPS协议。

### 输入验证

对所有输入参数进行验证，防止SQL注入、XSS等攻击。

### 敏感信息

不要在响应中返回敏感信息（如密码、Token等）。

## 性能优化

### 数据量控制

- 使用分页避免返回大量数据
- 只返回必要的字段，避免过度获取

### 缓存

对不经常变化的数据使用缓存。

### 异步处理

对于耗时操作，使用异步处理模式。

## 版本控制

### URL版本控制

```
/api/v1/users
/api/v2/users
```

### 向后兼容

新版本应保持向后兼容，避免破坏现有客户端。

## 文档

### 接口文档

为每个接口提供完整的文档，包括：
- 功能描述
- 请求参数
- 响应参数
- 示例代码
- 错误码说明

### 更新日志

记录API的变更历史，包括新增、修改、废弃的接口。