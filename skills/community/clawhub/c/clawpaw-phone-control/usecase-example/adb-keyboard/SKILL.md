---
name: adb-keyboard
description: Check, install, and activate ADBKeyboard for full Unicode/Chinese/emoji text input
metadata: { "openclaw": { "emoji": "⌨️" } }
---

# ADB Keyboard Setup

ADBKeyboard is required for typing Chinese, emoji, and special characters on the phone. Without it, only basic ASCII text works and non-ASCII input fails silently. This skill diagnoses, installs, and activates ADBKeyboard.

Package: `com.android.adbkeyboard`
IME ID: `com.android.adbkeyboard/.AdbIME`
APK source: `https://github.com/nicso/ADBKeyboard/releases`

## Steps

### 1. Check Current Status

Run these shell commands on the device to diagnose:

**Check if installed:**
```
pm list packages | grep adbkeyboard
```
- If output contains `package:com.android.adbkeyboard` → installed
- If empty → not installed, go to step 2

**Check if active:**
```
settings get secure default_input_method
```
- If output is `com.android.adbkeyboard/.AdbIME` → already active, done
- Otherwise → installed but not active, go to step 3

### 2. Install (if not installed)

Download and install the APK:

```
# Download APK to device temp directory
curl -L -o /data/local/tmp/ADBKeyboard.apk "https://github.com/nicso/ADBKeyboard/releases/download/v2.1/ADBKeyboard-v2.1.apk"

# Install
pm install /data/local/tmp/ADBKeyboard.apk

# Clean up
rm /data/local/tmp/ADBKeyboard.apk
```

If `curl` is not available on the device, try `wget`:
```
wget -O /data/local/tmp/ADBKeyboard.apk "https://github.com/nicso/ADBKeyboard/releases/download/v2.1/ADBKeyboard-v2.1.apk"
```

If download fails on-device (no curl/wget), tell the user to manually download the APK from `https://github.com/nicso/ADBKeyboard/releases` and install it.

After installation, verify:
```
pm list packages | grep adbkeyboard
```

### 3. Activate

Enable and set ADBKeyboard as the active input method:

```
ime enable com.android.adbkeyboard/.AdbIME
ime set com.android.adbkeyboard/.AdbIME
```

Verify activation:
```
settings get secure default_input_method
```
Expected output: `com.android.adbkeyboard/.AdbIME`

### 4. Test

After activation, test by typing a Chinese string or emoji using the `type_text` tool. If the text appears correctly on screen, setup is complete.

Test text: `你好世界 🎉`

## Status Messages

**Already set up:**
```
⌨️ ADB Keyboard Status: ✅ Ready

ADBKeyboard is installed and active. Chinese, emoji, and Unicode input are fully supported.
```

**Installed and activated:**
```
⌨️ ADB Keyboard Setup: Complete

✅ Installed ADBKeyboard
✅ Set as active input method
✅ Test passed — Unicode input working

You can now type Chinese, emoji, and special characters.
```

**Install failed:**
```
⌨️ ADB Keyboard Setup: Manual Step Needed

Could not auto-install APK on the device.
Please download ADBKeyboard from: https://github.com/nicso/ADBKeyboard/releases
Install the APK on your phone, then tell me to retry activation.
```

## When to Use

- User says "set up keyboard", "install ADB keyboard", "fix typing"
- Text input produces garbled output or empty results
- User tries to type Chinese/emoji and it fails
- First-time setup of ClawPaw phone control
- Proactively check before any task requiring non-ASCII text input

## When NOT to Use

- User is asking about physical keyboard or Bluetooth keyboard
- User wants to change their regular phone keyboard (Gboard, Sogou, etc.)
- ADBKeyboard is already installed and active (just confirm status)
