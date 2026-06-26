---
name: browser-cdp-tailnet
description: Use the detached shared Chromium browser exposed over the tailnet CDP endpoint. Trigger this when Lotfi asks for the detached browser, shared browser, remote CDP browser, tailnet browser, or a browser reachable at `http://100.101.184.33:9223` / `ws://100.101.184.33:9223/...`.
---

Use the shared remote Chromium/CDP browser over the tailnet.

Default target:
- CDP base URL: `http://100.101.184.33:9223`
- Browser WS endpoint: `ws://100.101.184.33:9223/devtools/browser/3fbb2459-85c5-40b5-8d50-6f3c596cf8d5`

Preferred connection method:
- `chromium.connectOverCDP("http://100.101.184.33:9223")`

Hard rules:
- Prefer the HTTP CDP base URL over hardcoding the raw WS endpoint when your client supports it.
- If `/json/version` reports `ws://localhost/...`, replace `localhost` with `100.101.184.33:9223`.
- Verify with a small probe before claiming it works.

Known-good checks already observed on this machine:
- `/json/version` responded on `http://100.101.184.33:9223`
- CDP WebSocket handshake succeeded
- `Browser.getVersion` succeeded
- live navigation to YouTube succeeded

Use this skill instead of local browser skills when the browser should be shared across agents or reached remotely over the tailnet.
