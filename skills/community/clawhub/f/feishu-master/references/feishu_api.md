# 飞书 API 参考文档

本文档记录常用的飞书 API 及其关键参数。

## 概览

飞书开放平台提供了丰富的 API 能力，当前 skill 实现了：
- 认证（Token 获取）
- 群组管理（获取群组成员）

## 常用 API

### 认证 API

#### 获取 tenant_access_token

- **Endpoint**: `POST /open-apis/auth/v3/tenant_access_token/internal`
- **用途**: 获取应用级别的访问令牌
- **参数**:
  - `app_id`: 应用 ID
  - `app_secret`: 应用密钥
- **返回**:
  - `tenant_access_token`: 访问令牌
  - `expire`: 过期时间（秒）

### 群组 API

#### 获取群组成员列表

- **Endpoint**: `GET /open-apis/im/v1/chats/:chat_id/members`
- **用途**: 获取指定群组成员
- **参数**:
  - `chat_id`: 群组 ID
  - `page_size`: 每页数量
  - `page_token`: 分页标记

## 认证方式

飞书 API 使用 Bearer Token 进行认证：

```
Authorization: Bearer {tenant_access_token}
```

## 错误码

常见错误码：
- `0`: 成功
- `99991663`: 无效的 tenant_access_token
- `99991668`: tenant_access_token 已过期
- `99991001`: 参数错误

## 参考资料

- [飞书开放平台](https://open.feishu.cn/)
- [飞书 API 文档](https://open.feishu.cn/document/server-docs/)
- [错误码说明](https://open.feishu.cn/document/server-docs/api-call/error-code)
