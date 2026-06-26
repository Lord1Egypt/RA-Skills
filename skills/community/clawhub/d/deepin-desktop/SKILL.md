# Deepin Desktop Control

Manage deepin/UOS desktop settings via D-Bus. Covers all major control center modules including power, display, network, bluetooth, accounts, sound, datetime, boot (Grub2), app store, and more.

## All D-Bus Services

Bus: `--system` (root-level daemon services)
Bus: `--session` (user session services)

### System Services (dde-system-daemon)

| Service | Path | Description |
|---------|------|-------------|
| org.deepin.dde.Power1 | /org/deepin/dde/Power1 | Power, battery, CPU governor, power modes |
| org.deepin.dde.Display1 | /org/deepin/dde/Display1 | Display monitors, backlight brightness |
| org.deepin.dde.Bluetooth1 | /org/deepin/dde/Bluetooth1 | Bluetooth device management |
| org.deepin.dde.AirplaneMode1 | /org/deepin/dde/AirplaneMode1 | Airplane mode, WiFi/Bluetooth radio |
| org.deepin.dde.Timedate1 | /org/deepin/dde/Timedate1 | Date, time, timezone, NTP server |
| org.deepin.dde.Accounts1 | /org/deepin/dde/Accounts1 | User accounts, groups, login settings |
| org.deepin.dde.Daemon1 | /org/deepin/dde/Daemon1 | System daemon: wallpaper, TTY, VM detection |
| org.deepin.dde.InputDevices1 | /org/deepin/dde/InputDevices1 | Touchscreen, mouse, wakeup devices |
| org.deepin.dde.Gesture1 | /org/deepin/dde/Gesture1 | Touchpad/gesture settings |
| org.deepin.dde.Network1 | /org/deepin/dde/Network1 | Network device enable/disable |
| org.deepin.dde.ImageEffect1 | /org/deepin/dde/ImageEffect1 | Desktop blur effect |
| org.deepin.dde.SystemInfo1 | /org/deepin/dde/SystemInfo1 | OS version/info |
| org.deepin.dde.SoundThemePlayer1 | /org/deepin/dde/SoundThemePlayer1 | System sound themes |
| org.deepin.dde.Uadp1 | /org/deepin/dde/Uadp1 | ADP backlight control |
| org.deepin.dde.SwapSchedHelper1 | /org/deepin/dde/SwapSchedHelper1 | Swap scheduler |
| org.deepin.dde.KeyEvent1 | /org/deepin/dde/KeyEvent1 | Key event monitoring (signals only) |
| org.deepin.dde.Grub2 | /org/deepin/dde/Grub2 | Grub2 boot settings, theme, timeout |

### System Services (other daemons)

| Service | Path | Description |
|---------|------|-------------|
| org.deepin.linglong.PackageManager1 | /org/deepin/linglong/PackageManager1 | Linglong app package manager |
| org.deepin.dde.Lastore1 | /org/deepin/dde/Lastore1 | App store (lastore) manager |
| com.deepin.system.Network | /com/deepin/system/Network | Network (system) |
| com.deepin.system.Power | /com/deepin/system/Power | Power (system) |
| com.deepin.system.Display | /com/deepin/system/Display | Display (system) |
| com.deepin.daemon.Timedated | /com/deepin/daemon/Timedated | Timedate daemon proxy |
| com.deepin.daemon.Accounts | /com/deepin/daemon/Accounts | Accounts daemon proxy |
| com.deepin.daemon.PowerManager | /com/deepin/daemon/PowerManager | Power manager proxy |
| com.deepin.defender.* | various | Defender security settings |
| org.deepin.dde.Network1 | /org/deepin/dde/Network1 | Network via deepin-service-manager |

### Session Services

| Service | Path | Description |
|---------|------|-------------|
| dde-session (:1.83) | /org/deepin/dde/SessionManager | Session manager |
| dde-clipboard (:1.107) | /com/deepin/dde/Clipboard | Clipboard management |
| dde-shell (:1.106) | various | DDE shell |

## Reference Files

All raw introspection XML files are saved in:
`~/.openclaw/workspace/skills/deepin-desktop/references/`

## Quick Commands

### Generic Pattern

```bash
# Get all properties
busctl --system call <service> <path> org.freedesktop.DBus.Properties GetAll s "<interface>"

# Get single property
busctl --system call <service> <path> org.freedesktop.DBus.Properties Get s "<interface>" s "<property>"

# Set property (must be writable)
busctl --system call <service> <path> org.freedesktop.DBus.Properties Set s "<interface>" s "<property>" v "<value>"

# Call method
busctl --system call <service> <path> <interface>.<method> <signature> <args...>
```

---

## 1. Power (org.deepin.dde.Power1)

**Path:** `/org/deepin/dde/Power1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| Mode | s | Current power mode: "balance", "performance", "powersave" |
| BatteryPercentage | d | Battery level 0-100 |
| BatteryStatus | u | 0=Unknown, 1=Discharging, 2=Charging, 3=Full |
| BatteryTimeToEmpty | t | Seconds until empty |
| BatteryTimeToFull | t | Seconds until full |
| OnBattery | b | true if on battery |
| HasBattery | b | true if device has battery |
| HasLidSwitch | b | true if has lid switch |
| LidClosed | b | true if lid is currently closed |
| CpuBoost | b | CPU boost enabled |
| CpuGovernor | s | CPU governor string |
| IsBalanceSupported | b | Balance mode supported |
| IsHighPerformanceSupported | b | Performance mode supported |
| IsPowerSaveSupported | b | Power-save mode supported |
| IsInBootTime | b | Currently in boot time |

### Properties (Writable)

| Property | Type | Description |
|----------|------|-------------|
| PowerSavingModeEnabled | b | Power saving mode on/off |
| PowerSavingModeAuto | b | Auto power saving |
| PowerSavingModeAutoBatteryPercent | u | Auto trigger at battery % |
| PowerSavingModeAutoWhenBatteryLow | b | Auto when battery low |
| PowerSavingModeBrightnessDropPercent | u | Brightness drop % |
| SupportSwitchPowerMode | b | Supports switching power mode |

### Methods

```bash
# Get batteries
busctl --system call org.deepin.dde.Power1 /org/deepin/dde/Power1 org.deepin.dde.Power1 GetBatteries

# Set power mode
busctl --system call org.deepin.dde.Power1 /org/deepin/dde/Power1 org.freedesktop.DBus.Properties Set s "org.deepin.dde.Power1" s "Mode" v "balance"

# Enable/disable power saving
busctl --system call org.deepin.dde.Power1 /org/deepin/dde/Power1 org.freedesktop.DBus.Properties Set s "org.deepin.dde.Power1" s "PowerSavingModeEnabled" v false

# Set CPU boost
busctl --system call org.deepin.dde.Power1 /org/deepin/dde/Power1 org.deepin.dde.Power1 SetCpuBoost b true

# Lock CPU frequency
busctl --system call org.deepin.dde.Power1 /org/deepin/dde/Power1 org.deepin.dde.Power1 LockCpuFreq s "performance"
```

---

## 2. Display (org.deepin.dde.Display1)

**Path:** `/org/deepin/dde/Display1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| SupportLabc | b | Supports automatic backlight |
| AutoBacklightEnabled | b | Auto backlight enabled |

### Methods

```bash
# Set backlight brightness (0.0-100.0)
busctl --system call org.deepin.dde.Display1 /org/deepin/dde/Display1 org.deepin.dde.Display1 SetBacklightBrightness d 50.0

# Get display config JSON
busctl --system call org.deepin.dde.Display1 /org/deepin/dde/Display1 org.deepin.dde.Display1 GetConfig

# Check Wayland support
busctl --system call org.deepin.dde.Display1 /org/deepin/dde/Display1 org.deepin.dde.Display1 SupportWayland
```

---

## 3. Bluetooth (org.deepin.dde.Bluetooth1)

**Path:** `/org/deepin/dde/Bluetooth1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| State | u | 0=Off, 1=On, 2=Discovering |
| CanSendFile | b | Can send files |

### Methods

```bash
# Get all adapters (returns JSON)
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 GetAdapters

# Example output: [{"Address":"XX:XX:XX:XX:XX:XX","Path":"/org/bluez/hci0","Name":"hostname","Powered":true,"Discovering":false,"Discoverable":true}]

# Get devices for an adapter
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 GetDevices o "/org/bluez/hci0"

# Set adapter power on/off
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 SetAdapterPowered o "/org/bluez/hci0" b true

# Connect device
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 ConnectDevice o "/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX"

# Disconnect device
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 DisconnectDevice o "/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX"

# Set device trusted
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 SetDeviceTrusted o "/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX" b true

# Remove unpaired device
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 ClearUnpairedDevice

# Set discoverable
busctl --system call org.deepin.dde.Bluetooth1 /org/deepin/dde/Bluetooth1 org.deepin.dde.Bluetooth1 SetAdapterDiscoverable o "/org/bluez/hci0" b true
```

---

## 4. Airplane Mode (org.deepin.dde.AirplaneMode1)

**Path:** `/org/deepin/dde/AirplaneMode1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| Enabled | b | Airplane mode is on |
| WifiEnabled | b | WiFi is on |
| BluetoothEnabled | b | Bluetooth is on |
| HasAirplaneMode | b | Device supports airplane mode |

### Methods

```bash
# Get all properties
busctl --system call org.deepin.dde.AirplaneMode1 /org/deepin/dde/AirplaneMode1 org.freedesktop.DBus.Properties GetAll s "org.deepin.dde.AirplaneMode1"

# Enable/disable airplane mode
busctl --system call org.deepin.dde.AirplaneMode1 /org/deepin/dde/AirplaneMode1 org.deepin.dde.AirplaneMode1 Enable b true
```

---

## 5. Date & Time (org.deepin.dde.Timedate1)

**Path:** `/org/deepin/dde/Timedate1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| NTPServer | s | NTP server address |

### Methods

```bash
# Get NTP server
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.freedesktop.DBus.Properties Get s "org.deepin.dde.Timedate1" s "NTPServer"

# Set NTP server
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.deepin.dde.Timedate1 SetNTPServer s "ntp.aliyun.com" s ""

# Enable/disable NTP
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.deepin.dde.Timedate1 SetNTP b true s ""

# Set timezone
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.deepin.dde.Timedate1 SetTimezone s "Asia/Shanghai" s ""

# Set system time (usec = microseconds since epoch)
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.deepin.dde.Timedate1 SetTime x 1742400000000000 b false s ""

# Set local RTC
busctl --system call org.deepin.dde.Timedate1 /org/deepin/dde/Timedate1 org.deepin.dde.Timedate1 SetLocalRTC b false b true s ""
```

---

## 6. User Accounts (org.deepin.dde.Accounts1)

**Path:** `/org/deepin/dde/Accounts1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| UserList | as | List of user object paths |
| GroupList | as | List of group names |
| AllowGuest | b | Allow guest account |
| GuestIcon | s | Guest icon path |
| IsTerminalLocked | b | Terminal is locked |
| QuickLoginEnabled | b | Quick login enabled |

### Methods

```bash
# List all groups
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.freedesktop.DBus.Properties Get s "org.deepin.dde.Accounts1" s "GroupList"

# Get user info
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.deepin.dde.Accounts1 FindUserByName s "zane"

# Get user's Groups property (on User1000 object)
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1/User1000 org.freedesktop.DBus.Properties GetAll s "" 2>/dev/null | head -50

# Create user (name, fullName, accountType: 0=standard, 1=admin)
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.deepin.dde.Accounts1 CreateUser s "newuser" s "New User" i 0

# Delete user
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.deepin.dde.Accounts1 DeleteUser s "username" b false

# Create group
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.deepin.dde.Accounts1 CreateGroup s "newgroup" u 1001 b false

# Allow/deny guest account
busctl --system call org.deepin.dde.Accounts1 /org/deepin/dde/Accounts1 org.deepin.dde.Accounts1 AllowGuestAccount b false
```

### User Object Properties (User1000 path example)

On path `/org/deepin/dde/Accounts1/User1000`, properties include:
- `DisplayName`, `UserName`, `UID`, `GID`, `HomeDirectory`, `Shell`
- `AccountType` (0=standard, 1=admin), `IsLogined`, `LoginHistory`
- `IconFile`, `Groups`, `PasswordHint`, `Locked`, `AutomaticLogin`

---

## 7. System Daemon (org.deepin.dde.Daemon1)

**Path:** `/org/deepin/dde/Daemon1`
**Service:** dde-system-daemon.service

### Methods

```bash
# Get custom wallpapers
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 GetCustomWallPapers s "desktop"

# Save custom wallpaper
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 SaveCustomWallPaper s "desktop" s "/path/to/image.jpg"

# Delete custom wallpaper
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 DeleteCustomWallPaper s "desktop" s "wallpaper.jpg"

# Check if PID is a VM
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 IsPidVirtualMachine u 1234

# Network connections (raw)
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 NetworkGetConnections

# Set plymouth theme
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 SetPlymouthTheme s "deepin"

# Scale plymouth
busctl --system call org.deepin.dde.Daemon1 /org/deepin/dde/Daemon1 org.deepin.dde.Daemon1 ScalePlymouth u 2
```

---

## 8. Input Devices (org.deepin.dde.InputDevices1)

**Path:** `/org/deepin/dde/InputDevices1`
**Service:** dde-system-daemon.service

### Properties (Writable)

| Property | Type | Description |
|----------|------|-------------|
| SupportWakeupDevices | a{ss} | Map of wakeup device paths to values (enabled/disabled) |
| Touchscreens | ao | List of touchscreen object paths |

### Methods

```bash
# Set wakeup device
busctl --system call org.deepin.dde.InputDevices1 /org/deepin/dde/InputDevices1 org.deepin.dde.InputDevices1 SetWakeupDevices s "/sys/bus/usb/devices/3-3/power/wakeup" s "enabled"
```

---

## 9. Gesture (org.deepin.dde.Gesture1)

**Path:** `/org/deepin/dde/Gesture1`
**Service:** dde-system-daemon.service

### Methods

```bash
# Set edge move stop duration (ms)
busctl --system call org.deepin.dde.Gesture1 /org/deepin/dde/Gesture1 org.deepin.dde.Gesture1 SetEdgeMoveStopDuration i 500

# Set input ignore
busctl --system call org.deepin.dde.Gesture1 /org/deepin/dde/Gesture1 org.deepin.dde.Gesture1 SetInputIgnore s "/dev/input/event5" b true
```

---

## 10. Network (org.deepin.dde.Network1)

**Path:** `/org/deepin/dde/Network1`
**Service:** deepin-service-manager.service

### Properties (Read/Write)

| Property | Type | Description |
|----------|------|-------------|
| VpnEnabled | b | VPN enabled (read/write) |

### Methods

```bash
# Toggle wireless enabled
busctl --system call org.deepin.dde.Network1 /org/deepin/dde/Network1 org.deepin.dde.Network1 ToggleWirelessEnabled

# Enable/disable device
busctl --system call org.deepin.dde.Network1 /org/deepin/dde/Network1 org.deepin.dde.Network1 EnableDevice s "wlan0" b true

# Check if device enabled
busctl --system call org.deepin.dde.Network1 /org/deepin/dde/Network1 org.deepin.dde.Network1 IsDeviceEnabled s "wlan0"

# Ping host
busctl --system call org.deepin.dde.Network1 /org/deepin/dde/Network1 org.deepin.dde.Network1 Ping s "baidu.com"
```

---

## 11. Grub2 / Boot (org.deepin.dde.Grub2)

**Path:** `/org/deepin/dde/Grub2`
**Service:** deepin-grub2.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| DefaultEntry | s | Default boot entry name |
| Timeout | u | Timeout in seconds |
| Gfxmode | s | Graphics mode (resolution) |
| EnableTheme | b | Theme enabled |
| ThemeFile | s | Theme file path |
| Updating | b | Currently updating |

### Methods

```bash
# Get available boot entry titles
busctl --system call org.deepin.dde.Grub2 /org/deepin/dde/Grub2 org.deepin.dde.Grub2 GetSimpleEntryTitles

# Set default entry (by title name)
busctl --system call org.deepin.dde.Grub2 /org/deepin/dde/Grub2 org.deepin.dde.Grub2 SetDefaultEntry s "统信桌面操作系统 V25 专业版"

# Set timeout
busctl --system call org.deepin.dde.Grub2 /org/deepin/dde/Grub2 org.deepin.dde.Grub2 SetTimeout u 5

# Set gfxmode
busctl --system call org.deepin.dde.Grub2 /org/deepin/dde/Grub2 org.deepin.dde.Grub2 SetGfxmode s "1920x1080"

# Enable/disable theme
busctl --system call org.deepin.dde.Grub2 /org/deepin/dde/Grub2 org.deepin.dde.Grub2 SetEnableTheme b false
```

---

## 12. Sound Theme (org.deepin.dde.SoundThemePlayer1)

**Path:** `/org/deepin/dde/SoundThemePlayer1`

### Methods

```bash
# Enable/disable sound for a theme
busctl --system call org.deepin.dde.SoundThemePlayer1 /org/deepin/dde/SoundThemePlayer1 org.deepin.dde.SoundThemePlayer1 EnableSound s "deepin" b false
```

---

## 13. UADP / Backlight (org.deepin.dde.Uadp1)

**Path:** `/org/deepin/dde/Uadp1`
**Service:** dde-system-daemon.service

### Methods

```bash
# Check if available
busctl --system call org.deepin.dde.Uadp1 /org/deepin/dde/Uadp1 org.deepin.dde.Uadp1 Available

# Delete backlight setting
busctl --system call org.deepin.dde.Uadp1 /org/deepin/dde/Uadp1 org.deepin.dde.Uadp1 Delete s "screen"
```

---

## 14. Image Effect / Blur (org.deepin.dde.ImageEffect1)

**Path:** `/org/deepin/dde/ImageEffect1`
**Service:** dde-system-daemon.service

### Methods

```bash
# Delete effect
busctl --system call org.deepin.dde.ImageEffect1 /org/deepin/dde/ImageEffect1 org.deepin.dde.ImageEffect1 Delete s "blur" s "/path/to/config"
```

---

## 15. App Store / Lastore (org.deepin.dde.Lastore1)

**Path:** `/org/deepin/dde/Lastore1`
**Service:** lastore-daemon.service

### Methods

```bash
# Check upgrade
busctl --system call org.deepin.dde.Lastore1 /org/deepin/dde/Lastore1 org.deepin.dde.Lastore1.Manager CheckUpgrade t 0 u 0

# Get all apps info
busctl --system call org.deepin.dde.Lastore1 /org/deepin/dde/Lastore1 org.deepin.dde.Lastore1.Manager GetAllApps

# Search apps
busctl --system call org.deepin.dde.Lastore1 /org/deepin/dde/Lastore1 org.deepin.dde.Lastore1.Manager SearchApps s "wps"
```

---

## 16. Linglong Package Manager (org.deepin.linglong.PackageManager1)

**Path:** `/org/deepin/linglong/PackageManager1`
**Service:** org.deepin.linglong.PackageManager1.service

### Methods

```bash
# List local packages
busctl --system call org.deepin.linglong.PackageManager1 /org/deepin/linglong/PackageManager1 org.deepin.linglong.PackageManager1 ListLocal

# Other methods include: Install, Uninstall, Update, etc.
# Full introspection in references/16_linglong.txt
```

---

## 17. Defender / Security

**Services:** com.deepin.defender.*

```bash
# Autostart manager
busctl --system call com.deepin.defender.AutostartManager /com/deepin/defender/AutostartManager com.deepin.defender.AutostartManager.GetAutoStartList

# Firewall status
busctl --system call com.deepin.defender.firewall /com/deepin/defender/firewall com.deepin.defender.firewall.GetFirewallStatus

# USB manager
busctl --system call com.deepin.defender.USBManager /com/deepin/defender/USBManager com.deepin.defender.USBManager.GetDevices

# Login safety
busctl --system call com.deepin.defender.LoginSafety /com/deepin/defender/LoginSafety com.deepin.defender.LoginSafety.GetLoginSafetySettings
```

---

## 18. System Info (org.deepin.dde.SystemInfo1)

**Path:** `/org/deepin/dde/SystemInfo1`
**Service:** dde-system-daemon.service

### Properties (Read)

| Property | Type | Description |
|----------|------|-------------|
| Version | s | OS version |
| Type | s | OS type |

---

## Apps / GUI Tools

```bash
# Open app store
deepin-home-appstore-client

# Open deepin terminal
deepin-terminal

# Search packages
apt-cache search <name>

# Install package
sudo apt install <package> -y
```

---

## Troubleshooting

```bash
# List all deepin-related services
busctl --system list | grep -E "dde|deepin|com\.deepin"

# List all available object paths for a service
gdbus introspect --system --dest <service> --object-path /

# Check if service is running
busctl --system list | grep <service-name>

# Watch property changes
busctl --system monitor --system <service> <path>
```

---

## Raw Reference Files

All introspection data is in:
`~/.openclaw/workspace/skills/deepin-desktop/references/`

Files:
- `01_power1.txt` - Power management
- `02_display1.txt` - Display
- `03_bluetooth1.txt` - Bluetooth
- `04_airplanemode1.txt` - Airplane mode
- `05_timedate1.txt` - Date/time
- `06_accounts1.txt` - User accounts
- `07_daemon1.txt` - System daemon
- `08_inputdevices1.txt` - Input devices
- `09_gesture1.txt` - Gesture
- `10_network1.txt` - Network
- `11_imageeffect1.txt` - Image effect
- `12_systeminfo1.txt` - System info
- `13_soundthemeplayer1.txt` - Sound theme
- `14_uadp1.txt` - UADP
- `15_grub2.txt` - Grub2 boot
- `16_linglong.txt` - Linglong package manager
- `17_system_network.txt` - Network (system)
- `18_system_power.txt` - Power (system)
- `19_system_display.txt` - Display (system)
- `21_daemon_accounts.txt` - Accounts daemon
- `22_power_manager.txt` - Power manager
- `24_defender.txt` - Defender security
