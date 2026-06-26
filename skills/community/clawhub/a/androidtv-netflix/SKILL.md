---
name: androidtv-netflix
description: Search and play Netflix content on Android TV. When the user asks to play a specific Netflix title on TV, the agent looks up the title ID and executes ADB commands for precise playback.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - adb
    os:
      - macos
      - linux
---

# Android TV Netflix Skill

This skill remotely controls an Android TV device to play Netflix content via ADB.

## Prerequisites

If the user has not set up ADB access before, guide them through these steps:

1. **Enable Developer Options on the Android TV**:
   - Go to **Settings → Device Preferences → About** and tap **Build** 7 times.
   - Go back to **Settings → Device Preferences → Developer options** and enable **USB debugging** (also called "Network debugging" on some devices).

2. **Assign a static IP to the Android TV** (either method works):
   - **Router-side (recommended)**: In the router's admin page, find DHCP reservation / static lease settings and bind a fixed IP to the Android TV's MAC address. This requires no changes on the TV itself.
   - **TV-side**: Go to **Settings → Network & Internet → (your Wi-Fi network) → IP settings → Static** and assign an address outside the DHCP range.

3. **Install ADB on the local machine**:
   - macOS: `brew install android-platform-tools`
   - Linux (Debian/Ubuntu): `sudo apt install adb`

4. **Connect and authorize**:
   ```bash
   adb connect <ANDROID_TV_IP>:5555
   ```
   A prompt will appear on the TV asking to allow USB debugging — the user must **confirm on the TV** (check "Always allow" to skip this next time). Verify with `adb devices` — it should show `device`, not `unauthorized`.

5. **Set the environment variable** (optional — defaults to `192.168.125.228`):
   ```bash
   export ANDROID_TV_IP="192.168.1.200"
   ```

## Core Workflow

1. **Look up the title ID**: Use `web_search` to find the Netflix Title ID for the requested content (typically an 8-digit number, search within the user's region).
2. **Ensure ADB connectivity**: Verify that `adb` is connected to the Android TV device.
3. **Execute playback**: Run `scripts/play_netflix.sh <TITLE_ID>` for precise deep-link playback.

## Tools

- **Direct playback script**: `scripts/play_netflix.sh <ID>`
- **ADB basic controls** (see `references/adb-keycodes.md` for the full list):
    - Pause / Play: `adb shell input keyevent 85`
    - Volume up: `adb shell input keyevent 24`
    - Volume down: `adb shell input keyevent 25`
    - Home: `adb shell input keyevent 3`

## Troubleshooting

- If Netflix is stuck on the profile selection screen, press Enter to confirm: `adb shell input keyevent 66`.
- If the video does not auto-play, send a D-pad Center press: `adb shell input keyevent 23`.
