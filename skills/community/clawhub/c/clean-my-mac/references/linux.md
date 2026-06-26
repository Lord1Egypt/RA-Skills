# Linux Storage Layout & Classification Reference Guide

Use this reference when analyzing Linux scan results. It describes directory purposes and classification categories.

## Crucial Directories

| Path | Purpose | Typical Classification |
|---|---|---|
| `~/.cache/*` | Application caches (browsers, thumbnail builders, terminal tools) | 🟢 Safe to Clean |
| `~/.cache/pip`, `~/.cache/uv`, `~/.npm`, `~/.cargo`, `~/.gradle`, `~/.m2`, `~/.bun` | Developer tools cache directories | 🟢 Safe to Clean |
| `~/.cache/ms-playwright` | Playwright browser downloads | 🟢 Safe to Clean |
| `~/go/pkg` | Go package cache | 🟢 Safe to Clean |
| `~/.docker` | Local Docker configurations and cached layers | 🟢 Safe to Clean |
| `~/Downloads` | Downloads directory, cached packages (.deb, .rpm files) | 🟢 Safe to Clean |
| `/usr/share/applications/*.desktop` | Application desktop launchers | 🔴 Caution (Manual Uninstall) |
| `/var/cache/apt/archives` (Debian/Ubuntu) | Cached package installer files | 🟢 Safe to Clean (Run `apt-get clean`) |
| `/var/log/*` | System logs and logs archives | 🟡 Needs Review (Use `journalctl --vacuum-size`) |
| `~/.local/share/Trash` | Freedesktop compliance Trash Bin | 🟡 Needs Review (Empty Trash) |

## Linux Deletion & Trash Specification

The `server.py` implements the **Freedesktop Trash specification**:
- Trashed items are moved to `~/.local/share/Trash/files/`.
- A metadata entry is created at `~/.local/share/Trash/info/[name].trashinfo` to store the deletion date and original absolute path.
- This allows native desktop environments (GNOME Nautilus, KDE Dolphin, XFCE Thunar) to restore files seamlessly.
- Deletions use `xdg-open` for opening directories inside the default file manager.
