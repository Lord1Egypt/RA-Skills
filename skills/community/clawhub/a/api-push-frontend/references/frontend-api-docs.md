# 前端数据接口平台 API 文档

## 推送接口

### 接口地址
```
POST https://jffe.techgp.cn/md/api/uploadV4
```

### 请求头
```
Content-Type: application/json
```

### 请求体

```json
{
  "prdId": "产品需求 ID",
  "apiDefinition": [
    {
      "接口定义对象"
    }
  ]
}
```

### 参数说明

#### prdId
- **类型**: String
- **必填**: 是
- **说明**: 产品需求 ID，用于关联产品需求和接口定义

#### apiDefinition
- **类型**: Array
- **必填**: 是
- **说明**: 接口定义数组，可以包含一个或多个接口

### 接口定义对象结构

```json
{
  "name": "接口名称",
  "path": "/api/path",
  "method": "GET",
  "description": "接口描述",
  "requestParams": [
    {
      "name": "参数名",
      "type": "String",
      "required": true,
      "description": "参数描述"
    }
  ],
  "responseSchema": {
    "type": "object",
    "properties": {}
  }
}
```

### 响应格式

#### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "uploadId": "上传 ID",
    "timestamp": "上传时间戳",
    "apiCount": 接口数量
  }
}
```

#### 失败响应
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 参数错误 | 检查请求参数格式和内容 |
| 401 | 未授权 | 检查认证信息 |
| 404 | 需求不存在 | 确认 prdId 是否正确 |
| 500 | 服务器错误 | 联系平台管理员 |

## 接口定义规范

### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String | 接口名称 |
| path | String | 接口路径 |
| method | String | HTTP 方法 |

### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| description | String | 接口描述 |
| requestParams | Array | 请求参数列表 |
| responseSchema | Object | 响应数据结构 |
| tags | Array | 接口标签 |
| deprecated | Boolean | 是否已废弃 |

### HTTP 方法

支持以下 HTTP 方法：
- `GET` - 查询
- `POST` - 创建
- `PUT` - 更新
- `DELETE` - 删除
- `PATCH` - 部分更新

### 参数类型

支持以下参数类型：
- `String` - 字符串
- `Integer` - 整数
- `Number` - 数字
- `Boolean` - 布尔值
- `Object` - 对象
- `Array` - 数组

## 示例

### 完整请求示例

```json
{
  "prdId": "PRD-2026-001",
  "apiDefinition": [
    {
      "name": "获取用户信息",
      "path": "/api/user/info",
      "method": "GET",
      "description": "获取当前登录用户的详细信息",
      "requestParams": [],
      "responseSchema": {
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
          }
        }
      }
    },
    {
      "name": "创建用户",
      "path": "/api/user",
      "method": "POST",
      "description": "创建新用户",
      "requestParams": [
        {
          "name": "userName",
          "type": "String",
          "required": true,
          "description": "用户名"
        },
        {
          "name": "email",
          "type": "String",
          "required": true,
          "description": "邮箱"
        },
        {
          "name": "password",
          "type": "String",
          "required": true,
          "description": "密码"
        }
      ],
      "responseSchema": {
        "type": "object",
        "properties": {
          "userId": {
            "type": "string",
            "description": "创建的用户 ID"
          }
        }
      }
    }
  ]
}
```

### cURL 示例

```bash
curl -X POST "https://jffe.techgp.cn/md/api/uploadV4" \
  -H "Content-Type: application/json" \
  -d '{
    "prdId": "PRD-2026-001",
    "apiDefinition": [
      {
        "name": "获取用户信息",
        "path": "/api/user/info",
        "method": "GET"
      }
    ]
  }'
```

### JavaScript 示例

```javascript
fetch('https://jffe.techgp.cn/md/api/uploadV4', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prdId: 'PRD-2026-001',
    apiDefinition: [
      {
        name: '获取用户信息',
        path: '/api/user/info',
        method: 'GET'
      }
    ]
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Python 示例

```python
import requests
import json

url = "https://jffe.techgp.cn/md/api/uploadV4"
headers = {"Content-Type": "application/json"}
data = {
    "prdId": "PRD-2026-001",
    "apiDefinition": [
        {
            "name": "获取用户信息",
            "path": "/api/user/info",
            "method": "GET"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 最佳实践

### 1. 接口命名
- 使用清晰、有意义的名称
- 遵循 RESTful 规范
- 使用英文或统一的命名语言

### 2. 路径设计
- 使用复数名词：`/api/users`
- 使用小写字母和连字符：`/api/user-profiles`
- 避免动词：使用 HTTP 方法表达操作

### 3. 参数定义
- 明确标注必填参数
- 提供详细的参数描述
- 指定参数类型和格式

### 4. 响应定义
- 定义完整的响应结构
- 包含错误响应示例
- 标注可能的状态码

### 5. 版本管理
- 接口变更时更新版本
- 保留历史版本记录
- 标注废弃接口和替代方案

## 常见问题

### Q: prdId 从哪里获取？
A: 联系产品经理获取产品需求 ID，通常格式为 `PRD-2026-001`

### Q: 接口定义格式错误怎么办？
A: 检查 JSON 格式，确保必填字段完整，参考本文档的示例

### Q: 推送失败如何排查？
A: 
1. 检查网络连接
2. 检查请求参数格式
3. 确认 prdId 是否正确
4. 查看错误响应信息

### Q: 可以批量推送多少个接口？
A: 建议每次推送不超过 50 个接口，大量接口分批推送

### Q: 推送后前端多久能看到？
A: 通常实时同步，如有延迟请联系平台管理员

---

**文档版本**: 1.0.0  
**最后更新**: 2026-03-31
