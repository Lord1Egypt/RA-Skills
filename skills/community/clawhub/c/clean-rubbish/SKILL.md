---
name: clean-rubbish
version: "1.1.0"
description: "清空系统废纸篓/回收站（macOS/Linux/Windows）。触发词：「清空废纸篓」「清空垃圾桶」「empty trash」「清理废纸篓」。斜杠命令：/clean-rubbish。"
allowed-tools: Bash(osascript:*) Bash(rm:*) Bash(powershell:*)
---

# 清空废纸篓/回收站

一键清空系统废纸篓（Trash）或回收站（Recycle Bin），自动适配操作系统。

## 使用方法

斜杠命令：`/clean-rubbish`

### macOS（自动检测）
```bash
osascript -e 'tell application "Finder" to empty trash'
```

### Linux（自动检测）
```bash
rm -rf ~/.local/share/Trash/*
```

### Windows（自动检测）
```powershell
Clear-RecycleBin -Force
```

## 自动适配逻辑

```
检测操作系统 → 选择对应命令执行：
  - Darwin (macOS)  → osascript 清空 Finder 废纸篓
  - Linux           → 清空 ~/.local/share/Trash/
  - Windows (MinGW) → PowerShell Clear-RecycleBin
```

## 说明

- 清空后文件**不可恢复**，执行前无需二次确认（用户已明确要求）
- 自动检测当前操作系统，无需手动指定平台
