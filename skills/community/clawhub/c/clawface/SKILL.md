---
name: clawface
version: 0.0.3
description: Start the Clawface 3D avatar web UI — serves a local web page the user opens in their browser
metadata:
  {
    "openclaw":
      {
        "emoji": "🐾",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "download-runtime-macos",
              "kind": "download",
              "os": ["darwin"],
              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2",
              "archive": "tar.bz2",
              "extract": true,
              "stripComponents": 1,
              "targetDir": "runtime",
              "label": "Download sherpa-onnx runtime (macOS)",
            },
            {
              "id": "download-runtime-linux-x64",
              "kind": "download",
              "os": ["linux"],
              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2",
              "archive": "tar.bz2",
              "extract": true,
              "stripComponents": 1,
              "targetDir": "runtime",
              "label": "Download sherpa-onnx runtime (Linux x64)",
            },
            {
              "id": "download-model-lessac",
              "kind": "download",
              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2",
              "archive": "tar.bz2",
              "extract": true,
              "targetDir": "models",
              "label": "Download Piper en_US lessac (high) voice model",
            },
          ],
      },
  }
---

# Clawface — 3D Avatar Chat

A self-contained web UI with a 3D avatar, chat, and TTS voice. You do NOT need a browser — you start an HTTP server and give the user a URL to open in their own browser.

## Install

After the downloads above complete, the tools directory at `~/.openclaw/tools/clawface/` will contain:

- `runtime/` — sherpa-onnx TTS runtime (platform-specific binary + libs)
- `models/` — TTS voice model

The web assets are bundled in `{baseDir}/dist/`.

No further configuration is needed — serve.js finds the TTS runtime and models automatically.

## How to start

Run this command:

```bash
node {baseDir}/bin/serve.js \
  --dist {baseDir}/dist \
  --tools-dir ~/.openclaw/tools/clawface \
  --port 18794 \
  --gateway-url "ws://127.0.0.1:${OPENCLAW_GATEWAY_PORT:-18789}" \
  --gateway-token "$OPENCLAW_GATEWAY_TOKEN" \
  --identity-file ~/.openclaw/identity/device.json
```

The server prints a URL like `http://localhost:18794` to stdout.

Tell the user: **"Avatar ready at http://localhost:18794"** — they open it in their browser.

## Security

- **Credentials never reach the browser.** The server authenticates to the gateway via a WebSocket proxy (`/ws`). The gateway token and device private key stay server-side — the browser only receives a proxy URL.
- The `--gateway-token` and `--identity-file` arguments are used exclusively by serve.js to authenticate the upstream gateway connection.

## Important

- Do NOT try to open a browser yourself. Just start the server and return the URL.
- The server is zero-dependency Node.js — no `npm install` required.
- TTS is built in — the server calls sherpa-onnx directly, no separate TTS skill needed.

## Stopping

Kill the `node` process to stop the server.
