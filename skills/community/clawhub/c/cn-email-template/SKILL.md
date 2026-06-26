---
name: cn-email-template
description: |
  Email Template skill.
  自动生成，无人工审查。
metadata: {"openclaw": {"emoji": "🔧"}}
---

# name: 专业商务邮件生成器

description: 输入场景和关键词，自动生成10+种专业商务邮件（初次联系、跟进、感谢、报价、拒绝、道歉、会议邀请、周报、离职告别、节日问候）。支持自定义收件人、发件人、职位等变量。
version: "1.0.0"
entry: scripts/email_template.py
install: ""

scope:
  - 支持10+种商务邮件场景模板
  - 自定义邮件主题、收件人、发件人信息
  - 生成结构完整的邮件正文（称谓+正文+落款）
  - 列出所有可用场景
  - 支持中文商务邮件规范格式

env: []

test: |
  python3 scripts/email_template.py --help
  python3 scripts/email_template.py 初次联系 发件人=张三 姓名=李四 目的=合作

example:
  input: "python email_template.py 初次联系 发件人=王经理 姓名=赵总 目的=AI工具合作"
  output: "生成完整邮件，包含主题、称谓、正文、落款"
  input: "python email_template.py 周报 姓名=李华 周期=本周 完成事项='项目A完成' 下周计划='继续迭代'"
  output: "生成周报格式邮件"

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
