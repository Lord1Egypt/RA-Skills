# Windows Storage Layout & Classification Reference Guide

Use this reference when analyzing Windows scan results. It describes directory purposes and classification categories.

## Multi-Drive Layout

Windows installations often feature multiple volumes (C:, D:, etc.). The total overview displays statistics for all connected drives, but optimization focuses primarily on the system partition (usually C:), where AppData, system temp, and user cache directories reside. Other folders on extra drives are classified under 🟡 Needs Review.

## Crucial Directories

| Path (Env Variables) | Purpose | Typical Classification |
|---|---|---|
| `%LOCALAPPDATA%` (`C:\Users\<u>\AppData\Local`) | Local application caches, telemetry, temporary stores | Cache 🟢 / User Data 🟡 |
| `%LOCALAPPDATA%\Temp`, `%TEMP%` | System and user temporary directory | 🟢 Safe to Clean |
| `%APPDATA%` (Roaming) | Application configurations, configurations, user databases | 🟡 Needs Review |
| Browser Cache: `%LOCALAPPDATA%\Google\Chrome\User Data\*\Cache` | Browser cache assets | 🟢 Safe to Clean |
| `%LOCALAPPDATA%\Packages\<dist>\LocalState\ext4.vhdx` | WSL (Windows Subsystem for Linux) virtual disk images | 🟡 Needs Review |
| `%LOCALAPPDATA%\Docker\wsl` | Docker Desktop WSL backing files | 🟢 Safe to Clean |
| `%USERPROFILE%\.cache`, `.npm`, `.gradle`, `.m2`, `.nuget\packages`, `.cargo`, `.bun` | Development tool environments | 🟢 Safe to Clean |
| `C:\Program Files`, `Program Files (x86)` | Standard installed software bundles | 🔴 Caution (Manual Uninstall) |
| `%USERPROFILE%\Downloads` | Download archives, installers (.exe, .msi files) | 🟢 Safe to Clean |
| `C:\$Recycle.Bin` | Windows Recycle Bin | 🟡 Needs Review (Empty Recycle Bin) |

## System Reserved Space (Do Not Clean Directly)

- `C:\Windows\WinSxS`: Windows Side-by-Side assembly cache. Use `DISM /Online /Cleanup-Image /StartComponentCleanup` instead of direct removal.
- `C:\Windows\SoftwareDistribution\Download`: Windows Update download staging cache. Best cleaned via Disk Cleanup (`cleanmgr`).
- `hiberfil.sys` & `pagefile.sys`: Windows hibernation state and virtual memory pagination files. Handled by OS settings.
- Reclaim space via: Settings > System > Storage > Storage Sense, or running Extended Disk Cleanup.
