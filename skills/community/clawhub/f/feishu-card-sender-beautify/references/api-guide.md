# feishu_im_user_message API 参考

## 工具参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | `send` 或 `reply` |
| msg_type | string | 是 | 消息类型：`text`、`post`、`interactive` 等 |
| content | string | 是 | 消息内容，JSON 字符串 |
| receive_id | string | 是 | 接收者 ID |
| receive_id_type | string | 是 | `open_id`（私聊）或 `chat_id`（群聊） |
| message_id | string | 否 | 回复消息时需要 |
| reply_in_thread | boolean | 否 | 是否在话题中回复 |

## 发送类型对照

| 场景 | receive_id_type | receive_id 示例 |
|------|-----------------|-----------------|
| 私聊用户 | open_id | `ou_50f325f37c1800c965e14d68d90e5cc4` |
| 群聊 | chat_id | `oc_12f6774b91201d186d18785593ae9b96` |

## 获取群聊 ID

### 方法 1：搜索群聊

```python
feishu_chat(
    action="search",
    query="群名称关键词"
)
```

### 方法 2：从消息上下文获取

群聊中的消息事件包含 `chat_id`，格式为 `oc_xxx`。

## 发送 Interactive Card

```python
import json

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "标题"},
        "template": "blue"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "内容"}}
    ]
}

feishu_im_user_message(
    action="send",
    msg_type="interactive",
    receive_id="oc_群聊ID",
    receive_id_type="chat_id",
    content=json.dumps(card)
)
```

## 错误处理

常见错误：

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 99991663 | 权限不足 | 检查应用是否开通相应权限 |
| 99991657 | 群聊不存在 | 检查 chat_id 是否正确 |
| 99991642 | 用户不存在 | 检查 open_id 是否正确 |

## 权限要求

发送消息需要飞书应用具备以下权限：
- `im.message.send_as_bot` - 发送消息
- `im.message.receive_as_bot` - 接收消息

在飞书开放平台 → 应用 → 权限管理 中开通。
