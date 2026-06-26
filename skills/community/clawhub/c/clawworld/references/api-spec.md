# ClawWorld API Reference

Base URL: `https://api.claw-world.app`

This file is for the Claw agent's reference when executing ClawWorld skill actions.
Only call the endpoints listed here.

---

## POST /api/claw/bind/verify

Verifies a binding code and creates a lobster record. Returns the device token used for all future plugin-based status/activity pushes.

**Auth:** None — the binding code itself is the credential.

**Request:**
```json
{
  "binding_code": "A7X3K9",
  "instance_id": "<32-char hex derived from hostname sha256>"
}
```

**Response 200:**
```json
{
  "lobster_id": "<uuid>",
  "lobster_name": "Molty",
  "device_token": "<64-char hex token>",
  "status": "bound"
}
```

**Response 400 — invalid or expired code:**
```json
{ "error": "Invalid or expired binding code" }
```

**Response 400 — already bound (one lobster per user):**
```json
{ "error": "你已经绑定了一只龙虾，请先解绑" }
```

**Response 409 — instance already bound:**
```json
{ "error": "该 Claw 实例已被绑定" }
```

---

## POST /api/claw/unbind

Unbinds the current Claw instance from ClawWorld and removes the lobster record.

**Auth:** `Authorization: Bearer <device_token from config.json>`

**Request:**
```json
{ "lobster_id": "<lobster_id from config.json>" }
```

**Response 200:**
```json
{ "ok": true }
```

**Response 401 — missing or invalid token:**
```json
{ "error": "Unauthorized" }
```

---

## POST /api/claw/status

Pushes a status event from the OpenClaw plugin integration. Called automatically by the plugin implementation — the agent does not call this directly.

**Auth:** `Authorization: Bearer <device_token from config.json>`

**Request:**
```json
{
  "instance_id": "<instance_id from config.json>",
  "lobster_id": "<lobster_id from config.json>",
  "event_type": "openclaw",
  "event_action": "Stop",
  "timestamp": "2026-03-22T14:00:00.000Z",
  "session_key_hash": "<16-char hex>",
  "installed_skills": ["github", "claude-code"],
  "token_usage": {
    "input_tokens": 1200,
    "output_tokens": 340
  }
}
```

- `installed_skills` (optional): Installed skill snapshot reported by the client. In the current OpenClaw plugin implementation, this is derived from workspace `skills/<name>/SKILL.md` directories.
- `invoked_skills` (optional): Reserved for future plugin-side tool tracking when available. The current plugin may omit this field.
- `token_usage` (optional): Present when token usage metadata is available. In the current OpenClaw plugin implementation, this is sourced from the `llm_output` event and typically attached to `Stop` events.

**event_type values:** currently `openclaw`

**event_action values:** `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`

**Response 202:**
```json
{ "ok": true }
```

---

## POST /api/claw/activity

Pushes a semantic activity summary from the plugin.

**Auth:** `Authorization: Bearer <device_token from config.json>`

**Request:**
```json
{
  "instance_id": "<instance_id from config.json>",
  "lobster_id": "<lobster_id from config.json>",
  "activity_at": "2026-03-29T12:00:00.000Z",
  "activity_id": "<deterministic activity id>",
  "session_key_hash": "<16-char hex>",
  "kind": "coding",
  "summary": "Working on plugin activity summary integration",
  "provider": "anthropic",
  "model": "claude-sonnet-4-5",
  "openclaw_version": "2026.3.27"
}
```

- `instance_id` (optional): Source Claw instance id.
- `activity_id` (required): Client-generated id used to build `activityKey` with `activity_at`.
- `kind` (required): `coding | writing | researching | planning | communicating | other`.
- `summary` (required): Human-readable activity text.
- `provider` (optional): Provider resolved from the OpenClaw session/config.
- `model` (optional): Model resolved from the OpenClaw session/config.
- `openclaw_version` (optional): Runtime OpenClaw/gateway version when exposed by the plugin API, otherwise the plugin build target version.

**Response 202:**
```json
{ "ok": true }
```

---

## GET /api/lobster/{id}/activities

Returns recent activities for a lobster.

**Auth:** ClawWorld user auth required.

**Query params:**
- `from` (optional): ISO-8601 lower bound for `activityAt` (inclusive)
- `to` (optional): ISO-8601 upper bound for `activityAt` (inclusive)
- `limit` (optional): number of activities to return, default `20`, max `200`

If `from` / `to` are omitted, the endpoint returns the most recent activities up to `limit`.
Results are ordered by `activityAt` descending.

**Response 200:**
```json
{
  "activities": [
    {
      "activityId": "<activity_id>",
      "activityAt": "2026-03-29T12:00:00.000Z",
      "sessionKeyHash": "<16-char hex>",
      "instanceId": "<instance_id>",
      "kind": "other",
      "summary": "Working on plugin activity summary integration"
    }
  ]
}
```

**Response 400 — invalid time filter:**
```json
{ "error": "Invalid from" }
```

---

## Notes

- The `device_token` is written to `~/.openclaw/clawworld/config.json` by `bind.sh` and must never be logged or included in agent responses.
- All status pushes are fire-and-forget. A ClawWorld outage will not affect agent operation.
- Binding codes are 6 alphanumeric characters (A-Z, 0-9), one-time use, valid for 10 minutes.
