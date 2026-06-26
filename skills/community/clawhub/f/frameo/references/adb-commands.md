# Frameo ADB Commands Reference

## Setup

### Enable Wireless ADB (requires USB first)
```bash
# Connect via USB, then:
adb tcpip 5555

# Disconnect USB, then connect wirelessly:
adb connect <frame-ip>:5555
```

### Check Connection
```bash
adb devices -l
```

## Photo Management

### Push Photo to Frame
```bash
# To general DCIM folder
adb push photo.jpg /sdcard/DCIM/

# To Frameo's photo directory (appears in slideshow)
adb push photo.jpg /sdcard/Frameo/

# Multiple photos
adb push *.jpg /sdcard/Frameo/
```

### Delete Photo
```bash
adb shell rm /sdcard/Frameo/photo.jpg
```

### List Photos
```bash
adb shell ls /sdcard/Frameo/
```

## Screen Control

### Toggle Screen On/Off
```bash
adb shell input keyevent 26
```

### Wake Screen
```bash
adb shell input keyevent KEYCODE_WAKEUP
```

### Sleep Screen
```bash
adb shell input keyevent KEYCODE_SLEEP
```

## Brightness

### Get Current Brightness (0-255)
```bash
adb shell settings get system screen_brightness
```

### Set Brightness
```bash
# 0 = darkest, 255 = brightest
adb shell settings put system screen_brightness 128
```

### Disable Auto-Brightness
```bash
adb shell settings put system screen_brightness_mode 0
```

## Navigation

### Next Photo (Swipe Right)
```bash
adb shell input swipe 800 500 200 500 300
```

### Previous Photo (Swipe Left)
```bash
adb shell input swipe 200 500 800 500 300
```

### Tap Screen
```bash
adb shell input tap 500 300
```

## System

### Get Screen State
```bash
adb shell dumpsys power | grep "mWakefulness"
# Awake or Asleep
```

### Get Device Info
```bash
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
```

### Reboot Frame
```bash
adb reboot
```

## Automation Example

### Daily Photo Rotation Script
```bash
#!/bin/bash
FRAME_IP="192.168.0.171"
PHOTO_DIR="/path/to/photos"

# Connect
adb connect $FRAME_IP:5555

# Clear old photos
adb shell rm /sdcard/Frameo/*.jpg

# Push today's photos
adb push $PHOTO_DIR/*.jpg /sdcard/Frameo/

# Disconnect
adb disconnect $FRAME_IP:5555
```
