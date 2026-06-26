# ================================
# fanzhi-provenance: fz:skill:1a2b3c4d:wsl_lobster:mpc2j3a6
# project: html-to-pdf v1.0.4
# content-hash: 1a2b3c4d
# license: MIT-0 (ClawHub)
# copyright: 泛智生态 / Ronie & 泛智小龙虾
# fanzhi-signature: (Phase 3)
# ================================

# 各平台 Chromium/Chrome 路径参考

## macOS

```bash
# Google Chrome（标准安装）
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome

# Chromium（若通过 Homebrew 安装）
/opt/homebrew/bin/chromium
```

## Linux / WSL

```bash
# 独立安装版（当前默认）
/opt/chrome-linux/chrome

# 标准包管理器安装
/usr/bin/chromium
/usr/bin/chromium-browser

# snap 版（⚠️ 沙箱隔离，不可用）
/snap/bin/chromium
```

## Windows

```powershell
# Google Chrome
C:\Program Files\Google\Chrome\Application\chrome.exe

# Microsoft Edge（Chromium 内核）
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

## 环境变量覆盖

```bash
# 所有平台均可通过环境变量指定
CHROME_PATH=/custom/path/to/chrome node scripts/html-to-pdf.mjs input.html
```
