---
name: daeva
description: Use this skill whenever the user wants to interact with local or remote GPU pods for AI inference tasks. This includes transcribing audio (Whisper/speech-to-text), generating images (ComfyUI/Stable Diffusion), running OCR or vision/image analysis, managing pod lifecycle (start, stop, swap, register, install), checking pod or job status, or debugging GPU pod issues. Trigger this skill when the user mentions Daeva, local inference, GPU pods, pod orchestration, or any task involving routing AI jobs to local or remote hardware. Also trigger when the user asks to transcribe a recording, generate an image locally, extract text from an image via OCR, or describe an image using vision — even if they don't mention "Daeva" by name. If the user references DAEVA_URL, DAEVA_PORT, localhost:8787, pod aliases, job queuing, exclusivity groups, pod swapping, the Daeva MCP server, or pod packages, use this skill.
compatibility: Requires the daeva service running locally or on a remote host. Set DAEVA_URL and/or DAEVA_PORT env vars to override the default localhost:8787. Requires curl or HTTP access. Optionally Node.js for the MCP server.
license: MIT
metadata:
  author: asmolebot
  version: "0.2.4"
  repository: https://github.com/asmolebot/daeva
---

# Daeva — GPU Pod Orchestrator

Daeva routes AI inference jobs (transcription, image generation, OCR, vision) to GPU-backed pods via a REST API and optional MCP server. It handles pod lifecycle, exclusivity groups (automatic GPU contention resolution), and portable pod packages. Daeva can run on the same machine as the agent or on a remote host — the default is localhost, but this is just a fallback.

## Resolving the Daeva Base URL

Daeva can run locally or on a remote host. Resolve the base URL using these steps in order:

1. **Check environment variables.** If `DAEVA_URL` is set, use it as the full base URL (e.g. `http://server.local:8787`). If only `DAEVA_PORT` is set, use `http://127.0.0.1:$DAEVA_PORT`.
2. **Try the default.** If neither variable is set, use `http://127.0.0.1:8787`.
3. **Verify with a health check.** Hit `/health` on the resolved URL. If it returns `{"ok":true}`, proceed.
4. **If the health check fails and no env vars were set**, ask the user where Daeva is hosted before continuing. Do not guess or retry blindly.

```bash
# Resolve base URL from environment, falling back to localhost default
DAEVA_BASE="${DAEVA_URL:-http://127.0.0.1:${DAEVA_PORT:-8787}}"

# Verify the service is reachable
curl -sf "$DAEVA_BASE/health"
# Expected: {"ok":true}
```

If the service is local and not running, start it:

```bash
# Foreground
daeva
# Or: PORT=8787 node dist/src/cli.js

# systemd
systemctl --user start daeva
```

All endpoints below use `$DAEVA_BASE` as the base URL. When constructing curl commands, MCP config, or downstream skill URLs, always substitute the resolved value — never hardcode `127.0.0.1` unless the agent is running on the same host as Daeva.

## Important: Behavioral Rules

**Daeva is a shared service.** It is not per-user or per-session. Multiple agents and users may share the same Daeva instance. Treat it like shared infrastructure — don't make assumptions about what's running or why.

**Use lifecycle endpoints for pod management.** To wake, switch, or stop pods, use the dedicated lifecycle endpoints (`/pods/:podId/activate`, `/pods/:podId/stop`, `/pods/swap`). Never enqueue a dummy or throwaway job just to force a pod swap — that pollutes the job queue and may produce unwanted side effects on a shared service.

**Route workload traffic through Daeva's proxy, not raw container ports.** When Daeva is installed, downstream skills and clients (e.g. a ComfyUI skill, a Whisper client) should send requests through Daeva's proxy at `$DAEVA_BASE/proxy/<podId>` — not directly to the pod's container port. For example, if ComfyUI is managed by Daeva, the ComfyUI skill should hit `$DAEVA_BASE/proxy/comfyapi` instead of `http://localhost:8188`. This ensures Daeva can handle pod activation, exclusivity switching, and routing transparently. Only bypass the proxy if Daeva is confirmed to not be managing that pod.

## Capabilities and Job Types

| Capability         | Job Type           | Required Input                          |
|--------------------|--------------------|-----------------------------------------|
| `speech-to-text`   | `transcribe-audio` | `filePath` or `url` + `contentType`     |
| `image-generation` | `generate-image`   | `prompt`                                |
| `ocr`              | `extract-text`     | `filePath` or `url`                     |
| `vision`           | `describe-image`   | `filePath` or `url`                     |

### Built-in Pods

| Pod ID      | Capabilities              | Description                |
|-------------|---------------------------|----------------------------|
| `comfyapi`  | image-generation, vision  | ComfyUI/comfyapi backend  |
| `whisper`   | speech-to-text            | Whisper transcription      |
| `ocr-vision`| ocr, vision               | OCR and visual analysis    |

## Submitting Jobs

Post JSON to `/jobs` with `type` and `files` (or legacy `input` field):

```bash
# Transcribe audio
curl -s -X POST $DAEVA_BASE/jobs \
  -H 'Content-Type: application/json' \
  -d '{"type":"transcribe-audio","files":[{"source":"path","path":"/tmp/audio.wav"}]}'

# Generate an image
curl -s -X POST $DAEVA_BASE/jobs \
  -H 'Content-Type: application/json' \
  -d '{"type":"generate-image","capability":"image-generation","input":{"prompt":"a red fox on a snowy mountain"}}'

# OCR
curl -s -X POST $DAEVA_BASE/jobs \
  -H 'Content-Type: application/json' \
  -d '{"type":"extract-text","capability":"ocr","input":{"filePath":"/tmp/document.png"}}'
```

After submitting, poll for completion and retrieve the result:

```bash
curl -s $DAEVA_BASE/jobs/<job-id>          # Job state
curl -s $DAEVA_BASE/jobs/<job-id>/result    # Job result when complete
curl -s $DAEVA_BASE/jobs                     # List all jobs
```

## Pod Management

These endpoints control the full pod lifecycle — registering new pods, installing packages, and managing runtime state.

```bash
# List all registered pods and their runtime state
curl -s $DAEVA_BASE/pods

# Register a new pod from a manifest
curl -s -X POST $DAEVA_BASE/pods/register \
  -H 'Content-Type: application/json' \
  -d '{ ... pod manifest JSON ... }'

# Install a pod package by alias (e.g. "whisper")
curl -s -X POST $DAEVA_BASE/pods/create \
  -H 'Content-Type: application/json' \
  -d '{"alias":"whisper"}'

# List available aliases from the registry
curl -s $DAEVA_BASE/pods/aliases

# List already-installed packages
curl -s $DAEVA_BASE/pods/installed

# Activate (start) a specific pod
curl -s -X POST $DAEVA_BASE/pods/<podId>/activate

# Stop a specific pod
curl -s -X POST $DAEVA_BASE/pods/<podId>/stop

# Swap to a different pod (handles exclusivity group conflicts automatically)
curl -s -X POST $DAEVA_BASE/pods/swap \
  -H 'Content-Type: application/json' \
  -d '{"podId":"comfyapi"}'
```

**Exclusivity groups:** When two pods share the same GPU and can't run simultaneously, Daeva automatically stops the current pod and starts the target when you swap or submit a job that requires a different pod.

### Pod Package Sources

Packages can be installed from multiple sources:
- **local-file** — local directory containing a `pod-package.json`
- **github-repo** — `owner/repo` with optional ref and subpath
- **git-repo** — arbitrary Git URL
- **uploaded-archive** — `.tar.gz` or `.zip` uploaded directly
- **registry-index** — delegated lookup from a registry catalog

During install, Daeva runs package install hooks, creates declared host directories, and persists resolved host-path template variables (e.g. `MODELS_DIR`, `INPUT_DIR`).

## Observability

Granular status endpoints for debugging and monitoring:

```bash
# Full combined status snapshot
curl -s $DAEVA_BASE/status

# Pod runtime state + container inspection
curl -s $DAEVA_BASE/status/runtime

# Installed packages + registry state
curl -s $DAEVA_BASE/status/packages

# Queue depth + exclusivity groups
curl -s $DAEVA_BASE/status/scheduler

# Recent job history
curl -s $DAEVA_BASE/status/jobs/recent
```

Use `/status/runtime` when a pod seems stuck — it includes container-level inspection. Use `/status/scheduler` to understand why a job is queued (often an exclusivity group conflict).

## Complete API Reference

### Core Endpoints

| Method | Path                    | Purpose                              |
|--------|-------------------------|--------------------------------------|
| GET    | `/health`               | Liveness check                       |
| GET    | `/pods`                 | List pods and runtime state          |
| POST   | `/pods/register`        | Register a new pod manifest          |
| POST   | `/pods/create`          | Install a pod package by alias       |
| GET    | `/pods/aliases`         | List registry aliases                |
| GET    | `/pods/installed`       | List installed packages              |
| POST   | `/pods/:podId/activate` | Start or activate a pod              |
| POST   | `/pods/:podId/stop`     | Stop a pod                           |
| POST   | `/pods/swap`            | Swap to a target pod (server-side)   |
| ALL    | `/proxy/:podId/*`       | Proxy requests to a pod's backend    |
| POST   | `/jobs`                 | Submit an async job                  |
| GET    | `/jobs`                 | List jobs                            |
| GET    | `/jobs/:id`             | Get job state                        |
| GET    | `/jobs/:id/result`      | Get job result                       |

### Observability Endpoints

| Method | Path                    | Purpose                              |
|--------|-------------------------|--------------------------------------|
| GET    | `/status`               | Combined status snapshot             |
| GET    | `/status/runtime`       | Pod runtime + container inspection   |
| GET    | `/status/packages`      | Installed packages + registry state  |
| GET    | `/status/scheduler`     | Queue depth + exclusivity groups     |
| GET    | `/status/jobs/recent`   | Recent job history                   |

## MCP Server Configuration

Daeva ships an MCP stdio server. The `--base-url` must point to the actual resolved Daeva URL — use `$DAEVA_BASE`, not a hardcoded localhost address (unless Daeva is genuinely local to the host running the MCP client).

```json
{
  "mcpServers": {
    "daeva": {
      "command": "daeva-mcp",
      "args": ["--base-url", "http://server.local:8787"]
    }
  }
}
```

Replace `http://server.local:8787` with the actual `$DAEVA_BASE` value for your environment. When the MCP server is configured, prefer using MCP tools over raw curl commands.

## Troubleshooting

- **Connection refused on `/health`** — Service not running. Start with `daeva` or `systemctl --user start daeva`.
- **Job stays `queued`** — No pod registered for that capability, or an exclusivity conflict is blocking it. Check `/pods` and `/status/scheduler`.
- **Pod won't start** — Check `/status/runtime` for container-level errors.
- **`404 alias not found`** — The alias doesn't exist in the registry. Check `/pods/aliases` for valid options.
- **Package install fails** — Verify the source (local path, git URL, archive) is accessible. Check `/status/packages` for install state.
