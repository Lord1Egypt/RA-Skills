# MEMORY.md

## Stable Facts

- 该技能包核心脚本：`scripts/d-switch.ps1`
- Windows 首选入口：`scripts/d-switch.cmd`
- 支持命令：`Dalt`、`Dctrl`、`list-windows`、`find-window`、`activate-window`、`activate-process`、`activate-handle`
- `--json` 为上层 AI 编排推荐输出模式
- 次数参数兼容 `N` 和 `-N`，推荐 `-N`（如 `-3`）

## Known Behavior

- `Dalt` -> `Alt+Tab`
- `Dctrl` -> `Ctrl+Tab`
- 每次切换间隔 100ms
- `activate-window` 会尝试恢复最小化并激活最佳候选
- `activate-process` 只按进程名匹配，适合标题变化频繁场景
- `activate-handle` 提供句柄级精确激活
