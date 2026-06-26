---
name: android-adb
description: "Execute Android ADB (Android Debug Bridge) commands for device management, app management, debugging, and automation. Use when the user requests any ADB-related operation such as: (1) Device management — list/connect/disconnect devices, query device info, WiFi debugging; (2) App management — install/uninstall APKs, start/stop apps, clear data, manage permissions; (3) Debugging — logcat capture and filtering, crash log extraction, process inspection; (4) Screen capture — screenshots, screen recording; (5) Performance profiling — memory/CPU/battery/GPU stats; (6) File transfer — push/pull files between host and device; (7) Input simulation — tap, swipe, key events, text input; (8) Network control — WiFi/data toggle, proxy settings; (9) System info — device properties, display info, settings. Also triggers when the user says 'adb', mentions Android device operations, or asks to debug an Android app via command line."
---

# Android ADB

Execute ADB commands via natural language or direct command input, with multi-device support, safety guardrails, and sandboxed ADB installation.

## Workflow

1. **List devices**: Directly run `adb devices -l`. If the command fails (command not found), go to [ADB Resolution](#adb-resolution) to find or install adb, then retry.
2. **Select device**: If multiple devices connected, list them and ask user to choose. Prepend `-s <serial>` to all subsequent commands.
3. **Translate request to ADB command(s)**: Map the user's intent to appropriate ADB commands. See [references/adb-commands.md](references/adb-commands.md) for the full command reference.
4. **Safety check**: If the command is destructive (see [Dangerous Operations](#dangerous-operations)), show the command and ask for confirmation before executing.
5. **Execute and report**: Run the command, parse output, and present results clearly.

## ADB Resolution

When `adb` is not found, resolve using `scripts/adb_env.sh` which checks in order: system PATH → common SDK paths (`~/Library/Android/sdk/`, `~/Android/Sdk/`) → sandbox local (`<skill_dir>/tools/platform-tools/adb`).

If none found, ask the user: **"ADB 未安装，是否需要我帮你安装到 skill 本地目录？（不影响系统配置）"**

If agreed, run `bash <skill_dir>/scripts/install_adb.sh` (no sudo, no PATH modification, uninstall via `rm -rf <skill_dir>/tools/`).

## Multi-Device Handling

When `adb devices -l` returns multiple devices:

1. Display a numbered list with serial, model, and Android version
2. Ask the user to pick one (or "all" for broadcast)
3. Store the chosen serial and use `-s <serial>` for all commands in the session
4. Run `bash scripts/device_check.sh` in the skill directory for a quick overview

## Safety Levels

| Level | Behavior | Examples |
|-------|----------|---------|
| **Safe** | Execute directly | `adb devices`, `logcat`, `screencap`, `getprop`, `pull`, file listing |
| **Moderate** | Show command, then execute | `install`, `push`, `am start`, `input tap`, `pm grant` |
| **Dangerous** | Show command, explain risk, require explicit "yes" | `pm clear`, `uninstall`, `factory reset`, `flash`, `wipe`, `reboot` |

## Quick Tasks

### Device Info
```bash
bash <skill_dir>/scripts/device_check.sh
```

### Screenshot
```bash
bash <skill_dir>/scripts/screenshot.sh [output_dir] [serial]
```

### Logcat Capture
```bash
bash <skill_dir>/scripts/logcat_capture.sh all [output_file] [serial]
bash <skill_dir>/scripts/logcat_capture.sh crash [output_file] [serial]
bash <skill_dir>/scripts/logcat_capture.sh app <package> [output_file] [serial]
bash <skill_dir>/scripts/logcat_capture.sh tag <TAG> [output_file] [serial]
```

## Long Output Rule

When the user requests any long-running or verbose log output (logcat streaming, dropbox dump, dumpsys, large trace output, etc.), **unless the user explicitly specifies an output file**, always **open a new system terminal window** to display the output. This gives the user a scrollable, stoppable, dedicated view without blocking the conversation.

Only write to file when the user explicitly says "保存到文件" / "输出到 xxx.txt" / provides a file path.

### macOS
```bash
osascript -e 'tell app "Terminal" to do script "<adb_logcat_command>"'
```

### Linux (common DEs)
```bash
# GNOME
gnome-terminal -- bash -c '<adb_logcat_command>; exec bash'
# KDE
konsole -e bash -c '<adb_logcat_command>; exec bash'
# Fallback
x-terminal-emulator -e bash -c '<adb_logcat_command>; exec bash'
```

Replace `<adb_logcat_command>` with the actual command, e.g.:
- `adb logcat` — all logs
- `adb logcat | grep -i "redirect" --line-buffered` — filter by keyword
- `adb logcat -s MyTag:D` — filter by tag
- `adb logcat --pid=$(adb shell pidof com.example.app)` — filter by app

### zsh compatibility

zsh treats `*` as a glob wildcard. When the command contains `*` (e.g. `Tag:*`), **escape it** in the osascript string:
```bash
# Wrong — zsh expands *
osascript -e 'tell app "Terminal" to do script "adb logcat -s MyTag:*"'
# Correct — escape the *
osascript -e 'tell app "Terminal" to do script "adb logcat -s MyTag:\\*"'
```

After launching, report to the user that the terminal window has been opened and what command is running.

## Common Scenarios

### "Install this APK"
```bash
adb install -r <path.apk>
```
If install fails, check: device storage (`adb shell df -h`), existing app version, test package flag (`-t`).

### "Show me crash logs"

Two-level fallback:

1. **logcat crash buffer** (first try):
```bash
adb logcat -b crash -d | grep <package>
```

2. **dropbox** (fallback if crash buffer is empty):

> **⚠️ 强制规则：严禁主动挑选 dropbox 条目。必须先列出所有条目，等用户选择后再输出内容。绝不允许跳过用户选择步骤。**

Step 1 — 列出 dropbox 中所有 crash/anr 条目及其时间戳，供用户选择：
```bash
adb shell dumpsys dropbox | grep -E "^[0-9].*(_crash|_anr)" 
```
输出示例：
```
2026-04-09 11:04:34  data_app_anr (compressed text, 23807 bytes)
    Process: com.netease.cloudmusic:play/PID: 2553 ...
2026-04-09 10:23:45  data_app_crash (text, 1234 bytes)
    Process: com.example.app/PID: 1234 ...
```

Step 2 — 将列表**完整呈现**给用户（包含完整日期时间、类型、进程信息），然后**必须等待用户明确选择**要查看哪一条。**严禁自行判断、自动选择最近一条或任何一条。**

Step 3 — 用户选择后，打开新终端窗口展示对应条目：
```bash
# 使用用户选择的条目的时间戳
adb shell dumpsys dropbox --print '<tag>' --since <timestamp_ms>
```

### "Dump UI hierarchy"

Two-level fallback:

1. **uiautomator dump** (first try):
```bash
adb shell uiautomator dump /sdcard/ui_dump.xml
adb pull /sdcard/ui_dump.xml <local_path>
adb shell rm /sdcard/ui_dump.xml
```

2. **dumpsys activity top** (fallback — some devices like Huawei may report `could not get idle state`):
```bash
adb shell dumpsys activity top -a > <local_path>
```
This outputs a text-based View Hierarchy instead of XML, but contains equivalent structural info.

### "Screen recording"
```bash
adb shell screenrecord /sdcard/recording.mp4              # default max 180s
adb shell screenrecord --time-limit 30 /sdcard/recording.mp4  # limit to 30s
# Ctrl+C to stop, then pull:
adb pull /sdcard/recording.mp4 <local_path>
adb shell rm /sdcard/recording.mp4
```

### "Which app is in the foreground?"
```bash
adb shell dumpsys activity activities | grep mResumedActivity
```

### "App performance check"
```bash
adb shell dumpsys meminfo <package>
adb shell dumpsys gfxinfo <package>
adb shell dumpsys cpuinfo | grep <package>
```

### "Connect via WiFi"
```bash
adb tcpip 5555
# Note the device IP from:
adb shell ip route | grep wlan
adb connect <ip>:5555
```

## Dangerous Operations

Always confirm before executing any of:

- `pm clear` — wipes app data permanently
- `uninstall` — removes app
- `rm -rf` — deletes files/directories
- `reboot` / `reboot recovery` / `reboot bootloader`
- `factory reset` / `wipe_data`
- `fastboot flash` — overwrites partitions
- `pm disable-user` — disables system apps
- `settings put` — modifies system/secure/global settings
- `setprop` — changes system properties
- `su` / `adb root` — elevates to root privileges
- `sideload` — flashes OTA packages
- Any command with `--user 0` on system packages

Present the exact command and a one-line risk description, then wait for explicit confirmation.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `device not found` | Check USB cable, enable USB debugging in Developer Options |
| `device unauthorized` | Accept RSA key prompt on device, or `adb kill-server && adb start-server` |
| `multiple devices` | Use `-s <serial>` |
| `INSTALL_FAILED_*` | Check error suffix — common: `ALREADY_EXISTS` (use `-r`), `INSUFFICIENT_STORAGE`, `OLDER_SDK` |
| `Permission denied` | Try `adb root` or `run-as <package>` |
| Command hangs | Ctrl+C, then `adb kill-server && adb start-server` |

## Reference

For the full ADB command cheat sheet organized by category, see [references/adb-commands.md](references/adb-commands.md).
