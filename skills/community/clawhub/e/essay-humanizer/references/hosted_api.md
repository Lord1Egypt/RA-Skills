# Hosted API — linking as an MCP / orchestrator tool

The **skill** (`SKILL.md`) is documentation and local scripts. A **separate** process can run [api/main.py](../../api/main.py) to expose humanization over HTTP.

## Why split?

- **Clawhub / bundles** may ship docs-only assets; MLX + weights stay on a machine you control.
- **MCP and other agents** often ingest an **OpenAPI** document — this server serves **`/openapi.json`** automatically (FastAPI).

## Minimal linking checklist

1. Start the server per [api/README.md](../../api/README.md).
2. In your tool / MCP provider, register an HTTP or OpenAPI integration with spec URL:
   - `https://<your-host>/openapi.json`
3. Prefer **HTTPS** and **`HUMANIZE_API_KEY`** on the server for any non-local use.

## Contract

- **POST** `/v1/humanize` with JSON `{ "text": "..." }`.
- Response `{ "output": "..." }` — plain essay body (no LaTeX dollars unless the model emitted them; consider stripping server-side if your policy requires it).

No essay content is stored by default; add logging only under your privacy policy.
