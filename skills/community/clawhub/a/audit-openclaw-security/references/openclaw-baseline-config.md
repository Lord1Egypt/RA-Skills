# OpenClaw secure baseline config (starting point)

This file contains conservative baseline snippets for current OpenClaw builds.

> OpenClaw config is usually `~/.openclaw/openclaw.json`. Depending on install/profile it may be JSON or JSON5-like. Back it up before editing.

## Baseline goals

- keep the Gateway private
- require strong Gateway auth
- isolate DMs
- require explicit mentions in groups
- default tools to least privilege
- avoid accidental remote browser / node / automation exposure

## 1) Minimal local baseline

Good for a single-user local install that still wants sensible defaults.

```js
{
  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789,
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## 2) Hardened inbox-facing baseline

This is the conservative starting point for support-style or user-facing agents.

```js
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  tools: {
    profile: "messaging",
    deny: [
      "group:automation", // gateway + cron
      "group:runtime",    // exec/bash/process
      "group:fs",         // read/write/edit/apply_patch
      "sessions_spawn",
      "sessions_send",
    ],
    fs: { workspaceOnly: true },
    exec: {
      security: "deny",
      ask: "always",
      applyPatch: { workspaceOnly: true },
    },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

## 3) Shared inbox / multi-account note

If more than one real person can DM the bot:

- use `session.dmScope: "per-channel-peer"`
- if the same provider has multiple bot accounts, prefer `per-account-channel-peer`
- keep `dmPolicy: "pairing"` or explicit allowlists
- do not combine broad runtime/fs/elevated tools with open DMs or open groups

## 4) Reverse proxy / non-loopback Control UI

If a reverse proxy fronts the Gateway, set trusted proxy IPs and explicit browser origins.

```js
{
  gateway: {
    bind: "loopback",
    trustedProxies: ["127.0.0.1"],
    allowRealIpFallback: false,
    auth: { mode: "token", token: "replace-with-long-random-token" },
    controlUi: {
      allowedOrigins: ["https://ui.example.com"],
    },
  },
}
```

Notes:

- keep `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` off
- keep `gateway.controlUi.dangerouslyDisableDeviceAuth` off
- if the proxy is not on localhost, replace the trusted proxy IPs accordingly

## 5) Tailscale Serve note

`tailscale.mode: "serve"` can be a good remote-access pattern, but remember:

- `tailscale.mode: "funnel"` is public and should be treated as a red flag
- `gateway.auth.allowTailscale` can enable tokenless Control UI / WebSocket auth via Tailscale identity headers
- that tokenless flow assumes the Gateway host itself is trusted
- if untrusted code may run on the host, or if any reverse proxy sits in front, disable `gateway.auth.allowTailscale` and require normal auth

## 6) Discovery and logging

Reduce ambient exposure:

```js
{
  discovery: {
    mdns: { mode: "minimal" }, // or "off" if unused
  },
  logging: {
    redactSensitive: true,
  },
}
```

## 7) Tool profile reminders

Current high-level profiles:

- `minimal` -> `session_status` only
- `messaging` -> message + session reply/history/status
- `coding` -> filesystem + runtime + sessions + memory + image
- `full` -> unrestricted

For user-facing inbox bots, `messaging` is usually the right starting point, then narrow further with `tools.deny`.

## Verification

After changes, re-run:

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
openclaw channels status --probe
```
