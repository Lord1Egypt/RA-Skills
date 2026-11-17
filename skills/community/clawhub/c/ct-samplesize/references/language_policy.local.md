# Language Policy — ct-samplesize 专属补充

> 通用双语策略以 ct-base 为单一事实来源（`references/language_policy.md`，真源 `ct-base/references/language_policy.md`）。
> 本文件只保留 ct-samplesize 的专属增补：模块分层与英文文档约定。

## Why it applies / 适用范围

This file is the detailed companion to the "Language policy" section in SKILL.md.
Why it applies: this skill is a statistical-analysis skill published on ClawHub,
so its **documentation follows the English-only rule**.
Runtime output language still follows the OS language setting (see below).

## Module tiers: runtime output coverage / 模块分层：运行期输出覆盖

### Common modules (runtime output may be EN + ZH) / 常见模块（运行期输出可中英双语）

- **Common test types**: `ttest_ind`, `ttest_paired`, `ttest_one`, `anova`, `proportion_one`, `proportion_two`, `proportion_paired`, `odds_ratio`, `risk_ratio`, `roc`, `poisson`, `non_inferiority`, `superiority_margin`, `be_tost`, `equivalence`, `survival`, `ni_survival`, `cluster`, `dunnett`
- **Shared components**: report template (`report_template.md`), quick menu, flag reference — these may keep EN/ZH bilingual runtime output.

### Complex/rare modules (EN-only for now) / 复杂/罕见模块（暂仅英文）

`group_sequential`, `adaptive`, `mixed_model`, `bayesian`, `win_ratio`, `must_win`, `historical_controls`, `assurance`, `conditional_power`, `dose_escalation`, `bland_altman`, `vaccine_efficacy`, `mams`, `survival_exact`, `mediation`

> When maintaining, if the user frequently uses one of the above, prioritize adding Chinese prompt content to promote it to a "common module".

## Doc language convention — ct-samplesize 专属例外 / 文档语言约定（本技能例外，优先于通用条款）

> **本节是 ct-samplesize 对通用 `language_policy.md`「Doc language convention」的显式例外**：
> 本技能已在 ClawHub 发布且文档策略为 **English-only**（见 AGENTS.md §5），故通用条款中
> 「references/*.md 仅英文」在本技能被强化为「所有文档文件 English-only」，且**不得**在文档中
> 保留双语标题 / 双语菜单。冲突时以本节为准。

- `README.md`: English only (keep the top EN/CN switch menu).
- `README_zh-CN.md`: Chinese only.
- `SKILL.md`, `AGENTS.md`, `references/*.md`（含本文件与通用 `language_policy.md` 副本）, `report_template.md`, `cli_examples.md` etc.: **English-only**. Do not keep bilingual titles or bilingual menus in the documentation.
- When editing docs, the documentation must be English-only; existing Chinese documentation fragments should be removed, not preserved.
