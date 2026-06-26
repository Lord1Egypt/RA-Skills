# Encoding Notes

## Windows + PowerShell Encoding Issues

### Problem
OpenClaw's `write` tool and `exec` tool use the system shell. On Windows with PowerShell 5.1 (pre-installed), the default encoding is the system locale (GBK/CP936 for Chinese Windows), not UTF-8. This causes Chinese and other non-ASCII content to be garbled.

### Solution
Upgrade to PowerShell 7.x:

```bash
winget install Microsoft.PowerShell
```

OpenClaw automatically detects PowerShell 7 at startup:
1. `C:\Program Files\PowerShell\7\pwsh.exe`
2. `pwsh` in PATH
3. Fallback: `powershell.exe` (5.1)

After installing, **restart the Gateway** for the change to take effect.

### Verification
```bash
# In exec tool, check version:
$PSVersionTable.PSVersion  # Should show 7.x

# Test Chinese encoding:
Set-Content -Path "test.txt" -Value "中文测试🥟" -Encoding UTF8
# Then read with the read tool to verify
```

### Workaround (if unable to upgrade)
Use explicit UTF-8 encoding when writing files:

```powershell
[System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
```

### Related OpenClaw Issues
- #45432 — write tool UTF-8 BOM on Windows
- #56106 — Transcript JSONL encoding corrupted on Windows
- #56462 — exec tool garbled Chinese on Windows
