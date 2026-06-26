# TOOLS.md

## Runtime

- Primary Platform: Windows
- Windows Native Entry:
  - CMD: `scripts\d-switch.cmd`
  - PowerShell: `powershell -File scripts/d-switch.ps1`
- Compatibility Path:
  - Git Bash / WSL: `bash scripts/d-switch.sh`
- Bridge (Windows): PowerShell `System.Windows.Forms.SendKeys` + Win32 API

## OS Dispatch (Agent First Decision)

- Windows:
  - Preferred entry: `scripts\d-switch.cmd`
  - Preferred command: `activate-window`
  - Secondary commands: `find-window`, `activate-process`, `activate-handle`
  - Fallback only: `Dalt` / `Dctrl`
- macOS:
  - Current repo has no equivalent automation script
  - Fallback shortcuts:
    - Window: `Cmd+Tab`
    - Tab: `Ctrl+Tab` or `Cmd+Shift+]`

## Common Commands

- `scripts\d-switch.cmd activate-window QQ`
- `scripts\d-switch.cmd find-window 微信 3`
- `scripts\d-switch.cmd activate-process Code`
- `scripts\d-switch.cmd activate-handle 0x2072C`
- `scripts\security-audit.cmd`
- `powershell -File scripts/d-switch.ps1 activate-window QQ`
- `bash scripts/d-switch.sh activate-window QQ`

## Gotchas

- 脚本会真实切换焦点，执行前确保当前窗口状态可控
- 某些系统策略可能限制 `SendKeys`
- Windows 下优先不要使用 `bash ...` 作为首选入口
- 在 macOS 上不要直接执行 Windows 激活链路；应走快捷键降级说明
