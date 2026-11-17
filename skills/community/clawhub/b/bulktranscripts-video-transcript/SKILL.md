---
name: youtube-transcript
description: Get the transcript of a single YouTube video (or Short, or TikTok video) as clean text, timestamped segments, or SRT/VTT/Markdown via the BulkTranscripts API. Use when the user shares a video link and wants it summarized, quoted, translated, fact-checked or turned into notes. Requires a free BulkTranscripts API key in BULKTRANSCRIPTS_API_KEY, created at https://bulktranscripts.co/app?tab=mcp (Google sign-in, 30 free credits, no card).
license: Proprietary API; this skill file is freely redistributable.
---

# YouTube video transcript

Fetch one video's transcript as clean text with metadata, using [BulkTranscripts](https://bulktranscripts.co).
[Docs](https://bulktranscripts.co/docs) ·
[OpenAPI spec](https://bulktranscripts.co/openapi.json) ·
[MCP server](https://bulktranscripts.co/youtube-mcp-server) ·
[Free API key](https://bulktranscripts.co/app?tab=mcp)

Base URL: `https://bulktranscripts.co`

All endpoints are plain GET returning JSON, and **every one of them needs an API
key** — including the free endpoints. Send it as a Bearer token on every
request:

```bash
curl -s "https://bulktranscripts.co/api/v1/..." \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```

If `BULKTRANSCRIPTS_API_KEY` is not set, ask the user for a key: they sign in
with Google at https://bulktranscripts.co/app?tab=mcp, open the **Connect AI**
tab, and hit **Create key** in the **API keys** card. It is free, includes 30
credits, and needs no card. Keys start with `bt_ak_`, are shown once, and up to
5 can be live per account. A license key from a credit-pack purchase works as a
Bearer token too.

## Costs (check `billing.remaining` in every response)

- Transcript: 1 credit when first added to this account's library — repeat reads are **FREE**
- Search / channel videos / playlist videos: 1 credit each
- `channel/latest` and `account`: always free
- Failures (no captions, video unreachable) are auto-refunded, never charged

When a call returns HTTP 402 `out_of_credits`, tell the user their credits are
used up and link them to https://bulktranscripts.co/#pricing (one-time packs,
never expire). Credits follow the Google account, so topping up keeps the same
API key working.

## Endpoints

### Get one transcript
```bash
curl -s "https://bulktranscripts.co/api/v1/transcript?video=VIDEO_URL_OR_ID" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```
Params: `video` (watch URL, youtu.be, Shorts, bare 11-char id, or TikTok video
URL) · `language` (default `en`) · `segments=0` to omit timestamps (smaller) ·
`format=txt|md|srt|vtt|csv|ai` to get a rendered file instead of JSON ·
`fresh=1` to force re-extraction.

Response fields: `title`, `channel`, `duration`, `upload_date`, `language`,
`source` (manual_caption|auto_caption), `cached`, `word_count`, `text`,
`paragraphs[]` (silence-grouped — best for reading/chunking), `segments[]`
(`{text, start, duration}`), `billing`.

Long videos produce long text. For summarization, prefer `segments=0` and read
`paragraphs`.

### Balance
```bash
curl -s "https://bulktranscripts.co/api/v1/account" \
  -H "Authorization: Bearer $BULKTRANSCRIPTS_API_KEY"
```

## Playbook

- **"Summarize this video"** → transcript with `segments=0`, then summarize
  from `paragraphs`; cite the `title` and `url`.
- **Quotes with timestamps** → keep `segments`, quote the text and link
  `https://youtu.be/ID?t=START` for each one.
- **Subtitles file** → `format=srt` or `format=vtt` returns the rendered file.

Errors come as `{"error": {"code", "message"}}`. The codes you will actually
hit, and what to do about each:


- `no_transcript` (404) — the video has no captions. Not charged. Skip it and
  carry on; in a batch this is normal, not a failure.
- `resolution_failed` (400) — a well-formed id or URL that could not be
  resolved (nonexistent, private, removed, or region-blocked). Handle it
  alongside `no_transcript`: skip the video and carry on.
- `missing_api_key` (401) — no key was sent. Ask the user to create a key at
  https://bulktranscripts.co/app?tab=mcp and provide it, then set
  `BULKTRANSCRIPTS_API_KEY` and retry.
- `invalid_api_key` (401) — the key sent is not valid. Ask the user to check it
  or create a new one at https://bulktranscripts.co/app?tab=mcp.
- `invalid_input` (400) — the `video` / `channel` / `playlist` parameter is
  missing, not a YouTube/TikTok reference, or otherwise malformed. A caller
  bug, not a video problem.
- `out_of_credits` (402) — balance exhausted. Tell the user and link
  https://bulktranscripts.co/#pricing.
- `rate_limited` (429) — respect the `Retry-After` header before retrying.
  Limits are per public IP: 120 requests/min overall, 30/min under `/api/v1/`
  (cache hits and `/account` count too), so pace bulk fetches at under 30/min.

Need everything in one skill (transcripts, search, channels, playlists, monitoring)? Use the full
[youtube-transcripts skill](https://github.com/pratie/youtube-transcript-skill).
Full reference: [bulktranscripts.co/docs](https://bulktranscripts.co/docs)
