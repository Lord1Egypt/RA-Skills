# Gaming-Optimierung — CachyOS

## Inhaltsverzeichnis
1. Proton / Wine
2. GameMode
3. MangoHud
4. Steam
5. Lutris / Heroic / Bottles
6. Kernel-Parameter für Gaming
7. Gamepad-Support
8. DXVK / VKD3D-Proton
9. Shader-Cache
10. Game-spezifisches Troubleshooting

---

## 1. Proton / Wine

```bash
# CachyOS-optimiertes Proton
sudo pacman -S proton-cachyos

# Wine-CachyOS (Nicht-Steam-Spiele)
sudo pacman -S wine-cachyos

# Wine-Abhängigkeiten (32-bit!)
sudo pacman -S lib32-mesa lib32-vulkan-radeon lib32-vulkan-intel \
  lib32-nvidia-utils lib32-pipewire lib32-libpulse wine-mono wine-gecko \
  lib32-gnutls lib32-sdl2 lib32-libxml2 lib32-mpg123 lib32-openal \
  lib32-giflib lib32-libpng lib32-gst-plugins-base lib32-libjpeg-turbo

# Winetricks
sudo pacman -S winetricks
winetricks vcrun2022 dotnet48 dxvk  # Typische Deps

# Wine-Prefix erstellen
WINEPREFIX=~/.wine64 WINEARCH=win64 winecfg
```

---

## 2. GameMode

```bash
sudo pacman -S gamemode lib32-gamemode

# Testen
gamemoded -t

# Steam Launch-Option:
# gamemoderun %command%
```

Config: `~/.config/gamemode.ini`

```ini
[general]
renice = 10
softrealtime = auto
ioprio = 0
inhibit_screensaver = 1
disable_splitlock = 1

[gpu]
apply_gpu_optimisations = accept-responsibility
gpu_device = 0
amd_performance_level = high
# nvidia_powermize_mode = 1

[cpu]
pin_cores = yes
# park_cores = no
# Bestimmte Cores zuweisen:
# pin_cores = 0-7

[custom]
start = /usr/bin/notify-send 'GameMode' 'Aktiviert'
end = /usr/bin/notify-send 'GameMode' 'Deaktiviert'
# start = /usr/bin/cpupower frequency-set -g performance
# end = /usr/bin/cpupower frequency-set -g schedutil
```

---

## 3. MangoHud

```bash
sudo pacman -S mangohud lib32-mangohud

# Steam: mangohud %command%
# Flatpak: MANGOHUD=1 flatpak run ...

# Toggler: Rechts-Shift + F12 (default)
```

Config: `~/.config/MangoHud/MangoHud.conf`

```ini
# Minimales Overlay
fps
fps_limit=0
frame_timing
gpu_stats
gpu_temp
gpu_core_clock
gpu_mem_clock
gpu_power
cpu_stats
cpu_temp
cpu_power
ram
vram
vulkan_driver
wine
gamemode
fsr
position=top-left
font_size=20
background_alpha=0.5
toggle_hud=Shift_R+F12
toggle_logging=Shift_L+F2
output_folder=/home/$USER/mangohud-logs
```

---

## 4. Steam

```bash
sudo pacman -S steam

# Multilib muss aktiviert sein!
# /etc/pacman.conf → [multilib] auskommentieren

# Steam Beta (optional, für neueste Proton-Features)
# Steam → Settings → Interface → Client Beta Participation

# Proton-CachyOS als Standard:
# Settings → Compatibility → Enable Steam Play for all titles
# Proton-CachyOS wählen
```

### Launch-Optionen (Pro Spiel)

| Option | Zweck |
|--------|-------|
| `gamemoderun %command%` | GameMode |
| `mangohud gamemoderun %command%` | GameMode + HUD |
| `DXVK_ASYNC=1 %command%` | Async Shader (DXVK, weniger Stutter) |
| `PROTON_ENABLE_NVAPI=1 %command%` | NVIDIA NVAPI (DLSS) |
| `PROTON_HIDE_NVIDIA_GPU=0 %command%` | GPU nicht verstecken |
| `VKD3D_CONFIG=dxr %command%` | DirectX Raytracing |
| `RADV_PERFTEST=gpl %command%` | AMD Graphics Pipeline Library |
| `mesa_glthread=true %command%` | OpenGL Threading (AMD/Intel) |
| `__GL_SHADER_DISK_CACHE=1 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%` | Shader-Cache unlimited (NVIDIA) |
| `WINE_FULLSCREEN_FSR=1 %command%` | FSR Upscaling (Wine/Proton) |
| `WINE_FULLSCREEN_FSR_STRENGTH=2 %command%` | FSR Sharpness (0-5, 2=Standard) |
| `SteamDeck=1 %command%` | Steam-Deck-Kompatibilitätsmodus erzwingen |
| `PROTON_NO_FSYNC=1 %command%` | Fsync deaktivieren (bei Crashes) |

### Steam-Verzeichnisse

```bash
~/.steam/steam/                          # Steam-Root
~/.steam/steam/steamapps/common/         # Installierte Spiele
~/.steam/steam/steamapps/compatdata/     # Proton-Prefixes (pro Spiel)
~/.steam/steam/steamapps/shadercache/    # Shader-Cache
```

---

## 5. Lutris / Heroic / Bottles

```bash
# Lutris (GOG, Epic, eigene Installer)
sudo pacman -S lutris

# Heroic Games Launcher (Epic, GOG, Amazon)
paru -S heroic-games-launcher-bin

# Bottles (Wine-Prefix-Manager)
sudo pacman -S bottles
# oder Flatpak:
flatpak install flathub com.usebottles.bottles

# ProtonUp-Qt (Proton/Wine-Version-Manager)
paru -S protonup-qt
# oder Flatpak:
flatpak install flathub net.davidotek.pupgui2
```

---

## 6. Kernel-Parameter für Gaming

```
preempt=full              # Volle Preemption, niedrigste Latenz
threadirqs                # IRQs als Kernel-Threads
nowatchdog nmi_watchdog=0 # Weniger Interrupts
tsc=reliable              # TSC als Clocksource (stabiler)
mitigations=off           # CPU-Mitigations aus (nur Desktop!)
split_lock_detect=off     # Kein Performance-Hit durch Split-Lock
```

Für NVIDIA zusätzlich:
```
nvidia_drm.modeset=1 nvidia_drm.fbdev=1
```

---

## 7. Gamepad-Support

```bash
# Xbox Wireless (Bluetooth)
sudo pacman -S xpadneo-dkms

# Xbox One USB/Wireless-Dongle
paru -S xone-dkms

# Steam Input (in Steam integriert, unterstützt fast alles)
# Steam → Settings → Controller → General Controller Settings

# DualSense (PS5) — nativ ab Kernel 5.12 via hid-playstation
# Bluetooth: pairen via bluetoothctl

# DualShock 4 (PS4)
sudo pacman -S ds4drv
# oder nativ via hid-playstation (Kernel ≥5.12)

# 8BitDo / generische Controller
# Meist via xpad oder hid-generic erkannt

# Controller testen
sudo pacman -S evtest jstest-gtk
evtest /dev/input/eventX
jstest-gtk  # GUI

# udev-Rule für Controller ohne root
# /etc/udev/rules.d/80-gamepad.rules
SUBSYSTEM=="input", ATTRS{name}=="*Xbox*", MODE="0666"
SUBSYSTEM=="input", ATTRS{name}=="*DualSense*", MODE="0666"
```

---

## 8. DXVK / VKD3D-Proton

```bash
# DXVK (DirectX 9/10/11 → Vulkan) — in Proton enthalten
# Standalone:
sudo pacman -S dxvk-bin

# VKD3D-Proton (DirectX 12 → Vulkan) — in Proton enthalten
# Standalone:
paru -S vkd3d-proton-bin

# DXVK-Konfiguration: ~/.config/dxvk.conf
# oder DXVK_CONFIG_FILE=/path/to/dxvk.conf

# dxvk.conf Beispiel:
dxvk.enableAsync = true
dxvk.numCompilerThreads = 4
dxvk.useRawSsbo = true
d3d9.maxFrameLatency = 1
d3d11.maxFrameLatency = 1
```

---

## 9. Shader-Cache

```bash
# Vulkan Pipeline-Cache (automatisch in ~/.cache/mesa_shader_cache)
# Größe konfigurieren:
export MESA_SHADER_CACHE_MAX_SIZE=10G

# NVIDIA Shader-Cache
# Default: ~/.nv/GLCache
export __GL_SHADER_DISK_CACHE=1
export __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1

# Steam Shader Pre-Caching aktivieren:
# Steam → Settings → Shader Pre-Caching → Enable
```

---

## 10. Game-spezifisches Troubleshooting

```bash
# Proton-Log aktivieren
PROTON_LOG=1 PROTON_LOG_DIR=/tmp/proton-logs %command%

# Wine-Debug
WINEDEBUG=+loaddll,+seh %command%

# Vulkan-Probleme diagnostizieren
vulkaninfo --summary
VK_LOADER_DEBUG=all vulkaninfo 2>&1 | head -50

# Stutter-Probleme
# 1. Shader Pre-Caching in Steam aktivieren
# 2. DXVK_ASYNC=1 nutzen
# 3. Shader-Cache nicht löschen

# Anti-Cheat (EAC/BattlEye)
# Proton-Status prüfen: https://www.protondb.com/
# EAC/BattlEye benötigen Game-Developer-Support für Linux

# Steam-Prefix zurücksetzen
rm -rf ~/.steam/steam/steamapps/compatdata/<APPID>/

# Spezifische Proton-Version pro Spiel erzwingen
# Steam → Rechtsklick auf Spiel → Properties → Compatibility
```
