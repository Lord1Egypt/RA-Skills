# ONBOARDING.md

## Status

- State: active
- Progress: 2/5

## Scope

- Product: ClawHub AI skill（面向 AI 编排消费）
- Platform Priority: Windows
- Contract Mode: Prefer `--json`

## Release Checklist

1. Contract Alignment
1.1 `SKILL.md` 与 `references/usage-patterns.md` 的命令面一致。
1.2 JSON 状态契约包含 `ok/activated/not_found/choice_out_of_range/activation_failed`。
1.3 退出码说明包含 `0/1/2/3/4`。

2. AI Routing Quality
2.1 存在 canonical 路由模板（明确窗口、不明确窗口、进程、句柄、回退）。
2.2 触发排除规则存在（快捷键问答不执行、概念讨论不执行）。
2.3 目标不明确时优先 `find-window` 再 `activate-window`。

3. Regression Samples
3.1 `references/ai-e2e-cases.md` 存在且至少包含 10 条样例。
3.2 样例包含窗口切换、页签切换、失败恢复三类场景。
3.3 每条样例包含 `Intent`、`Command`、`Expected status`。

4. Audit Gate
4.1 执行 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/security-audit.ps1`。
4.2 结果必须为 `0 issue(s)`；warning 应解释或修复。

5. Versioning
5.1 更新 `_meta.json` 版本号（语义化版本）。
5.2 发布说明记录：新增能力、契约变更、风险与回滚说明。

## Fast Verification Commands

1. `scripts\d-switch.cmd list-windows --json`
2. `scripts\d-switch.cmd find-window code 3 --json`
3. `scripts\d-switch.cmd activate-window code 1 --json`
