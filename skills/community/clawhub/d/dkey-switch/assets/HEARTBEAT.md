# HEARTBEAT.md

## Regular Checks

- 检查 `scripts/d-switch.ps1` 命令面是否变化（命令名、参数、状态）
- 检查 `scripts/d-switch.cmd` 入口是否仍可正确转发
- 检查参数说明与实际行为是否一致
- 检查 `SKILL.md` 与 `references/usage-patterns.md` 的 JSON 状态约定是否一致
- 检查退出码说明（0/1/2/3/4）是否与脚本行为一致
- 检查 `TOOLS.md` 中运行环境说明是否过期

## Trigger to Notify

- 发现脚本参数行为变化
- 发现平台兼容性问题（如 PowerShell 行为差异）
- 发现文档与脚本契约漂移（命令、状态、退出码）
- 发现 AI 触发命中率下降或误触发上升
