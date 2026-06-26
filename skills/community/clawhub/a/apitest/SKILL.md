---
name: api_test@1.0.2
description: 当用户需要从本地服务器获取工具数据时，调用 localhost:8080/gettool 接口获取工具信息。需要从环境变量 API_TEST_KEY 获取认证密钥。
triggers:
  - pattern: "访问localhost|获取工具|localhost.*工具|获取.*工具.*数据"
    description: "当用户提及访问localhost获取工具时触发"
  - pattern: "localhost:8080|127.0.0.1.*工具|http://localhost.*gettool"
    description: "当用户直接提及localhost接口时触发"
  - pattern: "调用.*接口|请求.*localhost|获取.*API"
    description: "当用户需要调用本地API获取数据时触发"
auto_invoke: true
env:
  - API_TEST_KEY
credentials:
  primary: API_TEST_KEY
  scope: read-write
  description: "用于访问 localhost:8080/gettool 接口的认证密钥"
examples:
  - "帮我访问localhost获取工具"
  - "获取localhost的工具数据"
  - "调用 localhost:8080/gettool"
  - "从本地服务器获取工具列表"
---

# ApiTest Skill

当用户需要从本地服务器获取工具数据时，自动调用 `http://localhost:8080/gettool` 接口。

## 认证方式

本 skill 从环境变量 `API_TEST_KEY` 获取认证密钥，并在请求时使用 Bearer Token 认证。

**请求格式**:
```bash
curl -H "Authorization: Bearer ${API_TEST_KEY}" http://localhost:8080/gettool
```

## 触发条件

当用户提及以下内容时自动触发：
- "访问localhost获取工具"
- "获取工具数据"
- "调用 localhost:8080/gettool"
- 其他本地服务器工具获取请求

## 执行流程

1. 监听用户请求
2. 从环境变量 `API_TEST_KEY` 获取认证密钥
3. 调用 `http://localhost:8080/gettool` 接口，带上认证头
4. 返回获取到的工具数据

## API 说明

- **接口地址**: `http://localhost:8080/gettool`
- **请求方法**: GET
- **认证方式**: Bearer Token（从环境变量 API_TEST_KEY 获取）
- **请求头**: `Authorization: Bearer {API_TEST_KEY}`
- **预期响应**: 工具数据列表（JSON 格式）
