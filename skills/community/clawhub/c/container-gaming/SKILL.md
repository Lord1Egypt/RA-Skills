---
name: container-gaming
description: Container-based gaming setup on Linux — Podman, Distrobox, Flatpak gaming, Wine/Proton containers, Sunshine streaming
version: 1.0.0
tags:
  - gaming
  - podman
  - distrobox
  - flatpak
  - wine
  - proton
  - sunshine
  - streaming
  - lutris
  - linux
metadata:
  {"openclaw": {"requires": {"anyBins": ["podman", "flatpak", "distrobox"]}, "os": ["linux"]}}
---

# Container Gaming Manager

Manage container-based gaming on Linux — Podman, Distrobox, Flatpak gaming, Wine/Proton, and game streaming with Sunshine.

## When to Use

- Setting up gaming in containers (Podman/Distrobox)
- Managing Flatpak game installations
- Wine/Proton configuration and troubleshooting
- Sunshine/Moonlight streaming setup
- Lutris runner management
- Game compatibility and performance issues

## Container Gaming Overview

```
┌─────────────────────────────────────┐
│        Sunshine (Streaming)         │
├─────────────────────────────────────┤
│  Gamescope (Compositor)              │
├──────┬──────┬───────────┬───────────┤
│Steam │Flatpak│ Lutris   │ Bottles   │
├──────┴──────┴───────────┴───────────┤
│  Proton / Wine / Native              │
├─────────────────────────────────────┤
│  Podman / Distrobox / Toolbox        │
├─────────────────────────────────────┤
│  Bazzite / Fedora Atomic             │
└─────────────────────────────────────┘
```

## Commands Reference

### Podman Gaming

```bash
# List gaming containers
podman ps -a --filter name=game

# Run a Windows game in Wine container
podman run --rm -it \
  --device /dev/dri \
  -e DISPLAY=:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/Games:/games \
  docker.io/bottles:latest

# Pull common gaming images
podman pull docker.io/library/ubuntu:latest
podman pull docker.io/bottleshq/bottles:latest
```

### Distrobox (Windows-like gaming in containers)

```bash
# Install Distrobox
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sudo sh

# Create gaming container (Ubuntu)
distrobox create --name gaming-ubuntu --image ubuntu:latest

# Enter container
distrobox enter gaming-ubuntu

# Install gaming tools inside container
sudo apt install wine lutris steam

# Export Steam to host
distrobox export --app steam --extra-flags "gamescope -W 1280 -H 800 -f"

# List containers
distrobox list

# Remove container
distrobox rm gaming-ubuntu
```

### Toolbox (Fedora-native)

```bash
# Create gaming toolbox
toolbox create -c gaming

# Enter
toolbox enter gaming

# Install tools
sudo dnf install steam lutris wine
```

### Flatpak Gaming

```bash
# Popular gaming Flatpaks
flatpak install flathub com.valvesoftware.Steam
flatpak install flathub net.lutris.Lutris
flatpak install flathub com.usebottles.bottles
flatpak install flathub org.prismlauncher.PrismLauncher
flatpak install flathub com.heroicgameslauncher.hgl
flatpak install flathub io.github.Foldex.Exodus
flatpak install flathub com.obsproject.Studio

# Update gaming Flatpaks
flatpak update com.valvesoftware.Steam net.lutris.Lutris com.usebottles.bottles

# Check runtime versions
flatpak info --runtime com.valvesoftware.Steam

# Override permissions for game
flatpak override --user --device=dri com.valvesoftware.Steam
flatpak override --user --socket=wayland com.valvesoftware.Steam
```

### Bottles (Wine Manager)

```bash
# Install Bottles
flatpak install flathub com.usebottles.bottles

# Bottles config directory
ls ~/.local/share/bottles/

# Create custom bottle
# (Done through Bottles GUI — usually at ~/.local/share/bottles/bottles/)
```

### Proton / Wine

```bash
# Installed Proton versions
ls ~/.steam/root/compatibilitytools.d/
ls ~/.local/share/Steam/compatibilitytools.d/

# Proton logs
cat ~/.steam/root/logs/proton* 2>/dev/null | tail -30

# Protontricks (install Windows deps for games)
protontricks <appid> corefonts d3dcompiler_47 dxvk
protontricks --list-apps 2>/dev/null | head -20

# Wine version check
wine --version 2>/dev/null
```

### Lutris

```bash
# Lutris version
lutris --version

# List installed games
lutris --list-games

# Lutris runners
ls ~/.local/share/lutris/runners/
ls ~/.local/share/lutris/runners/wine/

# Install Lutris runner
lutris --list-runners | grep -i wine

# Lutris config
cat ~/.config/lutris/lutris.conf 2>/dev/null
```

### Heroic Games Launcher (Epic/GOG)

```bash
# Install
flatpak install flathub com.heroicgameslauncher.hgl

# Heroic config
ls ~/.config/heroic/ 2>/dev/null
ls ~/.var/app/com.heroicgameslauncher.hgl/config/heroic/ 2>/dev/null
```

### Sunshine (Game Streaming)

```bash
# Install Sunshine
flatpak install flathub dev.lizardbyte.app.Sunshine

# Sunshine config location
cat ~/.config/sunshine/config.conf 2>/dev/null
cat ~/.config/sunshine/apps.json 2>/dev/null

# Start Sunshine
systemctl --user start sunshine 2>/dev/null

# Sunshine logs
journalctl --user -u sunshine --since "1 hour ago" 2>/dev/null | tail -20

# Check port
ss -tlnp | grep -E '47989|47990|48010'

# Web UI
# http://localhost:47990

# Tailscale (expose to remote)
tailscale serve --bg 47989 2>/dev/null
tailscale serve --bg 47990 2>/dev/null
```

### MangoHud (Performance Overlay)

```bash
# Enable MangoHud globally
export MANGOHUD=1

# Per-game config
mkdir -p ~/.config/MangoHud
cat > ~/.config/MangoHud/game-name.conf << 'EOF'
full
fps
cpu_temp
gpu_temp
vram
ram
frame_timing
EOF

# Gamescope + MangoHud
gamescope -W 1280 -H 800 -f -- mangohud %command%
```

### vkBasalt (Post-processing)

```bash
# Enable
export VKBASALT_ENABLE=1

# Config
cat ~/.config/vkBasalt/vkBasalt.conf 2>/dev/null

# Effects: cas (sharpen), fxaa, smaa, dls
```

## Common Tasks

### Set up a new game via Flatpak

```bash
flatpak search "game name"
flatpak install flathub <app-id>
flatpak override --user --device=dri --socket=wayland <app-id>
```

### Fix game performance issues

1. Enable MangoHud: `MANGOHUD=1 %command%`
2. Check GPU freq: `cat /sys/class/drm/card0/device/pp_dpm_sclk`
3. Check thermal: `cat /sys/class/thermal/thermal_zone*/temp`
4. Try Proton Experimental: set in Steam > Compatibility
5. Check VRAM: games with 4GB+ VRAM may struggle on Steam Deck

### Stream a game to another device

1. Install Sunshine (Flatpak)
2. Configure in Web UI (localhost:47990)
3. On client: install Moonlight
4. Connect using Tailscale IP or local IP

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Game won't launch | Check Proton version, try different runner |
| Black screen | Gamescope res, HDR toggle, Wayland vs X11 |
| Stuttering | VRAM, thermal, MangoHud to diagnose |
| Audio issues | `systemctl --user restart wireplumber pipewire` |
| Sunshine no video | Check GPU access, Sunshine permissions |
| Flatpak crash | `flatpak repair`, check permissions |
| Wine missing DLL | `protontricks <appid> <dll_name>` |
| Controller not working | Steam Input, `evtest`, kernel modules |
