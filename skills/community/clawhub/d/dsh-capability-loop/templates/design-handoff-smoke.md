# 设计驱动交接 · 真实工程实测清单（明日用）

> 目的：把「DSH 出设计 + 文档 → Trae 只按文档实现 → DSH 验收」在**真实工程**上跑通一次，把 `references/60-handoff.md §5` 从「规则就绪」升级为「已实测」。
> 前置：`handoff-smoke.ps1` 已 PASS；Trae 当前工程与目标一致（`trae-status.ps1 -Workspace <工程> -RequireMatch`）。
> 记录方式：每项填「结果 + 证据路径」，完成回写 `record.md` 与 `memory/team-learnings.md`。

## 0. 准备（10 分钟）

| 项 | 动作 | 期望 | 证据 |
|---|---|---|---|
| 目标工程 | 选定一个**非核心**工程或分支（如 `isoms-prototype-page`），避免污染主分支 | 有 git、可开分支 | 路径/分支 |
| 设计上下文 | 填 `design-context.md`（用 `product-context.ps1` 扫描 + 人工核对 token/样本页） | 8 项都有证据 | `docs/design/design-context.md` |
| 需求依据 | SRS 或需求片段（含 AC） | 至少 1 条可验收 AC | 需求路径 |
| 门禁 | `loop-gate.ps1 -TaskDir <任务目录> -RequireGrill` | PASS（或 FAIL 项有说明） | 命令输出 |
| 交接包 | `new-handoff.ps1 -Workspace <工程> -Slug <kebab> -Title "<UI 改动>"` | 四件套生成 | `docs/handoff/<slug>/` |
| 视觉 AC | 将 `templates/design-driven-acceptance.md` 追加到 `acceptance.md` | 至少 4 条视觉 AC | `acceptance.md` |

## 1. 交接前（DSH 侧）

- [ ] `brief.md`：范围/Out of scope/引用 `design-context.md`
- [ ] `tasks.md`：UI 任务逐条绑定设计依据（token/组件/禁止自造）；写明「不得引入新 UI 体系」
- [ ] `acceptance.md`：功能 AC + 视觉 AC + 未实测登记
- [ ] `check-handoff.ps1 -Stage prepare` → PASS
- [ ] `trae-status.ps1 -Workspace <工程> -RequireMatch` → MATCH
- [ ] `open-in-trae.ps1 -Workspace <工程> -File docs/handoff/<slug>/tasks.md` → 唤起并定位
- [ ] 在 Trae 对话里贴一次实现者契约 + 「只按 tasks.md 实现，交证据，不判 PASS」

## 2. 实现中（Trae 侧，DSH 只观察不代写）

- [ ] Trae 只改任务清单内文件（用 `git status` 核对）
- [ ] 未引入新 UI 框架/组件库/图标库
- [ ] 完成后在 `tasks.md` 填「实现回报」并标 `待验收`
- [ ] Trae 未自判 PASS

## 3. 回读与验收（DSH 侧）

- [ ] `collect-evidence.ps1 -Workspace <工程> -Slug <slug> -TestCommand "<测试命令>"` → 证据落盘
- [ ] 视觉证据：用户终端截图（375/768/1440 × 明/暗至少 375+1440）放 `design-qa/<slug>/`
- [ ] 逐条核对视觉 AC：缺图的标「未实测」，不得 PASS
- [ ] `check-handoff.ps1 -Stage deliver` → PASS
- [ ] `record.md` 结论：PASS / FAIL / 未实测（含视觉结论）
- [ ] `gate-check.ps1 -TaskDir <任务目录> -Kind design` / `loop-gate` 复跑
- [ ] `git diff` 仅含清单内文件 + 未删既有断言

## 4. 结论回写

| 项 | 内容 |
|---|---|
| 实测日期/环境 | |
| 工程/分支/commit | |
| 结论 | PASS / 有条件 / 未实测 |
| 与预期不符处 | |
| 需要改进的 skill/references | 写回 `70-playbook.md` 或 `60-handoff.md` |
| 证据路径 | |

## 5. 判定（什么算「已实测」）

- 至少 1 个 UI 交接包在真实工程完成：prepare → Trae 实现 → 证据 → 视觉 AC → deliver 全链路 PASS；
- 有截图或明确「未实测」登记；
- `record.md` 结论由 DSH 出具，Trae 只交证据；
- 完成后把 `references/90-provenance.md` §3 的「设计驱动交接未实测」改为「已实测（日期/工程）」。
