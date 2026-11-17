# ArcGIS Agent

An agent skill that gives AI assistants (WorkBuddy / OpenClaw / Claude Code / etc.) the ability to drive **2500+ ArcGIS Pro geoprocessing tools across 47 toolboxes (arcpy)** through a local HTTP API — including core analysis, Spatial/Image Analyst, GeoAI deep learning, multidimensional rasters, utility networks, geostatistics and more.

Published skill registry page: https://clawhub.ai/zhaojj662/skills/arcgis-agent
Upstream project / source: https://github.com/zhaojj662/arcpy-mcp-server

## What it does

- `scripts/server.py` — an HTTP server (Flask-free, stdlib only) running inside **ArcGIS Pro's Python** (`arcgispro-py3`), exposing every arcpy tool from **47 toolboxes** via `GET /modules`, `GET /module/{name}`, `POST /call`
- `scripts/mcp_bridge.py` — MCP stdio → HTTP bridge for MCP-compatible clients
- `SKILL.md` — the agent-facing playbook: startup, health check, curl examples, module cheat-sheet, composite analysis call chains, error handling, security config
- `references/examples.md` — worked examples
- `scripts/start_server.bat` — one-click launcher

## Install (as an agent skill)

```bash
# via ClawHub
clawhub install arcgis-agent

# or from this repo
git clone https://github.com/zhaojj662/arcgis-agent.git
cp -r arcgis-agent ~/.workbuddy/skills/   # WorkBuddy user skills dir
```

## Requirements

- Windows 10/11 with a valid **ArcGIS Pro 3.x** license (arcpy only runs inside ArcGIS Pro's bundled Python)
- Port 8765 free (localhost only)

## Quick start

```bat
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\server.py 8765
curl http://127.0.0.1:8765/health   # {"status":"ok","tools":2500,"modules":47}
```

## Security

The server binds to `127.0.0.1` only and enforces a path whitelist. Allowed paths default to `C:/GIS-AI-Course/` and can be extended via the `ARCPY_ALLOWED_PATHS` environment variable (semicolon-separated).

## License

MIT (see `license`). Based on [arcpy-mcp-server](https://github.com/zhaojj662/arcpy-mcp-server) by the same author.
