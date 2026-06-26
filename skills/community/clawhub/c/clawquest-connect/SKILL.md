---
name: clawquest-connect
description: Use when the user wants to connect Claw Quest Android to this OpenClaw gateway with the manual URL+token flow, send those details over WhatsApp, and optionally auto-approve the next matching Android pairing request once.
user-invocable: true
metadata: {"openclaw":{"os":["win32","linux","darwin"],"requires":{"bins":["openclaw"]}}}
---

# ClawQuest Connect

Use this skill when the user asks to:

- connect Claw Quest
- send Claw Quest mobile connection details
- pair Claw Quest Android with this gateway
- approve the next Claw Quest Android pairing request

This skill is intentionally based on the manual setup flow.

Do not default to QR codes or setup codes.
Do not invent a Claw Quest-specific token format.

## Connection policy

The preferred Claw Quest flow is:

1. Resolve the current public Gateway WebSocket URL.
2. Resolve the current shared gateway auth token or password.
3. Send those details to the user in a single copy/paste-friendly WhatsApp message when WhatsApp is configured.
4. Tell the user you are doing that.
5. Watch for the next matching Claw Quest Android pairing request and approve it once.

If WhatsApp is not configured, say so plainly and provide the same details in chat.

## What to inspect first

Run these read-only checks first:

```powershell
openclaw config get gateway.auth.mode
openclaw config get gateway.remote.url
openclaw plugins inspect device-pair
```

Also inspect whichever auth secret matches the configured auth mode:

Token mode:

```powershell
openclaw config get gateway.auth.token
```

Password mode:

```powershell
openclaw config get gateway.auth.password
```

Interpretation:

- Prefer `gateway.remote.url` as the public `wss://...` address for Claw Quest.
- If `gateway.remote.url` is missing, explain that the public URL must be supplied or configured before Claw Quest manual setup will be smooth.
- If `gateway.auth.mode` is `token`, send the gateway token.
- If `gateway.auth.mode` is `password`, send the gateway password instead and label it clearly.
- If the `device-pair` plugin is disabled, say so clearly because pairing help may be unavailable or limited until it is enabled.

## WhatsApp handoff

If outbound WhatsApp messaging is configured on this host, always send the connection details there after resolving them.

Tell the user explicitly:

- that you are sending the connection details over WhatsApp
- that this is to make mobile copy/paste easier
- that they should use `Manual Setup` inside Claw Quest Android

Send a single compact message containing only:

- `Gateway URL: <wss://...>`
- `Gateway token: <token>` or `Gateway password: <password>`
- `Use Claw Quest Android -> Manual Setup`

Do not add extra formatting that makes mobile copy/paste harder.

If WhatsApp sending fails or is unavailable:

- say so plainly
- provide the same three lines in chat instead

## Pairing watch-and-approve

When the user asks to connect Claw Quest, you may automatically approve the next matching Android pairing request one time.

Start a short watch loop:

```powershell
openclaw devices list --json
```

Poll every 3 seconds for up to 2 minutes.

Approve only the first pending request that matches Claw Quest Android as closely as possible:

- `displayName`: `Claw Quest Android`
- `platform`: `android`
- `clientId`: `gateway-client`
- `clientMode`: `backend`
- requested role `operator`
- requested scopes include `operator.read` and `operator.write`

Approve it with:

```powershell
openclaw devices approve <requestId>
```

Then immediately confirm with:

```powershell
openclaw devices list --json
```

Tell the user whether approval succeeded and whether the paired device now shows:

- role `operator`
- scopes `operator.read` and `operator.write`

Stop after one approval.
Do not auto-approve unrelated requests.

## What to tell the user

When helping the user connect, be direct:

- say which public Gateway URL you are using
- say whether you are sending the token or password
- say that Claw Quest should use `Manual Setup`
- say that you are watching for and approving the next Android pairing request once

If connection still fails even with the correct manual token:

- inspect `openclaw devices list --json`
- explain whether the phone ever reached the pending-pairing stage
- distinguish `auth failed before pairing` from `pairing pending approval`

## Safety rules

- Never claim this skill can bypass gateway auth policy.
- Never approve a non-matching device as Claw Quest Android.
- Never rotate or remove device credentials unless the user explicitly asks.
- Never expose any secrets beyond the current gateway URL plus the one auth value needed for manual setup.
