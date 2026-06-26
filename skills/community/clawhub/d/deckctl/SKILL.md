---
name: deckctl
description: Steam Deck & Bazzite system management — gamescope, flatpak, podman, GPU, performance, game mode, system health
version: 1.0.0
tags:
  - steam-deck
  - bazzite
  - gaming
  - linux
  - system
  - flatpak
  - gamescope
---

# deckctl — Steam Deck / Bazzite System Manager

Manage Steam Deck hardware and Bazzite OS through OpenClaw. Covers gaming performance, system health, Flatpak management, GPU monitoring, and Gamescope session control.

## When to Use

- User asks about Steam Deck system status, performance, or configuration
- Flatpak app installation, updates, or management
- Gamescope session or game mode troubleshooting
- GPU/memory/disk monitoring on Steam Deck hardware
- Proton, Lutris, or containerized gaming setup
- Sunshine/moonlight streaming configuration
- MangoHud, vkBasalt, or OBS VkCapture toggles

## Prerequisites

- Steam Deck (LCD/OLED) or Bazzite desktop
- `gamescope-session-plus@steam` systemd service
- Flatpak, podman, rpm-ostree available

## Commands Reference

### System Status

```bash
# Full system health check
echo "=== System ===" && uname -a && uptime
echo "=== Memory ===" && free -h
echo "=== Disk ===" && df -h / /var/home
echo "=== GPU ===" && lspci | grep -i vga
echo "=== CPU ===" && cat /proc/loadavg && nproc
echo "=== Temp ===" && cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null
```

### Gamescope / Game Mode

```bash
# Check gamescope session
systemctl --user status gamescope-session-plus@steam.service

# Gamescope logs
journalctl --user -u gamescope-session-plus@steam.service --since "1 hour ago" --no-pager | tail -20

# Steam runtime info
ls ~/.steam/root/ubuntu12_32/steam-runtime/ 2>/dev/null
```

### Flatpak Management

```bash
# List installed flatpaks
flatpak list

# Search for an app
flatpak search <query>

# Install a flatpak
flatpak install flathub <app-id>

# Update all flatpaks
flatpak update

# Check for updates without installing
flatpak remote-info flathub <app-id>
```

### GPU & Performance

```bash
# GPU info
lspci -nnk | grep -iA3 vga

# GPU memory (AMD VanGogh)
cat /sys/class/drm/card*/device/mem_info_vram_total 2>/dev/null

# Vulkan info
vulkaninfo --summary 2>/dev/null | head -30

# Active GPU frequency (AMD)
cat /sys/class/drm/card0/device/pp_dpm_sclk 2>/dev/null
cat /sys/class/drm/card0/device/pp_dpm_mclk 2>/dev/null

# MangoHud toggle (per-game via env var)
MANGOHUD=1 %command%
# Or in Gamescope:
gamescope -W 1280 -H 800 -f -- mangohud <game>
```

### Proton & Compatibility

```bash
# Installed Proton versions
ls ~/.steam/root/compatibilitytools.d/ 2>/dev/null
ls ~/.local/share/Steam/compatibilitytools.d/ 2>/dev/null

# Proton logs for a game
cat ~/.steam/root/logs/proton* 2>/dev/null | tail -20

# Protontricks
protontricks <appid> <verb>
```

### Lutris

```bash
# Lutris version
lutris --version

# Lutris installed games
lutris --list-games

# Lutris runners
ls ~/.local/share/lutris/runners/ 2>/dev/null
```

### Container Gaming

```bash
# Podman status
podman ps
podman images

# Distrobox containers
distrobox list 2>/dev/null

# Toolbox containers
toolbox list 2>/dev/null
```

### Streaming (Sunshine)

```bash
# Sunshine status
flatpak list | grep -i sunshine

# Sunshine config
cat ~/.config/sunshine/config.conf 2>/dev/null

# Sunshine logs
journalctl --user -u sunshine --since "1 hour ago" 2>/dev/null | tail -20
```

### OBS & Capture

```bash
# OBS plugins (VkCapture)
flatpak list | grep -i obs

# VkCapture layers
ls ~/.local/share/vulkan/implicit_layer.d/ 2>/dev/null
flatpak list | grep -i vkcapture
```

### Network & Tailscale

```bash
# Network interfaces
ip addr show | grep -E "inet |wl|en"

# Tailscale
tailscale status 2>/dev/null

# Port forwarding (for Sunshine)
tailscale serve --bg 47989 2>/dev/null
```

## Common Tasks

### Install a game from Flathub

```bash
flatpak search "game name"
flatpak install flathub <app-id>
```

### Check why a game is slow

1. Check GPU frequency: `cat /sys/class/drm/card0/device/pp_dpm_sclk`
2. Check thermal throttling: `cat /sys/class/thermal/thermal_zone*/temp`
3. Check if MangoHud is running: `pgrep -a mangohud`
4. Check Proton version: `ls ~/.steam/root/compatibilitytools.d/`
5. Check VRAM usage: `cat /sys/class/drm/card*/device/mem_info_vram_used 2>/dev/null`

### Enable/disable performance overlay

```bash
# MangoHud via environment
export MANGOHUD=1  # enable
export MANGOHUD=0  # disable

# Persistent for Steam games
echo "MANGOHUD=1" >> ~/.steam/root/steam.sh.d/mangohud.conf 2>/dev/null
```

### Factory reset a Flatpak

```bash
flatpak uninstall --delete-data <app-id>
```

## Troubleshooting

| Problem | Check |
|---------|-------|
| Game won't start | Proton version, disk space, GPU driver |
| Black screen | Gamescope resolution, HDR toggle, Wayland |
| Stuttering | VRAM, thermal throttling, swap |
| Audio crackling | PipeWire restart: `systemctl --user restart wireplumber pipewire` |
| Controller not working | `evtest`, `journalctl -f`, Steam Input settings |
| Flatpak won't update | `flatpak repair`, disk space |
| Steam Proton missing | Verify Proton in Steam Settings > Compatibility |

## Notes

- Steam Deck uses AMD VanGogh APU (RDNA 2, 8 CUs)
- OLED model has same APU, better screen
- Bazzite is Fedora-based with immutable root (rpm-ostree)
- Flatpak is the primary package manager for GUI apps
- Gamescope provides the gaming compositor layer
- Always check thermal zones before diagnosing performance issues
