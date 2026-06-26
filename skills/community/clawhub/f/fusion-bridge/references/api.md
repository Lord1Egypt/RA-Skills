# Fusion Bridge API Reference

## Base URLs

Try these depending on where the request originates:

- local: `http://<bridge-host>:8765`
- LAN: `http://<fusion-host-ip>:8765`

## Endpoints

### `GET /ping`

Health check.

Example response:

```json
{
  "ok": true,
  "service": "fusion-bridge",
  "version": "0.3.0"
}
```

### `GET /state`

Returns runtime state from inside Fusion.

Observed fields:

```json
{
  "ok": true,
  "fusionRunning": true,
  "documentName": "Unbenannt",
  "hasActiveDesign": true,
  "rootComponentName": "(Nicht gespeichert)",
  "queueSize": 0,
  "busy": false,
  "currentJobId": null,
  "pumpMode": "custom-event"
}
```

### `GET /logs`

Returns recent JSONL log lines.

### `POST /exec`

Runs Python in the Fusion context.

Request body:

```json
{
  "code": "print('ok')",
  "timeoutSeconds": 300
}
```

Rules:
- `code` must be a non-empty string
- `timeoutSeconds` defaults to `300`
- values above `300` are clamped to `300`
- code length is intentionally not capped by API policy

Success example:

```json
{
  "ok": true,
  "stdout": "ok\n",
  "result": null,
  "error": null,
  "durationMs": 69,
  "jobId": "..."
}
```

Timeout example:

```json
{
  "ok": false,
  "error": "execution timeout",
  "jobId": "..."
}
```

## Fusion execution context

Observed context objects available to raw Python include at least:

- `adsk`
- `app`
- `ui`
- `product`
- `design`
- `rootComp`
- `document`
- `result`

Use `print(...)` for stdout output and `result = ...` for structured return data when useful.
