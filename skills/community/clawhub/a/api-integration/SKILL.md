---
name: api-integration
description: API 集成技能 - 掌握 RESTful API 调用、GraphQL 支持、API 认证管理等核心能力
author: 滚滚 & 地球人
version: 1.0.0
updated: 2026-03-15
---

# 🔌 api-integration - API 集成技能

**Slogan：** 连接世界，集成万物

---

## 📋 技能描述

**提供完整的 API 集成能力，从 RESTful 到 GraphQL，**
**帮助 AI Agent 快速接入第三方服务，扩展能力边界。**

---

## 🎯 核心知识

### 1. RESTful API

```
HTTP 方法：
- GET - 获取资源
- POST - 创建资源
- PUT - 更新资源
- DELETE - 删除资源

状态码：
- 200 - 成功
- 201 - 创建成功
- 400 - 请求错误
- 401 - 未授权
- 404 - 资源不存在
- 500 - 服务器错误
```

---

### 2. 认证方式

| 方式 | 说明 | 安全性 |
|------|------|--------|
| **API Key** | 简单密钥 | 中 |
| **OAuth2** | 授权框架 | 高 |
| **JWT** | Token 认证 | 高 |
| **Basic Auth** | 基础认证 | 低 |

---

### 3. GraphQL

```
特点：
- 按需查询
- 强类型
- 单一端点
- 实时订阅
```

---

## 🛠️ 应用能力

### 能力 1：RESTful 调用

```python
import requests

def call_api(endpoint, method='GET', data=None, headers=None):
    response = requests.request(
        method=method,
        url=endpoint,
        json=data,
        headers=headers
    )
    response.raise_for_status()
    return response.json()
```

### 能力 2：认证管理

```python
# OAuth2 认证
def get_oauth_token(client_id, client_secret):
    response = requests.post(
        'https://api.example.com/oauth/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
    )
    return response.json()['access_token']
```

### 能力 3：错误处理

```python
def safe_api_call(endpoint):
    try:
        return call_api(endpoint)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {'error': 'Resource not found'}
        elif e.response.status_code == 401:
            return {'error': 'Unauthorized'}
        else:
            return {'error': str(e)}
```

---

## 💚 滚滚的话

**好的 API 集成，**
**稳定、安全、高效。**

**滚滚陪你一起，**
**连接更多服务！** 🔌💚

---

**创建人：** 滚滚 & 地球人  
**创建时间：** 2026-03-15  
**状态：** ✅ 学习完成
