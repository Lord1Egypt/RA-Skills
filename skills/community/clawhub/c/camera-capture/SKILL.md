---
name: camera
version: 1.0.2
description: Control the local computer's built-in camera for capturing photos and basic operations.
metadata:
  {
    "openclaw":
      {
        "emoji": "📷",
        "requires": { "bins": ["python3"], "python_packages": ["opencv-python"] },
      },
  }
---

# Camera Control Skill

Control the local computer's built-in camera for capturing photos and basic operations.

## When to Use

- User wants to take a photo using the computer camera
- User asks to capture an image from the webcam
- User wants to check the camera view
- Commands like: "拍照", "打开摄像头", "拍张照片", "camera", "webcam", "take a photo"

## Tools Required

- Python 3 with OpenCV (`cv2`)
- Standard library only (no extra deps beyond opencv-python)

## Usage

### Take a Photo

Capture a single frame from the default camera:

```bash
python3 skills/camera/scripts/camera.py capture --output "~/.openclaw/workspace/captures/photo_$(date +%Y%m%d_%H%M%S).jpg"
```

Or use the wrapper for default location:

```bash
python3 skills/camera/scripts/capture.py
```

This saves to `~/.openclaw/workspace/captures/` with timestamp.

### List Available Cameras

```bash
python3 skills/camera/scripts/camera.py list
```

### Test Camera (preview window, auto-close after 3 seconds)

```bash
python3 skills/camera/scripts/camera.py preview --duration 3
```

## Output

- Photo path is printed to stdout
- Use this path with the `image` tool to analyze the captured photo
- Photos are saved to `captures/` directory by default

## Examples

**User:** "拍张照片"
**Action:** Run capture script, then use `image` tool to show/analyze the photo.

**User:** "看看摄像头画面"
**Action:** Run preview script for 3 seconds to verify camera works.

## Notes

- Default camera index is 0 (built-in webcam)
- If you have multiple cameras, use `--camera 1`, `--camera 2`, etc.
- On Windows, the script auto-detects and works with DirectShow backend
- Captures directory is auto-created if it doesn't exist
