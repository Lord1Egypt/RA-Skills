# Feishu Messenger Skill

飞书消息发送技能 - 支持文本、图片、文件发送。

## 快速使用

```bash
# 文本消息
openclaw message send --channel feishu --target ou_xxx --message "Hello"

# 图片（使用相对路径）
openclaw message send --channel feishu --target ou_xxx --media ./image.png

# 文件
openclaw message send --channel feishu --target ou_xxx --media ./file.pdf
```

## 关键点

- ✅ 使用 `./` 相对路径
- ❌ 不要用绝对路径 `/tmp/xxx`
- ❌ 不要用 `~` 路径

完整文档见 `SKILL.md`。
