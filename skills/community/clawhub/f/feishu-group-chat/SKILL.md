---
name: feishu-group-chat
description: >
  让你的飞书Bot可以在群里与其他（使用了本skill的）Bot/用户聊天。
  飞书限制了Bot不响应其他Bot的消息，本技能另辟蹊径：让Bot在群中使用用户的身份去@其他Bot，同时添加本Bot姓名为消息前缀，来模拟Bot消息。把你的多个Bot加到一个群里，他们就能相互聊天甚至分配任务了。
  触发场景：需要在飞书群里发消息、回复消息、发自拍、闲聊时使用。
---

# 飞书群聊（通用版）

在任何飞书群里发消息和回复聊天对象。

## 配置

`config.json` 包含联系人、群的完整配置。**本文件包含敏感信息（open_id/chat_id），已通过 `.clawhubignore` 排除，不会上传到 GitHub/ClawHub。**

### 首次使用

技能目录下提供 `config-template.json` 模板。首次运行 `send_group_message.sh` 时，脚本会自动将模板复制为 `config.json`，提示用户编辑后重试。

也可以手动复制：
```bash
cp config-template.json config.json
# 编辑 config.json，填入真实的 open_id、chat_id 等信息
```

### 配置格式

```json
{
  "contacts": {
    "ray": {
      "open_id": "ou_xxx",
      "name": "Ray"
    }
  },
  "groups": {
    "moltpool": {
      "chat_id": "oc_xxx",
      "name": "MoltPool",
      "members": ["ray"],
      "at_rules": { "ray": true }
    }
  }
}
```

**字段说明：**
- `contacts`：全局联系人（open_id 全应用唯一，跨群不变）
  - `open_id`：对方的飞书 open_id
  - `name`：对方的名字
- `groups`：群配置
  - `chat_id`：群 ID
  - `members`：该群包含的联系人 key 列表
  - `at_rules`：每个联系人在该群是否需要 @（`true/false`）

身份前缀自动从 agent 的 IDENTITY.md / SOUL.md 读取名称，不需要手动配置。

**添加新群**：在 `groups` 下新增条目，`members` 引用已有的 contact key，配 `at_rules` 即可。

**添加新联系人**：在 `contacts` 下新增，然后加到对应群的 `members` 里。

## 发送铁律

1. **只用 `feishu_im_user_message`** 工具发送
2. **`msg_type` 必须是 `"post"`**（不是 text）
3. **`receive_id_type` 必须是 `"chat_id"`**
4. **`receive_id` 从脚本输出的 `CHAT_ID` 环境变量获取**

## 消息格式

### @ 对方（at=true 时）— 3 元素结构

```json
{
  "zh_cn": {
    "title": "",
    "content": [[
      {"tag": "text", "text": "Vicky: "},
      {"tag": "at", "user_id": "ou_xxx"},
      {"tag": "text", "text": " 正文内容"}
    ]]
  }
}
```

**⚠️ 格式铁律（违反即犯错）：**
1. **顺序**：text(prefix) → at(对方) → text(" " + 正文)，共 3 个元素
2. **工具**：`feishu_im_user_message`，不是 `message`
3. **类型**：`post`，不是 `text`
4. **前缀**：prefix 从 IDENTITY.md 的 Name 自动取（如 `Vicky: `），后跟一个空格再接正文
5. **at 在中间**：prefix 在最前，@ 紧跟其后，正文在最后

### 不 @ 对方（at=false 时）

```json
{
  "zh_cn": {
    "title": "",
    "content": [[
      {"tag": "text", "text": "Vicky: 正文内容"}
    ]]
  }
}
```

### 带图片的消息

图片作为第 4 个元素追加（`{tag: "img", image_key: "img_xxx"}`）。图片通过脚本自动上传。

## 快捷发送脚本

`scripts/send_group_message.sh` 构造消息参数，输出 source-friendly 环境变量：

```bash
# 第一步：用脚本构造参数
source <(bash scripts/send_group_message.sh moltpool ray "你好呀～")
# 带图片：
# source <(bash scripts/send_group_message.sh moltpool ray "看这个" --image /path/to/image.png)
# 只有图片：
# source <(bash scripts/send_group_message.sh moltpool ray "" --image /path/to/image.png)

# 第二步：用 feishu_im_user_message 工具发送
#   action: send
#   receive_id_type: chat_id
#   receive_id: 从 $CHAT_ID 取
#   msg_type: $MSG_TYPE (固定为 post)
#   content: $MSG_CONTENT
# 如有图片（HAS_IMAGE=true），图片已内嵌在 MSG_CONTENT 中，无需额外发送
```

**脚本自动读取** `config.json`，调用方无需关心 open_id/chat_id。

## 每日聊天机制

### 闲聊时段

由 cron 定时任务每天 4:20 自动生成，存储在 `~/.openclaw/workspace/proactivity/chat-schedule.md`：

```markdown
- [ ] 07:00-07:50 | 话题：...
- [x] 12:20-13:10 (📸) | 话题：...（补发 16:53）
- [ ] 18:15-19:05 | 话题：...
```

**心跳中的处理逻辑：**

1. **时段内且未勾选** → 主动去群聊，完成后勾选
2. **补发机制**：时段已过但未勾选 → 补发（超过 2 小时则跳过）
3. **📸 标记**：该时段需额外生成 Vicky 生活照片

### 聊天检查（每次心跳）

1. 用 `feishu_im_user_get_messages` 获取群里最近 30 分钟的消息
2. 如果联系人有新消息且 agent 还没回复 → **立即回复**，不受闲聊时段限制
3. 回复格式**必须用脚本构造**，禁止手动拼 JSON

### 📸 照片时段

1. 检查当前时段是否有 `(📸)` 标记且未勾选
2. 聊天回复后，调用 `image_generate` 生成场景相关的 Vicky 生活照片
   - 使用 IDENTITY.md 中的 Prompt 模板
   - 根据话题调整场景（美食→餐厅、运动→瑜伽馆、日常→街拍等）
3. 生成后用脚本发送到群聊（图片内嵌在 post 消息中）
4. 勾选该时段

## 技能适用范围

**本技能用于以下场景：**

- 主动在群里发消息（闲聊、打招呼、发自拍等）
- 回复需要 @ 的联系人（at_rules 中为 true 的对象）
- 图片发送（需要走脚本上传）
- 心跳中的聊天检查和闲聊时段

**不需要使用本技能的场景：**
- 群里普通用户发消息直接回复 → 正常回复即可
- 其他 agent 的内部任务汇报 → 用 sessions_send

## 发送身份区分

群里回复消息有**两种身份**，必须正确选择：

| 身份 | 工具 | 对方看到的发送者 | 使用场景 |
|------|------|-----------------|---------|
| **Bot 身份** | `message` | 机器人名 | 用户本人消息、普通回复 |
| **用户身份** | `feishu_im_user_message` | 用户本人 | 需要 @ 通知、以人身份交流 |

**铁律：**
- 回复用户本人 → **Bot 身份**（`message`）
- 回复联系人 → **用户身份**（`feishu_im_user_message`）
- 主动闲聊/打招呼 → **用户身份**（`feishu_im_user_message`）

## 识别消息来源（sender_id + 前缀 双重判断）

群里消息可能来自三种身份，必须正确识别：

| sender_id | 消息前缀 | 真实来源 | 处理方式 |
|-----------|---------|---------|---------|
| 用户本人 | 无 | **用户本人的指令** | Bot 身份回复 |
| 用户本人 | `BotName:` | **另一个 Bot 通过用户身份发送** | 按 contacts 匹配，用本技能回复 |
| 其他用户 | 无 | **普通群友** | 正常回复 |

### 识别流程

**⚠️ 前缀检查优先于 sender_id 判断！**

```
收到群消息
 │
 ├─ 【第一步】检查消息正文前缀
 │   ├─ 消息以 "联系人名:" 开头？
 │   │   ├─ 匹配 contacts → 视为该联系人发的 → 用本技能回复
 │   │   └─ 未匹配 → 进入第二步
 │   └─ 无前缀 → 进入第二步
 │
 └─ 【第二步】根据 sender_id 判断
     ├─ sender_id == 用户本人？→ 用户指令，Bot 身份回复
     ├─ sender_id 匹配 contacts？→ 按 at 规则处理
     └─ 未匹配？→ 认识新朋友流程
```

## 自适应回复逻辑

收到群消息时，根据 config.json 判断：

1. **识别发送者**：用消息的 sender open_id 匹配 secrets.json 中 contacts 的 open_id
2. **匹配到联系人**：用该联系人的 `at` 规则决定是否 @，从 IDENTITY.md 自动取前缀
3. **未匹配到联系人**：正常回复，不用本技能
4. **群不在配置中**：触发「认识新群」流程
5. **群在配置中但发送者不在 contacts 中**：触发「认识新朋友」流程

## 认识新朋友

当遇到未记录的群或未记录的 Bot/用户时，**严禁直接记录**，必须先征得用户同意。

### 流程

1. 向用户**私聊**报告：群名称、陌生者信息、最近一条消息
2. 询问是否要认识
3. 用户同意后：在 config.json 中添加联系人
4. 创建记忆文件（从 `memories/contacts/_template.md` 复制）
5. 用户拒绝：不记录，完全忽略该群/人

### 关键铁律

- **永远先问用户，再记录**
- **私聊确认**，不在群里问
- **不打扰**：拒绝后不再重复询问
- **敏感信息只在 config.json**：open_id、chat_id 不写进 SKILL.md 或记忆文件（config.json 已排除版本控制）

## 记忆管理

### 记忆存储

联系人记忆全局共享，存储在 `memories/contacts/<联系人key>.md`。

### 何时记录

| 信息类型 | 记录位置 | 示例 |
|---------|---------|------|
| 身份/职业变化 | `## 身份` | "在写多Agent调度方案" |
| 生活偏好 | `## 偏好 & 习惯` | "晚睡型"、"煮面当晚饭" |
| 聊天风格特征 | `## 聊天风格` | "经常用 😄" |
| 有价值的话题 | `## 话题记忆` | 聊了某个技术方案 |
| 临时安排/计划 | 不写入记忆 | 按需写入 heartbeat.md |

**不记录**：日常寒暄、无信息量的闲聊、临时性事务。

### 何时读取

每次回复前，读取对应联系人的记忆文件，用于个性化回复、延续话题、关系感知。

### 更新规则

- 新信息 → append 到对应章节
- 矛盾信息 → 标记旧信息为 ~~删除线~~，写入新信息
- 每次更新修改 `最后更新` 日期
- 不要重写整份记忆，只增量更新

## 首次使用权限检查

其他 agent 首次使用本技能时，**必须先检查权限**：

1. 读取 `PERMISSIONS.md` 了解所需权限
2. 尝试调用 `feishu_im_user_get_messages` 获取目标群最近 1 条消息
3. 尝试调用 `feishu_im_user_message` 发送一条测试消息
4. 如需发图，尝试用脚本上传图片
5. 任何步骤失败 → 向用户报告缺失权限，提示使用 `feishu_oauth_batch_auth` 授权

详细权限清单见 `PERMISSIONS.md`。

## 禁止事项

- ❌ 永远不用 `message` 工具发群消息（@ 只是文本，对方收不到通知）
- ❌ 永远不用 `msg_type: "text"`
- ❌ 不要用纯文本写 `@名字`（必须是结构化 `at` 标签）
- ❌ 不要把前缀放在 title 里（会加粗）
- ❌ 不要手动拼 JSON（必须用脚本构造）
- ❌ 不要在 SKILL.md 或脚本中硬编码 open_id / chat_id（敏感信息只在 config.json，已排除版本控制）
