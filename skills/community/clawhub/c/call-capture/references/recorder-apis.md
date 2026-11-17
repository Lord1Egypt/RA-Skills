# Recorder APIs, field by field

What you need to satisfy the `Recorder` contract in `recorder.ts` for fourteen recorders, taken
from each vendor's own developer documentation. Read `providers.md` first — it is how a recorder is
chosen and what an adapter is shaped like. This file is the raw material: base URLs, header
formats, the exact date parameters, the exact field names a transcript arrives under, and the
things that will produce a clean empty run if you guess.

Nine of the fourteen ship as adapters under `collect/recorders/`; for those, this file is what the
adapter was written against and where to look when a field name has moved. The other five do not
ship, each for a named reason in its own section, and this file is what you would write them from.

Everything below was read from an official spec or developer page and the URL is cited. Where a
vendor does not document something — a page-size ceiling, a rate limit number — it says
**unverified** rather than a plausible number.

Checked September 2026.

## The short version

| Recorder      | Ships           | Public API      | List by date range                | Transcript readiness signal          |
| ------------- | --------------- | --------------- | --------------------------------- | ------------------------------------ |
| Avoma         | `avoma`         | paid plans      | `from_date` / `to_date` (required) | `state` + `transcript_ready`         |
| Granola       | `granola`       | Business / Ent  | `created_after` / `created_before` | none — `summary_markdown` may be null |
| Fathom        | `fathom`        | all plans       | `created_after` / `created_before` | none — poll or use the webhook       |
| Gong          | `gong`          | any plan        | `fromDateTime` / `toDateTime` (required) | none — infer from records present |
| Fireflies     | `fireflies`     | all plans       | `fromDate` / `toDate`             | `meeting_info.summary_status`        |
| Grain         | `grain`         | Starter+ / Business+ | `after_datetime` / `before_datetime` | none                         |
| tl;dv         | `tldv`          | organizer on Pro+ | `from` / `to`                   | none — use the `TranscriptReady` hook |
| Modjo         | `modjo`         | unverified      | `from` / `to`                     | `status`, `transcriptRetentionStatus` |
| Clari Copilot | `clari`         | unverified      | `filterTimeGt` / `filterTimeLt`   | `status === "PROCESSED"`             |
| Otter.ai      | no — see below  | **Enterprise only** | **no date filter**            | `process_status.*`                   |
| Circleback    | no — see below  | unverified      | **no date filter**                | `statuses` filter                    |
| Zoom          | no — see below  | Pro+            | `from` / `to`, **one month max**  | `TRANSCRIPT` file in `recording_files` |
| Read.ai       | no — see below  | all plans (open beta) | `start_time_ms.gte` / `.lte` | `end_time_ms` present = ended        |
| Attention     | no — see below  | unverified      | `fromDateTime` / `toDateTime`     | `transcriptStatus`                   |

Two recorders cannot answer "what happened between these dates" in one request. Otter and
Circleback both page newest-first with no date parameter, so a rolling window means paging until
you cross the window's floor and stopping. Everything else takes a range.

## Check it against the live API, not against this file

Whether you are verifying a shipped adapter or writing a new one, run the list endpoint by hand
first. A wrong field name produces a clean, empty run every morning rather than an error, and one
curl settles it:

```sh
# Avoma; the other thirteen differ only in host, header and parameter names
curl -s -H "Authorization: Bearer $CALL_RECORDER_API_KEY" \
  "https://api.avoma.com/v1/meetings/?from_date=$(date -u -d '3 days ago' +%F)T00:00:00Z&to_date=$(date -u +%F)T23:59:59Z&page_size=5" \
  | head -c 2000
```

Then take one id and check the transcript endpoint the same way. When the adapter compiles, run the
collector with `--recorder=<slug> --dry-run`: it exercises `listReady` and the readiness filter and
prints what it would capture, writing nothing you would have to unpick.

---

## Avoma

**Public API.** Yes, on the paid plans; the key is generated per user in Avoma's settings.

**Base URL.** `https://api.avoma.com/v1`

**Auth.** `Authorization: Bearer <api_key>`

**List.** `GET /v1/meetings/` — `from_date` and `to_date` are both **required**, ISO-8601 with `Z`,
plus `page_size` (100 used here). Paginate by following the response's `next` link until it is
null; results are on `results[]`.

**Transcript.** `GET /v1/transcriptions/?meeting_uuid=<id>` → `transcript[]` of
`{ transcript, speaker_id }` plus a separate `speakers[]` of `{ id, name }`. The text field is
called `transcript`, on an object inside a field also called `transcript`, and the speaker is an id
to be joined against `speakers[]`.

**Notes.** `GET /v1/notes/?meeting_uuid=<id>` → `results[].data`, a **nested block structure**
rather than markdown: objects carrying `text`, `children` and `object: "block"`, walked
recursively.

**Attendees.** `attendees[]` with `{ email, name }`. `is_internal` exists on the meeting and
**cannot be trusted** — some workspaces return false on every meeting, including all-internal ones,
which is why the pipeline derives that from email domains.

**Meeting id.** `uuid`.

**Gotchas.** `transcript_ready` and `notes_ready` are false until processing finishes and **absent**
rather than false on anything not yet held, which is the whole reason the collector's window
overlaps the previous run. Readiness is `state === "completed"` and either flag true.

---

## Granola

**Public API.** Yes. API keys require a **Business or Enterprise** plan; on Enterprise an admin
can restrict which note-access scopes members may use. Personal keys carry the creating user's
access; workspace keys (Business and Enterprise, admin-created) never expire and read only public
notes plus spaces with **Allow Granola API access** turned on.
<https://docs.granola.ai/help-center/sharing/integrations/granola-api>

**Base URL.** `https://public-api.granola.ai`

**Auth.** `Authorization: Bearer <api_key>` — the spec declares `type: http, scheme: bearer,
bearerFormat: apiKey`.

**List.** `GET /v1/notes`

| Param            | Notes                                            |
| ---------------- | ------------------------------------------------ |
| `created_after`  | date or date-time                                |
| `created_before` | date or date-time                                |
| `updated_after`  | date or date-time                                |
| `folder_id`      | `^fol_[a-zA-Z0-9]{14}$`, includes child folders  |
| `cursor`         | opaque                                           |
| `page_size`      | default **10**, max **30**                       |

Response: `{ notes: [...], hasMore: boolean, cursor: string | null }`. Page until `hasMore` is
false. Each note in the list carries only `id`, `object`, `title`, `owner`, `created_at`,
`updated_at` — attendees and summary need `GET /v1/notes/{note_id}`.

**Transcript.** `GET /v1/notes/{note_id}/transcript?cursor=&page_size=` — `page_size` default 50,
max 100. Response `{ transcript: [...], hasMore, cursor }`, each item:

```
{ speaker: { source: "microphone" | "speaker",
             attribution?: "me" | "them",
             diarization_label?: "Speaker A",
             name?: "Alice Smith" },
  text: string,
  start_time: ISO-8601,
  end_time: ISO-8601 }
```

Only `speaker.source` is required. `speaker.name` appears only when a speaker was identified;
`attribution` is omitted when unknown. Timestamps are absolute ISO datetimes, not offsets — unlike
every other recorder here.

**Notes / summary.** On `GET /v1/notes/{note_id}`: `summary_text` and `summary_markdown` (nullable
when the note has no summary). `private_notes_text` / `private_notes_markdown` are the owner's own
notes and return `null` for shared notes and for workspace-scoped keys.

**Attendees.** `attendees[]` with `{ name, email }` — email always present. Also
`calendar_event.invitees[].email` and `calendar_event.organiser`. **No internal/external flag**;
derive it from email domains.

**Meeting id.** `id`, prefixed `not_` (`^not_[a-zA-Z0-9]{14}$`).

**Gotchas.** `GET /v1/notes/{note_id}?include=transcript` inlines the transcript, but returns
`TRANSCRIPT_TOO_LARGE` when it will not fit — you must fall back to the paged endpoint, so
implement that path from the start rather than as an error case. Rate limits: 25 burst, sustained
5 requests/second, applied per user or per workspace depending on the key's scope. Nothing
signals transcript readiness; `summary_markdown` being null is the closest proxy and it is not
documented as one.
Spec: <https://docs.granola.ai/openapi.json> · Docs: <https://docs.granola.ai>

---

## Fathom (fathom.video)

**Public API.** Yes, on **all plans including free**; keys are generated in User Settings → API
Access. Keys are user-scoped: they reach meetings you recorded or that were shared with you or
your team, never another user's private meetings.
<https://developers.fathom.ai/quickstart>

**Base URL.** `https://api.fathom.ai/external/v1`

**Auth.** `X-Api-Key: <api_key>` (primary), or `Authorization: Bearer <token>` for OAuth apps.
Both are declared in the spec's `security`.

**List.** `GET /meetings`

| Param                              | Notes                                                    |
| ---------------------------------- | -------------------------------------------------------- |
| `created_after`                    | e.g. `2025-01-01T00:00:00Z`, filters on `created_at`      |
| `created_before`                   | same                                                      |
| `cursor`                           | opaque                                                    |
| `recorded_by[]`                    | repeated email param                                      |
| `teams[]`                          | repeated team-name param                                  |
| `meeting_type`                     | name from `/meeting_types`                                |
| `calendar_invitees_domains[]`      | repeated, exact-match domain                              |
| `calendar_invitees_domains_type`   | `all` \| `only_internal` \| `one_or_more_external`        |
| `include_transcript`               | default false                                             |
| `include_summary`                  | default false                                             |
| `include_action_items`             | default false                                             |
| `include_highlights`               | default false                                             |
| `include_crm_matches`              | default false                                             |

Response `{ limit, next_cursor, items: [...] }`. **No page-size parameter is documented** —
`limit` appears in the response only, and the quickstart's worked example returns 10. Page until
`next_cursor` is null.

**Transcript.** `GET /recordings/{recording_id}/transcript`. Returns
`{ transcript: [ { speaker: { display_name, matched_calendar_invitee_email }, text, timestamp } ] }`
where `timestamp` is `HH:MM:SS` relative to meeting start.
`speaker.matched_calendar_invitee_email` is null when no exact match was found — that is the field
that maps a speaker to an attendee, and it is the only one.

Passing `?destination_url=` flips the same endpoint to async: it returns
`{ destination_url }` and POSTs the transcript there instead. Do not pass it if you want the data
inline.

**Summary.** `GET /recordings/{recording_id}/summary` →
`{ summary: { template_name, markdown_formatted } }`. Both nullable. `markdown_formatted` is
**always English** regardless of the meeting language. The same object appears inline as
`default_summary` on `/meetings` when `include_summary=true`.

**Attendees.** `calendar_invitees[]` with `{ name, email, email_domain, is_external,
matched_speaker_display_name }`. `is_external` is a **first-class boolean** — Fathom is one of the
few here that flags it for you. `matched_speaker_display_name` only populates when
`include_transcript=true` and only for meetings after 1 Feb 2025.

**Meeting id.** `recording_id` (integer). Note it is an integer, not a string, and the path
parameters take it as such.

**Gotchas.** OAuth-connected apps **cannot** use `include_summary` or `include_transcript` on
`/meetings` — they must call `/recordings/{id}/...` per meeting. Rate limits: 60 requests / 60
seconds globally; **30 / 60s for "heavy" requests**, which means every `/recordings` endpoint and
any `/meetings` call with `include_summary` or `include_transcript` true, and which may be
lowered to 5 / 60s under load. Headers are `RateLimit-Limit`, `RateLimit-Remaining`,
`RateLimit-Reset`, plus `Retry-After` on 429 only. No readiness flag; use the
`new-meeting-content-ready` webhook or poll.
Rate limits: <https://developers.fathom.ai/api-overview> · Spec:
<https://developers.fathom.ai/api-reference/meetings/list-meetings>

---

## Gong

**Public API.** Yes, on **any Gong plan** — API keys are created by a Tech admin in Admin center →
Settings → Ecosystem → API, optionally with a TTL and a trusted-IP allowlist (requests from other
addresses get 403).
<https://help.gong.io/docs/receive-access-to-the-api>

**Base URL.** Per-company, and you must look it up rather than hardcode: the documented source is
<https://app.gong.io/company/api-authentication?currentTab=MY_API_TAB>. `https://api.gong.io/v2`
is the common value; regional instances take the form `https://{region}.api.gong.io/v2`.

**Auth.** `Authorization: Basic <base64(accessKey:accessKeySecret)>`, or
`Authorization: Bearer <token>` from the OAuth flow for published apps.
<https://help.gong.io/apidocs/introduction-2>

**List.** Two endpoints, and the choice matters.

`GET /v2/calls` — `fromDateTime` and `toDateTime` are **required**, ISO-8601 with `Z` or an offset
(`2018-02-18T02:30:00-07:00`). Also `cursor` and `workspaceId`. Metadata only.

`POST /v2/calls/extensive` — the one you want, because it returns parties and AI content in the
same call:

```json
{ "filter": { "fromDateTime": "...", "toDateTime": "...",
              "callIds": ["..."], "primaryUserIds": ["..."], "workspaceId": "..." },
  "contentSelector": {
    "exposedFields": {
      "parties": true,
      "content": { "brief": true, "keyPoints": true, "outline": true,
                   "highlights": true, "callOutcome": true,
                   "trackers": true, "topics": true, "structure": true },
      "media": true } } }
```

Only `filter` is required. For web-conference calls the date is the **scheduled** time; for
everything else the actual start. `toDateTime` is exclusive.

Pagination on both: the response carries `records: { totalRecords, currentPageSize,
currentPageNumber, cursor }`, and `cursor` is **present only when more records exist**. Repeat the
call with that cursor and every other input unchanged. Page size is not client-controllable
(unverified what it is).

**Transcript.** `POST /v2/calls/transcript` with the same `filter` shape (`callIds` is the useful
one). Response:

```
{ requestId, records: {...},
  callTranscripts: [ { callId,
                       transcript: [ { speakerId, topic,
                                       sentences: [ { start, end, text } ] } ] } ] }
```

`transcript[]` is a list of **monologues**, not sentences — each entry is one speaker's turn and
holds its own `sentences[]`. `start` and `end` are integer **milliseconds** from call start.

**`speakerId` is an opaque id, never a name.** You resolve it by cross-referencing
`parties[].speakerId` from `/v2/calls/extensive`, which means a transcript fetch without a prior
extensive fetch gives you unattributable text. Carry the party list through.

**Notes / summary.** No separate endpoint — it is `content` on `/v2/calls/extensive`:
`content.brief` (string, the Spotlight brief), `content.keyPoints[].text`,
`content.outline[]` (`{ section, startTime, duration, items[] }`),
`content.highlights[]` (`{ title, items[] }`), `content.callOutcome` (`{ id, category, name }`).
Each is returned **only when available and only when its `contentSelector` flag is true** — an
absent key means "not requested or not generated", not "empty".

**Attendees.** `parties[]`: `{ id, emailAddress, name, title, userId, speakerId, phoneNumber,
affiliation, methods, context }`. `affiliation` is `Internal` | `External` | `Unknown` — a real
flag. `methods[]` distinguishes `Invitee` from `Attendee`. `speakerId` is present only for parties
who actually spoke. Call-level `scope` is `Internal` | `External` | `Unknown`.

**Meeting id.** `id` on the call object (`metaData.id` in the extensive response), a numeric string
of up to 20 digits — keep it a string, it overflows a JS number.

**Gotchas.** 3 requests/second and 10,000 requests/day per company; 429 carries `Retry-After` in
seconds. Scopes are per-endpoint: `api:calls:read:basic` for `/v2/calls`,
`api:calls:read:extensive`, `api:calls:read:transcript`, plus `api:calls:read:media-url` if you
ask for `media` (those URLs live 8 hours). No readiness flag anywhere — infer from whether a
transcript record comes back. Gong adds JSON fields without warning and says so in its own docs,
so parse defensively.
Limits: <https://help.gong.io/docs/what-the-gong-api-provides> · Reference:
<https://help.gong.io/apidocs/retrieve-detailed-call-data-by-various-filters-v2callsextensive-2>

---

## Fireflies.ai

**Public API.** Yes, GraphQL, available on all plans — the rate-limit table lists a Free tier, so
access is not gated, only throttled.
<https://docs.fireflies.ai/fundamentals/limits>

**Base URL.** `https://api.fireflies.ai/graphql` — one endpoint, POST only.

**Auth.** `Authorization: Bearer <api_key>` plus `Content-Type: application/json`.
<https://docs.fireflies.ai/fundamentals/authorization>

**List.** The `transcripts` query.

| Argument                          | Notes                                                          |
| --------------------------------- | -------------------------------------------------------------- |
| `fromDate` / `toDate`             | `DateTime`, ISO 8601 `YYYY-MM-DDTHH:mm.sssZ`                    |
| `limit`                           | **max 50** per query                                            |
| `skip`                            | offset                                                          |
| `keyword` + `scope`               | `title` \| `sentences` \| `all`; `scope` makes `keyword` required |
| `host_email`                      |                                                                 |
| `organizers[]` / `participants[]` | arrays of emails; mutually exclusive with the deprecated singulars |
| `user_id`, `mine`, `channel_id`   |                                                                 |
| `date`, `title`, `organizer_email`, `participant_email` | deprecated                          |

Offset pagination via `skip`/`limit`, no cursor.

**Transcript.** The same query — select `sentences { index speaker_name speaker_id text raw_text
start_time end_time ai_filters { ... } }`. There is no separate transcript endpoint, so
`listReady` can fetch everything in one round trip and `transcript(id)` becomes a lookup. Watch
the payload size: a wide selection over a three-day window returns the whole window at once.

`text` is the user-edited sentence, `raw_text` is what the audio produced. `speaker_name` is a
name; `speaker_id` is the id used in `speakers { id name }`.

**Notes / summary.** `summary { overview short_summary short_overview gist bullet_gist
shorthand_bullet notes outline action_items keywords meeting_type topics_discussed
transcript_chapters extended_sections { ... } }` — all on the same `Transcript` object, so no
extra request. `action_items` and `keywords` are **strings**, not arrays.
<https://docs.fireflies.ai/schema/summary>

**Attendees.** `meeting_attendees[]` → `{ displayName, email, phoneNumber, name, location }`
(`location` is deprecated). Also `participants` (array of guest email strings, including
non-Fireflies users), `fireflies_users`, and `workspace_users` — the last being the subset of
`fireflies_users` who are on the caller's team. **No internal/external flag**; `workspace_users`
minus the rest is the closest thing.

**Meeting id.** `id` (GraphQL `ID`).

**Gotchas.** `meeting_info.summary_status` is the readiness signal, one of `processing`,
`processed`, `failed`, `skipped` — Fireflies is one of the few recorders that gives you a real
one, so use it in `listReady` rather than guessing. Rate limits are plan-shaped: Free 50
requests/day, Pro 500/day, Business/Enterprise 60/minute. `audio_url` and `video_url` need Pro or
higher and expire after 24 hours. `duration` is in **minutes**, `date` is epoch milliseconds,
`dateString` is the ISO form.
<https://docs.fireflies.ai/graphql-api/query/transcripts> ·
<https://docs.fireflies.ai/schema/transcript>

---

## Otter.ai — not shipped

**Why not.** Two blockers, either one of which would be enough. The list endpoint has no date
parameter at all, so a rolling window means paging newest-first until you cross the floor — doable,
but it re-reads the same recent conversations every morning. And the transcript arrives as a
**plain-text blob** with the speaker and the offset baked into the string and no documented grammar
for parsing it, so a `Recorder` here either hands the scribe an unstructured wall of text or invents
a parser against an undocumented format. Write it if Otter is what your team uses: hand the blob
straight back from `transcript()` and let the scribe read it, which is honest, or parse it and own
the format when it changes.

**Public API.** Yes, but **Enterprise workspaces only**. Otter says so plainly: "Otter's Public
API is available for all Enterprise workspaces. If you do not see this feature for your workspace,
contact your Otter account manager." Keys are made under Integrations → Developer, limit two per
user, shown once.

**Base URL.** `https://api.otter.ai/v1`

**Auth.** `Authorization: Bearer <api_key>`

**List.** `GET /conversations` — and this is the important part: **there is no date-range
parameter.** The documented query parameters are `include_shared`, `channel_id`, `limit` and
`cursor`, nothing more. Results come back reverse-chronological, so a date window means paging
until `created_at` falls below your floor and then stopping yourself.

Pagination is cursor-based: `meta: { retrieved_at, has_more, next_cursor }` and `data: [...]`.
Pass `next_cursor` back as `cursor`. Default and maximum `limit` are **unverified** — the docs
show `limit=20` in examples without stating either bound.

**Transcript.** `GET /conversations/{id}?include=transcript` (or `include=all`). It arrives at
`relationships.transcript` as:

```json
{ "content": "Sam  00:15 \n Welcome to project launch meeting!\n", "format": "txt" }
```

**That is a plain-text blob.** There are no segment objects, no speaker field, no timestamp field —
speaker and offset are baked into the string. If your adapter wants structured turns it has to
parse them out, and there is no documented grammar for that string. Of every recorder in this
file, Otter is the one whose transcript you cannot consume structurally.

**Notes / summary.** `abstract_summary` (string) sits on the conversation object itself, in both
the list and the get response. Richer material comes through `include`:
`relationships.action_items[]` (`{ id, text, assignee, status { completed, created_at,
last_modified_at, completed_at } }`), `relationships.insights[]` (`{ topic, text[] }`),
`relationships.outline[]` (`{ section, text[] }`), and `relationships.custom_prompt`
(`{ label, output }`).

**Attendees.** `calendar_guests[]` → `{ name, email }`. Emails are included. **No internal/external
flag**, and note the field can be `null` rather than an empty array. `shared_emails[]` and
`shared_channels[]` describe sharing, not attendance.

**Meeting id.** `id` (string).

**Gotchas.** `process_status` is an object — `{ abstract_summary, action_item, outline }` — whose
values are `null` while pending and `"finished"` when done. That is your readiness signal, and it
is per-artefact rather than one flag. Rate limit is 10 requests/second on Enterprise. Otter's own
documentation recommends webhooks over polling and says so repeatedly; with no date filter on the
list endpoint, a polling adapter is doing more work here than anywhere else in this file.
<https://help.otter.ai> — "Otter.ai Public API"

---

## Grain

**Public API.** Yes, with two token types on different plans. **Personal Access Tokens** are
available on Starter, Business and Enterprise and carry the generating user's own permissions.
**Workspace Access Tokens** read *all* workspace data, require admin access, and are **Business
and Enterprise only**. The Free plan has no API access.
<https://support.grain.com/en/articles/15507288-grain-api>

**Base URL.** `https://api.grain.com`, with every path under `/_/public-api/v2`.

**Auth.** Two headers, both required:

```
Authorization: Bearer <PAT | WAT | OAuth access token>
Public-Api-Version: 2025-10-31
```

Omitting `Public-Api-Version` is not optional — it is how Grain introduces and deprecates fields.
OAuth2 authorization-code with PKCE is available for third-party integrations; tokens from it
behave as Personal API.

**List.** `POST /_/public-api/v2/recordings` (a POST, despite being a read):

```json
{ "cursor": "...",
  "filter": { "after_datetime": "2025-01-01T09:30:00Z",
              "before_datetime": "2025-01-04T09:30:00Z",
              "participant_scope": "external",
              "attendance": "hosted",
              "title_search": "...", "team": "<uuid>", "meeting_type": "<uuid>" },
  "include": { "participants": true, "ai_summary": true, "ai_action_items": true,
               "calendar_event": true, "highlights": true, "screenshares": true,
               "private_notes": true, "hubspot": true } }
```

Response `{ cursor, recordings: [...] }`; `cursor` is nullable and you send it back as the
top-level `cursor` param. `attendance` and `private_notes` are Personal API only.

**A documentation bug to know about:** Grain's reference describes `before_datetime` as "only
return recordings which `start_datetime` is **after** the selected date (exclusive)" and
`after_datetime` as "…**before** the selected date (inclusive)". The two descriptions are
transposed relative to the parameter names. Verify the direction against your own data before
trusting a window.

**Transcript.** `GET /_/public-api/v2/recordings/:recording_id/transcript` returns a **bare JSON
array** (no envelope):

```json
[ { "start": 8000, "end": 9000, "text": "Hello there.",
    "speaker": "Obi Wan Kenobi",
    "participant_id": "oooo1111-pp22-qq33-rr44-ssss55555555" } ]
```

`speaker` is the name directly; `participant_id` joins to `participants[].id` and is nullable.
`start`/`end` are **milliseconds**. `.txt`, `.vtt` and `.srt` variants of the same path return
formatted text instead.

**Notes / summary.** `ai_summary.text` — markdown — returned on the recording object when
`include: { ai_summary: true }`. Action items are `ai_action_items[]` with
`{ status: "pending" | "completed", timestamp, text, assignee: { id, name, user_id } }`.
`private_notes.text` is markdown and Personal API only.

**Attendees.** `participants[]` (only with `include: { participants: true }`):
`{ id, name, email, scope, confirmed_attendee, observed_join_time, observed_leave_time }`.
`scope` is `internal` | `external` | `unknown` — a real flag. `email` is nullable.
`confirmed_attendee` distinguishes invited-but-absent from actually present. The join/leave times
are what Grain's recorder observed, which its own docs warn may not match reality.

**Meeting id.** `id`, a UUID string.

**Gotchas.** 300 requests/minute, with `x-ratelimit-limit` and `x-ratelimit-remaining` on every
response and `Retry-After` added only when you exceed it. No transcript-readiness flag. The v1
Personal and Workspace APIs still exist but are being sunset — do not build against them.
<https://developers.grain.com/>

---

## tl;dv

**Public API.** Yes, currently **v1alpha1** and explicitly labelled alpha with breaking changes
expected. Access depends on the **meeting organizer's** plan, not the caller's: Free organizers
give no API access even when the meeting is shared with you; Pro, Business and Enterprise do.
Organization-wide automation is Enterprise. Ownership follows the calendar invite organizer.

**Base URL.** `https://pasta.tldv.io` — the docs' own words: "this endpoint may choose to change
its pasta shape."

**Auth.** `x-api-key: <api_key>` — a custom header, not `Authorization`. Keys come from
<https://tldv.io/app/settings/personal-settings/api-keys>.

**List.** `GET /v1alpha1/meetings`

| Param              | Notes                                                                    |
| ------------------ | ------------------------------------------------------------------------ |
| `from` / `to`      | `date` or `date-time`                                                    |
| `page`             | 1-based, default 1                                                       |
| `limit`            | default **50**, max **100**                                              |
| `query`            | free-text search                                                         |
| `onlyParticipated` | default false                                                            |
| `meetingType`      | `internal` \| `external`; defaults to both                               |

Response `{ page, pages, total, pageSize, results: [...] }`. **Total results cannot exceed
10,000** — past that the API tells you to narrow the date range, so a full-history backfill has to
be walked in windows.

**Transcript.** `GET /v1alpha1/meetings/{meetingId}/transcript` →
`{ id, meetingId, data: [ { speaker, text, startTime, endTime } ] }`. `speaker` is a plain name
string; `startTime`/`endTime` are **seconds**.

**Notes.** `GET /v1alpha1/meetings/{meetingId}/notes` →
`{ structuredNotes: [ { segmentId, timestamp, text, topicId } ],
   markdownContent: string,
   topics: [ { id, order, title, summary } ] }`.
`markdownContent` is the whole thing rendered; `topicId` on a note joins to `topics[].id`.
`/highlights` is deprecated.

**Attendees.** `invitees[]` → `{ name, email }`, described as "invited, or participated" — the two
are not distinguished. Plus `organizer` → `{ name, email }`. **No internal/external flag on the
participant**, though `meetingType` filters at the meeting level.

**Meeting id.** `id`, a 24-hex-character string (`^[0-9a-fA-F]{24}$` on some path params — a
MongoDB ObjectId).

**Gotchas.** Rate limits are **unverified** — the docs give none. Seeing a meeting in the web app
does not imply API access to it; sharing grants UI visibility only. Two webhook triggers exist,
`MeetingReady` and `TranscriptReady`, configurable at user, team or organization level, and
`TranscriptReady` is the only readiness signal available.
<https://doc.tldv.io/>

---

## Read.ai — not shipped

**Why not.** The credential cannot survive an unattended cron. There are no static API keys: it is
OAuth 2.1 with dynamic client registration, access tokens that expire after **ten minutes**, and
single-use refresh tokens that rotate on every exchange. A daily job would have to persist the
rotated refresh token somewhere durable and a broken chain needs a human with a browser — which is
a different shape of credential from one static `CALL_RECORDER_API_KEY` in the workspace catalog,
and would change the agent's wiring rather than just adding an adapter. Revisit when Read.ai ships the personal access tokens it
names as planned for GA.

**Public API.** Yes — a REST API and an MCP server, both in **open beta**, available to all users
regardless of plan, subject to two prerequisites: if you belong to a workspace it must have
**Downloads** enabled under Workspace Settings → Reports & Sharing, and you can only read reports
you can already see in the web app (admins need Global Report Access for workspace-wide reach).
This supersedes Read.ai's older webhook-only posture — third-party guides still describing it as
push-only are out of date.
<https://support.read.ai/hc/en-us/articles/49379985941523-Read-AI-API-and-MCP-Overview>

**Base URL.** `https://api.read.ai/`

**Auth.** `Authorization: Bearer <access_token>` — but **there are no static API keys.** Read.ai
uses OAuth 2.1 with RFC 7591 dynamic client registration:

1. `POST https://api.read.ai/oauth/register` for a `client_id` / `client_secret`
2. Authorization-code flow with PKCE, started in a browser at `https://api.read.ai/oauth/ui`
3. Exchange the code for `access_token` + `refresh_token`

**Access tokens expire after 10 minutes** and refresh tokens are single-use and rotate on every
exchange (with a short grace period). Read.ai names this as a known limitation and says personal
access tokens are planned for GA. For an unattended morning cron this is the hardest credential
story in this file: you must persist the rotated refresh token every time, and a broken token
chain needs a human with a browser.
<https://support.read.ai/hc/en-us/articles/49380809380371-API-Keys-Authentication>

**List.** `GET /v1/meetings`

| Param                                   | Notes                                    |
| --------------------------------------- | ---------------------------------------- |
| `start_time_ms.gt` / `.gte` / `.lt` / `.lte` | epoch **milliseconds**              |
| `limit`                                 | default 10, **max 10**                   |
| `cursor`                                | **the `id` of the last object you saw**  |
| `expand[]`                              | repeated                                 |

Response `{ object: "list", url, has_more, data: [...] }`, newest first. The cursor is not opaque —
it is literally the last meeting's ULID — and `limit` maxes out at **10**, so a three-day window
is several round trips.

**Transcript.** There is no transcript endpoint; it is an expansion:
`GET /v1/meetings/{id}?expand[]=transcript`. Shape:

```json
{ "transcript": {
    "speakers": [ { "name": "Alice Example" } ],
    "turns": [ { "speaker": { "name": "Alice Example" },
                 "text": "Let's start with the project updates.",
                 "start_time_ms": 1733800000000, "end_time_ms": 1733800005000 } ],
    "text": "[Alice Example]: Let's start with the project updates." } }
```

Note `turns` on REST but **`speaker_blocks`** on the webhook payload, with `words` instead of
`text` — the two surfaces disagree, so an adapter that also consumes webhooks needs both. REST
timestamps are absolute epoch milliseconds. `GET /v1/meetings/{id}/live` is for in-progress
meetings and only accepts `transcript` and `chapter_summaries` expansions.

**Notes / summary.** Expansions on the same object: `summary` (string), `chapter_summaries[]`
(`{ title, description, topics[] }`), `action_items[]` (`{ text }`), `key_questions[]`,
`topics[]`, `metrics` (`{ read_score, sentiment, engagement }`), `recording_download`.

**Attendees.** `participants[]` → `{ name, email, invited, attended }` on REST. Emails included.
`invited` and `attended` are separate booleans, which is more than most give you. **No
internal/external flag.** The webhook variant adds `first_name` / `last_name` and drops
`invited`/`attended`.

**Meeting id.** `id`, a 26-character Crockford base32 **ULID**. The webhook calls the same value
`session_id`.

**Gotchas.** 100 requests/minute per user; 429 on exceed. Expanding fields is documented as
noticeably slower, especially expansions on a list request — with `limit` capped at 10 you are
already making many calls, so decide whether to expand on the list or per meeting. Active meetings
are identified by `end_time_ms` being absent or null, and will have little or no expandable data.
Live transcript is not captured at all unless someone had the live dashboard open. Webhooks remain
available and are signed with `X-Read-Signature` (HMAC-SHA256 over the raw body, key
base64-decoded).
<https://support.read.ai/hc/en-us/articles/49381161088659-API-Reference>

---

## Zoom (cloud recording transcripts) — not shipped

**Why not.** Zoom is a recorder by accident and the adapter shows it. The transcript is a **WebVTT
file** you find by hunting for `file_type === "TRANSCRIPT"` in `recording_files` and then download
with a second authenticated request, so `transcript()` is a cue-block parser rather than a field
read. Attendee emails are usually **not available**: `user_email` is an empty string for anyone
outside the host's account, which is exactly the external attendee this pipeline slugs the account
from. Add Server-to-Server OAuth, two different meeting ids that silently resolve to different
instances, and a one-month cap on the list window, and it is a different class of work from the
nine that ship. Worth doing if Zoom's own recording is your system of record — start from the
participants endpoint, not the recordings one, because if the emails are not there nothing
downstream works.

**Public API.** Yes. Cloud Recording requires **Pro or higher**; AI Companion meeting summaries
require Pro/Business or higher plus the host's **Meeting Summary with AI Companion** setting
enabled. End-to-end encrypted meetings never produce summaries.

**Base URL.** `https://api.zoom.us/v2`

**Auth.** `Authorization: Bearer <access_token>` (OAuth 2.0; Server-to-Server OAuth for unattended
jobs).

**List.** `GET /users/{userId}/recordings` — pass `me` for user-level apps.

| Param             | Notes                                                       |
| ----------------- | ----------------------------------------------------------- |
| `from` / `to`     | `yyyy-mm-dd` **UTC dates, not datetimes**                   |
| `page_size`       | default 30, **max 300**                                     |
| `next_page_token` | expires after **15 minutes**                                |
| `trash`, `trash_type`, `mc`, `meeting_id` |                                     |

**The maximum range is one month.** A longer window has to be chunked. Omitting `from`/`to`
defaults to the current date. Scopes: `recording:read:admin`, `recording:read`; granular
`cloud_recording:read:list_user_recordings[:admin|:master]`. Rate limit label MEDIUM.

`GET /meetings/{meetingId}/recordings` fetches one meeting's files (LIGHT).

**Transcript.** There is no JSON transcript endpoint. Inside `recording_files[]`, find the entry
with `file_type === "TRANSCRIPT"` (`recording_type: "audio_transcript"`) and GET its
`download_url`. **The payload is WebVTT, not JSON** — you parse cue blocks yourself. The full
`file_type` enum is `MP4`, `M4A`, `CHAT`, `TRANSCRIPT`, `CSV`, `TB`, `CC`, `CHAT_MESSAGE`,
`SUMMARY`.

Authenticate the download with `Authorization: Bearer <ACCESS_TOKEN>`, or request
`include_fields=download_access_token` on `GET /meetings/{meetingId}/recordings` (with an optional
`ttl` up to 604800 seconds) and use that token instead. `CC` and `TIMELINE` files are missing
`id`, `status`, `file_size`, `recording_type` and `play_url` entirely.

**Notes / summary.** `GET /meetings/{meetingId}/meeting_summary`, keyed by **UUID not id**. The
current field is **`summary_content`** — the complete summary as Markdown. `summary_overview`,
`summary_details[]`, `next_steps[]` and `edited_summary` are all marked **deprecated** in the spec
and will stop being supported; do not build on them. Also `summary_title`, `summary_doc_url`,
`summary_created_time`, `summary_last_modified_time`.

Listing: `GET /meetings/meeting_summaries` (account-wide) or
`GET /users/{userId}/meeting_summaries`, both taking `from`/`to` as
`yyyy-MM-dd'T'HH:mm:ss'Z'` — note these are **datetimes** where the recordings endpoint takes bare
dates — plus `time_filter_field` (`summary_start_time` | `summary_created_time`), `page_size`
(max 300) and `next_page_token`.

Scopes: `meeting_summary:read`, `meeting_summary:read:admin`; granular `meeting:read:summary`,
`meeting:read:summary:admin`, `meeting:read:list_summaries[:admin]`. Several developer-forum
threads report `meeting:read:summary:admin` not appearing in the Server-to-Server scope picker on
some accounts — check before you design around it.

**Attendees.** Not on the recording object. `GET /past_meetings/{meetingId}/participants` returns
`participants[]` with `{ id, name, user_id, user_email, join_time, leave_time, duration,
registrant_id, failover, status, internal_user }`. `internal_user` is a real boolean (default
false). **`user_email` is an empty string for anyone outside the host's account**, with exceptions
governed by Zoom's email-address display rules — so external attendee emails are usually not
available. Data is retained 15 months. One-participant meetings are excluded unless the account
setting **Show one person meetings and webinars on Dashboard and Reports** is on. Scopes:
`meeting:read:list_past_participants[:admin]`.

**Meeting id.** Two, and using the wrong one silently gives you the wrong instance. `uuid` is
per-instance and is what the summary endpoint wants; `id` (int64) is the reusable meeting number
and resolves to the *latest* instance. **A UUID beginning with `/` or containing `//` must be
double URL-encoded.**

**Gotchas.** Rate limits are per-account and by label, not per-endpoint: Light 30/s (Pro) or 80/s
(Business+), Medium 20/s or 60/s, Heavy 10/s or 40/s, with Free tiers far lower and daily caps.
429 responses carry a message distinguishing per-second from daily exhaustion. There is no
readiness flag — a `TRANSCRIPT` file's presence in `recording_files` is the signal. Cloud
recordings may be auto-deleted (`auto_delete`, `auto_delete_date`).
<https://developers.zoom.us/docs/api/meetings/> ·
<https://developers.zoom.us/docs/api/rate-limits/>

---

## Circleback — not shipped

**Why not.** No date filter on the list endpoint and the cursor is in a `Link` **header** rather
than the body, which is a bare array — so a rolling window means paging newest-first until you
cross the floor, and `fetchJson` would have to hand back headers to do it. Nothing here is hard;
it is the one adapter that needs a shared helper changed, and that change belongs to a run where
someone actually uses Circleback. Everything else about it is clean: structured segments, notes on
the meeting object, emails on the attendees.

**Public API.** Yes. Keys are created in Settings → API keys, look like `cb_<secret>` and are
shown once. **Which plans include API keys is unverified** — the docs do not say.

**Base URL.** `https://circleback.ai/api`

**Auth.** `Authorization: Bearer cb_<secret>`

**List.** `GET /meetings` — and, like Otter, **there is no date-range parameter**. The documented
query parameters are `ownership` (`All` | `Mine` | `Shared`, default `Mine`), `statuses[]`,
`tagIds[]`, `attendeeProfileIds[]` and `cursor`. A date window means filtering client-side on
`createdAt`.

Pagination is RFC 8288: omit `cursor` on the first request, and when more exists the response
carries a `Link` header with `rel="next"`:

```
Link: </api/meetings?cursor=eyJwYWdlIjoxfQ>; rel="next"
```

Follow that URL. **The body is a bare array**, so the cursor is only in the header — an adapter
that reads the body alone can never paginate. Cursors are opaque and must not be reused with
different filters. Page size is not settable and its default is unverified.

`GET /search?searchTerm=&meetingIds[]=&tagIds[]=&attendeeProfileIds[]=&cursor=` returns the same
meeting objects filtered by full-text search.

**Transcript.** `GET /meeting/{meetingId}/transcript` — note the **singular** `meeting` in the
path while the list endpoint is plural `meetings`. Returns a bare array of
`{ speaker: string | null, text: string, timestamp: number }`, chronological, `timestamp` in
**seconds** marking the segment start. There is no end timestamp and no speaker id.

**Notes / summary.** No separate endpoint — `notes` (Markdown, nullable) is on the meeting object
itself, as is `privateNotes`, `actionItems[]` (`{ id, title, description, status: "PENDING" |
"DONE", assignee }`) and `insights`. `insights` is an unusual shape: an object **keyed by the name
of each user-created insight**, each value an array of `{ speaker, timestamp, insight }` where
`insight` is a string or an object of custom fields. You cannot know the keys ahead of time.

**Attendees.** `attendees[]` → `{ profileId, name, title, companyName, email,
isCalendarInvitee, isCalendarEventOrganizer }`. Emails are included but nullable, and are the
calendar-invitee email specifically. **No internal/external flag** — `companyName` is the closest
proxy. `isCalendarInvitee` false means the person joined without being on the invite.

**Meeting id.** `id` (string); the web URL is `https://circleback.ai/meetings/${id}`.

**Gotchas.** Rate limits are **unverified** — undocumented. `recordingUrl` is valid for 24 hours
and only exists if recording-saving is enabled in settings. The `statuses` filter is the nearest
thing to a readiness signal, but its allowed values are typed as a bare string array in the spec
and are **unverified**.
<https://circleback.ai/docs/api>

---

## Clari Copilot (formerly Wingman)

**Public API.** Yes. Key and password come from workspace settings → integrations → Clari Copilot
API. **Plan requirement is unverified.**

**Base URL.** `https://rest-api.copilot.clari.com`. The old `https://rest-api.trywingman.com`
domain is deprecated.

**Auth.** **Two custom headers, both required** — this is the only recorder here that does not use
`Authorization` at all:

```
X-Api-Key: <your_api_key>
X-Api-Password: <your_api_password>
```

**List.** `GET /calls`

| Param                                | Notes                                              |
| ------------------------------------ | -------------------------------------------------- |
| `filterTimeGt` / `filterTimeLt`      | ISO date-time, e.g. `2020-01-01T00:00:00Z`; filters on scheduled/start time |
| `filterModifiedGt` / `filterModifiedLt` | filters on last status update                   |
| `skip`                               | default 0, **max 10000**                           |
| `limit`                              | default 25, **max 100**                            |
| `filterUser[]`                       | by user email as shown in Copilot settings         |
| `filterAttendees[]`                  | by attendee email                                  |
| `filterStatus[]`, `filterType[]`, `filterTopics[]`, `filterSourceId[]` |                  |
| `filterDurationGt` / `filterDurationLt` | seconds, 0–7200                                 |
| `sortTime`, `sortProcessed`          | `asc` \| `desc`                                    |
| `includePrivate`                     | default `"false"` — a **string** enum, not boolean |
| `includeAudio`, `includeVideo`       | signed URLs, valid 4 hours                         |
| `includePagination`                  | default true                                       |

Skip/limit offset pagination, capped at 10,000 records deep. Response
`{ calls: [...], pagination: { matched, hasMore, nextPageSkip } }`. Setting
`includePagination=false` drops the `pagination` object and is documented as much faster — worth
it once you are simply walking forward with `skip`.

**Transcript.** Not on `/calls`. `GET /call-details?id=<call_id>` returns `{ call: {...} }` with a
`transcript[]` of:

```json
{ "text": "...", "start": 12.3, "end": 15.7, "personId": 4211,
  "annotations": [ { "tracker": "...", "phrase": "...", "category": "..." } ] }
```

**`personId` is an integer, not a name.** Resolve it against `users[].personId`,
`externalParticipants[].personId` or `joinedParticipants[].personId` on the same call object.
Clari's own docs say to fetch calls individually via `call-details` for transcripts — the list
endpoint will not return them.

**Notes / summary.** `summary` on the same `call-details` response:
`{ full_summary: string,
   topics_discussed: [ { name, start_timestamp, end_timestamp, summary } ],
   key_action_items: [ { action_item, speaker_name, start_timestamp, end_timestamp } ] }`.
Also `competitor_sentiments[]` (`{ competitor_name, sentiment, reasoning, personId,
turn_start_time }`) and `deal_stage_live`.

**Attendees.** Three separate arrays, and the split is the internal/external flag:
`users[]` → `{ userId, userEmail, isOrganizer, personId }` are your own team;
`externalParticipants[]` → `{ name, email, phone, personId }` were invited;
`joinedParticipants[]` → same shape, actually attended. Emails throughout.

**Meeting id.** `id` (string). `source_id` is the upstream platform's id.

**Gotchas.** Rate limits are **10 requests/second plus 100,000 requests/week**, the week resetting
Sunday 00:00 GMT — the weekly cap is unusual and worth budgeting against if you backfill.
Readiness comes from `status`, whose enum is long and mostly failure modes: `PROCESSED` and
`POST_PROCESSING_DONE` are good; `SCHEDULED`, `INITIATED`, `INPROGRESS`, `WAITING_IN_QUEUE`,
`PROCESSING` are pending; `ERROR_IN_TRANSCRIBE`, `ERROR_IN_PROCESSING`, `ERROR_IN_RECORDING`,
`UNABLE_TO_JOIN`, `CALL_DID_NOT_HAPPEN`, `IGNORED_BY_USER`, `BOTJOIN_DISABLED`, `NO_DATA_INCALL`,
`NOBODY_JOINED_CALL`, `BOTJOIN_DENIED` are terminal. Filter on it in `listReady`. Private calls
are excluded unless `includePrivate=true`.
<https://api-doc.copilot.clari.com/> · spec at
<https://api-doc.copilot.clari.com/spec.yaml>

---

## Modjo

**Public API.** Yes — v2 is current, v1 is deprecated. Creating a key needs **Administrator or
Manager** permissions (Settings → Integrations → Public API). **Plan requirement is unverified.**

**Base URL.** `https://api.modjo.ai/v2`

**A spec bug worth knowing:** Modjo's OpenAPI document declares its server as
`https://api.modjo.ai//v2` with a double slash, and repeats that in the prose. The double slash
**404s**; the single slash returns a proper `401 missing_api_key`. Generated clients will be
broken out of the box.

**Auth.** `Authorization: Bearer <api_key>`

**List.** `GET /calls`

| Param        | Notes                                                       |
| ------------ | ----------------------------------------------------------- |
| `from`       | ISO 8601 date-time                                          |
| `to`         | ISO 8601 date-time                                          |
| `page`       | 1-based, default 1                                          |
| `size`       | default 25, **max 100**                                     |
| `expand`     | comma-separated: `contacts`, `deal`, `account`, `users`     |
| `user_id`, `deal_id`, `account_id` | integers                              |

Response `{ data: [...], pagination: { page, size, total } }` — page/size, no cursor.

**`expand` swaps fields rather than adding them.** Without `expand=contacts` you get
`contactIds[]`; with it you get `contacts[]` and **`contactIds` is omitted**. Same for
`deal`/`dealId`, `account`/`accountId`, `users`/`userIds`. An adapter must handle both shapes or
always pass the same `expand`.

**Transcript.** `GET /calls/{id}/transcript` → `{ data: [ { startTime, endTime, content,
speaker: { id, name, type } } ] }`. The text field is **`content`**, not `text`.
`startTime`/`endTime` are **seconds** from call start. `speaker.type` is `user` (internal team
member), `contact` (external participant) or `unknown` — the internal/external flag lives on the
speaker, which is unusual and useful. `speaker.name` is nullable.

**It returns an empty `data` array while the call is `processing`** rather than erroring — so an
empty transcript is ambiguous between "not ready" and "nothing said", and you must check `status`
on the call to tell them apart.

**Notes / summary.** Two endpoints. `GET /calls/{id}/summaries` returns `{ data: [ { uuid,
templateUuid, templateTitle, templateLength, answer, language, createdOn, modifiedOn } ] }` — one
entry per configured summary template, and **`answer` is null when the summary has not been
generated yet**. `GET /calls/{id}/notes` returns human notes (`rawContent` is a rich-text JSON
structure, not markdown) and **only published notes**. There is also `GET /calls/{id}/next-steps`.

**Attendees.** With `expand=contacts,users`: `contacts[]` → `{ id, name, email, phoneNumber,
jobTitle }` (external), `users[]` → `{ id, email, firstName, lastName }` (internal). The array
membership is the internal/external distinction.

**Meeting id.** `id` (number) on the call object; path params accept **either** the integer id or
a UUID.

**Gotchas.** 100 requests/minute per key, with `X-RateLimit-Limit`, `X-RateLimit-Remaining` and
`X-RateLimit-Reset` (seconds until reset) on responses — note it is `X-RateLimit-Reset`, not
`Retry-After`. Data retention deletes content: `recordingRetentionStatus` and
`transcriptRetentionStatus` are each `available` or `deleted`, and a deleted resource returns
**410 Gone** with `{ "code": "gone" }`, which is distinct from 404. Error bodies are
`{ code, message }` with codes `validation_error`, `missing_api_key`, `invalid_api_key`,
`not_found`, `conflict`, `gone`, `rate_limited`, `internal_error`.
<https://api.modjo.ai/v2/docs> · spec at <https://api.modjo.ai/v2/open-api.json>

---

## Attention — not shipped

**Why not.** The transcript's field names are genuinely unknowable from the documentation.
Attention's own OpenAPI document types `attributes.transcript` as an untyped open object and the
example shows `transcript: {}`, so the segment, speaker and text keys can only be learned from a
live response with a real key. Writing this adapter from docs would mean guessing exactly the
field names whose wrong values produce a silent empty run. Everything else is documented and
straightforward, so this is a one-sitting adapter for anyone who has a key: call
`/conversations`, read what comes back, write it down here, then write it.

**Public API.** Yes. Keys are created under Settings → Organization → API Keys and require the
**Admin** role for organization-level keys. **Plan requirement is unverified.** Keys are
user-scoped or org-scoped and several endpoints require org-scoped keys explicitly.

**Base URL.** `https://api.attention.tech/v2`

**Auth.** `Authorization: Bearer <api_key>`. The OpenAPI document declares this as an `apiKey`
scheme on the `Authorization` header without stating the `Bearer` prefix, but the authentication
guide's curl, Node, Python and Go examples all send `Bearer` — follow the guide.
<https://docs.attention.com/api-authentication>

**List.** `GET /conversations`, or `GET /conversations/list` which is a faster batch-query alias
with identical filters.

| Param                                    | Notes                                          |
| ---------------------------------------- | ---------------------------------------------- |
| `fromDateTime` / `toDateTime`            | ISO 8601                                       |
| `page`                                   | 1-based                                        |
| `size`                                   | **max 50 on `/conversations/list`**; unverified on `/conversations` |
| `detailedTranscript`                     | default false                                  |
| `filter[owner.id]` / `filter[owner.email]` | arrays                                       |
| `filter[participants.email]`             | array                                          |
| `filter[team.id]`, `filter[title]`       |                                                |
| `filter[hide_internal]`                  | boolean                                        |
| `filter[hide_non_analyzed]`              | boolean (replaces deprecated `filter[analyzed]`) |
| `filter[hide_pending]`, `filter[hide_transcript]`, `filter[hide_failed]` | boolean        |
| `filter[include_internal_participants]`  | boolean                                        |
| `filter[crm_field.*]`, `filter[external_opportunity.id]` |                                |

The bracketed filter names are literal, including the brackets — encode them, do not translate
them to dots. Response is JSON:API-shaped:
`{ data: [ { type: "conversations", id, attributes: {...} } ], meta: { pageCount, totalRecords,
pageNumber, pageSize }, links: { self, related } }`.

`/conversations/list` differs in two ways: it omits `extractedIntelligence` and
`confirmedExtractedIntelligence` unless you pass `withCrmRecords=true`, and it does **not** exclude
empty conversations.

**Transcript.** There is no transcript endpoint. `attributes.transcript` arrives on the
conversation from `/conversations`, `/conversations/list` and `GET /conversations/{id}`, and
`detailedTranscript=true` asks for the fuller form.

**The transcript object is untyped in the specification** — `{ type: "object",
additionalProperties: true }` — and the documented example shows `transcript: {}`. Segment,
speaker and text field names are therefore **unverified from documentation**. Attention's own
guidance amounts to inspecting a live response. Do not guess these; call the API with a real key
and read what comes back before writing the adapter.

**Notes / summary.** No dedicated summary field. The AI-derived material is
`attributes.extractedIntelligence` and `attributes.confirmedExtractedIntelligence`, both objects
**keyed by insight name** with values `{ id, key, value, title, category, refreshing, options,
source, scope_insight }`. Also `attributes.scorecardResults[]` (`{ uuid, title, summary, items }`)
and `attributes.boards[]`.

**Attendees.** `attributes.participants[]` and `attributes.attendees[]`, both
`{ id, email, organizer, name, status }`. Emails included, `organizer` is a boolean. **No
per-participant internal/external flag**, but `attributes.isInternal` flags the conversation and
`filter[hide_internal]` / `filter[include_internal_participants]` control it at query time.

**Meeting id.** Two: `data[].id` (JSON:API resource id) and `attributes.uuid`. There is also
`GET /conversations/by-external-id/{externalId}` for imported calls.

**Gotchas.** Rate limits exist and return 429, but **no number is published** — Attention says to
contact your account manager for increases. Readiness comes from `attributes.transcriptStatus`
(example value `completed`), alongside `videoStatus` and `mediaStorageStatus`
(`PENDING` | `UNAVAILABLE` | `IMPORTING` | `READY`) and `importStatus`
(`NONE` | `PENDING` | `IN_PROGRESS` | `FINISHED` | `DISCARDED` | `FAILED`). The `filter[hide_*]`
family is the cheap way to do readiness filtering server-side.
<https://docs.attention.com/api-reference/conversation/list-conversations> ·
<https://docs.attention.com/openapi.json>

---

## What this changes about writing an adapter

Three patterns cut across the fourteen and are worth deciding once, which the shipped adapters
already have — read one of them rather than re-deciding.

**Speaker attribution is usually a join, not a field.** Avoma (`speaker_id`), Gong (`speakerId`),
Clari Copilot (`personId`), Grain (`participant_id`) and Modjo (`speaker.id`) all return an
identifier where you want a name. For Avoma, Grain and Modjo the mapping arrives with the
transcript; for Gong and Clari it lives on the *call* object, so a transcript fetched without a
prior list is unattributable text and the adapter keeps what the list told it. Granola, Fathom,
Fireflies, tl;dv and Circleback hand you a name directly.

**Internal versus external is only flagged by five of them.** Gong (`parties[].affiliation`),
Fathom (`calendar_invitees[].is_external`), Grain (`participants[].scope`), Zoom
(`participants[].internal_user`) and Modjo (by array membership, and on `speaker.type`) tell you
directly. The other nine do not, and Avoma's flag is actively wrong in some workspaces — which is
why the pipeline derives it from attendee email domains against the `INTERNAL_DOMAIN` in
`config.ts`, why the rule stays in `recorder.ts`, and why the adapters that DO have a flag
deliberately ignore it. One
rule for every recorder is what keeps the same call from reading as internal on one and external on
the next.

**Readiness is spelt eight ways or not at all.** Avoma gives you two flags that are absent rather
than false, Fireflies a clean enum, Clari a status with fourteen values, Otter three per-artefact
nulls; Modjo makes you correlate an empty array with a status field, Zoom makes you look for a file
type, and Granola, Fathom, Gong, Grain, tl;dv and Circleback give you nothing. This is the whole
reason `listReady` owns the filter and speaks the recorder's own vocabulary — and where a recorder
says nothing, returning the window whole and letting `transcript()` answer null is the shipped
answer, because the collector's window overlaps the previous run precisely so that tomorrow is the
retry.
