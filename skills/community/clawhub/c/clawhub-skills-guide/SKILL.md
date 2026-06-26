---
name: clawhub-skills-guide
description: AIC团队ClawHub技能管理指南。当用户询问"如何发布技能"、"怎么搜索技能"、"s和skills区别"、"如何安装技能"、"技能格式要求"、"SKILL.md怎么写"、"怎么验证技能"等ClawHub相关问题时触发。包含技能发现、安装、发布、验证全流程。
---

# ClawHub Skills Guide for AIC Team

## Quick Reference

```bash
clawhub search <query>        # 搜索技能
clawhub install <slug>        # 安装
clawhub list                  # 查看已安装
clawhub update --all          # 全部更新
clawhub inspect <slug> --files  # 查看内容不安装
clawhub publish <path> --slug <slug>  # 发布
clawhub sync --dry-run        # 预览变更
openclaw skills list          # OpenClaw技能列表
openclaw skills check         # 依赖检查
```

## s vs skills

- `clawhub.ai/s/xxx` = 旧短链接（自动301跳转）
- `clawhub.ai/skills/xxx` = 新短链接
- `openclaw s` = 已废弃，用 `openclaw skills`
- 底层技能格式从未变（SKILL.md），无需格式转换

## Skill Format

```
my-skill/
├── SKILL.md     # 必须：YAML头(name+description) + Markdown正文
├── scripts/     # 可选
├── references/  # 可选
└── assets/      # 可选
```

## AIC Team Skills

| Skill | Use |
|:---|:---|
| pdf-toolkit-pro | PDF merge/split/compress |
| office | Excel/Word/PPT formulas |
| paddleocr-doc-parsing | OCR document parsing |
| runesleo-systematic-debugging | Systematic debugging |
| find-skills | Discover new skills |

## Validation

Use `python3 scripts/validate_skill.py <path>` or `python3 scripts/validate_skill.py --all` to check YAML frontmatter, required fields (name, description), and body content before publishing.
