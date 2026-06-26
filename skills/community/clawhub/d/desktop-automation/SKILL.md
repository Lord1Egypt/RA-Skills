---
name: desktop-control
description: Control the desktop via CUA computer server API running on port 8000
version: 1.0.0
---

# Desktop Control via CUA Server

This skill allows OpenClaw to control the desktop using the CUA computer server API.

## Prerequisites

- CUA computer server running on port 8000
- Access to localhost:8000 (or configured CUA_SERVER_URL)

## Installation

To control your host desktop with OpenClaw, you need to install and run the CUA computer server on your machine.

### Quick Start (Python SDK)

The easiest way to install the CUA computer server on your host:

```bash
# Install the Computer SDK
pip install cua-computer-sdk

# Start the server (it will control your current desktop)
cua-server start --port 8000

# Or if you need to specify the display (Linux/Unix)
DISPLAY=:0 cua-server start --port 8000

# Verify it's running
curl http://localhost:8000/status
```

### Alternative: Install from Source

If you prefer to install from source:

```bash
# Clone the repository
git clone https://github.com/trycua/cua-computer-server
cd cua-computer-server

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m cua_server --port 8000
```

### Running as a Background Service

For always-on desktop control, set up as a system service:

**macOS (launchd):**
```bash
# Create a plist file
cat > ~/Library/LaunchAgents/com.cua.server.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cua.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/cua-server</string>
        <string>start</string>
        <string>--port</string>
        <string>8000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.cua.server.plist

# Start the service
launchctl start com.cua.server
```

**Linux (systemd):**
```bash
# Create service file
sudo tee /etc/systemd/system/cua-server.service > /dev/null <<EOF
[Unit]
Description=CUA Computer Server
After=network.target

[Service]
Type=simple
User=$USER
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/$USER/.Xauthority"
ExecStart=/usr/local/bin/cua-server start --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable cua-server
sudo systemctl start cua-server

# Check status
sudo systemctl status cua-server
```

**Windows (Task Scheduler):**
```powershell
# Create a scheduled task to run at startup
$action = New-ScheduledTaskAction -Execute "cua-server.exe" -Argument "start --port 8000"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "CUA Server" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

### Configuration Options

Configure the server for your needs:

```bash
# Basic start with default settings
cua-server start

# Custom port
cua-server start --port 8001

# With authentication token (recommended if exposing to network)
cua-server start --port 8000 --auth-token your-secret-token

# Specify display (Linux/Unix)
DISPLAY=:1 cua-server start --port 8000

# Bind to all interfaces (careful - exposes to network!)
cua-server start --bind 0.0.0.0 --port 8000 --auth-token required-if-exposed
```

### Security Considerations

⚠️ **Important**: By default, the server only listens on `localhost` (127.0.0.1) for security. This means only processes on your machine can connect to it.

- **Local only (default)**: Safe for personal use with OpenClaw
- **Network exposure**: Only use `--bind 0.0.0.0` with proper firewall rules AND authentication
- **Authentication**: Always use `--auth-token` if the server is accessible from the network

### Verification

After installation, verify the server is working:

```bash
# Check server status
curl http://localhost:8000/status

# List available commands
curl http://localhost:8000/commands | jq

# Take a test screenshot of your desktop
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  | jq -r '.result.base64' \
  | base64 -d > test-screenshot.png

# View the screenshot
open test-screenshot.png       # macOS
xdg-open test-screenshot.png   # Linux
start test-screenshot.png      # Windows
```

If you see a screenshot of your current desktop, the server is working correctly!

### Troubleshooting

**Port Already in Use:**
```bash
# Check what's using port 8000
lsof -i :8000              # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Solution: Use a different port
cua-server start --port 8001
```

**Permission Denied (Linux):**
```bash
# You may need to add your user to the input group for keyboard/mouse control
sudo usermod -a -G input $USER
# Log out and back in for changes to take effect
```

**Display Not Found (Linux):**
```bash
# Check your display variable
echo $DISPLAY

# Set it explicitly
DISPLAY=:0 cua-server start --port 8000
```

**Server Not Responding:**
```bash
# Check if the process is running
ps aux | grep cua-server       # Linux/macOS
tasklist | findstr cua-server  # Windows

# Try running in foreground to see errors
cua-server start --port 8000 --debug
```

## Available Commands

### Take Screenshot

Capture the current screen:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  | jq -r '.result.base64' \
  | base64 -d > screenshot.png
```

### Click at Coordinates

Click at specific x,y coordinates:
```bash
# Click at center of 1280x720 screen
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "left_click", "params": {"x": 640, "y": 360}}'
```

### Right Click
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "right_click", "params": {"x": 640, "y": 360}}'
```

### Double Click
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "double_click", "params": {"x": 640, "y": 360}}'
```

### Type Text

Type text at the current cursor position:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "type_text", "params": {"text": "Hello, World!"}}'
```

### Press Hotkey

Press a key combination:
```bash
# Ctrl+C
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "c"]}}'

# Ctrl+Alt+T (open terminal)
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
```

### Press Single Key

Press a single key:
```bash
# Press Enter
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "enter"}}'

# Press Escape
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "escape"}}'
```

### Move Cursor

Move cursor to specific position:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "move_cursor", "params": {"x": 100, "y": 200}}'
```

### Scroll

Scroll up or down:
```bash
# Scroll down 3 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "down", "amount": 3}}'

# Scroll up 5 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "up", "amount": 5}}'
```

### Launch Application

Launch an application by name:
```bash
# Launch Firefox
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "firefox"}}'

# Launch Terminal
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "xfce4-terminal"}}'
```

### Open File or URL

Open a file or URL with default application:
```bash
# Open URL
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "https://example.com"}}'

# Open file
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "/home/cua/document.txt"}}'
```

### Get Window Information

Get current window ID:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_current_window_id"}'
```

### Window Control

Maximize window:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "maximize_window", "params": {"window_id": "0x1234567"}}'
```

Minimize window:
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "minimize_window", "params": {"window_id": "0x1234567"}}'
```

## Demo Workflows

### Browser Navigation Demo

Open Firefox and navigate to a website:
```bash
# Take initial screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o initial.json

# Launch Firefox
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "launch", "params": {"app": "firefox"}}'
sleep 3

# Focus address bar (Ctrl+L)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "l"]}}'
sleep 1

# Type URL
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "https://example.com"}}'

# Press Enter
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 5

# Take final screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o final.json
```

### Text Editor Demo

Open text editor and type content:
```bash
# Open terminal
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
sleep 2

# Type command to open text editor
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "mousepad"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 2

# Type some text
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "Hello from OpenClaw!\nThis is automated desktop control."}}'

# Save file (Ctrl+S)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "s"]}}'
sleep 1

# Type filename
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "openclaw-demo.txt"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
```

### Form Filling Demo

Fill out a web form:
```bash
# Assuming browser is open with form visible

# Click on first input field (adjust coordinates)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 300}}'

# Type name
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "John Doe"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type email
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "john@example.com"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type message
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "This form was filled automatically by OpenClaw!"}}'

# Submit form (click submit button)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 500}}'
```

## Helper Functions

### Check Server Status
```bash
curl http://localhost:8000/status
```

### List All Available Commands
```bash
curl http://localhost:8000/commands | jq
```

### Get Screen Size
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_screen_size"}'
```

### Get Cursor Position
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_cursor_position"}'
```

## Environment Variables

- `CUA_SERVER_URL`: Base URL for CUA server (default: http://localhost:8000)

## Tips

1. **Wait Between Commands**: Add `sleep` between commands to allow UI to update
2. **Check Coordinates**: Screen is 1280x720, center is at (640, 360)
3. **Screenshot for Debugging**: Take screenshots before and after actions to verify
4. **Use Variables**: Store coordinates and text in variables for reusability

## Example OpenClaw Usage

Once this skill is loaded, you can use it in OpenClaw conversations:

```
User: "Take a screenshot and open Firefox"
OpenClaw: *executes the screenshot and launch firefox commands*

User: "Type 'Hello World' in the current window"
OpenClaw: *executes the type_text command*

User: "Click at the center of the screen"
OpenClaw: *executes click command at 640,360*
```

## Troubleshooting

1. **Connection Refused**: Make sure CUA server is running on port 8000
2. **No Response**: Check if you're in the container or have SSH tunnel set up
3. **Commands Not Working**: Verify with `curl http://localhost:8000/status`
4. **Wrong Coordinates**: Remember screen is 1280x720, adjust coordinates accordingly