---
name: frameo
description: Control Frameo digital photo frames. Use when: sending photos to Frameo frames, listing paired frames, controlling frame via ADB (brightness, screen, navigation). Supports both cloud API (read-only) and ADB (full control including photo upload). Requires either Frameo account credentials or ADB access to the frame.
---

# Frameo Digital Photo Frame Control

Control Frameo photo frames via cloud API or ADB.

## Methods

### Method 1: Cloud API (Limited)
- ✅ List paired frames
- ✅ Get account info
- ❌ Send photos (requires FCM/Firebase)

### Method 2: ADB (Full Control)
- ✅ Push photos directly
- ✅ Control brightness
- ✅ Toggle screen
- ✅ Navigate photos

## Quick Start

### Cloud API Setup
1. Install: `pip3 install requests pillow`
2. Get Bearer token from Frameo app traffic (Proxyman/Charles)
3. Save token: `echo '{"access_token": "YOUR_TOKEN"}' > ~/.frameo_token`
4. Run: `python3 scripts/frameo_client.py --frames`

### ADB Setup (Recommended)
1. Enable Developer Options on Frameo (Settings → About → tap Build 7x)
2. Enable USB Debugging
3. Connect USB-C data cable to computer
4. Run: `adb tcpip 5555` to enable wireless
5. Disconnect USB, connect wireless: `adb connect <frame-ip>:5555`

## Usage Examples

### List Frames (Cloud API)
```bash
python3 scripts/frameo_client.py --frames
```

### Send Photo (ADB)
```bash
adb push photo.jpg /sdcard/DCIM/
# Or to Frameo's photo directory:
adb push photo.jpg /sdcard/Frameo/
```

### Control Frame (ADB)
```bash
# Screen on/off
adb shell input keyevent 26

# Set brightness (0-255)
adb shell settings put system screen_brightness 128

# Next photo (swipe right)
adb shell input swipe 800 500 200 500

# Previous photo (swipe left)  
adb shell input swipe 200 500 800 500
```

## Remote Access via SSH Relay

If frame is on local network and agent is remote:
```bash
ssh user@local-mac "adb push /tmp/photo.jpg /sdcard/DCIM/"
```

## References

- `references/api-endpoints.md` - Frameo cloud API endpoints
- `references/adb-commands.md` - Common ADB commands for Frameo

## Troubleshooting

### Token Expired (401)
Frameo tokens expire in ~5 minutes. Get fresh token from Proxyman.

### ADB Connection Refused
Wireless ADB not enabled. Need USB cable first to run `adb tcpip 5555`.

### USB Cable Not Detected
Ensure using a **data cable**, not charge-only. Data cables are usually thicker.
