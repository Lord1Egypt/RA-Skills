---
name: cn-smart-reply
version: "1.2.0"
description: |
  Smart Reply skill.
  自动生成，无人工审查。
metadata: {"openclaw": {"emoji": "🔧"}}
---

# name: 智能回复生成器

description: 微信/邮件/知乎/小红书等场景的智能回复建议，10+种常见社交场景自动生成得体回复。
version: "1.0.0"
entry: scripts/smart_reply.py
install: ""

scope:
  - 支持10+种回复场景（感谢/道歉/确认/拒绝/催促/安慰/祝贺/请教/介绍/知乎/小红书）
  - 随机抽取多条候选回复
  - 列出所有可用场景
  - 中文社交回复规范

env: []
test: |
  python3 scripts/smart_reply.py --help
  python3 scripts/smart_reply.py 感谢
  python3 scripts/smart_reply.py 催促 "项目进度"

example:
  input: "python smart_reply.py 感谢"
  output: "💬 太感谢了！真的帮了我大忙..."
  input: "python smart_reply.py 回复知乎"
  output: "💬 泻药。亲身经历来说..."

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
