# Shell Command Reference by OS

Quick-reference one-liners for remote device management via `nodes(action="invoke")`.

## Windows (PowerShell)

### System Info
```powershell
# OS version
Get-CimInstance Win32_OperatingSystem | Select Caption, Version, BuildNumber

# Installed software
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName, Version

# Disk space
Get-PSDrive C | Select Used, Free

# Network adapters
Get-NetAdapter | Select Name, Status, LinkSpeed

# Windows services
Get-Service | Where Status -eq 'Running' | Select Name, DisplayName | Sort DisplayName
```

### Process Management
```powershell
# Top 10 by CPU
Get-Process | Sort CPU -Descending | Select -First 10 Name, Id, CPU, @{N='MEM_MB';E={[math]::Round($_.WorkingSet/1MB,1)}}

# Kill by name
Get-Process -Name notepad | Stop-Process

# Kill by PID
Stop-Process -Id 1234 -Force
```

### File Operations
```powershell
# List directory
Get-ChildItem C:\Users\ -Depth 1

# Read file
Get-Content C:\temp\log.txt -Tail 50 -Encoding UTF8

# Write file
Set-Content -Path C:\temp\output.txt -Value "output here"

# Append file
Add-Content -Path C:\temp\log.txt -Value "new line $(Get-Date)"

# Delete file
Remove-Item C:\temp\old.txt -Force

# Copy file
Copy-Item C:\src\file.txt -Destination C:\dst\file.txt
```

### App Management
```powershell
# Install via winget
winget install --id <package-id> --silent --accept-package-agreements --accept-source-agreements

# Uninstall via winget
winget uninstall --id <package-id> --silent

# Start app
Start-Process C:\path\to\app.exe

# List running apps
Get-Process | Where {$_.MainWindowTitle} | Select Name, MainWindowTitle
```

### Registry
```powershell
# Read key
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"

# Write key
Set-ItemProperty "HKCU:\Software\MyApp" -Name "Setting" -Value "data"
```

## Android (adb)

```bash
# Device info
adb shell dumpsys battery

# List packages
adb shell pm list packages

# Install APK
adb install app.apk

# Uninstall
adb uninstall com.example.app

# Take screenshot
adb shell screencap /sdcard/screen.png && adb pull /sdcard/screen.png

# Record screen
adb shell screenrecord /sdcard/screen.mp4 && adb pull /sdcard/screen.mp4

# Start app
adb shell am start -n com.example.app/.MainActivity

# Press key
adb shell input keyevent 26  # power
adb shell input text "hello"

# List files
adb shell ls /sdcard/
```

## Linux (bash)

```bash
# System info
uname -a && cat /etc/os-release

# Disk usage
df -h

# Top processes
ps aux --sort=-%mem | head -15

# Kill process
kill -9 <PID>

# Services (systemd)
systemctl status <service>
systemctl restart <service>

# File operations
ls -la /tmp
cat /var/log/syslog | tail -50
```

## macOS (bash)

```bash
# System info
sw_vers && system_profiler

# Battery
pmset -g batt

# Running apps
osascript -e 'tell application "System Events" to get name of every process'

# Take screenshot
screencapture -x /tmp/screen.png

# Quit app
osascript -e 'quit app "Safari"'
```
