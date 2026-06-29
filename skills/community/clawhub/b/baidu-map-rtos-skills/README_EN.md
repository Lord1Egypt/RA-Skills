# Workspace

[中文](README.md)

This repository provides an AI Coding Agent Skill for **Baidu Map RTOS SDK (mapsdk-rtos)**, helping developers efficiently integrate RTOS map applications, implement Canvas adapters, control map components, draw overlays, use search and route planning, manage offline maps, and build navigation features within intelligent coding tools (e.g. Cursor, Claude Code).

## Skills Overview

This repository includes the following Skill:

| Skill | Description |
| --- | --- |
| [baidu-map-rtos-skills](./) | Baidu Map RTOS SDK (mapsdk-rtos) application-layer integration assistant |

---

### baidu-map-rtos-skills

Application-layer integration guidelines and code generation for Baidu Map RTOS SDK (mapsdk-rtos).

- **Initialization and authentication** — License authentication, base configuration, package name/cache path/version info, initialization order, and integration checklist
- **Map component control** — `MapComponentApi` setup, lifecycle, map state control, render requests, and touch events
- **Canvas adapter layer** — C function stubs, C++ adapter classes, `MapCanvasImpl` binding, drawing/text/clipping/transform implementation notes
- **Overlay drawing** — Markers, polylines, point lists / GeoJSON, style setup, visibility control, and layer updates
- **Search and route planning** — POI search, reverse geocoding, walking/driving route planning, and route tile preloading
- **Offline maps** — Version requests, downloadable city list, download status, and offline package management
- **Navigation** — `NaviApi` setup, route result integration, navigation startup, and state callbacks
- **Demo extension** — Add application-layer demos in the rtos-mac-simulator (mapAPP) project

This Skill applies to RTOS map application development that integrates public `*_api.h` headers under `outputIncludes/`.

## Requirements

- **Platform**: RTOS / macOS simulator (rtos-mac-simulator / mapAPP)
- **Language**: C / C++
- **SDK**: mapsdk-rtos
- **Core APIs**: `MapComponentApi`, `AuthLicenseApi`, `SearchApi`, `NaviApi`, `MapOfflineApi`
- **Integration**: Public headers under `outputIncludes/` plus platform Adapter / Canvas implementations

## Directory structure

```
rtos-sdk-skills/
├── README.md                         # This file (Chinese)
├── README_EN.md                      # English README
├── SKILL.md                          # Skill definition
└── references/
    ├── adapter-build.md              # Platform Adapter and Canvas implementation
    ├── demo.md                       # End-to-end runnable examples
    ├── init-auth.md                  # Initialization, authentication, and troubleshooting
    ├── overlay-map-control.md        # Map control and overlays
    └── search-navi-offline.md        # Search, navigation, and offline maps
```

## How to use

### 1. Clone this repository

```bash
git clone https://github.com/baidu-maps/rtos-sdk-skills.git
cd rtos-sdk-skills
```

### 2. Download from Release (optional)

You can also download the `rtos-sdk-skills.zip` asset from [Releases](https://github.com/baidu-maps/rtos-sdk-skills/releases) and extract it:

```bash
unzip rtos-sdk-skills.zip
cd rtos-sdk-skills
```

### 3. Register the Skill with your AI assistant

Link or copy this repository folder to your environment’s skills directory so the AI can load these docs during conversations.

**Claude Code (local)**

- Skills directory is usually: `~/.claude/skills/`
- Register (symlink, recommended):
  ```bash
  ln -sfn "$(pwd)" ~/.claude/skills/baidu-map-rtos-skills
  ```
- Or copy this repository folder into `~/.claude/skills/baidu-map-rtos-skills`.

**Cursor**

- Skills directory is usually: `~/.cursor/skills-cursor/`
- Register (symlink, recommended):
  ```bash
  ln -sfn "$(pwd)" ~/.cursor/skills-cursor/baidu-map-rtos-skills
  ```
- Or copy this repository folder into `~/.cursor/skills-cursor/baidu-map-rtos-skills`.

### 4. Use in conversation

In a client that supports Skills, when your question involves keywords like “RTOS map SDK”, “mapsdk-rtos”, “MapComponentApi”, “AuthLicenseApi”, “SearchApi”, “NaviApi”, “MapOfflineApi”, “Canvas adapter”, “RTOS overlays”, “RTOS navigation”, or “RTOS offline maps”, the assistant will prefer this repository’s docs and give answers and code aligned with Baidu Map RTOS SDK.

## References

- [SKILL.md](SKILL.md) — Skill trigger guidance, boundaries, and quick reference
- [references/init-auth.md](references/init-auth.md) — Authentication, initialization order, Canvas adapter, integration checklist, and troubleshooting keywords
- [references/adapter-build.md](references/adapter-build.md) — Platform Adapter interface list, `MapCanvasImpl` implementation notes, and binding flow
- [references/overlay-map-control.md](references/overlay-map-control.md) — Map state control, markers, polylines, touch events, and route tile preloading
- [references/search-navi-offline.md](references/search-navi-offline.md) — Search, navigation, offline maps, and mapAPP demo extension
- [references/demo.md](references/demo.md) — End-to-end runnable examples

## License

This project is an internal Baidu project for authorized use only.
