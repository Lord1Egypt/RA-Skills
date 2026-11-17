---
name: a11y-audit
description: 对一个页面/组件跑静态无障碍审计并产出分级修复报告，可接入 CI 作门禁。
source:
  type: derived
  repo: skills-repo/accessibility-engineer
  path: skills/a11y-audit/SKILL.md
  version: 1.0.0
  updated: 2026-09-02
  url: https://skills.sh/addyosmani/web-quality-skills/accessibility
metadata:
  category: 无障碍工程
  platform: Web
  difficulty: 进阶
---

# 无障碍审计（A11y Audit）

> 把"哪里不合规"变成一份可排期的报告：自动静态审计 + 严重度分级 + 修复建议。

## 能力

- 对 HTML 跑静态审计（缺 lang/title/alt、无名链接按钮、表单无 label、跳级标题等）
- 校验 ARIA 用法合法性（角色、必需子角色、冗余 role）
- 计算关键对比度并判定 AA/AAA
- 按 Blocker/Major/Minor 分级，套用报告模板产出可交付物

## 使用方式

```
/a11y-audit 审计这个页面并给我一份修复清单
/a11y-audit 把这个审计接到 CI，error 就阻断合并
```

## 工作流

1. 跑 `scripts/a11y_audit.py page.html --strict` 得静态缺陷（0 error 才进下一步）。
2. 跑 `scripts/aria_lint.py page.html --strict` 查 ARIA 用法。
3. 用 [scripts/contrast_check.py](../../scripts/contrast_check.py) 复核关键前景/背景对比度。
4. 按 [references/audit-remediation.md](../../references/audit-remediation.md) 严重度模型分级（Blocker/Major/Minor）。
5. 套 [assets/a11y-audit-report-template.md](../../assets/a11y-audit-report-template.md) 产出报告；把前两步 `--strict` 接入 CI。

## 适用场景

- 存量项目首次摸底
- 发布前合规检查
- 把无障碍检查固化进 PR 门禁

## 限制

- 静态审计只能覆盖约 30% 问题；读屏体验、焦点实际表现需 `screen-reader-testing` 人工层。
- 不替代法律合规结论；报告给出技术对齐路径。
