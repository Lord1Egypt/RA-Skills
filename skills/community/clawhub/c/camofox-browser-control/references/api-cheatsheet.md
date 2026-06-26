# camofox-browser API cheatsheet

Base URL defaults to `http://127.0.0.1:9377`.

## Health

`GET /health`

Returns service/browser status.

## Open tab

`POST /tabs`

```json
{
  "userId": "lotfi",
  "sessionKey": "default",
  "url": "https://example.com"
}
```

Returns:

```json
{
  "tabId": "uuid",
  "url": "https://example.com"
}
```

Notes:
- `userId` and `sessionKey` are required here.
- `POST /tabs/open` exists too, but uses `listItemId`; reserve that for compatibility cases.

## List tabs

`GET /tabs?userId=lotfi`

Returns:

```json
{
  "running": true,
  "tabs": [
    {
      "targetId": "uuid",
      "tabId": "uuid",
      "url": "https://example.com",
      "title": "Example",
      "listItemId": "default"
    }
  ]
}
```

Important: without `userId`, this may look empty.

## Wait

`POST /tabs/:tabId/wait`

```json
{
  "userId": "lotfi",
  "timeout": 10000,
  "waitForNetwork": false
}
```

Returns `{ "ok": true, "ready": true }`.

## Snapshot

`GET /tabs/:tabId/snapshot?userId=lotfi&format=text`

Returns:

```json
{
  "url": "https://example.com",
  "snapshot": "- button \"Search\" [e1] ...",
  "refsCount": 12,
  "truncated": false,
  "totalChars": 1234,
  "hasMore": false,
  "nextOffset": null
}
```

Notes:
- Refs like `e1`, `e2` come from the snapshot.
- Snapshot again after page changes.

## Click

`POST /tabs/:tabId/click`

By ref:

```json
{ "userId": "lotfi", "ref": "e17" }
```

By selector:

```json
{ "userId": "lotfi", "selector": "button.submit" }
```

Returns:

```json
{
  "ok": true,
  "url": "https://example.com/next",
  "refsAvailable": true
}
```

## Type

`POST /tabs/:tabId/type`

Fill mode:

```json
{
  "userId": "lotfi",
  "ref": "e2",
  "text": "hello",
  "mode": "fill"
}
```

Keyboard mode:

```json
{
  "userId": "lotfi",
  "text": "97304",
  "mode": "keyboard",
  "delay": 120,
  "submit": true
}
```

Notes:
- `fill` requires `ref` or `selector`.
- `keyboard` can type into the current focus.
- Use keyboard mode for reactive or stubborn inputs.

## Press

`POST /tabs/:tabId/press`

```json
{ "userId": "lotfi", "key": "Enter" }
```

## Scroll

`POST /tabs/:tabId/scroll`

```json
{ "userId": "lotfi", "direction": "down", "amount": 500 }
```

## Navigate existing tab

`POST /tabs/:tabId/navigate`

```json
{ "userId": "lotfi", "url": "https://chatgpt.com" }
```

Returns:

```json
{
  "ok": true,
  "tabId": "uuid",
  "url": "https://chatgpt.com/",
  "refsAvailable": true
}
```

## Evaluate

`POST /tabs/:tabId/evaluate`

```json
{
  "userId": "lotfi",
  "expression": "(() => document.title)()"
}
```

Returns:

```json
{ "ok": true, "result": "Telegram" }
```

Use sparingly.

## Cookie import

`POST /sessions/:userId/cookies`

Requires `Authorization: Bearer <CAMOFOX_API_KEY>`.

Body contains Playwright-style cookies.

## Storage state export

`GET /sessions/:userId/storage_state`

Requires `Authorization: Bearer <CAMOFOX_API_KEY>` unless loopback/non-production allowances apply.

Useful after VNC/manual login.

## VNC notes

Common ports from the VNC plugin:
- `5900` VNC
- `6080` noVNC web UI

Typical flow:
1. open login page
2. complete login visually in noVNC
3. export storage state
4. reuse state later
