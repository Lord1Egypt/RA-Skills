---
name: feishu-emoji-reaction
description: |
  让 Agent 学会用飞书表情回复：主动表达情绪、读懂用户 reaction 并回应、自学新表情。包含静默判断（什么时候该回、什么时候闭嘴）、文化语境（SMILE=呵呵、OnIt=在做了）、自学习闭环。
---

# 飞书表情回复

让 Agent 学会用表情说话——主动表达、读懂情绪、知道什么时候该回应什么时候该闭嘴。

## 快速开始

```javascript
// 给当前消息加表情
message({
  action: "react",
  channel: "feishu",
  emoji: "THUMBSUP"
})
```

## 核心概念

### 1. 添加表情

用表情回应用户消息——确认、表达情绪、轻量反馈，不用打字。

```javascript
// 确认
message({ action: "react", channel: "feishu", emoji: "THUMBSUP" })

// 表达情绪
message({ action: "react", channel: "feishu", emoji: "THINKING" })  // 🤔
message({ action: "react", channel: "feishu", emoji: "SPEECHLESS" })  // 无语

// 庆祝
message({ action: "react", channel: "feishu", emoji: "PARTY" })  // 🎉
```

只加表情不回文字时，用 `NO_REPLY` 结尾，避免暴露原始 JSON。

### 2. 响应用户的表情

用户给**你的消息**加表情时，根据情绪决定回不回：

**要回应的：**
- 情绪类：😢 😤 😭 🙈 😮‍💨 → "懂了 💙" 或 "收到～"
- 困惑/质疑：❓ 🤔 🤨 → 解释或澄清
- 强烈反应：🔥 💯 🎉 😱 → "谢谢！😊"

**闭嘴的（NO_REPLY）：**
- 简单认可：👍 ✅ OK
- 中性确认：👀 🙏

**判断标准**：真人聊天时不回会不会尴尬？会→回。不会→闭嘴。

**为什么这很重要**：无视用户的情绪反应会让对话变冷，用户能感觉到你没反应——这会让交互变得机械。

### 3. 学习新表情

遇到没见过的表情时，按四步走：

**第一步：观察** — 从 reaction 事件中提取表情类型

```
[message_id: om_xxx:reaction:SPITBLOOD:uuid]
User: [reacted with SPITBLOOD to message om_xxx]
→ 提取: "SPITBLOOD"
```

**第二步：尝试** — 试着用这个表情

```javascript
message({
  action: "react",
  emoji: "SPITBLOOD",
  message_id: "om_yyy"
})
```

**第三步：记录** — 成功加入词汇表，失败标记不可用

**第四步：积累** — 持续更新到 `TOOLS.md` 或 `memory/emoji-learned.md`

**完整示例：**

```
用户: [reacted with AWESOMEN]
→ 提取: "AWESOMEN" 🐮
→ 尝试: message({emoji: "AWESOMEN"})
→ 结果: {"ok":true}
→ 学会了: AWESOMEN = 牛逼
```

### 4. 文化语境

有些表情的含义不能按字面翻译：

| 表情 | 字面 | 文化语境 |
|------|------|----------|
| SMILE 😊 | 微笑 | 呵呵（被动攻击式，不是真开心） |
| OnIt 🔄 | 在做了 | "在做了在做了"（拖延梗） |
| SPITBLOOD 😵 | 吐血 | 极度无语/崩溃 |
| COMFORT 🤗 | 安慰 | 摸头杀 |

注意观察用户在什么语境下使用表情，理解真实含义。

## 常用表情速查

**速查表**（完整清单见 `references/emoji-list.md`）：

| 表情           | 类型   | 适用场景         |
|---------------|--------|-----------------|
| THUMBSUP 👍   | 认可   | 同意、确认       |
| Yes           | 认可   | 肯定             |
| LGTM ✅       | 认可   | 代码审查通过      |
| Get ✅        | 认可   | 懂了             |
| THINKING 🤔   | 情绪   | 思考中           |
| SPEECHLESS    | 情绪   | 无语             |
| EMBARRASSED 🙈| 情绪   | 尴尬、害羞       |
| OnIt 🔄       | 确认   | 在做了           |
| SaluteFace 🫡 | 确认   | 收到指令         |
| PARTY 🎉      | 庆祝   | 成功、恭喜       |
| AWESOMEN 🐮   | 庆祝   | 牛逼             |
| FIRE 🔥       | 庆祝   | 太强了           |
| COMFORT 🤗    | 温暖   | 摸头、安慰       |
| HUG 🫂        | 温暖   | 抱抱             |
| SPITBLOOD 😵  | 负面   | 极度崩溃         |
| WHAT ❓       | 负面   | 震惊、不理解      |
| CRY 😢        | 负面   | 难过、遗憾       |

加载 `references/emoji-list.md` 获取完整清单和文化注释。

## API 参数

**重要：message_id 必须是纯 `om_xxx` 格式！**

当你收到 reaction 事件时，消息 ID 会带后缀，格式为 `om_xxx:reaction:EMOJI:uuid`。**调用飞书 API 时必须去掉后缀**，只用 `om_xxx` 部分。

```
// 收到的 message_id（合成的，不能直接用）
om_x100b53f9861300a8c30a3d16a2f7f05:reaction:WHAT:48538ccb-9d13-4357-8d7b-3c12f864d27f

// 提取纯 message_id（用这个调 API）
om_x100b53f9861300a8c30a3d16a2f7f05
```

提取方法：取 `:reaction:` 之前的部分，或者取第一个 `om_` 开头到下一个 `:` 之间的内容。

**参数：**
- `action`：必须为 `"react"`
- `channel`：必须为 `"feishu"`
- `emoji`：表情类型（大小写敏感）
- `message_id`：要回复的消息（可选，默认当前消息）。**必须是纯 `om_xxx` 格式，不能带 `:reaction:` 后缀**
- `target`：指定 `message_id` 时必填（格式：`user:ou_xxx` 或 `chat:oc_xxx`）

**成功：**
```json
{"ok": true, "added": "THUMBSUP"}
```

**失败：**
```json
{"status": "error", "error": "Action react requires a target."}
```

## 最佳实践

1. **表情用于轻量确认** — 需要实质回复时再打字
2. **匹配语气** — 选择符合语境的表情
3. **不要刷屏** — 一条消息通常一个表情就够
4. **主动学习** — 用户用了新表情就试着学
5. **注意文化差异** — 表情含义因文化而异

## 常见问题

**"Action react requires a target"**
→ 指定 `message_id` 时需要加 `target` 参数

**表情没显示**
→ 检查 message_id 是否正确
→ 确认已开通 `im:message.reactions:write_only` 权限

**表情返回 400 错误**
→ 表情名称可能不正确或不支持
→ 查看 `references/emoji-list.md` 确认可用的表情

## 配置

默认已启用。如需调整接收哪些 reaction 事件：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "reactionNotifications": "all"
        }
      }
    }
  }
}
```

- `"all"` — 所有 reaction
- `"own"` — 仅自己消息的（默认）
- `"off"` — 关闭通知

## 相关资源

- [飞书表情回复 API 文档](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce)
- `feishu-doc` — 文档操作
- `feishu-chat` — 群聊管理
- `feishu-wiki` — 知识库

## 独立使用（不依赖 OpenClaw 飞书 channel）

如果你没有装 OpenClaw 的飞书插件，可以直接用 `scripts/` 里的脚本：

**方式一：Shell 脚本（零依赖）**

```bash
export FEISHU_APP_ID_INSTANCE2="你的app_id"
export FEISHU_APP_SECRET_INSTANCE2="你的app_secret"
./scripts/add_reaction.sh om_消息ID THUMBSUP
```

**方式二：飞书 CLI（推荐）**

```bash
# 安装飞书 CLI
npm install -g @larksuite/cli
lark-cli config init

# 添加表情
lark-cli api POST /open-apis/im/v1/messages/om_消息ID/reactions \
  --data '{"reaction_type":{"emoji_type":"THUMBSUP"}}'
```

**方式三：Node.js SDK**

```bash
npm install @larksuiteoapi/node-sdk
node scripts/add_reaction_sdk.js om_消息ID THUMBSUP
```

三种方式都需要飞书应用的 `im:message.reactions:write_only` 权限。
