# 卡片模板示例

## 基础卡片

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 标题"},
        "template": "blue"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "正文内容"}}
    ]
}
```

## 多段落卡片（带分割线）

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📊 每日报告"},
        "template": "green"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "**今日收益：**+1.5%\n**持仓：**10支基金"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": "💡 建议：当前处于黄金坑位置，建议加仓"}}
    ]
}
```

## 按钮卡片

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "🔔 确认通知"},
        "template": "blue"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "请确认以下操作："}},
        {"tag": "action", "actions": [
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "确认"},
                "type": "primary",
                "url": "https://example.com/confirm"
            },
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "取消"},
                "type": "default",
                "url": "https://example.com/cancel"
            }
        ]}
    ]
}
```

## 内容格式

支持 Lark MD 语法：

| 语法 | 效果 |
|------|------|
| `**文字**` | 粗体 |
| `*文字*` | 斜体 |
| `~~文字~~` | 删除线 |
| `\n` | 换行 |
| `---` | 分割线（需单独一行） |
| `•` | 列表项 |
| `[文字](链接)` | 链接 |

## 完整示例：基金日报

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📈 每日基金报告"},
        "template": "blue"
    },
    "elements": [
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**📊 收益概况**\n今日收益：+1.5%\n持仓收益：+8.7%\n\n**💰 持仓明细**\n• 债券基金：60%\n• 沪深300：20%\n• 纳指：10%\n• 恒生科技：5%\n• 机器人：5%"}
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**💡 操作建议**\n当前处于黄金坑位置，建议定投加仓\n\n**📅 明日提示**\n• 9:00 基金分析\n• 14:00 科普推送"}
        }
    ]
}
```
