# 服务端 API 概述

> 基于官方文档: https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/server-api-introduction

## 简介

抖音小程序、小游戏给开发者提供了服务端使用的 HTTPS API 接口。服务端 API 用于在开发者服务器上调用抖音开放平台能力，包括登录凭证校验、用户数据管理、二维码生成、消息推送、礼包核销等功能。

## access_token

access_token 是开发者调用服务端 API 的唯一凭证，开发者应使用服务端 API 获取 access_token，并使用 access_token 调用其它服务端 API。

| 特性 | 说明 |
|------|------|
| 有效期 | 最多 **2 小时** |
| 刷新机制 | 重复获取会导致上次 access_token 失效 |
| 平滑过渡 | 新老 access_token 在 **5 分钟**内都可使用 |
| 级别 | 小游戏级别 token，不要为每个用户单独分配 |

**安全提醒**：
- 只能在开发者服务器使用 AppSecret
- 不应该把会话密钥下发到小游戏
- 不应该对外提供 AppSecret 密钥

## 请求参数格式

| 请求方法 | 格式要求 |
|------|------|
| GET | 无特殊要求，参数通过 Query 传递 |
| POST | body 中的参数以 JSON 字符串形式写入 |
| 请求头 | 需设置 `"content-type": "application/json"` |

## OpenAPI SDK

抖音开放平台提供统一的服务端 OpenAPI SDK，支持三种编程语言：

| 语言 | 安装方式 | 说明 |
|------|------|------|
| Java | Maven 依赖 `com.douyin.openapi:sdk:1.0.5` | pom.xml 添加仓库和依赖 |
| NodeJS | `npm add @open-dy/open_api_sdk` | 需同时安装 @open-dy/open_api_credential |
| Go | `go get github.com/bytedance/douyin-openapi-sdk-go` | 需额外处理 token 注入 |

**注意**：SDK 中的 Token 参数需要开发者自行注入。credential 包提供了默认的 token 获取方法，但基于单实例实现。多实例部署需自行实现 token 获取逻辑。

### Java SDK 示例

```java
Config config = new Config()
    .setClientKey("your_app_id")
    .setClientSecret("your_app_secret");
Client client = new Client(config);
AppsV2TokenRequest sdkRequest = new AppsV2TokenRequest();
sdkRequest.setAppid("your_app_id");
sdkRequest.setSecret("your_secret");
sdkRequest.setGrantType("client_credential");
AppsV2TokenResponse sdkResponse = client.AppsV2Token(sdkRequest);
```

### NodeJS SDK 示例

```js
import Client from '@open-dy/open_api_sdk';
import CredentialClient from '@open-dy/open_api_credential';

const credentialClient = new CredentialClient({
    clientKey: 'xxx', clientSecret: 'xxx'
});
const { accessToken } = await credentialClient.getClientToken();
const client = new Client({ clientKey: 'xxx', clientSecret: 'xxx' });
```

### Go SDK 示例

```go
opt := new(credential.Config).
    SetClientKey("your_app_id").
    SetClientSecret("your_app_secret")
sdkClient, err := openApiSdkClient.NewClient(opt)
credentialHandler, _ := credential.NewCredential(opt)
token, _ := credentialHandler.GetClientToken()
```

## API 基础域名

所有服务端 API 使用以下域名：

```
https://minigame.zijieapi.com/mgplatform/api/
```

旧域名 `https://developer.toutiao.com/api/apps/xxx` 仍可用，但建议迁移到新域名。

## 全 API 接口列表

| 功能类型 | OpenAPI | SDK 方法名 | Method | URL 路径 |
|------|------|------|------|------|
| 接口调用凭证 | getAccessToken | AppsV2Token | POST | /apps/v2/token |
| 接口调用凭证 | genStableAccessToken | AppsStableToken | POST | /apps/stable_token |
| 登录 | code2Session | AppsJscode2session | GET | /apps/jscode2session |
| 登录 | 用户登录态签名 | (sign) | - | - |
| 登录 | checkSessionKey | AppsCheckSessionKey | GET | /apps/check_session_key |
| 登录 | resetSessionKey | AppsResetSessionKey | POST | /apps/reset_session_key |
| 数据缓存 | setUserStorage | AppsSetUserStorage | POST | /apps/set_user_storage |
| 数据缓存 | removeUserStorage | AppsRemoveUserStorage | POST | /apps/remove_user_storage |
| 二维码 | createQRCode | - | POST | /apps/qrcode |
| 订阅消息 | 发送订阅消息 | V1Notify | POST | /apps/subscribe_notification/developer/v1/notify |
| 客服消息 | 回复文字格式消息 | ReplyReplyUserText | POST | /apps/reply/reply_user_text |
| Link链接 | 生成Link | AppsUrlLinkGenerate | POST | /apps/url_link/generate |
| Link链接 | 查询Link | AppsUrlLinkQueryInfo | POST | /apps/url_link/query_info |
| Link链接 | 查询Link配额 | AppsUrlLinkQueryQuota | POST | /apps/url_link/query_quota |
| Schema链接 | 生成Schema | SchemaGenerate | POST | /apps/schema/generate |
| Schema链接 | 查询Schema | SchemaQueryInfo | POST | /apps/schema/query_info |
| Schema链接 | 查询Schema配额 | SchemaQueryQuota | POST | /apps/schema/query_quota |
| 游戏群标签 | 查询用户群标签 | GetUserGroupTag | POST | /apps/group_tag/get_user_group_tag |
| 游戏群标签 | 设置用户群标签 | SetUserGroupTag | POST | /apps/group_tag/set_user_group_tag |
| 游戏礼包 | 核销兑换码 | GiftReceiveReward | POST | /gift/receive_reward |
| 动态分享 | 生成活动ID | ShareCreateActivityId | GET | /apps/share/create_activity_id |
| 动态分享 | 更新动态消息 | ShareUpdateDynamicMessage | POST | /apps/share/update_dynamic_message |
| 公会群 | 公会群解绑 | ShareUnbindUnionGroup | POST | /apps/share/unbind_union_group |

所有 API 的 Scope 均为 `open.ttgame.mgplatform`。
