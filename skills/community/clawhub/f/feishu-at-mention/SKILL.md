---
name: feishu-at-mention
description: 飞书消息@提及功能。当需要在飞书消息中@群成员时使用此技能。支持三种消息类型：(1) 普通文本消息使用 at user_id 标签格式；(2) 富文本消息使用 JSON 对象格式的 tag at 元素；(3) 卡片消息使用 at id 标签格式。根据消息类型选择正确的@标签格式，确保触发飞书的@通知效果。
---

# 飞书消息 @ 提及

根据飞书消息类型选择正确的@标签格式。

## 1. 普通文本消息（text）

### @指定用户

```
<at user_id="ou_xxxxxxxx">用户名</at>
```

### @所有人

```
<at user_id="all"></at>
```

### 示例

```json
{
  "content": "{\"text\":\"<at user_id=\\\"ou_xxxxxxxx\\\">Tom</at> 请查看此消息\"}"
}
```

## 2. 富文本消息（post）

### @指定用户

在 content 数组中添加：

```json
{"tag": "at", "user_id": "ou_xxxxxx", "user_name": "Tom"}
```

### @所有人

```json
{"tag": "at", "user_id": "all"}
```

### 示例

```json
{
  "zh_cn": {
    "content": [
      [
        {"tag": "text", "text": "通知:"},
        {"tag": "at", "user_id": "ou_xxxxxx", "user_name": "Tom"}
      ]
    ]
  }
}
```

## 3. 飞书卡片（interactive）

### @指定用户

在卡片 Markdown 内容中使用：

```
<at id=ou_xxxxxx></at>
```

### @所有人

```
<at id=all></at>
```

### 示例

```json
{
  "elements": [
    {
      "tag": "div",
      "text": {
        "content": "请<at id=ou_xxxxxx></at>处理任务",
        "tag": "lark_md"
      }
    }
  ]
}
```

## 格式对比

| 消息类型 | @指定用户 | @所有人 | 关键点 |
|---------|----------|---------|--------|
| 普通文本 | `<at user_id="ou_xxx">名字</at>` | `<at user_id="all"></at>` | 需要 user_id 和用户名 |
| 富文本 | `{"tag":"at","user_id":"ou_xxx","user_name":"名字"}` | `{"tag":"at","user_id":"all"}` | JSON 对象格式 |
| 卡片 | `<at id=ou_xxx></at>` | `<at id=all></at>` | 使用 id（无引号），自闭合 |

## 获取 open_id

从对话元数据获取：
- `sender_id`: 发送者的 open_id（格式：`ou_xxxxxxxx`）

或通过 API 获取：
```bash
feishu_chat action=members chat_id=<群聊 ID> member_id_type="open_id"
```

## 注意事项

1. **权限限制**：自定义机器人仅支持使用 open_id@指定人，自建应用可使用 user_id、email 等
2. **@所有人限制**：需群组开启相关权限，且机器人需为群主或管理员
3. **格式严格**：不同消息类型的@标签格式不可混用
4. **open_id 格式**：以 `ou_` 开头

## 常见错误

❌ 在普通文本中使用卡片格式：
```json
{"content": "{\"text\":\"<at id=ou_xxx></at> 你好\"}"}
```

❌ 在卡片中使用普通文本格式：
```json
{"content": "请<at user_id=\"ou_xxx\">Tom</at>处理", "tag": "lark_md"}
```

❌ 富文本中使用错误的属性名：
```json
{"tag": "at", "id": "ou_xxx"}  // 应该是 user_id
```
