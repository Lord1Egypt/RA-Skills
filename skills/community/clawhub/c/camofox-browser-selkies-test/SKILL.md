---
name: camofox-browser-selkies-test
description: Use the Selkies test browser stack for desktop-stream/browser-in-desktop checks, Selkies-specific debugging, and viewport/mobile-context experiments. Trigger this when Lotfi mentions Selkies, the test browser, the test image, browser-in-desktop behavior, or the services on `http://127.0.0.1:9378` / `http://127.0.0.1:3003`.
---

Use the Selkies test browser stack.

Default targets:
- camofox-browser API: `http://127.0.0.1:9378`
- Selkies UI: `http://127.0.0.1:3003`
- Docker container: `camofox-selkies-test`
- Current pushed image reference: `medtouadmin/camofox-browser:selkies-beta`

Use this skill for:
- Selkies stream/websocket debugging
- browser-in-desktop validation
- viewport/mobile-context experiments tied to the Selkies test stack
- reproducing issues specific to the test image/container

Hard rules:
- Treat this as separate from the main camofox-browser service.
- If the task is about the shared remote browser over tailnet CDP, use `browser-cdp-tailnet` instead.
- If the task is about the default local service on `127.0.0.1:9377`, use `camofox-browser-main` instead.
