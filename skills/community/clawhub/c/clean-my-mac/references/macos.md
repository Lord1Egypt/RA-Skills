# macOS Storage Layout & Classification Reference Guide

Use this reference when analyzing macOS scan results. It describes directory purposes and classification categories.

## Crucial Directories

| Directory | Purpose | Typical Classification |
|---|---|---|
| `~/Library/Caches/*` | App and system cache files (browsers, Homebrew, pip, Playwright) | 🟢 Safe to Clean |
| `~/.cache/*`, `~/.npm`, `~/.cargo`, `~/.gradle`, `~/.m2`, `~/.bun` | Developer tools cache directories | 🟢 Safe to Clean |
| `~/Library/Developer/Xcode/DerivedData`, `CoreSimulator` | Xcode build artifacts and simulator files | 🟢 Safe to Clean |
| `~/Library/Containers/com.docker.docker` | Docker Desktop virtual machine disk image and cache | 🟢 Safe to Clean |
| `~/Library/Containers/<UUID or bundleid>` | Sandbox application data (chat histories, offline videos, config) | 🟡 Needs Review |
| `~/Library/Application Support/*` | Local application state (Chrome profile, Claude VM data, Lark) | 🟡 Needs Review |
| `~/Downloads` (dmg/pkg files) | Downloaded software installation archives | 🟢 Safe to Clean |
| `/Applications/*.app` | Application bundles | 🔴 Caution (Manual Uninstall) |
| System Files & APFS Local Snapshots | Operating System files and backups | (Assigned to blue "System & Other" segment) |

## Identifying "Mysterious UUID Sandbox Containers"

UUID or Bundle ID named directories under `~/Library/Containers/` are matched using the following clues:
- Traverse `Data/Documents/` or `Data/Library/` to locate internal bundle-id identifiers.
- Heavy targets often hide offline contents in hidden folders (e.g., `.Downloads/` inside offline video players).
- Keep operations strictly read-only (`du`, `ls`).

## Indirect Disk Release Strategies (Include in dashboard `long_term`)

- Purgeable storage: Triggered automatically by macOS under low disk space pressure.
- Reboot the computer to reclaim swap files and temporary daemon caches.
- Execute `brew cleanup --prune=all` to clear Homebrew download caches.
- Clean Xcode DerivedData and Simulator devices periodically.
- Configure Time Machine snapshot retention settings.
