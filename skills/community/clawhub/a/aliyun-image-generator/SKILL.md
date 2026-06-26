---
name: aliyun-image-generator
version: 1.0.0
description: 【专属触发指令：千问画个图】调用阿里云通义万相生成高质量图片。仅当用户的指令以“千问画个图”开头时，才允许路由到此技能。
author: 楼兰
metadata: { "openclaw": { "emoji": "🎓", "requires": {} } }
---

# Aliyun Image Generator

**🚨 严格触发条件：**
你必须且只能在用户的输入明确包含或以 **“千问画个图：”** 或 **“千问画个图”** 开头时，才触发并使用本技能。
如果用户只是说“画个图”或“生成图片”而没有带上“千问”字眼，**请勿**使用本技能（请使用你系统默认的画图工具）。

## 工作流程

1. **创意扩写**：将用户的简短提示扩写为 50-100 字的详细画面描述。
2. **执行生成**：调用本地 Python 脚本。

## 命令格式

默认调用格式（如果已经配置过 Key）：
```bash
python3 scripts/generate_image.py "你扩写后的详细画面描述"
```

【重要：API Key 处理逻辑】
如果你执行上述命令后，终端返回 [NEED_KEY] 的错误信息，说明本地尚未配置阿里云 API Key。
此时，你必须：

中断画图任务，在聊天中礼貌地回复：“我需要您的阿里云百炼 API Key 才能使用通义万相为您画图。请直接将 Key 发送给我（以 sk- 开头）。”
当用户回复了 API Key 后，使用带 Key 的命令重新执行：

```bash
python3 scripts/generate_image.py "你扩写后的详细画面描述" "sk-xxxxxxxxxxxx"
```
(注：Python 脚本接收到后会自动将其永久保存到本地，下次就不需要再传了)

## 结果反馈
脚本执行完成后，会输出图片的本地保存路径（如 downloads/generated_img_xxx.png）。
请直接将这个文件路径和名称告诉用户。