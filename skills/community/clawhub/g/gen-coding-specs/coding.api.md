# 接口规范

## 概述
本文档定义API接口设计标准和规范，确保接口的一致性、可维护性和易用性。

## 设计原则

### API 风格选择

项目可根据团队约定选择以下风格之一：

#### 方式 A：统一 POST（适合内部系统 / 网关统一鉴权场景）
- 所有接口统一使用 POST 请求，方便统一处理和参数传递
- 操作类型通过 URL 路径中的动作标识（如 `/list`, `/create`）区分

```http
POST   /api/v1/users/list          # 获取用户列表
POST   /api/v1/users/detail        # 获取指定用户
POST   /api/v1/users/create        # 创建用户
POST   /api/v1/users/update        # 更新用户
POST   /api/v1/users/delete        # 删除用户
```

#### 方式 B：RESTful 风格（推荐，适合对外 API / 标准化场景）
- 使用 HTTP 方法语义（GET/POST/PUT/DELETE）
- 资源路径使用复数名词，操作通过 HTTP 方法区分

```http
GET    /api/v1/users                # 获取用户列表
GET    /api/v1/users/:id            # 获取指定用户
POST   /api/v1/users                # 创建用户
PUT    /api/v1/users/:id            # 更新用户
DELETE /api/v1/users/:id            # 删除用户
```

> 本模板以下章节以 **方式 A（统一 POST）** 为示例。若项目采用 RESTful 风格，请将 HTTP 方法替换为对应语义，请求体格式保持不变。

### 请求体格式
所有POST请求统一使用JSON格式的请求体：
```json
{
  "request_id": "req_123456789",
  "params": {
    "pagination": {
      "page": 1,
      "size": 20
    },
    "filters": {
      "status": "active"
    },
    "sort": {
      "field": "created_at",
      "order": "desc"
    }
  },
  "metadata": {
    "client_type": "web",
    "timestamp": "2025-01-15T10:00:00Z"
  }
}
```

## 版本管理

### URL版本控制
- 版本号包含在URL路径中：`/api/v1/`, `/api/v2/`
- 主版本号表示不兼容的变更
- 保持向后兼容至少2个主版本

### 版本策略
```http
/api/v1/users     # 当前版本
/api/v2/users     # 新版本（不兼容变更）
```

## 请求格式

### 请求头
```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>
X-Request-ID: <unique_id>
```

### 请求参数
- **路径参数**：用于区分不同的接口端点
- **请求体**：所有参数统一放在请求体中，遵循标准请求体格式：
  - `request_id`：客户端生成的唯一请求标识，用于链路追踪
  - `action`：接口动作标识，对应 URL 路径（如 "users/list"）
  - `params`：业务参数对象，包含所有接口需要的参数
  - `metadata`：请求元数据，包含客户端信息、时间戳等

### 示例
```http
POST /api/v1/users/list
Content-Type: application/json

{
  "request_id": "req_123456789",
  "params": {
    "pagination": {
      "page": 1,
      "size": 20
    },
    "filters": {
      "status": "active",
      "name": "张三"
    },
    "sort": {
      "field": "created_at",
      "order": "desc"
    }
  },
  "metadata": {
    "client_type": "web",
    "timestamp": "2025-01-15T10:00:00Z"
  }
}

POST /api/v1/users/create
Content-Type: application/json

{
  "request_id": "req_987654321",
  "params": {
    "name": "张三",
    "email": "zhangsan@example.com"
  },
  "metadata": {
    "client_type": "web",
    "timestamp": "2025-01-15T10:00:00Z"
  }
}
```

## 响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "id": "123",
    "name": "张三",
    "email": "zhangsan@example.com"
  },
  "timestamp": "2025-01-15T10:00:00Z",
  "request_id": "abc123"
}
```

### 列表响应
```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  },
  "timestamp": "2025-01-15T10:00:00Z"
}
```

## 错误处理

### 错误响应格式
```json
{
  "code": 400,
  "message": "请求参数错误",
  "error_code": "USER_001",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确",
      "code": "INVALID_EMAIL_FORMAT"
    }
  ],
  "timestamp": "2025-01-15T10:00:00Z",
  "request_id": "abc123"
}
```

### HTTP状态码
- **200 OK**: 请求成功（所有成功操作统一返回200）
- **400 Bad Request**: 请求参数错误
- **401 Unauthorized**: 未授权
- **403 Forbidden**: 禁止访问
- **404 Not Found**: 资源不存在
- **500 Internal Server Error**: 服务器错误

**注意**：统一 POST 风格下，所有操作的成功状态都通过响应体中的 `code` 字段区分，HTTP 状态码主要用于表示请求处理状态。RESTful 风格下请使用标准 HTTP 状态码语义。

## 认证授权

> 认证授权规范（JWT、RBAC、CSP、速率限制等）见 `coding.security.md`。

## API文档

### 文档要求
- 使用OpenAPI/Swagger规范
- 包含请求/响应示例
- 标注认证要求和权限
- 提供错误码说明

### 文档生成
```yaml
# 使用OpenAPI 3.0规范
openapi: 3.0.0
info:
  title: API文档
  version: 1.0.0
paths:
  /api/v1/users:
    get:
      summary: 获取用户列表
      parameters:
        - name: page
          in: query
          schema:
            type: integer
```

## 性能要求

### 响应时间
- 简单查询：< 100ms
- 复杂查询：< 500ms
- 列表查询：< 1s

### 分页
- 默认每页20条
- 最大每页100条
- 使用cursor或offset分页

## 安全要求

### 输入验证
- 验证所有输入参数
- 防止SQL注入、XSS攻击
- 使用参数化查询

### 敏感信息
- 不在URL中传递敏感信息
- 使用HTTPS传输
- 不在日志中记录敏感信息

---

> **上下文提示**：在实现API接口时，建议同时加载：
> - `coding.coding-style.md` - 编码风格规范
> - `coding.testing.md` - 测试规范
> - `coding.security.md` - 安全规范

