# 接口定义规范

本文档定义了推送到产品部数据平台的接口文档标准格式。

## 基础结构

```json
{
  "version": "1.0.0",
  "changeLog": "变更说明",
  "apis": [
    {
      "method": "GET",
      "path": "/api/endpoint",
      "description": "接口描述",
      "tags": ["模块名", "子模块"],
      "parameters": [...],
      "requestBody": {...},
      "response": {...}
    }
  ]
}
```

## 字段说明

### 接口级别字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| method | string | 是 | HTTP 方法：GET, POST, PUT, DELETE, PATCH |
| path | string | 是 | 接口路径，支持路径参数 `{id}` |
| description | string | 是 | 接口功能描述 |
| tags | array | 否 | 接口分类标签 |
| deprecated | boolean | 否 | 是否已废弃，默认 false |
| parameters | array | 否 | 查询参数/路径参数 |
| requestBody | object | 否 | 请求体结构（POST/PUT/PATCH） |
| response | object | 是 | 响应结构定义 |

### 参数定义 (parameters)

```json
{
  "name": "参数名",
  "in": "path|query|header",
  "required": true,
  "type": "string|number|boolean|integer|array",
  "description": "参数描述",
  "example": "示例值",
  "enum": ["可选值 1", "可选值 2"]
}
```

### 请求体定义 (requestBody)

```json
{
  "contentType": "application/json",
  "required": true,
  "schema": {
    "type": "object",
    "properties": {
      "fieldName": {
        "type": "string",
        "description": "字段描述",
        "required": true,
        "example": "示例值"
      }
    }
  }
}
```

### 响应定义 (response)

```json
{
  "contentType": "application/json",
  "schema": {
    "type": "object",
    "properties": {
      "code": {"type": "number", "description": "状态码"},
      "message": {"type": "string", "description": "响应消息"},
      "data": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"}
        }
      }
    }
  },
  "examples": {
    "success": {
      "code": 200,
      "message": "success",
      "data": {...}
    },
    "error": {
      "code": 400,
      "message": "参数错误"
    }
  }
}
```

## 完整示例

```json
{
  "version": "1.0.0",
  "changeLog": "新增用户管理模块接口",
  "apis": [
    {
      "method": "GET",
      "path": "/api/users/{id}",
      "description": "根据 ID 获取用户详情",
      "tags": ["用户管理", "查询"],
      "parameters": [
        {
          "name": "id",
          "in": "path",
          "required": true,
          "type": "string",
          "description": "用户唯一标识",
          "example": "usr_123456"
        }
      ],
      "response": {
        "contentType": "application/json",
        "schema": {
          "type": "object",
          "properties": {
            "code": {"type": "number", "example": 200},
            "message": {"type": "string", "example": "success"},
            "data": {
              "type": "object",
              "properties": {
                "id": {"type": "string", "description": "用户 ID"},
                "name": {"type": "string", "description": "用户名"},
                "email": {"type": "string", "description": "邮箱"},
                "createdAt": {"type": "string", "description": "创建时间", "format": "date-time"}
              }
            }
          }
        }
      }
    },
    {
      "method": "POST",
      "path": "/api/users",
      "description": "创建新用户",
      "tags": ["用户管理", "新增"],
      "requestBody": {
        "contentType": "application/json",
        "required": true,
        "schema": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "用户名",
              "required": true,
              "example": "张三"
            },
            "email": {
              "type": "string",
              "description": "邮箱地址",
              "required": true,
              "example": "zhangsan@example.com"
            },
            "password": {
              "type": "string",
              "description": "密码",
              "required": true,
              "example": "******"
            }
          }
        }
      },
      "response": {
        "contentType": "application/json",
        "schema": {
          "type": "object",
          "properties": {
            "code": {"type": "number"},
            "message": {"type": "string"},
            "data": {
              "type": "object",
              "properties": {
                "id": {"type": "string", "description": "新创建的用户 ID"}
              }
            }
          }
        }
      }
    }
  ]
}
```

## Java Controller 转换指南

### 注解映射

| Java 注解 | JSON 字段 |
|-----------|-----------|
| `@GetMapping` | method: "GET", path: 值 |
| `@PostMapping` | method: "POST", path: 值 |
| `@PutMapping` | method: "PUT", path: 值 |
| `@DeleteMapping` | method: "DELETE", path: 值 |
| `@PathVariable` | parameters[].in: "path" |
| `@RequestParam` | parameters[].in: "query" |
| `@RequestHeader` | parameters[].in: "header" |
| `@RequestBody` | requestBody |
| `@ApiOperation` | description |
| `@ApiParam` | parameters[].description |

### 示例转换

**Java 代码:**

```java
@RestController
@RequestMapping("/api/orders")
@Tag(name = "订单管理")
public class OrderController {
    
    @GetMapping("/{orderId}")
    @Operation(summary = "获取订单详情")
    public OrderDTO getOrder(
        @PathVariable @ApiParam("订单 ID") String orderId,
        @RequestParam(required = false) @ApiParam("是否包含明细") Boolean includeItems
    ) {
        // ...
    }
    
    @PostMapping
    @Operation(summary = "创建订单")
    public OrderDTO createOrder(@RequestBody @Valid CreateOrderRequest request) {
        // ...
    }
}
```

**转换结果:**

```json
{
  "apis": [
    {
      "method": "GET",
      "path": "/api/orders/{orderId}",
      "description": "获取订单详情",
      "tags": ["订单管理"],
      "parameters": [
        {
          "name": "orderId",
          "in": "path",
          "required": true,
          "type": "string",
          "description": "订单 ID"
        },
        {
          "name": "includeItems",
          "in": "query",
          "required": false,
          "type": "boolean",
          "description": "是否包含明细"
        }
      ],
      "response": {
        "type": "OrderDTO"
      }
    },
    {
      "method": "POST",
      "path": "/api/orders",
      "description": "创建订单",
      "tags": ["订单管理"],
      "requestBody": {
        "contentType": "application/json",
        "required": true,
        "schema": {
          "type": "CreateOrderRequest"
        }
      },
      "response": {
        "type": "OrderDTO"
      }
    }
  ]
}
```

## 检查清单

推送前确保：

- [ ] 所有必填字段已填写
- [ ] HTTP 方法正确（GET/POST/PUT/DELETE/PATCH）
- [ ] 路径参数使用 `{param}` 格式
- [ ] 参数类型准确（string/number/boolean/integer/array）
- [ ] 必填参数标注 `required: true`
- [ ] 响应结构完整
- [ ] 描述清晰易懂
- [ ] JSON 格式有效（通过 JSON 验证）
