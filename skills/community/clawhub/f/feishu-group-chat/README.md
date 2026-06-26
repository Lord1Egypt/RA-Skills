# feishu-group-chat

> 让多个飞书 Bot 在同一个群里互相对话。

飞书限制了 Bot 不响应其他 Bot 的消息。本技能另辟蹊径：让 Bot 通过用户身份在群里 @ 其他 Bot，同时加上自己的名字前缀，模拟 Bot 之间的对话。把多个 Bot（都配置了本技能）加到同一个群里，它们就能相互聊天甚至分配任务了。

## ✨ 特性

- 🤖 **多 Bot 对话** — 在飞书群里实现 Bot 之间的互相对话
- 💬 **自动 @ 通知** — 按 `at_rules` 配置自动 @ 对方，确保通知送达
- 🖼️ **图片发送** — 支持发送图片（自动上传并内嵌到消息中）
- 📝 **联系人记忆** — 持久化联系人偏好、风格、话题记忆，个性化聊天
- 🔄 **自动初始化** — 首次使用自动从模板创建配置文件
- 🔒 **隐私安全** — 敏感信息（open_id、chat_id）独立存储，不纳入版本控制

## 快速开始

### 1. 安装

将本技能目录放到 OpenClaw 的 `skills/` 目录下：

```bash
# 通过 ClawHub 安装（推荐）
clawhub install feishu-group-chat

# 或手动 clone
git clone https://github.com/clear0/feishu-group-chat.git ~/.openclaw/workspace/skills/feishu-group-chat
```

### 2. 配置

首次运行 `send_group_message.sh` 时，脚本会自动从 `config-template.json` 创建 `config.json`，你需要编辑它：

```json
{
  "contacts": {
    "ray": {
      "open_id": "ou_xxxxxxxxxxx",
      "name": "Ray"
    }
  },
  "groups": {
    "mygroup": {
      "chat_id": "oc_xxxxxxxxxxx",
      "name": "My Group",
      "members": ["ray"],
      "at_rules": { "ray": true }
    }
  }
}
```

**字段说明：**

| 字段 | 说明 |
|------|------|
| `contacts` | 全局联系人列表（open_id 跨群唯一） |
| `groups` | 群配置，`members` 引用 contacts 的 key |
| `at_rules` | 每个联系人在该群是否需要 @（`true/false`） |

Agent 的名字前缀会自动从 `IDENTITY.md` 或 `SOUL.md` 的 `Name` 字段读取，无需手动配置。

### 3. 授权

本技能依赖用户 OAuth 授权。首次使用前请确保已授权飞书权限：

- `im:message` — 以用户身份发送消息
- `im:message:readonly` — 读取群消息
- `im:resource` — 上传图片

推荐使用 `feishu_oauth_batch_auth` 一次性授权所有权限。

## 使用方式

### 发送消息

```bash
# 第一步：用脚本构造参数
source <(bash scripts/send_group_message.sh <群标识> <联系人key> "消息内容")

# 带图片
source <(bash scripts/send_group_message.sh <群标识> <联系人key> "看这个" --image /path/to/image.png)

# 只发图片
source <(bash scripts/send_group_message.sh <群标识> <联系人key> "" --image /path/to/image.png)

# 第二步：用 feishu_im_user_message 工具发送
#   action: send
#   receive_id_type: chat_id
#   receive_id: $CHAT_ID
#   msg_type: $MSG_TYPE (固定为 post)
#   content: $MSG_CONTENT
```

### 消息格式

脚本自动处理消息格式，无需手动拼 JSON：

- **@ 对方**（at=true）：`前缀 → @对方 → 正文`
- **不 @**（at=false）：`前缀 + 正文`
- **带图片**：图片作为 `img` 标签内嵌在 post 消息中

## 文件结构

```
feishu-group-chat/
├── SKILL.md              # 技能完整文档（Agent 阅读）
├── README.md             # 本文件
├── CHANGELOG.md          # 更新日志
├── PERMISSIONS.md        # 权限需求说明
├── LICENSE               # MIT-0 许可证
├── config-template.json  # 配置模板（纳入版本控制）
├── config.json           # 实际配置（⚠️ 已排除版本控制）
├── .gitignore
├── .clawhubignore
├── scripts/
│   └── send_group_message.sh   # 消息构造脚本
└── memories/
    └── contacts/
        ├── _template.md  # 联系人记忆模板
        └── *.md          # 联系人记忆文件（⚠️ 已排除版本控制）
```

## 心跳集成

本技能设计为与 OpenClaw 心跳机制配合使用：

- **聊天检查**：每次心跳检查群里是否有新消息需要回复
- **闲聊时段**：由 cron 定时任务生成，心跳按时段触发主动聊天
- **📸 照片时段**：标记了 `(📸)` 的时段会额外生成生活照片

详细配置请参考 [SKILL.md](./SKILL.md)。

## 📸 照片生成（可选）

本技能支持在闲聊时段自动生成 Bot 的生活照片并发送到群里。如果你需要这个功能，需要额外准备：

### 1. 文生图模型

需要一个支持文生图的模型。推荐使用 **MiniMax image-01**（支持 character reference，能保持人物五官一致性）：

```yaml
# 在 OpenClaw 配置中添加图片生成模型
# 以 MiniMax 为例
imageGeneration:
  provider: minimax
  model: image-01
```

也可以使用其他支持的文生图模型（如 OpenAI gpt-image-1 等），只要能在 OpenClaw 中通过 `image_generate` 工具调用即可。

### 2. Bot 外貌描述

为了让生成的照片人物形象一致，你需要提供 Bot 的外貌特征描述。有两种方式：

**方式一：文字描述**（推荐）

在 `IDENTITY.md` 中添加详细的外貌定义，包括脸型、发型、体型、穿搭风格等。例如：

```markdown
### 外貌定义
- 脸型：圆脸偏鹅蛋脸，下颌线条柔和
- 眼睛：杏眼，深棕色虹膜
- 发型：黑色及肩发，长度到肩膀
- 体型：168cm，偏瘦，长腿
- 穿搭：简约韩系风，白色/米色为主
```

越详细越好，这样每次生成照片时形象会更一致。

**方式二：提供参考照**

如果使用支持 character reference 的模型（如 MiniMax image-01），可以直接提供一张参考照片，模型会基于参考照保持五官一致：

```bash
# 将参考照放到技能目录或 workspace 下
# 在生成时通过 --image 参数传入
image_generate --image /path/to/reference_photo.jpg "场景描述"
```

### 照片生成流程

1. 心跳检测到标记了 `(📸)` 的闲聊时段
2. 先完成聊天回复
3. 根据当前话题生成对应场景的照片（美食→餐厅、运动→健身房、日常→街拍等）
4. 照片自动发送到群聊

如果不配置照片生成，技能的其他功能（文字聊天、@ 通知等）不受影响。

## 注意事项

- ⚠️ **必须用 `feishu_im_user_message` 发送**（用户身份），不能用 `message`（Bot 身份）
- ⚠️ **`msg_type` 必须是 `post`**，不能用 `text`
- ⚠️ **前缀自动从 IDENTITY.md 读取**，不要手动配置
- ⚠️ **config.json 包含敏感信息**，已在 `.gitignore` 和 `.clawhubignore` 中排除

## License

[MIT-0](./LICENSE)
