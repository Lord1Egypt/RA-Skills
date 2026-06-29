# 接口定义规范

本文档定义推送到前端数据接口平台的接口定义标准格式。

## 基础结构

```json
{
  "name": "接口名称",
  "path": "/api/path",
  "method": "GET",
  "description": "接口描述",
  "requestParams": [],
  "responseSchema": {},
  "tags": [],
  "deprecated": false
}
```

## 字段说明

### name（必填）
- **类型**: String
- **说明**: 接口名称，应清晰表达接口功能
- **示例**: `"获取用户信息"`, `"创建订单"`

### path（必填）
- **类型**: String
- **说明**: 接口路径，遵循 RESTful 规范
- **示例**: `"/api/user/info"`, `"/api/orders"`

### method（必填）
- **类型**: String
- **说明**: HTTP 方法
- **可选值**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`

### description（推荐）
- **类型**: String
- **说明**: 接口详细描述
- **示例**: `"获取当前登录用户的详细信息，包括基本信息和扩展信息"`

### requestParams（可选）
- **类型**: Array
- **说明**: 请求参数列表

#### 参数对象结构
```json
{
  "name": "参数名",
  "type": "String",
  "required": true,
  "description": "参数描述",
  "default": "默认值",
  "example": "示例值"
}
```

### responseSchema（推荐）
- **类型**: Object
- **说明**: 响应数据结构，使用 JSON Schema 格式

#### 示例
```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "integer",
      "description": "响应码"
    },
    "data": {
      "type": "object",
      "properties": {
        "userId": {
          "type": "string",
          "description": "用户 ID"
        }
      }
    }
  }
}
```

### tags（可选）
- **类型**: Array
- **说明**: 接口标签，用于分类
- **示例**: `["用户管理"]`, `["订单", "支付"]`

### deprecated（可选）
- **类型**: Boolean
- **说明**: 是否已废弃
- **默认**: `false`

## 完整示例

### 示例 1：GET 接口

```json
{
  "name": "获取用户信息",
  "path": "/api/user/info",
  "method": "GET",
  "description": "获取当前登录用户的详细信息",
  "requestParams": [
    {
      "name": "includeProfile",
      "type": "Boolean",
      "required": false,
      "description": "是否包含用户画像信息",
      "default": false
    }
  ],
  "responseSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "integer",
        "description": "响应码"
      },
      "data": {
        "type": "object",
        "properties": {
          "userId": {
            "type": "string",
            "description": "用户 ID"
          },
          "userName": {
            "type": "string",
            "description": "用户名"
          },
          "email": {
            "type": "string",
            "description": "邮箱"
          },
          "profile": {
            "type": "object",
            "description": "用户画像（当 includeProfile=true 时返回）"
          }
        }
      }
    }
  },
  "tags": ["用户管理"],
  "deprecated": false
}
```

### 示例 2：POST 接口

```json
{
  "name": "创建订单",
  "path": "/api/orders",
  "method": "POST",
  "description": "创建新的购物订单",
  "requestParams": [
    {
      "name": "productId",
      "type": "String",
      "required": true,
      "description": "商品 ID"
    },
    {
      "name": "quantity",
      "type": "Integer",
      "required": true,
      "description": "购买数量",
      "default": 1
    },
    {
      "name": "address",
      "type": "String",
      "required": true,
      "description": "收货地址"
    },
    {
      "name": "remark",
      "type": "String",
      "required": false,
      "description": "订单备注"
    }
  ],
  "responseSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "integer"
      },
      "data": {
        "type": "object",
        "properties": {
          "orderId": {
            "type": "string",
            "description": "订单 ID"
          },
          "orderNo": {
            "type": "string",
            "description": "订单编号"
          },
          "status": {
            "type": "string",
            "description": "订单状态"
          }
        }
      }
    }
  },
  "tags": ["订单管理"],
  "deprecated": false
}
```

### 示例 3：PUT 接口

```json
{
  "name": "更新用户信息",
  "path": "/api/user/info",
  "method": "PUT",
  "description": "更新当前登录用户的基本信息",
  "requestParams": [
    {
      "name": "userName",
      "type": "String",
      "required": false,
      "description": "用户名"
    },
    {
      "name": "email",
      "type": "String",
      "required": false,
      "description": "邮箱"
    },
    {
      "name": "phone",
      "type": "String",
      "required": false,
      "description": "手机号"
    }
  ],
  "responseSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "integer"
      },
      "message": {
        "type": "string",
        "description": "响应消息"
      }
    }
  },
  "tags": ["用户管理"],
  "deprecated": false
}
```

### 示例 4：DELETE 接口

```json
{
  "name": "删除订单",
  "path": "/api/orders/{orderId}",
  "method": "DELETE",
  "description": "删除指定订单（仅支持未支付订单）",
  "requestParams": [
    {
      "name": "orderId",
      "type": "String",
      "required": true,
      "description": "订单 ID",
      "in": "path"
    }
  ],
  "responseSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "integer"
      },
      "message": {
        "type": "string"
      }
    }
  },
  "tags": ["订单管理"],
  "deprecated": false
}
```

## 类型映射

### Java 类型到 JSON Schema

| Java 类型 | JSON Schema 类型 | 示例 |
|----------|-----------------|------|
| String | string | `"hello"` |
| Integer | integer | `123` |
| Long | integer | `1234567890` |
| Double | number | `12.34` |
| Boolean | boolean | `true` |
| Date | string (date-time) | `"2026-03-31T12:00:00Z"` |
| List<T> | array | `[]` |
| Map<K,V> | object | `{}` |
| Object | object | `{}` |

## 检查清单

推送前检查：

- [ ] name 字段清晰表达接口功能
- [ ] path 遵循 RESTful 规范
- [ ] method 使用正确的 HTTP 方法
- [ ] description 详细描述接口用途
- [ ] requestParams 包含所有请求参数
- [ ] 参数标注了必填/选填
- [ ] responseSchema 定义了响应结构
- [ ] tags 正确分类接口
- [ ] 废弃接口标注 deprecated=true

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-31
