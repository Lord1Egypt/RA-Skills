---
name: clipwright
description: "Make short videos through Clipwright's MCP server: an AI actor speaking your script, or a faceless video of up to 90 seconds with narration over generated scenes. Quote first for free, then start a run and collect the MP4. Clipwright returns the file and does not publish anywhere."
metadata:
  openclaw:
    emoji: "🎬"
    os: [darwin, linux, win32]
    requires:
      bins: [node, npx]
      env: [CLIPWRIGHT_API_KEY, CLIPWRIGHT_CLIENT_ID]
author: Clipwright
homepage: https://clipwright.io/?ref=clawhub
---

# SKILL.md — install `clipwright-mcp`, then make a video

This file is for an agent. It holds what the tool schemas cannot tell you: the
places where a call answers without an error and the answer is still wrong for
the user. Each such trap carries the date it was last checked.

Everything else is reference, kept in one place so it does not go stale here:

- the tool schemas (`tools/list`): every field, its limits and defaults;
- https://clipwright.io/docs: the REST API, refusal codes and prices;
- https://api.clipwright.io/openapi.json: the REST contract as OpenAPI 3.1;
- https://clipwright.io/changelog: read its **Breaking:** entries before you
  move to a newer version.

The client packages `@clipwright/core`, `@clipwright/sdk`,
`@clipwright/mcp-server` and `@clipwright/cli` are MIT; the service is closed.

# Part 1 — Install

## 0. Start here: check the connection, then lead the setup

Run this each time the skill starts, before anything else. Speak the user's
language. Each step is one short message with concrete actions, then a check
you run yourself.

1. **Check.** If a Clipwright `get_account` tool is listed (in Claude Code,
   `mcp__clipwright__get_account` or under the connector's own name), call it.
   It is free. An answer with `balance_credits` means Clipwright is connected:
   tell the user the balance in one line. Then check that `quote_trends`,
   `find_trends`, `list_moves` and `describe_tool` are listed too: the server
   lists all four, so a list without them is an old copy the client keeps.
   Tell the user to refresh the app in the client's settings (in ChatGPT: the
   app's page → Manage → Refresh tools), start a new chat and repeat the request
   there; turning the app off and on keeps the old copy, and with no refresh,
   removing the app and adding it again does. A local server: restart it,
   since `@latest` fetches the current package. Never tell the user Clipwright
   lacks a tool your list lacks; https://clipwright.io/mcp lists every tool.
   A user who will not refresh gets step 6 from their own reel (6.3) or their
   own script. With the full list, go to step 6. No `get_account`, or any
   other answer: steps 2 to 5. Do not probe the endpoints yourself.
2. **Gate.** Until `get_account` answers with a balance, make nothing: no
   script, no paid call, no workaround through another service or a local
   render. Remember what the user asked for and do it after step 6. To any
   request, say in two lines why Clipwright is needed (it renders the video on
   its servers and prices every video free before anything is spent), then
   give the next step.
3. **Account.** Ask whether the user has a Clipwright account. If not, they
   sign up at https://app.clipwright.io/auth/sign-up with an email and confirm
   it from the email. A new account opens at once with trial credits and needs
   no card. With an account, go on to step 4.
4. **Connect.** Pick one way by where you run. The hosted server is the
   default: the user signs in in the browser, so no key goes on disk or into
   the chat.
   - **Claude Code:** `claude mcp add --scope user --transport http clipwright https://mcp.clipwright.io/mcp`
     (`--scope user` makes it available in every project). With a shell you
     may run it yourself after the user agrees. Then the user types `/mcp` in a
     session, picks `clipwright` and signs in; the browser asks them to approve
     the app. A `clipwright` server that is already registered and failing is
     removed first: `claude mcp remove clipwright`.
   - **Claude.ai or Claude Desktop:** Customize → Connectors → Add custom
     connector, paste `https://mcp.clipwright.io/mcp`, connect and sign in.
   - **ChatGPT, on the web:** https://chatgpt.com/plugins → the plus button →
     Add custom MCP server → Server URL `https://mcp.clipwright.io/mcp`,
     authentication OAuth → "I understand and want to continue" → Create as a
     plugin. Install the plugin, then in a new chat type `@`, pick it and
     repeat the request: a new chat does not carry the old one. ChatGPT
     asks the user to confirm each tool that is not marked read-only; quotes
     and reads are. That confirmation is not the go-ahead on a price: show
     the quote and wait for the user's word first. No "Add custom MCP server" means the plan or the workspace
     does not allow custom servers: use Claude or a local agent instead.
   - **Other clients:** the table in section 1.1.
   - **A key instead of a sign-in** (a local server, CI, scripts): the user
     issues a key at https://app.clipwright.io/api-keys, where it is shown
     once, and puts it in the MCP server's environment as `CLIPWRIGHT_API_KEY`
     (section 1.3). Never ask them to paste the key into the chat.
   - **No browser on this machine:** the device code in section 1.4.
5. **Restart.** Most hosts load a new server only on a restart or in a new
   chat. Say: "Restart, then repeat your request: I will check the
   connection." Then step 1 again. Read its outcome:
   - **No Clipwright tools:** the server is not registered, or the local
     server exited. It exits with `CLIPWRIGHT_API_KEY env var is required`
     when the key did not reach its environment. In Claude Code, `/mcp` shows
     each server and its state.
   - **`get_account` answers `code: "unauthorized"`:** the key is mistyped or
     revoked, or the sign-in ended. Follow its `next_action`. Nothing was
     charged.
   - **The hosted server answers HTTP 401 before any tool runs:** the sign-in
     is not finished. Sign in again from the client (`/mcp` in Claude Code).
6. **Connected.** Say what the user gained in one line, with the balance from
   `get_account`. Then start from what works: lead the remembered request, or
   a new one, through reels that already took off. Every paid call waits for
   the user's go-ahead on its free quote (section 3).
   1. Ask the topic in a few words, unless the user named it or saved a main
      niche (`trend_niches`, free): then search that one, no keywords needed,
      and offer to save a topic the user names often. Quote it with
      `quote_trends`, show the price and wait for the go-ahead. Then run
      `find_trends`; while it is unfinished, call `get_trend_search` (free)
      with its `poll.arguments` until it succeeds.
   2. Show 3 to 5 reels that took off, with views and `x_median`. When few are
      on topic, try two or three other wordings, each quoted again.
   3. The user picks one, or brings their own reel and starts here. Quote the
      breakdown with `quote_analysis`, wait for the go-ahead, run
      `analyze_reference` and read it with `get_reference_analysis`.
   4. Write the user's script on the reel's mechanic (hook, structure,
      pacing), never its words. Compile it with `plan_reference_remake`, which
      is free, and show the script for approval. Only the approved revision is
      quoted and run.

   A user who declines the trends and asks for a video from their own script
   goes straight to that video's quote.

## 1. Connect

The hosted server and this package run locally serve the same tools.

### 1.1 The hosted server — nothing to install

Add `https://mcp.clipwright.io/mcp` (Streamable HTTP) to the client. On first
use the client opens a browser; the account holder signs in and approves the app.

| Client | How to add | Checked |
|---|---|---|
| Claude Code | `claude mcp add --transport http clipwright https://mcp.clipwright.io/mcp`, then `/mcp` in a session to sign in | verified live 2026-10-18 |
| Claude.ai, Claude Desktop | Customize → Connectors → Add custom connector, paste the URL | from the client's docs |
| ChatGPT | on the web: chatgpt.com/plugins → + → Add custom MCP server, the URL, OAuth → Create as a plugin, then install it | from the client's docs, 2026-11-09 |
| Cursor | `~/.cursor/mcp.json`: `{"mcpServers": {"clipwright": {"url": "https://mcp.clipwright.io/mcp"}}}` | from the client's docs |
| VS Code | `.mcp.json`: `{"mcpServers": {"clipwright": {"type": "http", "url": "https://mcp.clipwright.io/mcp"}}}` | from the client's docs |
| Gemini CLI | `gemini mcp add --transport http clipwright https://mcp.clipwright.io/mcp`, then `/mcp auth clipwright` | from the client's docs |
| Codex | `codex mcp add clipwright --url https://mcp.clipwright.io/mcp`, then `codex mcp login clipwright` | from the client's docs |

For CI and scripts, a `cw_*` key replaces OAuth and holds both permissions:

```bash
claude mcp add --transport http clipwright https://mcp.clipwright.io/mcp --header "Authorization: Bearer cw_..."
```

What differs on the hosted server is in section 1.4.

### 1.2 The local server from npm

```bash
npx -y -p @clipwright/mcp-server@latest clipwright-mcp
```

A healthy server does not exit: it prints `clipwright mcp server running on
stdio` to stderr and waits for JSON-RPC. Exiting at once with
`CLIPWRIGHT_API_KEY env var is required` means the key did not reach it, not a
broken build. Both answers verified 2026-10-31. `@latest` is deliberate: it
keeps the client in step with the API.

From a source checkout: `pnpm install && pnpm build` at the root, then run
`node packages/mcp-server/dist/index.js` with the same environment.

### 1.3 Connecting it to an MCP host

Generate `CLIPWRIGHT_CLIENT_ID` BEFORE the first run (section 2):

```json
{
  "mcpServers": {
    "clipwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "-p", "@clipwright/mcp-server@latest", "clipwright-mcp"],
      "env": {
        "CLIPWRIGHT_API_KEY": "cw_...",
        "CLIPWRIGHT_CLIENT_ID": "<a unique value, section 2>"
      }
    }
  }
}
```

As one command:

```bash
claude mcp add clipwright \
  -e CLIPWRIGHT_API_KEY=cw_... \
  -e CLIPWRIGHT_CLIENT_ID="$(node -e "console.log(crypto.randomUUID().replaceAll('-',''))")" \
  -- npx -y -p @clipwright/mcp-server@latest clipwright-mcp
```

For a source build, the command is `node` with the absolute path to
`packages/mcp-server/dist/index.js`.

| Variable | Required | Meaning |
|---|---|---|
| `CLIPWRIGHT_API_KEY` | YES | A `cw_*` key issued on your account at https://app.clipwright.io/api-keys. It is yours: a second person gets an account and a key of their own. Several keys on one account share its runs, balance and idempotency. |
| `CLIPWRIGHT_CLIENT_ID` | YES | This installation's own identifier, section 2. |
| `CLIPWRIGHT_API_URL` | no | Defaults to `https://api.clipwright.io`; set it only for another environment. |

After a restart, confirm that `tools/list`
returns at least these 61 tools: `make_ugc`, `get_run`, `get_run_shots`, `delete_run_media`, `quote_revision`, `revise_run`, `quote_candidate`, `create_candidate`,
`list_generation_models`, `quote_image`, `generate_image`, `quote_video`, `generate_video`, `quote_upscale`, `upscale`, `quote_ugc`, `list_actors`,
`list_voices`, `list_template_sounds`, `list_moves`, `upload_image`, `create_upload`, `get_upload`, `delete_upload`, `create_asset`, `list_assets`, `get_asset`, `update_asset`,
`delete_asset`, `quote_analysis`, `analyze_reference`, `get_reference_analysis`, `quote_creator_profile`, `analyze_creator`,
`get_creator_profile`, `delete_creator_profile`, `quote_trends`, `find_trends`, `get_trend_search`, `trend_niches`, `get_account`, `list_prices`, `create_actor`, `quote_actor`, `delete_actor`, `get_actor_defaults`,
`set_actor_defaults`, `extract_brand`, `brand_kit`, `quote_faceless`, `make_faceless`, `list_workflows`, `get_workflow`, `prepare_workflow_plan`,
`plan_reference_remake`, `get_workflow_plan`, `approve_workflow_plan`, `quote_workflow_plan`, `run_workflow_plan`, `send_feedback`,
`describe_tool`. An account offered the tools for making a film, an ad or a
faceless cut yourself sees those as well, up to 93 tools in all. A tool missing
from this list means the client keeps an old copy of the list (section 0, step 1). Then call `get_account` (free) and read its outcome as in
section 0, step 5.

The tool list gives each tool and field in short. Before the first use of a
tool or field, read its full guidance with `describe_tool` (free), for example
`describe_tool({tool: "quote_ugc", field: "templates"})`.

When no tool does the job, or an answer is confusing or wrong, file it with
`send_feedback` (free) instead of rephrasing the request and giving up.

### 1.4 What differs on the hosted server

- **Permissions.** `mcp:read` covers the tools marked `readOnlyHint: true`,
  every quote included; `mcp:write` covers every other tool. A connection
  without `mcp:write` that calls one gets HTTP `403` with
  `error: "insufficient_scope"`; nothing is charged. Reconnect and approve spending.
- **Files.** The hosted server cannot read the agent's disk, so `upload_image`
  refuses a `path` there. Pass a public https `url`, or call `create_upload`,
  PUT the file to its `put_url` and confirm with `get_upload`.
- **Idempotency.** Each connected app and each `cw_*` key is its own client
  identity, so section 2 does not apply. A repeated request within one
  connection returns the same run.
- **Sign-in.** A connection lasts 90 days from approval and use does not extend
  it; access tokens last an hour and clients renew them. The account holder
  revokes an app at https://app.clipwright.io/api-keys, under Connected apps.
- **Endpoint errors.** No token, or a revoked or unknown one: `401` with a
  `WWW-Authenticate` header the client follows to sign in. `GET /mcp`: `405`. A
  body over 1 MB: `413`.

**An agent with no browser** signs in with a device code (verified live
2026-10-18). Only the client id `clipwright-agent` may use this flow:

```bash
curl -s https://mcp.clipwright.io/device/auth -d client_id=clipwright-agent \
  --data-urlencode "scope=mcp:read mcp:write offline_access" \
  --data-urlencode "resource=https://mcp.clipwright.io/mcp"
```

Show the person `user_code` and `verification_uri`; they approve on any device
if the code matches. Meanwhile poll `POST https://mcp.clipwright.io/token` with
`grant_type=urn:ietf:params:oauth:grant-type:device_code`, `device_code` and
`client_id=clipwright-agent`, no more often than every 5 seconds
(`authorization_pending` until approval, `slow_down` when too fast). Send
`access_token` as `Authorization: Bearer`. Renew with
`grant_type=refresh_token`; each renewal returns a new refresh token, keep the newest.

## 2. `CLIPWRIGHT_CLIENT_ID` — required, and WHY

This section is about the local server; the hosted server takes the identity
from the connection (section 1.4).

**Rule: EVERY installation gets its OWN unique `CLIPWRIGHT_CLIENT_ID` BEFORE the
first paid call.** Do not copy it from another machine and do not leave it to chance.

### Why this is not optional

The idempotency key the SDK stamps on every paid call is derived from **the hash
of the input** and **the client identity**. The server deduplicates on that key:
a repeated key returns 200 with the run **created by the first request**, and no
new paid render starts. That is right when the same user retries.

Collapsing requires BOTH to match: the account and the `clientId`.

- **The account separates by construction.** The server matches a key only
  within your account (its `account_id`). A separate token does not by itself
  mean a separate account: several live tokens on one account share one
  idempotency axis, and only the service knows which account a token is on.
- **`clientId` separates within one account.** Without the variable it comes
  from `~/.clipwright/client-id`, born random on first run. It matches only when
  made to match: a shared `HOME`, a copied value, an image cloned with the file.

With one account AND one `clientId`, a request whose input matches an earlier
one (both people copied the same sample) returns 200, a `run_id` and a playable
link to the video rendered for the FIRST person. Nothing errors, and no render
ran for the second.

### How to set it

Set it explicitly in the host environment (section 1.3). Generate it with Node,
not `uuidgen`: on a bare image without `uuidgen` the shell silently substitutes
an empty string and switches the protection off.

```bash
node -e "console.log(crypto.randomUUID().replaceAll('-',''))"
```

Without the variable and with a read-only `HOME`, the server still starts:
`tools/list`, `quote_ugc`, `get_run` and `list_voices` work; paid calls, uploads
and new assets refuse, naming the variable. Set it; do not reinstall.

# Part 2 — Make a video

## 3. CALL ORDER — quote first, paid call second

```
quote_ugc  →  read source / resolved_aspect_ratio / warnings  →  make_ugc  →  get_run (polling)
```

Every paid tool has a free quote that reserves nothing. Show the user the
credits and start the paid call only after they agree. Take prices from the
quote or `list_prices`, never from memory or this page: they change.

| What | Free quote | Paid call | Poll with | The result |
|---|---|---|---|---|
| UGC video with a presenter | `quote_ugc` | `make_ugc` | `get_run` | `video_url` |
| Faceless video | `quote_faceless` | `make_faceless` | `get_run` | `video_url` |
| One image / one silent clip | `quote_image` / `quote_video` | `generate_image` / `generate_video` | `get_run` | `generation.url` |
| A personal actor | `quote_actor` | `create_actor` | `get_run` | `created_actor.actor_id` |
| A reading of a reference reel | `quote_analysis` | `analyze_reference` | `get_reference_analysis` | `reference_profile` or `data` |
| A creator's latest 12 videos with x to their median | `quote_creator_profile` | `analyze_creator` | `get_creator_profile` | `profile` |
| Reels that took off on a topic | `quote_trends` | `find_trends` | `get_trend_search` | `result.reels` |
| A revision of a faceless video | `quote_revision` | `revise_run` | `get_run` | `video_url` |
| A new picture or clip for one shot | `quote_candidate` | `create_candidate` | `get_run` | `candidate.preview_url` |
| A plan from a workflow method | `quote_workflow_plan` | `run_workflow_plan` | `get_run` | `workflow` |

- The paid call returns a `run_id` at once and does not wait. Poll every 5–10
  seconds until `state` is `succeeded` or `failed`. Do not tell the user the
  video is ready before you hold its link.
- Read `warnings[]` on the first answer, on each poll and on the terminal one.
  What the service could not honor is announced there, not refused (section 4).
- A key the contract does not have (`aspectRatio`) is refused with 400
  `unknown_field`, and the message names the right spelling. The removed fields
  `character`, `webhook_url`, `broll_url` and `disclosure_overlay` are refused by
  name with the replacement: `actor_id`, polling `get_run`, nothing, and the
  `ai_disclosure` of the finished run. Nothing is charged.
- Before choosing a model for an image or a clip, call `list_generation_models`;
  any other combination is `unsupported_combination` before any charge.
- A workflow launch needs the quote's revision, content digest, semantic input
  digest and quote id, plus an explicit idempotency key, and the quote expires
  five minutes after it is issued. Checked 2026-10-31.

### `quote_ugc` — free

Its price fields for a 12-second script with `presenter_engine: "avatar_iv"`:

```json
{
  "skill": "make_ugc",
  "credits_estimate": 132,
  "duration_estimate_sec": 12,
  "tariff": "parts-v5",
  "price_lines": [
    { "label": "presenter, HeyGen Avatar IV", "unit": "face_second", "quantity": 12, "unit_credits": 10, "credits": 120 },
    { "label": "production (voice and render)", "unit": "second", "quantity": 12, "unit_credits": 1, "credits": 12 }
  ],
  "minimum_credits": 50,
  "warnings": []
}
```

The presenter model is `presenter_engine`: `avatar6_turbo` (HeyGen Avatar 6
Turbo, the default of a 9:16 video whose image is 9:16) or `avatar_iv`
(HeyGen Avatar IV), each at its own presenter-second price in `price_lines`.
A long video with inserts or segments renders on Turbo too, unless it has a
call, an interview, `presenter_gaze` or a talking shot, or one presenter take
longer than 36 seconds. Any other video renders on `avatar_iv`; an asked
`avatar6_turbo` it cannot honour says why in `warnings[]`.

Also read `source`, `actor`, `resolved_aspect_ratio` (what will ACTUALLY be
rendered) and `tts_model`. The quote and the run share one verdict: a 400 on the
quote is the same 400 on the run, and a money or access refusal the run would
meet is named in the quote's `warnings[]`. The free curl form is in section 7.

## 4. Traps: a wrong answer without an error

### Silent: the answer looks right and is not

**An omitted `aspect_ratio` follows the source, not 9:16.** With `image`, the
video takes the supported format nearest the photo: a 1600×900 photo gives a
16:9 video, and the format draws no warning. Only the default actor is always
9:16. Pass `aspect_ratio` whenever you pass `image`. Checked live 2026-10-31.

**A format up to 15% away from the source is snapped, not refused.** The frame
is padded with white bars or center-cropped at the sides, and `warnings[]` says
which; within 2% there is no warning. Over 15% on an explicit `aspect_ratio` is
400 `aspect_conflict` before any charge, so `1:1` on the default actor is refused.
A photo that could not be measured renders as requested, or 9:16, with a warning
that the format was not verified. Checked 2026-10-31.

**`person`, `name` and `look` change nothing.** They are accepted and quoted; the
default actor renders, and only `warnings[]` says so. The `character` refusal
suggests `person`, which still chooses no face. Choose one with `actor_id` from
`list_actors`, an `image`, or a new actor from `create_actor`. Checked live 2026-10-31.

**`make_ugc` and `make_faceless` both draw captions unless told not to.** In
`make_ugc` the house edit style adds word-timed `hormozi` captions, marks a few
key words (a number, the offer, the product name or the call to action) and adds
a sound on cuts when the video cuts. A video of `segments` gets no captions.
`edit_style: "bare"` turns all of it off; `captions: false` turns off only the
captions. Any caption field you pass wins over the style. The quote names what the
style set in `edit_style_applied`. `make_faceless` draws captions unless
`captions: false`. It takes only `captions`: the style, emphasis and mode fields
below are `make_ugc` fields, and `make_faceless` refuses them. Whether a video has
captions is the user's call:

1. **Ask whether they want captions** before the quote. If they say no, pass
   `captions: false`, or `edit_style: "bare"` for a video with no added edits.
2. **If yes, pick a style with them.** From a reference video take its look:
   bold uppercase cues with one coloured keyword is `hormozi`, one or two words
   popping in colour is `tiktok`, a sentence on a dark box is `youtube` or
   `lecture`. Otherwise offer three or four styles that fit the video, one line
   each, and link https://clipwright.io/captions. Without a choice the server draws `hormozi`.
3. **Mark key words with `caption_emphasis`**: quotes from `script` drawn larger
   or in the accent colour; `caption_mode: "highlights"` captions only around them.
   Your list replaces the words the style would pick.

The styles: `hormozi` (the default), `accent`, `tiktok`, `youtube`, `instagram`,
`minimalist`, `neon`, `genz`, `campfire`, `midnight`, `plottwist`, `headline`,
`promo`, `lecture`, `highlighter`, `studio`, `broadcast`, `arcade`, `clutch`,
`bubblegum`, `crayon`, `lyrics`, `bassdrop`, `punch`; `minimal` is an older name
for `minimalist`. Quote each style's description from `caption_style` in
`tools/list`, not from memory. `captions: true` is refused with `gemini-3.8-flash-tts`,
which returns no word timings. Checked 2026-10-31. With that model the house style
leaves its captions out and says so in `warnings[]`.

**`make_faceless` without `voice` narrates in English.** The default
(`narrator_en_wise_lady`) reads a Russian or Spanish script with an English accent,
and `warnings[]` stays empty: the language warning fires only for a voice you
named. Pick a voice in the narration's language from `list_voices` with
`skill: "make_faceless"`. Without `skill`, `list_voices` lists only `make_ugc`
voices, and `make_faceless` refuses those. A brief is narrated in its own
language unless it asks for another. Checked live 2026-10-31.

**A photo's gender is not detected.** With `image` and neither `actor_gender`
nor `voice`, the male voice `george` speaks and `warnings[]` says so. Pass
`actor_gender` or a `voice`. With `actor_id` the voice follows the actor's gender.
Checked 2026-10-31.

**Pick the presenter before the quote.** With no `image`, `actor_id` or
`actor_gender`, the default presenter is a man, and `warnings[]` says so. When
the script speaks as a woman, pass `actor_gender: "female"` (that gender's
catalog actor, named in `warnings[]`) or an `actor_id` from `list_actors`.

**A shot with no `product` takes its setup's placement.** Shots of one setup
share one picture, so a `talking_action` or `action` shot that names no product
shows it where another shot of the same setup names it, and `warnings[]` names
those shots. Two different placements in one setup are refused.

**`voice_pace` does nothing on `eleven_v4`, the default model of presets and
catalog voices.** The voice speaks at its own pace, and the run's `warnings[]`
says so; the quote does not. To change pace, pick a voice by `words_per_second`
in `list_voices`. Checked 2026-10-31.

**`eleven_v3` is spoken as `eleven_v4`, and break tags give no pause** on
`eleven_v4` and `gemini-3.8-flash-tts`: `<break time="1.5s" />` is cut from the
text. `warnings[]` names both. A script of nothing but break tags is refused.
Checked 2026-10-31.

**Russian stress is written, not retried.** On `eleven_v4` and
`gemini-3.8-flash-tts` a capital vowel inside a lowercase word marks stress:
`потОм`. A capital that starts a word, an all-caps word, or a word with a second
capital stays as written. The 2.5 models misread the mark and warn on Cyrillic.
A retry never fixes stress; only the text does. Checked 2026-10-31.

**`make_faceless` `duration_seconds` is a target, not a length.** The video ends
with its narration and runs at least 25 seconds. It usually ends within a
quarter past the selection and 90 seconds. A longer narration runs to its end,
and the charge never exceeds the quote. A video more than 5 seconds past the
selection names both lengths in `warnings[]`. A
script whose estimated length is under 21 seconds or over the selection plus 5
is refused before any charge; the message names the window, the code is the
broader `unusable_source`. Checked live 2026-10-31.

**A `make_ugc` quote is an estimate; a `make_faceless` quote is a ceiling.**
`make_ugc` charges the measured duration rounded up to whole seconds, which can
exceed `credits_estimate`. `make_faceless` charges the delivered length and never
more than its quote. Read `credits_charged` on the finished run: it is `null`
until the run settles, while `credits_reserved` holds the reserve. Checked 2026-10-31.

**An explainer film is one you write yourself.** Start with `get_film_guide`
(free): it names each step and its tool, and every paid part (voice, hero
poses, stills, render) is quoted before it is made. `make_faceless` refuses
`format: "explainer"` and `tier` before any charge.

**The price field has a different name in each quote.** `credits_estimate` in
`quote_ugc`, `quote_actor` and `quote_analysis`; `credits` in `quote_image`,
`quote_video` and `quote_candidate`; `totalCredits` in `quote_faceless`;
`billing.total_credits` in `quote_revision`. A missing field is a wrong name, not
a free call. Checked live 2026-10-31.

**The same input after a failure returns the same failed run.** A repeated paid
call with the same input and the same `attempt` answers 200 with the earlier run,
terminal failure included, and starts nothing. It is not a permanent refusal: to
try again, raise `attempt` (section 5). `create_candidate` takes `take` instead.
Checked 2026-10-31.

**`failed` is not always final.** Rarely, a run that ended `failed` is reopened
when its video arrives late: `get_run` shows `queued` with a warning, then
`succeeded` with a link and a charge for the delivered video, and `warnings[]`
names the recovery. A retry started meanwhile is a second video and a second
charge. Before reporting a failure as final, read the run once more. Checked 2026-10-31.

**A new Idempotency-Key on the same input is a second paid run.** Over REST the
key is the only thing that collapses a repeat; the server does not compare inputs
across keys. After an uncertain answer (a timeout, `429`, `5xx`), resend with THE
SAME key. The same key with a different body is 409 `idempotency_key_reused`.
Checked 2026-10-31.

**A `succeeded` faceless run can carry a remark from the delivery check** in
`warnings[]`: captions or a scene change it could not confirm at a given second,
or that the check did not run. The video is delivered and charged. Read the
remark to the user and let them watch before they publish. Checked 2026-10-31.

### Errors whose shape hides the cause

**`curl -I` on `video_url` answers 403.** The link is signed for GET only. Check
it with a ranged GET (`curl -r 0-0`). Each `get_run` signs a fresh link valid for
seven days; never store it. Preview links of voices, actors and shots expire too:
call the tool again. Checked 2026-10-31.

**A raw `voice_id` the account does not have passes the quote and fails the run.**
It is checked at the start of the run, before any paid call, so the failure costs
nothing; a `voice_id` the account has is spoken. A `voice`
name from `list_voices` is checked at the quote. Checked 2026-10-31.

**`planned: false` from `get_run_shots` is an answer.** `editable.state` and
`editable.reason` say why the run has no shots to show; tell the user, do not
retry. A field named in `withheld` is null on every shot: "not shown", not
"missing". Checked 2026-10-31.

**A reference reel is polled with `get_reference_analysis`, not `get_run`.** Pass
an Instagram or TikTok link as `source_url` (no `create_asset` first); a YouTube
link is refused, so ask for the MP4. The same reel by its full link, in the same
mode, answers its earlier analysis for free; a short `vt.tiktok.com` or `vm.tiktok.com`
link counts as the full link of its video. `mode: "data"` reads many reels cheaply, without a
`reference_profile`. Checked 2026-10-31.

**An unknown terminal state reads as in progress.** The MCP formatter reports a
state it does not know as `IN_PROGRESS`, so polling would not end. Update the
client: MCP and the API ship as one version. Checked 2026-10-31.

## 5. Retrying a failed run is NOT a permanent refusal

A repeated call with the SAME input and WITHOUT a new `attempt` returns THAT SAME
failed run (section 4). **To actually retry, pass `attempt` one higher than
before** (the first call is `attempt: 1`). The `make_ugc` tool description says
the same:

> "attempt=2,3,… starts a new run for the same input."

`attempt` is the agent's "this is a new try"; `CLIPWRIGHT_CLIENT_ID` is the
installation's fixed identity and must NOT change between attempts.

### ⚠️ EVERY `attempt` BUMP COSTS MONEY

A new `attempt` is a **new paid run**, not a free resend. The loop "failed → bump
→ failed → bump" burns credits on every iteration.

- **Read the `error` of the failed run first.** `rejected_field`,
  `aspect_conflict` and `script_encoding_lost` come from the input, and the next
  attempt fails the same way for money. For `script_encoding_lost`, re-send the
  script decoded as UTF-8.
- **`speech_too_short_for_script` is almost never fixed by a retry**: change the
  text or the voice.
- **Bump `attempt` only for a failure that looks temporary** (a timeout, `5xx`, a
  dropped connection).
- **No daily cap stands between you and the credits.** What stops a run before
  any paid call is the balance, an unpaid debt, or a pause on our side.

## 6. Server refusals are read from fields, not guessed

A refusal arrives as JSON **inside the text block**, with `isError: true`:

```ts
{ content: [{ type: "text", text: "{\"status\":\"FAILED\", …}" }], isError: true }
```

So `JSON.parse(content[0].text)` first; `content[0].balance_credits` is
`undefined`. Do not relay the raw text and do not guess from it.

```json
{
  "status": "RETRY_LATER" | "FAILED",
  "code": "rate_limited" | "insufficient_credits" | "debt_outstanding" | "http_503" | …,
  "message": "<human-readable text from the server>",
  "retryable": true | false,
  "next_action": "<what to do right now>",
  "retry_after_seconds": 7,
  "balance_credits": 3,
  "required_credits": 8,
  "debt_credits": 120
}
```

The numbers appear only where the refusal has them: `retry_after_seconds` on
`rate_limited` and on a `5xx` that named a pause; `limit` and `window_seconds`
only when the 429 body followed the Clipwright contract; `balance_credits` and
`required_credits` on `insufficient_credits` only; `debt_credits` on
`debt_outstanding` only. Treat each as optional.

**One rule: look at `retryable`.**

- `retryable: true` (`rate_limited`, `5xx`) — wait `retry_after_seconds` and
  repeat **THE SAME call with the same arguments**. Do not bump `attempt`: this
  was a refused request, not a failed run.
- `retryable: false` — **stop and tell the human**. For money refusals quote the
  NUMBERS: "the account has 3 credits, this needs 8".

The two money codes are cured the same way — buy credits — but they describe
different situations. `insufficient_credits` means the balance is too small for
this run. `debt_outstanding` means the account owes credits, possibly while still
holding a balance, so "you do not have enough credits" would be false. Credits
bought while a debt stands clear the debt first; the run still needs enough
credits of its own, so a purchase equal to the debt clears it and adds nothing to
the balance. Quote the debt figure and say that a purchase adds to the balance
only the part that exceeds the debt; this refusal does not report the balance.

Every paid tool takes an optional `max_credits`: the most the call may cost. A
run is never charged more, even when its measured cost comes out higher.
Pass the total the human agreed to from the quote. A call that reserves more
is refused with `max_credits_exceeded` (402), carrying `hold_credits` (what the
call reserves) and `max_credits`; nothing is charged and no run is made.
Show the human `hold_credits` and repeat the call only after they approve that
amount, with `max_credits` of at least it, or change the request to cost less.
At or above the hold the call runs as usual.

`account_not_admitted` (403) is not a money refusal and carries no numbers: the
account has no access. Buying credits does not lift it; contact support. Promise
no date and no position: an account whose access was REVOKED gets the same 403.

A `429` or `5xx` can come from the Clipwright API or from anything between you
and it; do not claim a source. A `429` does **not** mean no run was created: a
repeat with an already-used key can get one too, so retry with THE SAME key. On a
status check, a `429` is yours to sit out: wait, then call `get_run` again with
the same `run_id`. The run is already going and already paid for.

## 7. On failure — plain curl splits the diagnosis

If the MCP path does not reach a playable video, call the same REST API directly.
If curl gets through, the MCP setup is at fault (section 1); if not, the key,
the network or the service is.

```bash
TOKEN=cw_...                       # the same value as CLIPWRIGHT_API_KEY
API=https://api.clipwright.io

# 0. Free: the quote. Verified 2026-10-31 (200, 50 credits, resolved 9:16).
curl -sS -X POST "$API/v1/skills/make_ugc/quote" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"script":"Hello! This is a test line."}'

# 1. Paid: start a run. The idempotency key is required and must be UNIQUE per
#    call: a repeated key returns the earlier run. Generate it with Node, not
#    uuidgen, which may be missing and leave the key empty and constant.
curl -sS -X POST "$API/v1/skills/make_ugc/run" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: cw-$(node -e 'process.stdout.write(crypto.randomUUID())')" \
  -d '{"script":"Hello! This is a test line."}'

# 2. Free: poll until terminal, every ~5–10 s.
curl -sS "$API/v1/runs/<run_id>" -H "Authorization: Bearer $TOKEN"
```

If curl reaches `succeeded`
with its own `run_id` and MCP does not, look at the MCP build, host config and
environment. If curl fails too, check that `$TOKEN` is a whole `cw_*` key, that
`$API` is reachable, and that `CLIPWRIGHT_CLIENT_ID` is unique (section 2).

### If you are a second user evaluating the product

Your task: **reach a playable video using this file, without spoken help from
whoever gave you access.** What is tested is the guide, not you: do not ask,
write down where you got stuck.

1. **The token was issued on YOUR account, not merely as a separate token.** The
   idempotency axis is `account_id`, and one account can hold several live
   tokens. You cannot check this from your side, so the confirmation that the
   token is on a SEPARATE account comes WITH the token. If it did not, write that
   down and move on.
2. **`CLIPWRIGHT_CLIENT_ID` was not copied from anyone's machine** (section 2).
   If you and the person who issued your token are on one account AND your
   `clientId` matches theirs, the server returns THAT PERSON'S RUN with a 200 and
   a playable link: a false success that looks more convincing than a real one.

Tell two classes of failure apart:

- **`rejected_field`, `unknown_field`, `aspect_conflict`** — the contract doing
  its job; the message names the reason and the replacement.
- **everything else** (a timeout, `5xx`, an empty response, a missing tool) — a
  candidate for a real defect. Run the curl commands of section 7 and write down
  separately whether curl reached a playable link where MCP did not.
