# ADB Command Reference

## Table of Contents

- [Device Management](#device-management)
- [App Management](#app-management)
- [File Transfer](#file-transfer)
- [Logging](#logging)
- [Screenshot & Recording](#screenshot--recording)
- [UI Hierarchy](#ui-hierarchy)
- [Performance](#performance)
- [System Info](#system-info)
- [Input & Interaction](#input--interaction)
- [Network](#network)
- [Dangerous Operations](#dangerous-operations)

---

## Device Management

```bash
# List connected devices
adb devices -l

# Specify device for all commands
adb -s <serial> <command>

# Connect over WiFi
adb tcpip 5555
adb connect <ip>:5555

# Disconnect WiFi device
adb disconnect <ip>:5555

# Restart adb server
adb kill-server && adb start-server

# Device properties
adb shell getprop ro.build.version.release   # Android version
adb shell getprop ro.build.version.sdk       # API level
adb shell getprop ro.product.model           # Device model
adb shell getprop ro.product.brand           # Brand
adb shell getprop ro.serialno                # Serial number
```

## App Management

```bash
# Install / reinstall
adb install <path.apk>
adb install -r <path.apk>         # Replace existing
adb install -t <path.apk>         # Allow test packages
adb install -d <path.apk>         # Allow downgrade

# Uninstall
adb uninstall <package>
adb uninstall -k <package>        # Keep data

# List packages
adb shell pm list packages                   # All
adb shell pm list packages -3                # Third-party
adb shell pm list packages | grep <keyword>  # Filter

# App info
adb shell dumpsys package <package> | grep versionName
adb shell dumpsys package <package> | grep versionCode

# Start activity
adb shell am start -n <package>/<activity>
adb shell am start -a android.intent.action.VIEW -d <url>

# Force stop
adb shell am force-stop <package>

# Clear app data
adb shell pm clear <package>

# Grant / revoke permission
adb shell pm grant <package> <permission>
adb shell pm revoke <package> <permission>

# List permissions
adb shell dumpsys package <package> | grep permission

# Dump current activity
adb shell dumpsys activity activities | grep mResumedActivity
adb shell dumpsys window | grep mCurrentFocus
```

## File Transfer

```bash
# Push file to device
adb push <local> <remote>

# Pull file from device
adb pull <remote> <local>

# List files on device
adb shell ls <path>
adb shell ls -la <path>

# File size
adb shell du -sh <path>

# Create directory
adb shell mkdir -p <path>

# Remove file/directory
adb shell rm <path>
adb shell rm -rf <path>
```

## Logging

```bash
# Basic logcat
adb logcat

# Clear log buffer
adb logcat -c

# Filter by tag
adb logcat -s <TAG>

# Filter by priority (V/D/I/W/E/F)
adb logcat *:E                    # Errors and above
adb logcat <TAG>:D *:S            # Specific tag at Debug+

# Save to file
adb logcat -d > logcat.txt        # Dump then stop
adb logcat -t 1000 > recent.txt   # Last 1000 lines

# Time filter
adb logcat -T "MM-DD HH:MM:SS.mmm"

# Crash logs
adb logcat -b crash

# Buffer info
adb logcat -g                     # Buffer size
adb logcat -b main,system,crash   # Specific buffers

# Process-specific log
adb logcat --pid=$(adb shell pidof <package>)

# Common useful filters
adb logcat -s AndroidRuntime:E    # Runtime crashes
adb logcat -s ActivityManager:I   # Activity lifecycle
```

## Screenshot & Recording

```bash
# Screenshot
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .
adb shell rm /sdcard/screenshot.png

# Screen recording (max 180s)
adb shell screenrecord /sdcard/video.mp4
adb shell screenrecord --time-limit 30 /sdcard/video.mp4
adb shell screenrecord --size 720x1280 /sdcard/video.mp4
adb shell screenrecord --bit-rate 6000000 /sdcard/video.mp4

# Pull recording
adb pull /sdcard/video.mp4 .
adb shell rm /sdcard/video.mp4
```

## UI Hierarchy

```bash
# Dump UI tree to XML (standard)
adb shell uiautomator dump /sdcard/ui_dump.xml
adb pull /sdcard/ui_dump.xml .
adb shell rm /sdcard/ui_dump.xml

# Dump compressed (smaller output)
adb shell uiautomator dump --compressed /sdcard/ui_dump.xml

# Direct stdout dump (no temp file)
adb exec-out uiautomator dump /dev/tty

# Fallback: text-based view hierarchy via dumpsys
adb shell dumpsys activity top -a
```

## Performance

```bash
# Memory info
adb shell dumpsys meminfo <package>
adb shell dumpsys meminfo                    # System-wide
adb shell cat /proc/meminfo                  # Raw kernel info

# CPU info
adb shell dumpsys cpuinfo
adb shell top -n 1 -s cpu

# Battery stats
adb shell dumpsys battery
adb shell dumpsys batterystats

# GPU rendering profiling
adb shell dumpsys gfxinfo <package>

# Network stats
adb shell dumpsys netstats detail

# Disk usage
adb shell df -h
adb shell du -sh /data/data/<package>

# Process list
adb shell ps -A | grep <keyword>

# Thread info for a process
adb shell ps -T -p <pid>
```

## System Info

```bash
# Full device info
adb shell getprop

# Display info
adb shell wm size                  # Screen resolution
adb shell wm density               # Screen density

# System settings
adb shell settings list system
adb shell settings list secure
adb shell settings list global

# Input methods
adb shell ime list -s

# Services list
adb shell service list

# WiFi info
adb shell dumpsys wifi | grep "mWifiInfo"

# Storage info
adb shell sm list-volumes
```

## Input & Interaction

```bash
# Tap at coordinates
adb shell input tap <x> <y>

# Swipe
adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>

# Type text
adb shell input text "<text>"

# Key event
adb shell input keyevent <keycode>
# Common keycodes:
#   3=HOME  4=BACK  24=VOL_UP  25=VOL_DOWN
#   26=POWER  82=MENU  187=APP_SWITCH
#   66=ENTER  67=DEL  111=ESCAPE
#   61=TAB  122=MOVE_HOME  123=MOVE_END

# Long press power (reboot menu)
adb shell input keyevent --longpress 26
```

## Network

```bash
# Enable/disable WiFi
adb shell svc wifi enable
adb shell svc wifi disable

# Enable/disable mobile data
adb shell svc data enable
adb shell svc data disable

# Set HTTP proxy
adb shell settings put global http_proxy <host>:<port>

# Remove HTTP proxy
adb shell settings delete global http_proxy

# Airplane mode
adb shell settings put global airplane_mode_on 1
adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
```

## Dangerous Operations

> These commands may cause data loss or render the device unusable. Always confirm before executing.

```bash
# Factory reset
adb shell recovery --wipe_data

# Flash partition
adb reboot bootloader
fastboot flash <partition> <image>

# Wipe app data for ALL apps
adb shell pm list packages -3 | while read pkg; do adb shell pm clear ${pkg#package:}; done

# Disable system app
adb shell pm disable-user --user 0 <package>

# Modify system settings
adb shell settings put system <key> <value>
adb shell settings put secure <key> <value>
adb shell settings put global <key> <value>

# Change system properties
adb shell setprop <key> <value>

# Root access
adb root
adb shell su

# Sideload OTA
adb sideload <ota.zip>

# Reboot
adb reboot
adb reboot recovery
adb reboot bootloader
```
