# NxVET API — what the tool needs

Full docs: **https://api.nx.vet/** — machine-readable references to fetch and read:

- `https://api.nx.vet/llms-full.txt` — complete API guide written for AI agents.
- `https://api.nx.vet/openapi/nxvet-api.yaml` — OpenAPI spec.

**Base URL:** `https://app.nx.vet`
**Auth header on every call:** `Authorization: Bearer nxvet_sk_...` (Bearer, **not** `X-API-Key`).

## Recommended: the hosted MCP server

Instead of raw REST, connect Claude Code to the hosted MCP server — it exposes ~22 tools
(labels, transcripts, NxHub conversations, devices) directly:

```bash
claude mcp add nxvet --transport http https://mcp.nx.vet/mcp \
  --header "Authorization: Bearer nxvet_sk_YOUR_API_KEY"
```

After connecting, call `get_identity` first — it returns the `organizationId` that nearly every
other call needs. Setup examples: https://api.nx.vet/mcp.html

## Key REST endpoints (if not using MCP)

| Purpose | Call |
|---|---|
| Verify key + get org id | `GET /api/auth/me` |
| List devices | `GET /api/devices?organizationId={orgId}` |
| List records (button recordings) | `GET /api/organizations/{orgId}/labels?types=A&types=B&limit=...&offset=...` — offset pagination, total in `X-Total-Count` header. The type filter is `types=` **repeated**; `types[]=` is silently ignored and returns an empty list |
| Full record incl. transcript | `GET /api/labels/{labelId}` — `ownedPatientNotes` is **null in list responses**, always fetch the detail |
| Download raw audio | `GET /api/labels/{labelId}/audio` |
| List NxHub conversations | `GET /api/nxhub/conversations?organizationId={orgId}&deviceId=...&pageSize=...&pageToken=...` — token pagination, `hasMore` flag |
| Conversation detail | `GET /api/nxhub/conversations/{deviceId}/{conversationId}` |

## Data-format gotchas (verified against live production data, 2026-07)

- **Where the transcript actually lives (labels).** NOT in a `transcript` field. A label
  detail has `ownedPatientNotes[]`, typically two entries: `type: "Transcript"` (plain text
  with speaker prefixes like `Staff:` / `Vet:` / `Speaker A:`) and `type: "SOAP"` (a JSON
  **string** — the AI clinical note). Use the `Transcript` entry. `ownedPatientNotes` is
  `null` in list responses — always fetch the detail.
- **`types[]=` silently fails.** The list-labels type filter is `types=` **repeated**
  (`types=ClinicConversation&types=NxHubBatch`). `types[]=X` returns an empty list with
  HTTP 200 — no error, just zero rows.
- **List rows have no `createdAt`.** Window/sort labels by `fromTime` (epoch **milliseconds**,
  present in list rows), or fall back to the id: label ids are UUIDv7, whose first 48 bits are
  the creation time in epoch ms.
- **JSON-inside-JSON.** Some fields (`metadata`, SOAP note `content`) are JSON strings *inside*
  the JSON response — parse them a second time.
- **Timestamp units differ.** Labels use epoch-ms `fromTime`/`toTime`; webhooks use ISO 8601.
  Every epoch-ms field in an MCP response has an `...Iso` sibling — prefer the `Iso` field.
- **Empty until processed.** Notes can be `"{}"` (or the note list empty) until AI processing
  finishes. If a transcript is empty, **retry on the next poll** — do not mark it processed.
- **Ambient recordings mixed in.** NxHUB devices capture ambient conversations (can be 20k+
  chars, multi-speaker) alongside button voice notes — same label type. The classifier must
  handle both; see SKILL.md Phase 3.
- **Date filtering.** For any date-based query via MCP, pass `fromDate`/`toDate` plus the IANA
  timezone to `list_labels`/`list_conversations` rather than paginating offsets by hand.
- **Webhooks exist but skip them.** `conversation_completed`, `new_label`, HMAC-signed — but
  they need a public HTTPS URL. A clinic laptop behind clinic Wi-Fi should **poll**, not host a
  webhook receiver.

## If a response confuses the tool

Save the exact request + response (**minus the API key**) and send it to NerveX support
(support@nx.vet). Do not paste keys or full clinic data into any external channel.
