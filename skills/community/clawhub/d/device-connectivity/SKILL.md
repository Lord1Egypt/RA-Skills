---
name: device-connectivity
description: Use when pairing a phone with Linux via KDE Connect.
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
---

# Device Connectivity (Phone ↔ Desktop)

Pair your Android/iOS device with your Linux desktop for file sharing, notification sync, clipboard sync, media control, virtual touchpad, and more via the KDE Connect protocol.

## Available Implementations

| Implementation | Platform | Notes |
|---|---|---|
| KDE Connect (native) | Any distro with dnf/apt/pacman | `sudo dnf install kdeconnectd` |
| **Valent** (Flatpak) | All distros, incl. immutable | GTK4 implementation, nightly Flatpak. Best option on Fedora Atomic/bootc. |
| GSConnect | GNOME Shell | GNOME Shell extension implementing KDE Connect protocol |

## Valent (Recommended on Fedora Atomic / bootc)

KDE Connect is **not** available on Flathub. Homebrew has no Linux formula. Pip/PyPI has nothing. KDE's own Flatpak repo (`distribute.kde.org`) has been unreliable.
Valent is the only straightforward path on immutable systems.

### Installation

```bash
flatpak install --user -y --from https://valent.andyholmes.ca/valent.flatpakref
```

### Ports

Valent uses the KDE Connect protocol with a narrower port range than the original:

| Port | Protocol | Purpose |
|---|---|---|
| **1716** | UDP | Device discovery (broadcasts) |
| **1716** | TCP | Main connection, pairing, commands |
| **1739–1764** | TCP | Auxiliary streams (file transfers, etc.) |

### Firewall

On Fedora, the default **FedoraWorkstation** zone opens ports 1025–65535, so **no changes needed**:

```xml
<port protocol="udp" port="1025-65535"/>
<port protocol="tcp" port="1025-65535"/>
```

If the interface is on the **public** zone (more restrictive), allow the ports:

```bash
sudo firewall-cmd --permanent --add-port=1716/tcp --add-port=1716/udp
sudo firewall-cmd --permanent --add-port=1739-1764/tcp
sudo firewall-cmd --reload
```

To check which zone is active:
```bash
sudo firewall-cmd --get-active-zones
```

### Running

```bash
flatpak run ca.andyholmes.Valent
```

Launches as a background daemon + pairing GUI. Works on any Wayland compositor (niri, sway, river, GNOME, KDE).

## Pitfalls

- **KDE Connect and Valent conflict** — they cannot run simultaneously. Both claim port 1716. Stop one before launching the other.
- **Valent is alpha** (1.0.0.alpha.49 as of mid-2026). Some features may be missing vs. KDE Connect.
- **No GNOME Shell extension needed** on non-GNOME WMs — the Flatpak handles device discovery, pairing, and all protocol functions without it.
- **Flatpak permissions** include system D-Bus access to BlueZ (Bluetooth), Avahi (mDNS), ModemManager, UPower, and login1 — all necessary for protocol features.
- **Phone app**: pair with the official KDE Connect app (Android/F-Droid) or KDE Connect for iOS — Valent speaks the same protocol.
