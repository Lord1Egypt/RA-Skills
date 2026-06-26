# DuoPlus CloudPhone Agent

📱 OpenClaw skill for controlling Android cloud phones via ADB broadcast commands.

## Installation

### From ClawHub
```bash
clawhub install duoplus/duoplus-agent
```

### Local Install (Testing)
```bash
# 复制到 OpenClaw 的 skills 目录
cp -r duoplus-agent ~/.openclaw/skills/duoplus-agent
```

Or use workspace-level:
```bash
mkdir -p ./skills
cp -r duoplus-agent ./skills/duoplus-agent
```

## Prerequisites

- `adb` installed and in PATH
- Target Android device running `StandardSoftwareService`

## Usage

Just tell OpenClaw what you want to do:

```
Connect to device 192.168.1.100:5555 and open WeChat
```

```
Take a screenshot of the current screen on device emulator-5554
```

```
Click the "Login" button on the Android device
```

The agent will use ADB broadcast commands to control the device.

## How It Works

Commands are sent as Base64-encoded JSON via ADB broadcast to `com.duoplus.service.PROCESS_DATA`. The Android system service receives and executes operations (tap, swipe, type, screenshot, etc.).

## License

MIT
