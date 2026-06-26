---
name: orbcafe-pivot-ainav
description: Build ORBCAFE advanced analytics and voice navigation with CPivotTable/usePivotTable and CAINavProvider/useVoiceInput using official examples patterns. Use for drag-drop pivot dimensions, PivotChart companion views, aggregation controls, preset persistence, or space-key voice workflows, especially when interactions appear not to take effect.
---

# ORBCAFE Pivot + AINav

## Workflow

1. 先对照 `skills/orbcafe-ui-component-usage/references/module-contracts.md`，确认这是 `Hook-first` 模块。
2. 用 `references/domain-patterns.md` 判定 pivot、voice 或组合模式。
3. 执行安装与最小可运行接入。
4. 用 `references/recipes.md` 产出实现骨架。
5. 对 pivot 需求额外检查是否需要三段式布局（配置区 + 图表区 + 结果区）、独立折叠、图表选择器和 preset 图表快照。
6. 用 `references/guardrails.md` 检查受控状态、preset 持久化、ASR 配置。
7. 输出验收步骤与“没效果”排障。

## Installation and Bootstrapping (Mandatory)

```bash
npm install orbcafe-ui @mui/material @mui/icons-material @mui/x-date-pickers @emotion/react @emotion/styled dayjs
```

本仓库联调：

```bash
npm run build
cd examples
npm install
npm run dev
```

参考实现：
- `examples/app/_components/PivotTableExampleClient.tsx`
- `examples/app/_components/AINavExampleClient.tsx`
- `src/components/PivotTable/PivotChart/`

## Output Contract

0. `Mode`: `Hook-first`.
1. `Module choice`: pivot or AINav (or both).
2. `Minimal implementation`: controlled if persistence/integration needed.
3. `Ops note`: preset 持久化、PivotChart 默认逻辑或 ASR 契约。
4. `Verify`: 至少包括拖拽布局生效、聚合切换、图表切换、独立折叠、生效后持久化、语音触发与回调。
5. `Troubleshooting`: 至少包含 3 条失效排查点。

## Examples-Based Experience Summary

- 需要持久化时优先 `usePivotTable` 受控模式，不要只依赖组件内部状态。
- preset 持久化应在 `onPresetsChange` 回调落地（本地可用 localStorage，生产建议服务端）。
- Pivot 默认是三段式：配置区、PivotChart、结果表格；图表区和表格区都能独立折叠。
- PivotChart 最多只映射 1 个维度和 2 个度量。默认维度优先取 `rows[0]`，否则 `columns[0]`；默认主度量取 `values[0]`。
- 多维或多度量时，图表工具条应显示 4 个统一宽度的下拉：`Dimension / Measure / Compare measure / Chart type`。
- preset 不只保存布局和筛选，也要保存图表维度、主度量、对比度量和图表类型。
- localStorage 读写放在浏览器安全边界（初始化判定 `window`，写入放 `useEffect`）。
- AINav 强制提供 `onVoiceSubmit`，否则“录音了但业务不动作”。
- 空格热键建议保持 `ignoreWhenFocusedInput=true`，避免输入框场景误触。
