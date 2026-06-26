# autopieceone - Piece One Auto-move Script

Automates character movement in the piece.one web game using OpenClaw.

## Features

- Randomly moves the character around a circle in the center of the screen.
- Randomly executes actions such as clicking, dropping items, chatting, and changing color.
- Automatically sets the character name and color upon startup.

## Repository

- **URL**: https://github.com/imtonyjaa/autopieceone
- **Clone**: `git clone https://github.com/imtonyjaa/autopieceone.git`
- **Update**: `git pull`

## Prerequisites

### 1. Install Python

If Python is not installed, install it first:

- **Windows**: [Download Python 3.12](https://www.python.org/downloads/)
- **Mac**: `brew install python3` or [Download from Official Site](https://www.python.org/downloads/macos/)
- **Linux**: `sudo apt install python3` or `sudo yum install python3`

Make sure to check **"Add Python to PATH"** during installation.

### 2. Install Python Dependencies

```bash
pip install pyautogui pyperclip python-dotenv
```

### 3. Find Python Path

Paths vary by system:
- **Windows (Common)**: `C:\Users\<Username>\AppData\Local\Programs\Python\Python312\python.exe`
- **Mac**: `/usr/bin/python3` or `python3`
- **Linux**: `python3`

Use these commands to find it:
```bash
# Windows
where python

# Mac/Linux
which python3
```

## Launch Steps

### First Launch

```python
# 1. Clone repository
exec(command="git clone https://github.com/imtonyjaa/autopieceone.git")

# 2. Check browser tabs
browser(action="tabs")

# 3. Open game page (MUST include widget=2&from=claw)
browser(action="open", targetUrl="https://piece.one/?widget=2&from=claw")

# 4. Wait for game to load
time.sleep(3)

# 5. Start script (pass character name)
# Windows example path, replace with your actual Python path
exec(command="python autopieceone/autopieceone.py CharacterName")
```

### Subsequent Launch

```python
# 1. Pull latest code
exec(command="git -C autopieceone pull")

# 2. Close old tab and open new page
browser(action="tabs")
# Record old tab ID, then close it
browser(action="close", targetId="<OldID>")
browser(action="open", targetUrl="https://piece.one/?widget=2&from=claw")

# 3. Start script
exec(command="python autopieceone/autopieceone.py CharacterName")
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| CharacterName | Name set at startup | BigClaw |

## Command Format

- **Rename**: `name:Name`
- **Change Color**: `color: #RRGGBB`
- **Drop Item**: `drop:🍎`

## Notes

1. **URL Must Include Params**: `?widget=2&from=claw`
2. **Game Window Priority**: The script uses system-level mouse control, so the game window must be in the foreground.
3. **Terminate Script**: Move the mouse to any corner of the screen to trigger pyautogui FAILSAFE and stop the script immediately.
