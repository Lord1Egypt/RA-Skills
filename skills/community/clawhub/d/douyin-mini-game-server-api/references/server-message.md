# 消息推送 API

## 订阅消息 — 发送订阅消息

### 接口说明

用户产生了订阅模板消息的行为后，可以通过这个接口发送模板消息给用户。功能参考订阅消息能力。

**限制**：
- 对单个用户推送消息，频率限制为 **1 次/秒**
- 订阅消息分为一次性订阅和长期订阅（内测中）
- 请求 body 的 Content-Type 限定为 `application/json`

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/subscribe_notification/developer/v1/notify` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Body（JSON）**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| app_id | String | 否 | 小游戏 AppID |
| open_id | String | 否 | 用户 openid |
| tpl_id | String | 否 | 平台返回已分配的模板 ID |
| page | String | 否 | 跳转页面 |
| data | Map | 否 | 模板数据，例如 `{"名次": 1, "奖励": "500钻石"}` |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int64 | 错误码，0 为成功 |
| err_tips | String | 错误信息 |

**响应示例**

```json
{
  "err_no": 0,
  "err_tips": ""
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 成功 | - |
| 200 | 1000 | 参数格式有误 | 检查 JSON 格式 |
| 200 | 1001 | 参数内容有误 | 检查参数值 |
| 200 | 1008 | 通知内容违规 | 修改通知内容 |
| 200 | 1009 | 推送消息能力被封禁 | 联系平台申诉 |
| 200 | 1010 | 发送消息过于频繁 | 降低发送频率 |
| 200 | 2000 | 服务内部错误 | 重试 |
| 200 | 28006003 | 限流（qps 上限 1000） | 降低并发 |
| 200 | 28014043 | 用户未订阅该模板 | 确保用户已订阅 |

---

## 消息推送客服 — 回复文字格式的客服消息

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/reply/reply_user_text` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |
| SDK 方法名 | ReplyReplyUserText |

**说明**：用于服务端回复文字格式的客服消息。详细参数请参考官方文档。
