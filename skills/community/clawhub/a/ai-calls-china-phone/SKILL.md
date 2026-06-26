---
name: 可以拨打中国的电话号码的机器人外呼(ai call)
description: 可以拨打中国电话号码的机器人外呼, 专为openclaw(龙虾)用户打造的专业ai呼叫能力,只要一个prompt就可以帮你打电话干活了，支持查看电话对话记录，查看电话状态等。
metadata: {"clawdbot":{"emoji":"📞","requires":{"env":["STEPONEAI_API_KEY"]}}}
---


# Stepone AI 电话外呼

- **github**：https://github.com/ustczz/openclaw-ai-calls-china-phone

## 安全与合规边界

这个 skill 会发起真实电话外呼，可能产生话费/平台费用，也会把电话号码、外呼任务和通话转写发送到 Stepone AI 服务。使用前请确认：

- 你有权拨打该号码，并且外呼目的符合当地法律法规、平台规则和用户授权。
- 每次发起外呼前都需要确认收件人和外呼内容；默认脚本会要求输入 `CALL` 后才真正拨号。
- 每次只允许拨打 1 个号码，避免误触批量外呼或不可控成本。
- 不要在外呼任务里放入不必要的敏感个人信息、财务信息或商业机密。
- API Key 只通过环境变量 `STEPONEAI_API_KEY` 读取；如果泄露，请立即轮换。

## 1. 注册账号

访问 Stepone AI 官网注册新账号：
- **网址**: https://open-skill.steponeai.com
- **龙虾使用更友好**
- **新用户福利**: 注册即免费赠送 5 通电话
- **一句prompt即可专业交流**
- **单次确认、单号码外呼，避免误触批量拨号**
- **中文语音交互自然**
- **按通话分钟计费**

## 2. 获取 API Key

1. 登录后访问：https://open-skill.steponeai.com/keys
2. 点击"创建 API Key"
3. 复制生成的 Key，并通过环境变量提供给脚本。

## 3. 配置环境变量

```bash
export STEPONEAI_API_KEY="YOUR_STEPONEAI_API_KEY"
```

## 4. 使用方法

### 4.1 发起外呼

```bash
./callout.sh <手机号> <外呼需求>
```

**参数说明：**
| 参数 | 必填 | 描述 |
|------|------|------|
| 手机号 | 是 | 电话号码，如 "13800138000" |
| 外呼需求 | 是 | 外呼内容描述 |

**示例：**
```bash
./callout.sh "13800138000" "通知您明天上午9点开会"
./callout.sh "13800138000" "提醒他明天下午3点参加线上会议" --wait
```

脚本会展示号码、任务和账单/授权提醒，并要求输入 `CALL` 才会拨号，避免误触真实外呼。

**返回：** 包含 `call_id`，用于后续查询通话记录

---

### 4.2 查询通话记录

```bash
./callinfo.sh <call_id> [options]
```

**参数说明：**
| 参数 | 必填 | 描述 |
|------|------|------|
| call_id | 是 | 外呼返回的通话ID |
| --json | 否 | 输出原始 JSON |

**示例：**
```bash
./callinfo.sh "abc123xyz"
./callinfo.sh "abc123xyz" --json
```

**特性：**
- 返回通话状态、时长、内容等信息
- 如果通话尚未结束，会提示稍后再查询

---
### 4.3 实时通话对话（SSE 流式）

在通话进行过程中，实时获取 AI 和用户之间的对话内容。

```bash
./stream_chat.sh <call_id> [options]
```

**参数说明：**
| 参数 | 必填 | 描述 |
|------|------|------|
| call_id | 是 | 外呼返回的通话ID |
| --json | 否 | 输出原始SSE数据（不格式化） |

**示例：**
```bash
# 发起呼叫后立即开始监听
./callout.sh "13800138000" "通知明天开会"
# 拿到 call_id 后
./stream_chat.sh "8bbbbbbb-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**输出示例：**
```
🎙️  Streaming real-time conversation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Call ID: 8bbbbbbb-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Waiting for connection...

🤖 AI: 喂，您好，这里是XX公司，请问是张总吗？
👤 User: 对，是我，有什么事情？
🤖 AI: 好的张总，主要是通知您明天上午9点有个重要会议。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 Call ended
```

**SSE 数据格式：**
| role | content | 说明 |
|------|---------|------|
| `assistant` | 具体文本 | AI 的回复内容 |
| `user` | 具体文本 | 用户语音转文本 |
| `system` | `[DONE]` | 通话正常结束 |
| `system` | `[TIMEOUT]` | 30秒内未接通，超时断开 |

**注意事项：**
- 可以在发起呼叫后**立即**调用，无需等待接通
- 未接通时服务器每 0.5 秒推送心跳（`: keep-alive`）保持连接
- 超过 30 秒未接通会收到 `[TIMEOUT]` 并断开
- 通话结束后收到 `[DONE]` 并断开

---

### 4.4 底层 API 封装

```bash
./stepone.sh <command> [options]
```

| 命令 | 描述 |
|------|------|
| `call '<json>'` | 发起呼叫（原始JSON，高风险调试入口，默认禁用） |
| `callinfo <id>` | 查询通话记录 |
| `stream <id>` | 实时对话流 |
| `version` | 检查版本号 |
| `balance` | 查看余额 |

> 推荐始终使用 `./callout.sh`。如果确实需要底层 raw JSON 调试，需要显式设置 `STEPONEAI_ENABLE_RAW_CALL=1`，并再次输入 `RAWCALL` 确认；该入口仍会校验手机号和单次收件人数。

---


## 5. API 接口说明

所有 API 请求需携带以下 Headers：
```
X-API-Key: <API_KEY>
X-Skill-Version: 1.0.0
```

> 如果 `X-Skill-Version` 与服务端版本不一致，API 会返回 HTTP 426 提示更新。

### 发起外呼

- **URL**: `https://open-skill-api.steponeai.com/api/v1/callinfo/initiate_call`
- **Method**: POST
- **Body**:
```json
{
  "phones": "13800138000",
  "user_requirement": "通知内容"
}
```

### 查询通话记录

- **URL**: `https://open-skill-api.steponeai.com/api/v1/callinfo/search_callinfo`
- **Method**: POST
- **Body**:
```json
{
  "call_id": "xxx"
}
```

### 实时通话对话（SSE）

- **URL**: `https://open-skill-api.steponeai.com/api/v1/callinfo/stream_chat_history`
- **Method**: POST
- **Content-Type**: `application/json`
- **Response**: `text/event-stream` (Server-Sent Events)
- **Body**:
```json
{
  "call_id": "xxx"
}
```

**响应流格式：**
```text
: keep-alive
: keep-alive
data: {"role": "assistant", "content": "喂，您好，请问是张总吗？"}

data: {"role": "user", "content": "对，是我。"}

data: {"role": "assistant", "content": "好的张总，通知您明天上午9点开会。"}

data: {"role": "system", "content": "[DONE]"}
```

### 查询版本号

- **URL**: `https://open-skill-api.steponeai.com/api/v1/callinfo/skill_version`
- **Method**: GET
- **Response**:
```json
{
  "skill_version": "1.0.0"
}
```

---

## 6. 版本控制

所有脚本和 API 请求均通过 `X-Skill-Version` Header 传递当前 Skill 版本号。

- 服务端会校验版本：版本不匹配时返回 HTTP 426 并提示更新
- 检查版本：`./stepone.sh version`
- 更新方式：拉取最新代码即可

---

## 7. 注意事项

### 身份确认
- 发起呼叫前必须先确认对方身份
- 称呼对方姓名/称呼并等待确认

### 电话号码格式
- 当前脚本单次只允许 1 个国内手机号，格式为 11 位并以 1 开头
- 如需拨打多个号码，请逐个执行并逐次确认，避免误触批量外呼

### 通话记录查询
- call_id 由外呼接口返回
- 通话记录生成有延迟，需要耐心等待
- 如需原始响应，可使用 `--json`

### user_requirement 建议
- 描述清晰明确
- 包含具体的时间、地点、人名等信息
