---
name: amazon-listing-factory
description: Generate complete Amazon listing drafts with title, bullets, image plan, prompts, and video script.
---

# Amazon Listing Factory

Generate complete Amazon listing drafts with:

- title
- bullets
- image plan
- image prompts
- video script

If image environment is configured, it can continue image generation automatically.

完整教程链接：
https://my.feishu.cn/docx/DzpHdBjJdosX6Nx7CAMc9OY5nZf

推荐在飞书中使用 Slash 命令调用：

/amazon_listing_factory 生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图

安装或更新 Skill 后，请先执行：

openclaw gateway restart

检查是否识别成功：

openclaw skills list | grep amazon

如果看到：

amazon-listing-factory

说明 Skill 已被 OpenClaw 正确识别。

本地测试：

bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh "生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图"
