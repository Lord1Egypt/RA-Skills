---
name: feishu-card-sender-beautify
description: |
  发送飞书 Interactive Card 格式消息，用于美化富文本卡片推送和优化通知。
  触发条件：(1) 用户要求发送卡片消息 (2) 定时任务推送 (3) 格式化通知需求
---

# feishu-card-sender-beautify

发送飞书 Interactive Card 富文本消息。

## 快速开始

### 发送卡片到当前聊天

使用 `feishu_im_user_message` 工具：

```python
feishu_im_user_message(
    action="send",
    msg_type="interactive",
    receive_id="oc_群聊ID",  # 群聊用 oc_xxx
    receive_id_type="chat_id",
    content=json.dumps(card)
)
```

### 卡片结构

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 标题"},
        "template": "blue"  # blue/red/green/yellow/wathet/orange/grey
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "正文内容"}}
    ]
}
```

## 颜色模板

| 值 | 颜色 |
|---|------|
| blue | 蓝 |
| red | 红 |
| green | 绿 |
| yellow | 黄 |
| wathet | 浅蓝 |
| orange | 橙 |
| grey | 灰 |

## 详细文档

- [卡片模板](references/card-templates.md) - 完整模板示例
- [API 参考](references/api-guide.md) - feishu_im_user_message 详细参数

## 注意

- 群聊 ID 格式：`oc_xxx`
- 用户 ID 格式：`ou_xxx`
- 发送群聊用 `receive_id_type="chat_id"`
- 发送私聊用 `receive_id_type="open_id"`
