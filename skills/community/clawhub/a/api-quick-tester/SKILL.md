---
name: api-quick-tester
description: API 快速测试工具。一键测试 REST/GraphQL API，生成测试报告，模拟请求。适合前端/后端开发者。
version: 1.0.0
author: OpenClaw CN
tags:
  - api
  - testing
  - rest
  - graphql
  - developer-tools
---

# API 快速测试工具

专为开发者设计。一键测试 API、生成报告、模拟请求，提升开发效率。

## 功能

- 🚀 **快速测试** - 一键发送 HTTP 请求
- 📊 **测试报告** - 自动生成测试报告
- 🔄 **批量测试** - 支持批量测试多个 API
- 📝 **Mock 数据** - 自动生成测试数据
- 🔐 **认证支持** - 支持 Bearer/Basic/API Key

## 安装

```bash
npx clawhub@latest install api-quick-tester
```

## 使用方法

### 1. 测试单个 API

```bash
node ~/.openclaw/skills/api-quick-tester/test.js --url "https://api.example.com/users" --method GET
```

输出：
```
📊 API 测试报告

URL: https://api.example.com/users
Method: GET
Status: 200 OK
Time: 156ms

Response:
{
  "users": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ]
}

✅ 测试通过
```

### 2. 批量测试

创建测试文件 `api-tests.json`：
```json
[
  {
    "name": "获取用户列表",
    "url": "https://api.example.com/users",
    "method": "GET",
    "expectedStatus": 200
  },
  {
    "name": "创建用户",
    "url": "https://api.example.com/users",
    "method": "POST",
    "body": { "name": "Test User" },
    "expectedStatus": 201
  }
]
```

运行测试：
```bash
node ~/.openclaw/skills/api-quick-tester/batch-test.js --file api-tests.json
```

### 3. Mock 数据生成

```bash
node ~/.openclaw/skills/api-quick-tester/mock.js --schema user
```

输出：
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2026-03-24T04:40:00Z"
}
```

### 4. GraphQL 测试

```bash
node ~/.openclaw/skills/api-quick-tester/graphql.js --url "https://api.example.com/graphql" --query '{ users { id name } }'
```

## 支持的方法

- GET
- POST
- PUT
- PATCH
- DELETE

## 认证方式

### Bearer Token
```bash
node test.js --url "https://api.example.com/users" --auth bearer:YOUR_TOKEN
```

### Basic Auth
```bash
node test.js --url "https://api.example.com/users" --auth basic:username:password
```

### API Key
```bash
node test.js --url "https://api.example.com/users" --auth apikey:X-API-Key:YOUR_KEY
```

## 测试报告

自动生成 Markdown 测试报告：

```markdown
# API 测试报告

**时间**: 2026-03-24 12:40
**总测试数**: 10
**通过**: 9
**失败**: 1

## 失败的测试

### 1. 创建用户
- URL: POST https://api.example.com/users
- 预期状态: 201
- 实际状态: 400
- 错误信息: Invalid email format

## 建议

- 检查 email 字段格式
```

## 配置

编辑 `~/.openclaw/skills/api-quick-tester/config.json`：

```json
{
  "baseUrl": "https://api.example.com",
  "timeout": 5000,
  "retries": 3,
  "defaultHeaders": {
    "Content-Type": "application/json"
  }
}
```

---

## 💬 Pro 版本（¥199）

### 免费版（当前）
- 基础 API 测试
- 批量测试
- 测试报告生成

### Pro 版（¥199）
- ✅ 自动化测试（CI/CD 集成）
- ✅ 性能测试（并发/压力）
- ✅ Mock 服务器
- ✅ API 文档生成
- ✅ 环境变量管理
- ✅ 1年更新支持

### 联系方式
- **QQ**: 1002378395（中国用户）
- **Telegram**: `待注册`（海外用户）

> 添加 QQ 1002378395，发送"API测试"获取 Pro 版信息

---

## License

MIT（免费版）
Pro 版：付费后可用
