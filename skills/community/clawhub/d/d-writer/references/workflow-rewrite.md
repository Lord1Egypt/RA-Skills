# 模式 E：改写 / 修复

## 触发时机

重写某一章。

## 安全规则（禁止隐式删除）

1. **首先生成受影响文件和章节清单**。
2. **用户确认前将候选稿写入 `story/runtime/rewrites/<rewrite-id>/`**，不删除正文、不修改权威状态。
3. **明确"分支"是 Git 分支还是文件级候选稿**：本契约中"分支"仅指 Git 分支，文件级候选稿统一称 `runtime rewrite candidate`。
4. **真正删除前创建恢复点**（快照）。
5. **删除后报告范围**、是否可恢复及恢复位置。

## 步骤

1. **识别回滚点**：用户指定重写到第 N 章。
2. **三步回滚机械**（仅在用户 N 之后没有章节，或用户**明确同意删后续**时启用真实删除）：
   - **恢复快照**：把 `story/snapshots/<NNNN-1>/` 的状态文件恢复到工作区。
   - **清后续产物**：删除第 N 章之后的**所有**运行时产物——`chapters/NNNN_*.md`（N 之后）、`chapters/index.json` 中 N 之后的条目、`chapter_summaries.md` 中 N 之后的行、`current_state.md` / `pending_hooks.md` 中 N 章之后的改动。
   - **重建快照**：从 N-1 章状态重新起草第 N 章，完成后新建快照 `snapshots/<NNNN>/`。
3. **绝不擅自删章**：只在 N 之后无章节、或用户明确同意时才启用真实删除。否则走"候选稿"路径——把新稿存到 `runtime/rewrites/<rewrite-id>/` 让用户对比取舍。
4. **对齐**：小改动（行文级）直接编辑章节后同步 summaries / state / hooks，仍过双层质检。大改动（结构级）重新生成 chapter intent 并从恢复态起草。
5. **过双层质量门禁**：重写稿必须走 SKILL.md 双层质检（10 项驻场初筛 + 43 个候选深化审计维度 · 审-改循环），不因为是重写而豁免。
6. **留痕**：把回滚点、删除范围、重写差异写入 `story/audit-drift.md` 的"已修复"节。

## 相关文档

- 重写流程安全规则：`references/file-contract.md`
- 快照契约：`references/file-contract.md`
- 章首 / 章末技法（起草前必读）：`references/chapter-craft.md`
- 双层质量门禁：`references/audit-dimensions.md`
- rewrite manifest 模板：`references/templates.md`
