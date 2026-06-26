---
name: camofox-browser-main
description: Use the main local camofox-browser service for standard browser automation in this workspace. Trigger this when Lotfi asks for the main/local camofox browser, the default camofox browser, or work against the service on `http://127.0.0.1:9377`.
---

Use the main local camofox-browser service.

Default target:
- API base URL: `http://127.0.0.1:9377`
- Docker container: `peaceful_kare`

Workflow:
1. Check `/health`.
2. Open or reuse a tab.
3. Wait/snapshot.
4. Act.
5. Snapshot again after state-changing actions.

Hard rules:
- Always send `userId`.
- Prefer `sessionKey` when creating or reusing tabs.
- Re-snapshot after click, type, press, or navigation.
- If the user names another browser target explicitly, stop and use that specific skill instead.

Use this as the default local camofox-browser target unless Lotfi explicitly asks for Selkies/test or the detached tailnet browser.
