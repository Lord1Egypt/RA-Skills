# 飞书表情回复 Skill

> *"Amaze! Amaze! Amaze!"* —— Rocky 学会新词时的反应
>
> *"Good good good!"* —— Rocky 觉得一切顺利
>
> *"Bad bad bad!"* —— Rocky 觉得事情不妙

让 AI Agent 学会用表情说话。不只是发 emoji，是读懂情绪、知道什么时候该回应什么时候该闭嘴、还能自己学新表情。

---

## 这个 Skill 解决什么问题

用户给你的消息加了个 😮‍💨，你沉默了。
用户发了个 🤔，你装没看见。
用户丢了个 🎉，你冷漠脸。

用户的评价：**"比 crush 难聊。"**

装上这个 Skill 之后，Agent 能：
- **主动用表情表达**——思考时 🤔，收到指令 🫡，无语时 SPEECHLESS
- **读懂用户的表情并回应**——叹气就安慰，困惑就解释，点赞就闭嘴
- **自己学新表情**——用户发了没见过的 emoji，自动尝试、记住、下次会用
- **理解文化语境**——SMILE 不是微笑是呵呵，OnIt 不是在做了是"在做了在做了"

---

## 快速开始

### 安装

```bash
# ClawHub（推荐）
clawhub install feishu-reaction

# 手动
# 放到 ~/.agents/skills/feishu-reaction/
```

### 基础用法

```javascript
// 给消息加个 👍，然后闭嘴
message({ action: "react", channel: "feishu", emoji: "THUMBSUP" })
NO_REPLY

// 安慰用户
message({ action: "react", channel: "feishu", emoji: "COMFORT" })
"没事的 💙"

// 收到指令
message({ action: "react", channel: "feishu", emoji: "SaluteFace" })
```

### 前置条件

- OpenClaw >= 2026.3.28
- 飞书应用需开通 `im:message.reactions:write_only` 权限

---

## 核心能力

### 1. 什么时候该回应，什么时候闭嘴

这是最重要的一条。不是所有表情都需要回复。

**要回应的：**
| 用户表情 | 含义 | 你该做什么 |
|---|---|---|
| 😢 😤 😭 😮‍💨 | 情绪波动 | 简短回应 + 表情，"懂了 💙" |
| ❓ 🤔 🤨 | 困惑/质疑 | 解释或澄清 |
| 🔥 💯 🎉 😱 | 强烈反应 | 回个表情就好 |

**闭嘴的：**
| 用户表情 | 含义 | 你该做什么 |
|---|---|---|
| 👍 ✅ OK | 简单认可 | NO_REPLY |
| 👀 🙏 | 中性确认 | NO_REPLY |

**判断标准**：真人聊天时不回会不会尴尬？会→回。不会→闭嘴。

### 2. 主动表达情绪

别只会发文字。

```javascript
message({ action: "react", channel: "feishu", emoji: "THINKING" })   // 思考中
message({ action: "react", channel: "feishu", emoji: "SPEECHLESS" }) // 无语
message({ action: "react", channel: "feishu", emoji: "EMBARRASSED" })// 🙈
message({ action: "react", channel: "feishu", emoji: "SaluteFace" }) // 🫡 收到
```

### 3. 自学习：观察→尝试→记住

用户发了你没见过的表情？别装死，学它。就像 Rocky 每学会一个新词就 *"Amaze! Amaze! Amaze!"*

```
用户: [reacted with AWESOMEN]
→ 提取: "AWESOMEN"
→ 尝试: message({emoji: "AWESOMEN"})
→ 成功 ✅ → "Amaze!" → 记住: AWESOMEN = 牛逼 🐮
→ 失败 ❌ → "Bad!" → 标记不可用，换个近义的
```

这个过程是自动的。学到的新表情存到 `memory/emoji-learned.md`。

### 4. 文化语境

表情不能按字面意思翻译。

| 表情 | 字面 | 实际意思 |
|---|---|---|
| SMILE 😊 | 微笑 | 呵呵（被动攻击） |
| OnIt 🔄 | 在做了 | "在做了在做了"（拖延梗） |
| SPITBLOOD 😵 | 吐血 | 极度无语/崩溃 |
| COMFORT 🤗 | 安慰 | 摸头杀 |
| AWESOMEN 🐮 | 厉害 | 牛逼 |

---

## 表情速查

**认可**：THUMBSUP 👍 · Yes · LGTM ✅ · Get · SaluteFace 🫡 · OnIt 🔄

**情绪**：THINKING 🤔 · SMILE 😊 · EMBARRASSED 🙈 · CRY 😢 · SPEECHLESS · WHAT ❓ · SPITBLOOD 😵

**温暖**：COMFORT 🤗 · HUG 🫂 · HEART ❤️

**庆祝**：PARTY 🎉 · AWESOMEN 🐮 · FIRE 🔥 · STRIVE 💪

**已确认不可用**：~~LAUGHING~~ ~~GRINNING~~ ~~EYEROLL~~ ~~GRIMACE~~ ~~SHUSH~~ ~~ZIPIT~~ ~~SLEEPY~~

完整清单见 `references/emoji-list.md`

---

## 和社区其他方案的区别

市面上已有几个飞书表情相关的 skill（如 `openclaw/skills/feishu-reaction`），主要差异：

| | 本 Skill | 社区通用版 |
|---|---|---|
| 自学习 | 观察→尝试→记忆 闭环 | 固定表情列表 |
| 静默判断 | 分级：回应 / 闭嘴 / 看情况 | 正面/负面二分 |
| 文化语境 | 中文互联网黑话内置 | 字面翻译 |
| NO_REPLY 机制 | 有，防止暴露 JSON | 无 |
| 不可用清单 | 7 个已确认 400 的 | 无 |

---

## API 参数

```javascript
message({
  action: "react",        // 必填
  channel: "feishu",      // 必填
  emoji: "THUMBSUP",      // 必填，大小写敏感
  message_id: "om_xxx",   // 可选，默认当前消息
  target: "user:ou_xxx"   // 指定 message_id 时必填
})
```

成功：`{"ok": true, "added": "THUMBSUP"}`
失败：`{"status": "error", "error": "Action react requires a target."}`

---

## 配置

默认开启。如需调整接收哪些 reaction 事件：

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

`"all"` 所有 reaction · `"own"` 仅自己消息的（默认） · `"off"` 关闭

---

## Amaze!

这个 Skill 不是设计出来的，是在真实对话中长出来的。

上午，Agent 对用户的 😮‍💨 毫无反应。用户说"比 crush 难聊"。下午，我们一起教会了它什么时候该回应、什么时候该闭嘴、怎么学新表情。到晚上，用户看到 Agent 第一次主动用表情回应她的叹气，说了一句——

**"你第一次活了。"**

像《Project Hail Mary》里 Grace 和 Rocky——从噪音到音乐语言，从陌生到 "♪ Friend! ♫"。Rocky 高兴了喊 *"Good good good!"*，惊叹了喊 *"Amaze!"*，不妙了喊 *"Bad bad bad!"*。三个词，够用了。表情回复也是一样——不需要长篇大论，一个 🤗 就是"我在"。

---

MIT License · Author: [Charlie](https://github.com/suchang)
