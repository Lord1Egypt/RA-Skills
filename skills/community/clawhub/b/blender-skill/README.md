# Blender MCP Skill

An OpenClaw Agent Skill for connecting to and controlling Blender via the official [Blender MCP Server](https://www.blender.org/lab/mcp-server/).

**Version: 2.0.0** — Updated for Blender 5.1 + 5.2 LTS Beta compatibility

## What's New in v2.0.0

- **Blender 5.2 LTS Beta support** — 12 breaking changes documented with migration code
- **40+ new 5.2 APIs** — Geometry Nodes (XPBD Physics, Mesh Bevel, Lists, PCA, Geometry Bundles, Sample Sound), Cycles Texture Cache, Grease Pencil Delaunay Fill, VSE Compositor Effect Strip, and more
- **All 17 release note modules covered** — Python API, Geo Nodes, Cycles, EEVEE, GP, Sculpt, VSE, Animation, Assets, Compositor, UI, Modeling, Pipeline/I/O, Rendering, Physics, Motion Tracking, VR
- **Compatible code patterns** — Version-check templates for all breaking changes
- **Blender 5.1 breaking changes** — Brush stroke_method, VSE renames, Principled BSDF updates included

## Features

- **20 built-in tools** — scene analysis, screenshots, rendering, navigation, doc search
- **Arbitrary bpy code execution** — full Python API access through the MCP channel
- **3 connection modes** — mcporter (recommended), direct TCP socket, background/headless
- **Blender 5.1 + 5.2 LTS Beta compatible** — includes workarounds for all breaking API changes

## Quick Start

```bash
# 1. Install mcporter
npm install -g mcporter

# 2. Install the Blender MCP Addon
# Download from: https://projects.blender.org/lab/blender_mcp/releases
# Then: Edit → Preferences → Add-ons → Install from Disk

# 3. Start Blender, enable the addon, click "Start Server"

# 4. Configure mcporter
mcporter config add blender-mcp --transport stdio --command "python -m blmcp --transport stdio"

# 5. Call tools
mcporter call blender-mcp.get_objects_summary
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"count": len(bpy.data.objects)}'
```

## Repository Contents

| File | Description |
|------|-------------|
| `blender-mcp-SKILL.md` | Complete skill definition — architecture, installation, 20 tools, protocol, 5.1/5.2 compatibility notes, troubleshooting |
| `README.md` | Project overview and quick start guide |

## Requirements

- Blender 5.1+ (5.2 LTS Beta supported)
- Python 3.13+
- Node.js 18+

## Blender 5.2 LTS Timeline

| Stage | Date | Status |
|-------|------|--------|
| Alpha | 2026-02-04 | ✅ Done |
| Beta | 2026-06-03 | ✅ Current |
| RC | 2026-07-08 | ⏳ Expected |
| Release | 2026-07-14 | ⏳ Expected |
| Support | 2026-07 ~ 2028-07 | 2-year LTS |

## License

Apache-2.0
