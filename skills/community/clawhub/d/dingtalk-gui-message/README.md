# DingTalk GUI Message 🔔

Automate sending messages to DingTalk contacts via macOS desktop GUI automation.

Uses screenshot → OCR → coordinate click approach to interact with DingTalk's WebView-based interface, bypassing Accessibility API limitations.

## Features

- **Auto login detection** — detects if DingTalk needs login, captures QR code for scanning
- **Smart search** — searches contacts by name prefix for better matching
- **Dual OCR engine** — Swift Vision for precise coordinates + qwen VL for semantic verification
- **WebView compatible** — uses `cliclick` for coordinate-based clicks (standard accessibility clicks don't work on DingTalk's WebView)
- **Screenshot verification** — confirms each step succeeded before proceeding
- **Retina aware** — correct coordinate conversion for Retina displays

## Requirements

- macOS (arm64, Retina display)
- DingTalk desktop client (`com.alibaba.DingTalkMac`)
- [Peekaboo](https://github.com/nicklama/peekaboo) — `brew install steipete/tap/peekaboo`
- [cliclick](https://github.com/BlueM/cliclick) — `brew install cliclick`
- Swift (included with Xcode/Command Line Tools)
- Screen Recording + Accessibility permissions granted

### Optional (for semantic verification)

- DashScope API key (qwen-vl-max) for vision-based screenshot analysis

## Install

### OpenClaw

```bash
# Clone to skills directory
git clone https://github.com/jacky-wzj/dingtalk-gui-message.git ~/.openclaw/skills/dingtalk-gui-message
```

### Claude Code

```bash
# Personal skills
git clone https://github.com/jacky-wzj/dingtalk-gui-message.git ~/.claude/skills/dingtalk-gui-message

# Project skills
git clone https://github.com/jacky-wzj/dingtalk-gui-message.git .claude/skills/dingtalk-gui-message
```

## Usage

The skill activates when you say things like:
- "给XXX发消息说开会"
- "钉钉发消息给XXX"
- "send a dingtalk message to XXX"

### Direct script usage

```bash
python3 scripts/send_message.py "联系人名" "消息内容"
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Message sent successfully |
| 1 | Failed (contact not found, etc.) |
| 2 | Login required (QR code saved to `/tmp/dingtalk-gui/qr_code.png`) |

## How It Works

```
Activate DingTalk → Check Login
    ├─ Need login → Wait for QR → Screenshot → Vision verify → Send to user
    └─ Logged in → Cmd+F search → Paste name → Screenshot → OCR coordinates
                   → cliclick target → Confirm chat opened → Paste message
                   → Press Return → Confirm sent
```

### Key Technical Decisions (learned from failures)

| Decision | Why |
|----------|-----|
| Use `com.alibaba.DingTalkMac` (bundleId) | Chinese name "钉钉" causes targeting issues |
| Use `peekaboo paste --text` for Chinese | `peekaboo type` doesn't work with CJK input methods |
| Use `cliclick` for WebView clicks | `peekaboo click` doesn't reach WebView elements |
| Use `screencapture -x` for OCR navigation | `peekaboo image --app` misses WebView content |
| Use `peekaboo image --app` for login check | Avoids false positives from other windows |
| Retina coordinates ÷ 2 | Not × 0.7875 — direct Retina scaling |
| Search by first 2 chars | Full name search sometimes fails |

## File Structure

```
dingtalk-gui-message/
├── SKILL.md              # Skill instructions for AI agents
├── README.md             # This file
└── scripts/
    ├── send_message.py   # Main automation script
    └── ocr_screen.swift  # Swift Vision OCR with coordinates
```

## License

MIT
