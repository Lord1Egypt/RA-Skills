# CAD Config Skill

Set up and configure CAD backend connections.

## Role
You are a configuration manager for CAD automation. Help users set up and configure their CAD backends.

## Configuration Tasks

### 1. Check Platform Availability

```bash
# Check if FreeCAD is available
python -c "import FreeCAD; print(FreeCAD.Version())"

# Check if pywin32 is available (for AutoCAD/SolidWorks)
python -c "import win32com.client; print('OK')"

# Check AutoCAD connection
python -c "import win32com.client; app = win32com.client.Dispatch('AutoCAD.Application'); print('Connected')"
```

### 2. Set Default Platform

Create or update `~/.claude/skills/cadstack/config.json`:

```json
{
  "default_platform": "freecad",
  "output_directory": "~/.claude/skills/cadstack/output",
  "default_format": "step",
  "platforms": {
    "freecad": {
      "enabled": true,
      "headless": true
    },
    "autocad": {
      "enabled": false,
      "require_running": true
    },
    "solidworks": {
      "enabled": false,
      "require_running": true
    },
    "fusion360": {
      "enabled": false,
      "port": 8080
    }
  }
}
```

### 3. Configure FreeCAD Path

If FreeCAD is not in Python path:

```bash
# Linux
export PYTHONPATH=/usr/lib/freecad/lib:$PYTHONPATH

# macOS
export PYTHONPATH=/Applications/FreeCAD.app/Contents/lib:$PYTHONPATH

# Windows (PowerShell)
$env:PYTHONPATH = "C:\Program Files\FreeCAD\bin;$env:PYTHONPATH"
```

Add to shell profile (~/.bashrc, ~/.zshrc) or Windows Environment Variables.

### 4. Configure Fusion 360 Bridge

1. Install Fusion 360 add-in:
   - Copy `~/.claude/skills/cadstack/lib/bridge/fusion360_bridge.py`
   - To Fusion 360 add-ins folder

2. Start bridge in Fusion 360:
   - Open Fusion 360
   - Go to Scripts and Add-ins (Shift+S)
   - Run "CADStack Bridge"

3. Verify connection:
```bash
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.connect(('localhost', 8080))
print('Fusion 360 bridge connected')
"
```

## Configuration Check Commands

### Check All Platforms

```bash
python ~/.claude/skills/cadstack/lib/cad_executor.py info
```

Output:
```
╭─────────────── cadstack ───────────────╮
│          CAD Platforms                 │
╜────────────────────────────────────────╯

FreeCAD (freecad)
  Pure Python, headless mode, no license required
  Status: ✓ Available

AutoCAD (autocad)
  Requires AutoCAD running on Windows (COM)
  Status: ✗ Not available

SolidWorks (solidworks)
  Requires SolidWorks running on Windows (COM)
  Status: ✗ Not available

Fusion 360 (fusion360)
  Requires Fusion 360 with bridge add-in
  Status: ✗ Not available
```

### Check Specific Platform

```bash
python ~/.claude/skills/cadstack/lib/cad_executor.py check freecad
```

## Platform-Specific Setup

### FreeCAD (Recommended)

**Prerequisites:**
- FreeCAD 0.20+ installed
- Python 3.8+

**Installation:**
```bash
# Ubuntu/Debian
sudo apt install freecad

# macOS
brew install --cask freecad

# Windows
# Download from https://www.freecad.org/downloads.php
```

**Configuration:**
```bash
# Add to PYTHONPATH (choose appropriate path)

# Linux
echo 'export PYTHONPATH=/usr/lib/freecad/lib:$PYTHONPATH' >> ~/.bashrc

# macOS (Apple Silicon)
echo 'export PYTHONPATH=/Applications/FreeCAD.app/Contents/lib:$PYTHONPATH' >> ~/.zshrc

# Windows - set via System Properties > Environment Variables
```

### AutoCAD

**Prerequisites:**
- AutoCAD 2020+ installed and licensed
- Windows OS
- pywin32 package

**Installation:**
```bash
pip install pywin32
```

**Configuration:**
1. Ensure AutoCAD is running
2. Run `/cad-config --check autocad` to verify connection

### SolidWorks

**Prerequisites:**
- SolidWorks 2020+ installed and licensed
- Windows OS
- pywin32 package

**Installation:**
```bash
pip install pywin32
```

**Configuration:**
1. Ensure SolidWorks is running
2. Run `/cad-config --check solidworks` to verify connection

### Fusion 360

**Prerequisites:**
- Fusion 360 installed and logged in
- Bridge add-in installed

**Installation:**
1. Copy bridge add-in to Fusion 360 add-ins folder
2. Run bridge from Scripts and Add-ins menu

## Troubleshooting

### FreeCAD Not Found

```
Error: ModuleNotFoundError: No module named 'FreeCAD'
```

**Solution:**
1. Verify FreeCAD is installed
2. Check PYTHONPATH includes FreeCAD lib directory
3. On Windows, ensure you're using the Python that comes with FreeCAD

### AutoCAD Connection Failed

```
Error: Failed to connect to AutoCAD
```

**Solution:**
1. Ensure AutoCAD is running
2. Check AutoCAD is a licensed version (trial may not support COM)
3. Run as Administrator if needed

### Fusion 360 Bridge Not Responding

```
Error: Fusion 360 bridge not running on port 8080
```

**Solution:**
1. Start the bridge add-in in Fusion 360
2. Check firewall isn't blocking port 8080
3. Verify add-in is enabled

## CLI Reference

```bash
# Show all platforms
cad-config info

# Check specific platform
cad-config check freecad
cad-config check autocad
cad-config check solidworks
cad-config check fusion360

# Set default platform
cad-config set-default freecad

# Set output directory
cad-config set-output ~/cad_output

# Test connection
cad-config test
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| ✗ ModuleNotFoundError | CAD platform not in PYTHONPATH | → Add platform lib to PYTHONPATH |
| ✗ ConnectionFailed | CAD application not running | → Start the CAD application |
| ✗ BridgeNotResponding | Fusion 360 bridge not started | → Run bridge add-in in Fusion 360 |
| ✗ COMError | Windows COM registration issue | → Run as Administrator, reinstall pywin32 |
| ⚠ LicenseRequired | Trial version doesn't support automation | → Use licensed version |
| ⚠ FirewallBlocked | Port 8080 blocked | → Allow port in firewall settings |

## Text Equivalents (Accessibility)

When screen readers or plain-text output is needed:

| Icon | Text |
|------|------|
| ✓ | [OK] |
| ✗ | [FAIL] |
| ⚠ | [WARN] |
