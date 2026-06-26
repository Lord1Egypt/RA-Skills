---
name: adb-controller
description: Control an Android device via ADB. Use when the user asks to control an Android device, tap, swipe, input text, or perform actions via adb. Automatically uses the adbServer configured in openclaw.json and takes screenshots.
---

# ADB Controller

This skill allows you to execute ADB (Android Debug Bridge) commands on a connected Android device and automatically retrieve a screenshot of the result.

## Configuration

The user can configure the target ADB device/server in their `openclaw.json` (this is automatically read by the script):
```json
{
  "skills": {
    "entries": {
      "adb-controller": {
        "adbServer": "192.168.1.100:5555" // or device serial
      }
    }
  }
}
```

## Usage

To run an ADB command, execute the provided Python script:

```bash
python3 ~/.openclaw/workspace/skills/adb-controller/scripts/run_adb.py shell input tap x y
```

You can pass any standard ADB arguments to the script. For example:
- `python3 .../run_adb.py shell input text "hello"`
- `python3 .../run_adb.py shell input keyevent 26` (Power button)
- `python3 .../run_adb.py shell swipe 500 1000 500 500`

## Workflow (Mandatory)

1. Understand the user's intent and determine the correct ADB command.
2. Execute the user's requested action using the `run_adb.py` script via the `exec` tool.
3. The script will output the path to a newly captured screenshot.
4. **Send the Image:** You MUST use the `message` tool (with `action="send"` and `media="<path-to-screenshot>"`) to send the resulting screenshot to the user, allowing them to see the outcome of the action. Do not just output the file path.