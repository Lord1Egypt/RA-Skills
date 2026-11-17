---
name: freecad-cadpilot
description: "FreeCAD, CADPilot, or CAD modeling. Connect local FreeCAD through the cadpilot stdio MCP server and call only tools the probe advertises."
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - openclaw
        - uvx
      anyBins:
        - python
        - python3
---

# FreeCAD CADPilot

Use the installed CADPilot translator. Do not write an MCP server, reimplement CAD tools, or edit the FreeCAD addon.

## Connect

1. Prove FreeCAD is listening before changing OpenClaw. Run Python `xmlrpc.client.ServerProxy("http://127.0.0.1:9875", allow_none=True).ping()`. Done when the printed result is `True`. If it is not, stop and report that the RPC server is not running. Do not restart FreeCAD unless the user asks.

2. Resolve `uvx` on PATH. Done when the printed result is an executable path. If it is missing, stop and report that `uv` must be installed. Do not hardcode another machine's path.

3. Confirm the saved server is local stdio. Run `openclaw mcp show cadpilot --json`. Done when `command` is the resolved `uvx` path, `args` is `["cadpilot"]`, and there is no `url`. If the server is missing, register it with `openclaw mcp add cadpilot --command "<resolved-uvx>" --arg cadpilot --connect-timeout 90 --timeout 60`. A 5-second initialize timeout is an OpenClaw registration failure, not a FreeCAD failure.

4. Prove the MCP handshake. Run `openclaw mcp probe cadpilot --json`. Done when `diagnostics` is empty and the tool list is non-empty. Call only names from that list. OpenClaw exposes them as `cadpilot__<name>`.

## Use

5. Keep both hops local. MCP stays stdio. The XML-RPC hop stays `127.0.0.1:9875`. Do not point MCP at that URL, bind `0.0.0.0`, enable remote FreeCAD access, or put an API key in any file.

6. For a connectivity check, stop after the probe. No advertised tool is named `ping`. Do not call `diagnose`, `execute_code`, `execute_code_async`, `cad`, `create_document`, or any other mutating tool to invent a health check. Report the read-only names returned by that probe.

7. For a modeling request, call `operation_help` for the operation, then the matching advertised tool. Prefer `cad` over `execute_code`. Done when the result names the requested document or object, or returns a FreeCAD error. If a call hangs after the probe succeeded, report a possible modal dialog blocking the FreeCAD GUI thread and stop. Do not restart FreeCAD unless the user asks.
