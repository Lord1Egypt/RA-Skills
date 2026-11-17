# 审计与修复工作流（Playbook）

> 适用技能：[skills/a11y-audit](../skills/a11y-audit/SKILL.md)（流水线宿主：静态审计与报告产出）、[skills/alt-text](../skills/alt-text/SKILL.md)、[skills/keyboard-a11y](../skills/keyboard-a11y/SKILL.md)、[skills/semantic-markup](../skills/semantic-markup/SKILL.md)（被编排的修复执行技能）。

> 端到端地把"一团乱"变成"可交付的合规状态"。本篇是流程编排层：把其它 references、脚本、子技能串成一条流水线，并定义产出与完成标准。

## 何时用本篇

- 接手一个存量项目要"做无障碍"
- 需要给客户/团队交一份审计报告 + 修复排期
- 想把无障碍检查固化进 CI

## 审计流水线（三层）

```
第 1 层 自动化静态      第 2 层 人工走查        第 3 层 读屏实测
────────────────       ──────────────        ──────────────
a11y_audit.py          对比度(contrast_check)  NVDA + VoiceOver
aria_lint.py           WCAG 清单(wcag-checklist) screen-reader-testing 脚本
axe / Lighthouse        键盘走查(keyboard-focus) 
```

- 第 1 层必须 0 error 才进下一层（CI 门禁可拦）。
- 第 2、3 层发现的问题记入报告，按严重度排期。

## 严重度分级（用于排期）

| 等级 | 定义 | 例子 | 排期 |
|------|------|------|------|
| **Blocker** | 核心功能盲用完全不可用 / 法律红线 | 无 lang、键盘进不去弹窗、对比度严重不达标 | 立即 |
| **Major** | 可用但有显著障碍 | 表单无 label、动态提示不播报、跳级标题 | 本迭代 |
| **Minor** | 体验瑕疵，不影响主流程 | 冗余 role、焦点环偏小 |  backlog |

> 排期优先级 = 法律/合规风险 × 用户影响 ÷ 修复成本。Blocker 永远优先。

## 报告格式

用 [assets/a11y-audit-report-template.md](../assets/a11y-audit-report-template.md)，至少包含：
- 范围与标准（WCAG 2.2 AA）
- 三层发现汇总（数量 + 严重度分布）
- 逐条缺陷：位置 / 现象 / 期望 / 对应 SC / 严重度 / 建议
- 修复排期与负责人
- 复测结论

## 常见修复模式

| 问题 | 一键修法 |
|------|----------|
| 缺 alt | `alt=""`(装饰) 或描述文本 |
| 表单无 label | `<label for>` 或 `aria-label` |
| 弹窗焦点丢失 | 焦点陷阱 + 关闭归还（`keyboard-focus.md`） |
| 动态提示不播报 | `role="alert"` / `aria-live="polite"` |
| 对比度不足 | 调色后用 `contrast_check.py` 复核 |
| 链接无名 | 改为有意义文本或 `aria-label` |

## CI 集成（把合规变门禁）

- 在 PR 中跑 `a11y_audit.py --strict` 与 `aria_lint.py --strict`，非零退出即阻断合并。
- 组件库层用 `jest-axe` / `@axe-core/playwright` 做单元级断言。
- 对比度属设计令牌，应在设计系统层校验，而非每次手测。

## 完成定义（Definition of Done）

- [ ] 第 1 层脚本 0 error
- [ ] 关键页面通过 NVDA + VoiceOver 走查
- [ ] 全部 Blocker / Major 关闭，Minor 有排期
- [ ] 报告归档，复测结论明确

## 限制

- 本篇是编排与判定的方法论，不重复写具体组件写法（见 `semantic-html-aria.md`、各子技能）。
- 法律结论以官方文本为准；本篇仅给技术对齐路径。
