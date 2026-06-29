---
name: douyin-mini-game-server-api
description: Comprehensive skill reference for Douyin (TikTok China) mini-game server-side OpenAPI. Covers HTTPS API interfaces for backend developers — access token management, login credential verification, user data storage, QR code generation, subscription messages, gift redemption, Link/Schema generation, dynamic sharing, game group tags, and all server-side `mgplatform/api` endpoints. Use when developing, debugging, or asking questions about Douyin mini-game backend APIs — especially the server-side login flow (code2Session/checkSessionKey/resetSessionKey), access token (getAccessToken/genStableAccessToken), user cloud storage (setUserStorage/removeUserStorage), QR codes (createQRCode), subscription notifications, gift reward verification, or any OpenAPI SDK integration.
---

> 基于抖音小游戏服务端 OpenAPI 官方文档生成，生成时间 2026-06-24
> 官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/

抖音小游戏服务端 OpenAPI 是提供给开发者服务端调用的 HTTPS API 接口集合。用于在开发者后台服务器上完成登录凭证校验、用户数据管理、二维码生成、消息推送、礼包核销等功能。所有 API 域名基于 `https://minigame.zijieapi.com/mgplatform/api/`，Scope 均为 `open.ttgame.mgplatform`。支持 Java/NodeJS/Go 三种官方 SDK。

## 概述与 SDK

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 服务端 API 概述 | access_token 机制、请求格式规范、OpenAPI SDK 总览（Java/NodeJS/Go）、完整 API 接口列表（21个接口） | [server-overview](references/server-overview.md) |

## 核心 API

### 接口调用凭证

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 接口调用凭证 | getAccessToken（获取全局调用凭据，2h 有效期）、genStableAccessToken（稳定版 token，普通/强制刷新两种模式） | [server-auth](references/server-auth.md) |

### 登录

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 登录相关 | code2Session（登录凭证校验，获取 openid/session_key/unionid）、用户登录态签名（hmac_sha256 签名规则）、checkSessionKey（校验登录态）、resetSessionKey（重置登录态） | [server-login](references/server-login.md) |

### 数据与二维码

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 数据缓存 | setUserStorage（写入用户云存储数据，支持排行榜 KVData 格式）、removeUserStorage（删除用户数据）、存储限制（key≤128B, key+value≤1024B, ≤128对） | [server-data](references/server-data.md) |
| 二维码 | createQRCode（生成二维码/抖音码，支持圆形码、自定义颜色、icon、版本控制、启动参数） | [server-qrcode](references/server-qrcode.md) |

### 消息与其它

| 模块 | 描述 | 参考文件 |
|------|------|---------|
| 消息推送 | 订阅消息发送（模板消息推送，1次/秒限制）、消息推送客服（回复文字客服消息） | [server-message](references/server-message.md) |
| 其他能力 | 游戏礼包核销、Link链接（生成/查询/配额）、Schema链接（生成/查询/配额）、动态分享（活动ID/更新动态消息）、游戏群标签（查询/设置）、公会群解绑、赛事上报、内容安全检测、广告变现数据 API | [server-other](references/server-other.md) |

## 快速参考

### access_token 机制

```
获取: POST /api/apps/v2/token (getAccessToken) 或 POST /api/apps/stable_token (genStableAccessToken)
有效期: 2小时（getAccessToken 重复获取会使旧 token 缩短至 5 分钟）
稳定版: genStableAccessToken 在有效期内返回不变 token，两种模式（普通/强制刷新）
```

### 核心认证流程

```javascript
// 1. 获取 access_token
const tokenRes = await fetch('https://minigame.zijieapi.com/mgplatform/api/apps/v2/token', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ appid: 'ttxxx', secret: 'xxx', grant_type: 'client_credential' })
});
const { data: { access_token } } = await tokenRes.json();

// 2. code2Session 校验登录
const loginRes = await fetch(
  `https://minigame.zijieapi.com/mgplatform/api/apps/jscode2session?appid=ttxxx&secret=xxx&code=${code}`
);
const { openid, session_key, unionid } = await loginRes.json();

// 3. 生成用户登录态签名（hmac_sha256）
const crypto = require('crypto');
function sign(sessionKey, method, uriPath, postBody) {
  let data = method.toLowerCase() + '&' + encodeURIComponent(uriPath);
  if (postBody) data += '&' + postBody;
  return crypto.createHmac('sha256', sessionKey).update(data).digest('hex');
}

// 4. 写用户数据（带签名）
const signature = sign(session_key, 'post', '/mgplatform/api/apps/set_user_storage', body);
await fetch('https://minigame.zijieapi.com/mgplatform/api/apps/set_user_storage?...', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ kv_list: [{ key: 'score', value: '100' }] })
});
```

### SDK 快速选择

| 语言 | SDK 包 | 适用场景 |
|------|------|------|
| Java | `com.douyin.openapi:sdk:1.0.5` | 企业级后端服务 |
| NodeJS | `@open-dy/open_api_sdk` | Node.js 后端服务 |
| Go | `github.com/bytedance/douyin-openapi-sdk-go` | Go 微服务 |

### API 速查表

| 功能 | API URL（相对路径） | Method | 需要签名 |
|------|------|------|------|
| 获取 token | /api/apps/v2/token | POST | 否 |
| 稳定 token | /api/apps/stable_token | POST | 否 |
| 登录校验 | /api/apps/jscode2session | GET | 否 |
| 校验 session | /api/apps/check_session_key | GET | 是 |
| 重置 session | /api/apps/reset_session_key | POST | 是 |
| 写用户数据 | /api/apps/set_user_storage | POST | 是 |
| 删用户数据 | /api/apps/remove_user_storage | POST | 是 |
| 生成二维码 | /api/apps/qrcode | POST | 否 |
| 发送订阅消息 | /api/apps/subscribe_notification/developer/v1/notify | POST | 否 |
| 核销礼包 | /api/gift/receive_reward | POST | 否 |
| 回复客服消息 | /api/apps/reply/reply_user_text | POST | 否 |

### 最佳实践

1. **Token 管理**：推荐使用 `genStableAccessToken`，避免多服务实例互刷 token；单实例可用 `getAccessToken` 每小时刷新
2. **AppSecret 安全**：永远只在服务端使用 AppSecret，不下发到客户端或外部
3. **签名正确性**：涉及用户数据的 API 必须正确生成 hmac_sha256 签名，注意 POST body 的 JSON 字符串要与签名时一致
4. **频率控制**：注意各 API 的限频（如二维码 5000次/分钟、订阅消息 1次/秒/用户），实现指数退避重试
5. **错误处理**：针对 access_token 过期（28001008）和无效（28001003）自动刷新重试
6. **幂等设计**：礼包核销使用 uuid 保证幂等，防止重复发放
7. **SDK 优先**：优先使用官方 OpenAPI SDK，减少自行实现签名和 token 刷新逻辑
8. **session_key 保护**：session_key 仅在服务端保存，不通过任何方式下发到客户端
