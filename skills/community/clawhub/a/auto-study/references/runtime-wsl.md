# runtime-wsl

## Use this file when

- the host is WSL

## Prerequisites

- WSL interop enabled
- Google Chrome installed on Windows
- `agent-browser` installed in the WSL environment

## Core policy

- the task should drive a Windows Chrome instance from WSL
- **CRITICAL**: When executing Windows commands, scripts, or navigating UNC paths (e.g., `\\wsl.localhost\...`), you MUST invoke `pwsh.exe` or `powershell.exe` instead of `cmd.exe`.
- When invoking PowerShell from Bash/WSL, pass the PowerShell code as a single script block wrapped in Bash single quotes to avoid interpolation and escaping issues.
- If a socket error occurs while writing task artifacts, try using a shell loop outside the sandbox.
