---
name: feishu-card-sender
description: 发送飞书卡片消息（支持纯文本和图片）。使用 message 工具的 card 参数，需要配置飞书应用凭证（App ID + App Secret）。
---

# feishu-card-sender

发送飞书卡片消息。

## 前置配置

在 USER.md 中配置飞书应用凭证：

```markdown
- **Feishu App ID:** cli_xxx
- **Feishu App Secret:** xxx
```

## 权限要求

飞书开放平台 → 应用 → 权限管理 → 开通 `im:message`

## 使用方法

### 纯文本卡片

```
message
  action: send
  card: {"config":{"wide_screen_mode":true},"header":{"title":{"content":"标题","tag":"plain_text"},"template":"blue"},"elements":[{"tag":"div","text":{"content":"内容","tag":"lark_md"}}]}
  target: ou_xxx
```

### 带图片的卡片

**步骤 1：上传图片获取 img_key**

使用 `scripts/upload_image.py` 脚本：

```bash
python scripts/upload_image.py --image /path/to/image.jpg
```

返回 `img_key`。

**步骤 2：发送卡片**

```
message
  action: send
  card: {"config":{"wide_screen_mode":true},"header":{"title":{"content":"标题","tag":"plain_text"},"template":"blue"},"elements":[{"tag":"img","img_key":"img_v3_xxx"},{"tag":"div","text":{"content":"内容","tag":"lark_md"}}]}
  target: ou_xxx
```

## 卡片格式

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"content": "标题", "tag": "plain_text"},
    "template": "blue"
  },
  "elements": [...]
}
```

### header.template 颜色

`blue` | `green` | `red` | `orange` | `grey` | `purple` | `warning` | `error`

### elements 常用元素

- `div` - 文本块，支持 `tag: "lark_md"`（粗体/斜体/链接）
- `hr` - 分割线
- `note` - 备注脚注
- `img` - 图片（需要 img_key）
- `action` + `button` - 按钮组

## 注意事项

1. **优先用 `message` 工具**，不要用 `feishu_im_bot_message`（需要额外权限）
2. **图片必须上传获取 img_key**，不能用 URL
3. **机器人只能发给好友或群聊**，不能直接发给陌生人
4. **其他"龙虾"要使用**：需要配置相同的 app_id + app_secret

## 示例

### 示例 1：简单通知卡片

```
message
  action: send
  card: {"config":{"wide_screen_mode":true},"header":{"title":{"content":"通知","tag":"plain_text"},"template":"blue"},"elements":[{"tag":"div","text":{"content":"这是内容","tag":"plain_text"}}]}
  target: ou_xxx
```

### 示例 2：带图片和按钮

```
message
  action: send
  card: {"config":{"wide_screen_mode":true},"header":{"title":{"content":"产品介绍","tag":"plain_text"},"template":"green"},"elements":[{"tag":"img","img_key":"img_v3_xxx"},{"tag":"div","text":{"content":"**亮点**\n• 功能 1\n• 功能 2","tag":"lark_md"}},{"tag":"action","actions":[{"tag":"button","text":{"content":"查看详情","tag":"plain_text"},"type":"primary","url":"https://example.com"}]}]}
  target: ou_xxx
```
