---
name: camofox-browser-control
description: Control a standalone camofox-browser server over its REST API, especially when a local or remote service is already running on port 9377. Use for opening tabs, navigating, snapshotting pages, clicking refs, typing into forms, pressing keys, scrolling, exporting storage state, importing cookies, or debugging browser automation against camofox-browser/Camoufox behavior.
---

Use the standalone camofox-browser server directly over HTTP.

Default assumptions for this workspace:
- Base URL: `http://127.0.0.1:9377`
- The service is already running.
- `userId` is mandatory on nearly every useful request.
- `sessionKey` (or legacy `listItemId`) groups tabs; default to `default`.

## Golden workflow

1. Check `/health`.
2. Create a tab with `/tabs`.
3. Call `/tabs/:tabId/wait`.
4. Call `/tabs/:tabId/snapshot` and read refs.
5. Act with `/click`, `/type`, `/press`, `/scroll`, or `/navigate`.
6. Snapshot again after any state-changing action.

Prefer this loop over HTML scraping.

## Hard rules

- Always send `userId`.
- Prefer `POST /tabs` with `sessionKey` for raw server use.
- Re-snapshot after click, type, press, or navigation.
- If a field ignores `fill`, retry with `type` using `mode: "keyboard"`.
- If `/tabs` returns an empty list, check whether `userId` was omitted.
- Use direct navigation when the target URL is known; do not over-click through search results if a stable URL exists.
- Use VNC/manual login for MFA, CAPTCHAs, or brittle auth flows, then reuse storage state or persistence.

## Minimal endpoint map

Read `references/api-cheatsheet.md` when you need request/response shapes.

Most-used endpoints:
- `GET /health`
- `POST /tabs`
- `GET /tabs?userId=...`
- `POST /tabs/:tabId/wait`
- `GET /tabs/:tabId/snapshot?userId=...`
- `POST /tabs/:tabId/click`
- `POST /tabs/:tabId/type`
- `POST /tabs/:tabId/press`
- `POST /tabs/:tabId/scroll`
- `POST /tabs/:tabId/navigate`
- `POST /tabs/:tabId/evaluate`
- `POST /sessions/:userId/cookies`
- `GET /sessions/:userId/storage_state`

## Recommended helper script

Use `scripts/camofox.py` instead of rewriting raw HTTP every time.

Examples:

```bash
python3 skills/camofox-browser-control/scripts/camofox.py health
python3 skills/camofox-browser-control/scripts/camofox.py open --user lotfi --session default --url https://github.com
python3 skills/camofox-browser-control/scripts/camofox.py snapshot --user lotfi --tab <tabId>
python3 skills/camofox-browser-control/scripts/camofox.py click --user lotfi --tab <tabId> --ref e17
python3 skills/camofox-browser-control/scripts/camofox.py type --user lotfi --tab <tabId> --ref e2 --text 'hello' --mode fill
python3 skills/camofox-browser-control/scripts/camofox.py type --user lotfi --tab <tabId> --text '97304' --mode keyboard --submit
python3 skills/camofox-browser-control/scripts/camofox.py navigate --user lotfi --tab <tabId> --url https://example.com
```

## Known quirks

- `GET /tabs` without `userId` can misleadingly show no tabs even when tabs exist.
- Refs go stale after page changes. Snapshot again instead of reusing old refs blindly.
- `click` already retries normal click, force click, and mouse sequence; success does not guarantee the frontend changed the state you expect, so verify with a fresh snapshot.
- Some sites accept direct URL navigation more reliably than UI clicking.
- Some frontend inputs require true keyboard events. Use `mode: "keyboard"` plus `--submit` when `fill` does not trigger app logic.
- Large multi-step chained calls are more fragile than short calls with verification between them.

## Login strategy

For normal forms:
- open → wait → snapshot → type → click/submit → snapshot

For stubborn auth:
- use VNC/noVNC login
- export `storage_state`
- rely on persistence or restore state on later runs

For cookie bootstrap:
- import Netscape cookies through `/sessions/:userId/cookies`
- requires `CAMOFOX_API_KEY`

## Escape hatch

Use `/tabs/:tabId/evaluate` only when refs/typing/clicking are insufficient. Keep expressions small and targeted.

## Local note for this machine

The current host already has a live server on `127.0.0.1:9377`, with VNC/noVNC exposed by the container. Treat that as the default target unless the task says otherwise.
