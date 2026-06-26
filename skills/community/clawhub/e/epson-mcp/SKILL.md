---
name: epson-mcp
description: Print, scan, copy, and job control for the Epson WF-2250 (and other network-attached Epson inkjets) via MCP. Exposes tools for text/raster/PDF printing, printer diagnostics, and spooler job management over a Tailnet-authenticated HTTP endpoint.
metadata: {"clawdbot":{"emoji":"🖨️","requires":{"urls":["https://cyber.talpa-stargazer.ts.net/epson/mcp"]},"install":[{"id":"docker","kind":"docker-compose","label":"Deploy Epson MCP server (Docker)"}]}}
---

# Epson MCP

MCP server for the Epson WF-2250 inkjet printer. Connects to the printer over
TCP/9100 (ESC/P-R) or LPD, with an optional Windows PowerShell spooler backend.

## Tools

- `epson_diag` — Diagnose connectivity and capabilities
- `epson_print_text` — Print plain text via ESC/P-R
- `epson_print_file` — Print a file from the shared volume (PDF auto-converted)
- `epson_print_raw` — Send a base64-encoded ESC/P or PostScript payload
- `epson_status` — Re-probe the printer and return a status summary
- `epson_ink` — Ink level info (stub — WF-2250 doesn't expose ink over network)
- `epson_list_jobs` — List Windows spooler jobs (requires PowerShell)
- `epson_cancel_job` — Cancel a Windows spooler job (requires PowerShell)
- `epson_scan` — Network scan (stub — WF-2250 doesn't support network scanning)
- `epson_copy` — Network copy (stub)

## Setup

1. Deploy the Docker container (see repo README).
2. Expose over Tailnet: `tailscale serve --bg --set-path=/epson http://localhost:18790`
3. Wire into Codex/OpenClaw:
   ```bash
   codex mcp add epson --url https://cyber.talpa-stargazer.ts.net/epson/mcp \
       --bearer-token-env-var EPSON_MCP_AUTH_TOKEN
   ```

## Backends

| Backend   | Protocol       | Notes                              |
|-----------|----------------|------------------------------------|
| `raw9100` | TCP/9100 ESC/P | Default; works with WF-2250       |
| `lpd`     | TCP/515 LPR    | Fallback; most low-end Epsons ignore |
| `windows` | PowerShell     | Only when PowerShell is available  |

When `backend=auto` (default), tries lpd → raw9100 → windows in order.
On Linux containers, the Windows backend is automatically skipped if
`powershell.exe` / `pwsh` is not found.

## License

MIT-0
