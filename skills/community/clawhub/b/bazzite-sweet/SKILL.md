---
name: bazzite-sweet
description: Bazzite-specific setup, optimization, and troubleshooting — Steam Deck tweaks, Flatpak management, Wayland, GNOME/KDE, uBlue image layers
version: 1.0.0
tags:
  - bazzite
  - steam-deck
  - immutable
  - flatpak
  - wayland
  - gaming
  - ublue
  - linux
metadata:
  {"openclaw": {"os": ["linux"]}}
---

# Bazzite Sweet — Your Bazzite Companion

Everything specific to Bazzite: setup, optimization, Steam Deck tweaks, Flatpak management, Wayland compositors, and uBlue image customization.

## When to Use

- Setting up or tweaking Bazzite on desktop or Steam Deck
- Managing Flatpaks and system packages on Bazzite
- Steam Deck gaming optimization
- Wayland display/compositor issues
- uBlue custom images and rebase
- Bazzite-specific bugs or quirks
- Switching between Bazzite editions (Nvidia, Wayfire, Sway, KDE)

## Bazzite Quick Reference

### Editions

| Edition | Use Case |
|---------|----------|
| `bazzite` | GNOME-based desktop |
| `bazzite-nvidia` | GNOME + Nvidia proprietary |
| `bazzite-deck` | Steam Deck (KDE Plasma) |
| `bazzite-deck-nvidia` | Steam Deck + Nvidia |
| `bazzite-arch` | Arch-based (unstable) |

### Core Identity

Bazzite is built on **Fedora Atomic** (rpm-ostree) + **uBlue** framework. Key facts:
- Immutable root filesystem (use `rpm-ostree` for system changes)
- Flatpak for GUI apps (pre-configured with Flathub + uBlue repos)
- No `dnf install` — layer packages with `rpm-ostree install`
- Updates are atomic deployments
- Steam Deck variant uses KDE Plasma (not GNOME)

## System Status

```bash
# Check Bazzite version and deployment
rpm-ostree status

# Check for updates
rpm-ostree upgrade --check

# Apply update
rpm-ostree upgrade && systemctl reboot

# Current kernel
uname -r

# Check Bazzite-specific services
systemctl --user list-units 'bazzite*' 2>/dev/null
systemctl list-units 'bazzite*' 2>/dev/null
```

## Flatpak Management

Bazzite comes with Flathub and uBlue Flatpak repos pre-configured.

```bash
# List all Flatpaks
flatpak list

# List only user-installed
flatpak list --user --app

# Update all Flatpaks
flatpak update --assumeyes

# Search for an app
flatpak search "app name"

# Install from Flathub
flatpak install flathub <app-id>

# Install from uBlue repo
flatpak installublue <app-id> 2>/dev/null || flatpak install <app-id>

# Remove
flatpak uninstall <app-id>

# Clear unused runtimes
flatpak uninstall --unused

# Check repo list
flatpak remotes

# Add Flathub if missing
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Fix Flatpak issues
flatpak repair
flatpak update --app
```

### Essential Gaming Flatpaks

```bash
# Core gaming
flatpak install flathub com.valvesoftware.Steam
flatpak install flathub net.lutris.Lutris
flatpak install flathub com.usebottles.bottles
flatpak install flathub org.prismlauncher.PrismLauncher
flatpak install flathub com.heroicgameslauncher.hgl
flatpak install flathub io.github.Foldex.Exodus

# Streaming
flatpak install flathub dev.lizardbyte.app.Sunshine

# Media
flatpak install flathub org.freedesktop.Platform.VAAPI.Intel
flatpak install flathub org.freedesktop.Platform.VAAPI.Intel.i386

# GPU-specific (Nvidia)
flatpak install flathub org.freedesktop.Platform.GL32.nvidia
flatpak install flathub org.freedesktop.Platform.GL.nvidia
```

## Steam Deck Specific

### Steam Deck UI

```bash
# Check Gamescope (Steam Deck compositor)
gamescope --help 2>/dev/null | head -5

# Current session type
echo $XDG_SESSION_TYPE

# Check if in Game Mode
# Game Mode = Weston compositor running
ps aux | grep -E 'gamescope|weston' | grep -v grep

# Check Steam Deck GPU
cat /sys/class/drm/card*/device/vendor 2>/dev/null
# 0x1002 = AMD (Van Gogh APU)

# Check thermal
cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | awk '{print $1/1000"°C"}'

# Check battery (Steam Deck OLED/LCD)
cat /sys/class/power_supply/BAT*/capacity 2>/dev/null
cat /sys/class/power_supply/BAT*/status 2>/dev/null
```

### Steam Deck Tweaks

```bash
# Set Gamescope fractional scaling
GAMESCOPE_FSR_SHARPNESS=2 gamescope -W 1280 -H 800 -f -- steam

# Enable FSR upscaling
GAMESCOPE_FSR_SHARPNESS=5 gamescope -f -W 1920 -H 1200 -w 1280 -h 800 -- %command%

# Steam Deck OLED: native resolution
gamescope -W 1280 -H 800 -f -- %command%

# Check controller input
evtest /dev/input/event* 2>/dev/null | head -10

# Check SD card
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -E 'mmcblk|sd'
```

### Switching Desktop Mode

```bash
# Desktop Mode = KDE Plasma Wayland
# Game Mode = Gamescope/Weston

# Check current mode
# Game Mode: gamescope process running, no KDE
# Desktop Mode: plasmashell running
ps aux | grep -E 'plasmashell|gamescope' | grep -v grep

# Force restart into Desktop Mode
# Hold power button → select "Switch to Desktop"

# In Desktop Mode, check Wayland
loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type
```

## Wayland & Display

```bash
# Wayland compositor info
echo $WAYLAND_DISPLAY
echo $XDG_CURRENT_DESKTOP

# List connected displays
wlr-randr 2>/dev/null || xrandr 2>/dev/null || kscreen-doctor --outputs 2>/dev/null

# Screenshots
grim screenshot.png          # wlroots (Wayfire/Sway)
spectacle -f                 # KDE Plasma
gnome-screenshot -f          # GNOME

# Screen recording
wf-recorder -f recording.mp4  # wlroots
OBS                          # Flatpak

# Check HDR support
wlr-randr 2>/dev/null | grep -i hdr
```

## Layering Packages

```bash
# Install CLI tools (requires reboot)
rpm-ostree install gh vim tmux htop neofetch fastfetch

# Install development tools
rpm-ostree install gcc make cmake git

# Install Wine (for Lutris/Bottles)
rpm-ostree install wine

# Overlay specific RPM
rpm-ostree overlay /path/to/package.rpm

# Remove layered package
rpm-ostree uninstall <package>

# Reset to base image (removes all overlays)
rpm-ostree override reset

# Apply and reboot
systemctl reboot
```

## Rebase & Updates

```bash
# Rebase between Bazzite editions
rpm-ostree rebase ostree-image-signed:docker://ghcr.io/ublue-os/bazzite:stable
rpm-ostree rebase ostree-image-signed:docker://ghcr.io/ublue-os/bazzite-nvidia:stable
rpm-ostree rebase ostree-image-signed:docker://ghcr.io/ublue-os/bazzite-deck:stable

# Rollback if something breaks
rpm-ostree rollback
systemctl reboot

# Pin current deployment
rpm-ostree pin

# Clean old deployments
rpm-ostree cleanup -rp
```

## uBlue Custom Images

Bazzite is built on the uBlue framework. You can create custom images:

```bash
# Check if using custom image
cat /etc/os-release | grep -E 'IMAGE|VARIANT'

# uBlue overlay (apply after each update)
# Place in /etc/ublue-os/
ls /etc/ublue-os/ 2>/dev/null

# Check uBlue signing
rpm-ostree status | grep -i sign
```

## Performance & Tweaks

```bash
# Enable MangoHud globally
flatpak override --user --env=MANGOHUD=1 com.valvesoftware.Steam

# Check GPU performance
cat /sys/class/drm/card0/device/pp_dpm_sclk 2>/dev/null
cat /sys/class/drm/card0/device/pp_dpm_mclk 2>/dev/null

# Thermal governor
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor | sort -u

# Memory usage
free -h

# Disk usage
df -h /

# udev rules for controllers
ls /etc/udev/rules.d/ 2>/dev/null
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Update stuck | `rpm-ostree cancel` then retry |
| Flatpak won't launch | `flatpak repair` then restart |
| No sound | `systemctl --user restart wireplumber pipewire` |
| Display wrong resolution | `kscreen-doctor --outputs` (KDE) |
| Steam Deck won't enter Game Mode | Check `systemctl --user status` for errors |
| Package conflict after layering | `rpm-ostree override replace <url>` |
| SD card not mounting | `lsblk` then `sudo mount /dev/mmcblk0p1 /run/media/deck/sd` |
| Controller not detected | `evtest` + check `steam-input` service |
| Wayland app blurry | Check fractional scaling, try integer scale |
