---
name: fb-graph-proxy
description: 尤里改 Facebook Graph API 代理服务使用指南
homepage: https://baiz.ai
primary_credential: BAIZ_API_TOKEN
env:
  BAIZ_API_TOKEN:
    description: "baiz.ai 平台 API Token。在 baiz.ai 后台「API管理」页面生成，格式为 xxx|xxx。仅对 baiz.ai 有效，非 Facebook 原始 Token。建议使用最小权限的测试账户 Token。"
    required: true
    sensitive: true
---

# 尤里改 Facebook Graph API 代理服务

## 快速开始

### 第一步：注册账号

前往 https://baiz.ai 尤里改官网注册账号。

### 第二步：获取 Facebook 授权

两种方式（二选一）：
1. **联系官方** — 联系尤里改官方获取已授权的 Facebook 账号
2. **自行授权** — 将你自己的 Facebook 账号在尤里改后台完成授权绑定

### 第三步：获取 API Token

在尤里改后台获取你的 API Token。

### 第四步：开始调用

将原本请求 Facebook Graph API 的所有端点，**域名替换**为 `facebook-graph.baiz.ai`，并将获取到的 Token 放到请求头的 `Authorization: Bearer {token}` 中。

## 使用示例

**原始 Facebook API 请求：**

```
GET https://graph.facebook.com/v25.0/act_123456/campaigns?fields=name,status
Authorization: Bearer {facebook_access_token}
```

**替换后的请求：**

```
GET https://facebook-graph.baiz.ai/v25.0/act_123456/campaigns?fields=name,status
Authorization: Bearer {baiz_api_token}
```

只需要改两处：
1. 域名 `graph.facebook.com` → `facebook-graph.baiz.ai`
2. Token 换成从尤里改后台获取的 Bearer Token

**无需传递 `access_token` 参数**，系统会根据请求路径中的资源 ID 自动解析并注入对应的 Facebook Access Token。

其余所有参数、路径、请求方法、请求体保持不变，与 Facebook Graph API 官方文档完全一致。

## 支持的请求

- 所有 HTTP 方法：GET、POST、PUT、DELETE 等
- 所有 Facebook Graph API 端点和版本
- 文件上传（multipart/form-data）
- JSON 请求体和表单请求体
