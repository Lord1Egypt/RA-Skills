# Desktop, Audio & Display — CachyOS

## Inhaltsverzeichnis
1. PipeWire & WirePlumber
2. Wayland
3. Xorg
4. Desktop-Umgebungen
5. Fonts & Rendering
6. Locale, Tastatur, Zeitzone
7. Display-Manager
8. Multi-Monitor

---

## 1. PipeWire & WirePlumber (CachyOS Default)

```bash
# Status
systemctl --user status pipewire pipewire-pulse wireplumber

# Geräte auflisten
wpctl status
pactl list sinks short
pactl list sources short

# Standard-Ausgabe setzen
wpctl set-default <sink-id>

# Lautstärke
wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.5       # 50%
wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+        # +5%
wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-        # -5%
wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle

# Bluetooth-Audio-Codecs
# PipeWire unterstützt: SBC, AAC, aptX, aptX-HD, LDAC
# /etc/pipewire/pipewire.conf.d/99-bluetooth.conf oder
# ~/.config/pipewire/pipewire.conf.d/99-bluetooth.conf
context.properties = {
  bluez5.codecs = [ sbc sbc_xq aac ldac aptx aptx_hd ]
}

# Latenz reduzieren (für Pro-Audio)
# ~/.config/pipewire/pipewire.conf.d/99-lowlatency.conf
context.properties = {
  default.clock.rate          = 48000
  default.clock.quantum       = 256
  default.clock.min-quantum   = 128
}

# Neustart
systemctl --user restart pipewire pipewire-pulse wireplumber

# Troubleshooting
pw-top                    # Echtzeit-Monitoring
pw-dump                   # Kompletter Graph
pw-cli list-objects       # Alle Objekte
journalctl --user -u pipewire -b
journalctl --user -u wireplumber -b

# ALSA-Kompatibilität
sudo pacman -S pipewire-alsa lib32-pipewire
# JACK-Kompatibilität
sudo pacman -S pipewire-jack lib32-pipewire-jack

# Easyeffects (System-weiter Equalizer)
sudo pacman -S easyeffects
```

---

## 2. Wayland

```bash
# Prüfen ob Wayland aktiv
echo $XDG_SESSION_TYPE
# "wayland" oder "x11"

# Wayland-Variablen (falls nötig)
# /etc/environment oder ~/.config/environment.d/wayland.conf
QT_QPA_PLATFORM=wayland
GDK_BACKEND=wayland
SDL_VIDEODRIVER=wayland
CLUTTER_BACKEND=wayland
MOZ_ENABLE_WAYLAND=1
ELECTRON_OZONE_PLATFORM_HINT=auto

# XWayland (für X11-Apps unter Wayland)
sudo pacman -S xorg-xwayland
# Läuft automatisch bei Bedarf

# Wayland-Diagnose
wlr-randr                  # Wlroots-basiert (Hyprland, Sway)
# KDE: systemsettings → Display
# GNOME: gnome-display-manager

# Screen-Sharing unter Wayland
sudo pacman -S xdg-desktop-portal xdg-desktop-portal-gtk
# KDE: xdg-desktop-portal-kde
# GNOME: xdg-desktop-portal-gnome
# Hyprland: xdg-desktop-portal-hyprland

# Clipboard unter Wayland
sudo pacman -S wl-clipboard
wl-copy "text"
wl-paste

# Screenshot
sudo pacman -S grim slurp
grim screenshot.png              # Ganzer Bildschirm
grim -g "$(slurp)" region.png   # Bereich auswählen
```

---

## 3. Xorg

```bash
# Xorg installieren
sudo pacman -S xorg-server xorg-xinit

# Config generieren
sudo Xorg :0 -configure
# → /root/xorg.conf.new

# Manuelle Config: /etc/X11/xorg.conf.d/
# GPU-spezifisch:
# /etc/X11/xorg.conf.d/20-nvidia.conf
Section "Device"
  Identifier "NVIDIA"
  Driver "nvidia"
  Option "Coolbits" "28"
EndSection

# Xorg-Logs
cat /var/log/Xorg.0.log | grep "(EE)"
cat /var/log/Xorg.0.log | grep "(WW)"

# Input-Geräte
xinput list
xinput list-props <id>

# Auflösung
xrandr
xrandr --output HDMI-1 --mode 2560x1440 --rate 165
xrandr --output eDP-1 --primary --auto --output HDMI-1 --right-of eDP-1 --auto
```

---

## 4. Desktop-Umgebungen

```bash
# KDE Plasma (CachyOS Default-Option)
sudo pacman -S plasma-meta kde-applications-meta
# Minimal:
sudo pacman -S plasma-desktop konsole dolphin sddm

# GNOME
sudo pacman -S gnome gnome-extra
sudo systemctl enable gdm

# Hyprland (Wayland Tiling WM, beliebt bei CachyOS)
sudo pacman -S hyprland hyprpaper waybar wofi foot
# Config: ~/.config/hypr/hyprland.conf

# Sway (i3-kompatibel, Wayland)
sudo pacman -S sway swaybar swaylock wofi foot

# XFCE (leichtgewichtig)
sudo pacman -S xfce4 xfce4-goodies

# i3 (X11 Tiling WM)
sudo pacman -S i3-wm i3status i3lock dmenu
```

---

## 5. Fonts & Rendering

```bash
# Essentielle Fonts
sudo pacman -S noto-fonts noto-fonts-cjk noto-fonts-emoji \
  ttf-liberation ttf-dejavu ttf-roboto \
  ttf-fira-code ttf-jetbrains-mono  # Coding-Fonts

# Microsoft-Fonts (AUR)
paru -S ttf-ms-win11-auto

# Font-Cache aktualisieren
fc-cache -fv

# Installierte Fonts auflisten
fc-list | sort
fc-list : family | sort | uniq

# Font-Rendering optimieren
# /etc/fonts/local.conf
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <match target="font">
    <edit name="antialias" mode="assign"><bool>true</bool></edit>
    <edit name="hinting" mode="assign"><bool>true</bool></edit>
    <edit name="hintstyle" mode="assign"><const>hintslight</const></edit>
    <edit name="rgba" mode="assign"><const>rgb</const></edit>
    <edit name="lcdfilter" mode="assign"><const>lcddefault</const></edit>
  </match>
</fontconfig>

# Subpixel-Rendering aktivieren
# /etc/profile.d/freetype2.sh
export FREETYPE_PROPERTIES="truetype:interpreter-version=40"
```

---

## 6. Locale, Tastatur, Zeitzone

```bash
# Locale
sudo nano /etc/locale.gen
# de_DE.UTF-8 UTF-8  → einkommentieren
sudo locale-gen

# /etc/locale.conf
LANG=de_DE.UTF-8
LC_COLLATE=C

# Tastatur (Console)
# /etc/vconsole.conf
KEYMAP=de-latin1

# Tastatur (Wayland/X11) — je nach DE
localectl set-x11-keymap de "" "" ""
# oder manuell:
# /etc/X11/xorg.conf.d/00-keyboard.conf
Section "InputClass"
  Identifier "keyboard"
  MatchIsKeyboard "on"
  Option "XkbLayout" "de"
EndSection

# Zeitzone
timedatectl set-timezone Europe/Berlin
timedatectl set-ntp true
timedatectl status

# Hardware-Clock
sudo hwclock --systohc
```

---

## 7. Display-Manager

```bash
# SDDM (KDE Standard, CachyOS Default)
sudo pacman -S sddm
sudo systemctl enable sddm

# GDM (GNOME)
sudo systemctl enable gdm

# LightDM
sudo pacman -S lightdm lightdm-gtk-greeter
sudo systemctl enable lightdm

# TTY-Login (kein DM)
# ~/.bash_profile oder ~/.zprofile:
if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then
  exec Hyprland  # oder startx, sway, etc.
fi

# DM wechseln
sudo systemctl disable sddm
sudo systemctl enable gdm
```

---

## 8. Multi-Monitor

```bash
# Wayland (KDE)
# systemsettings → Display & Monitor
# oder kscreen-doctor
kscreen-doctor --outputs

# Wayland (Hyprland)
# ~/.config/hypr/hyprland.conf
monitor=DP-1,2560x1440@165,0x0,1
monitor=HDMI-A-1,1920x1080@60,2560x0,1

# Wayland (Sway)
# ~/.config/sway/config
output DP-1 resolution 2560x1440@165Hz position 0 0
output HDMI-A-1 resolution 1920x1080@60Hz position 2560 0

# Xorg
xrandr --output DP-1 --primary --mode 2560x1440 --rate 165 \
       --output HDMI-1 --mode 1920x1080 --right-of DP-1

# NVIDIA Multi-Monitor (Xorg)
sudo nvidia-settings  # GUI-basierte Konfiguration
```
