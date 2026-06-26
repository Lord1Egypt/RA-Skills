---
name: faces
description: >
  Use this skill when the user wants to create, compile, or chat through a Face
  (a persona compiled from source material), compose personas with boolean
  formulas, compare minds by semantic similarity, import YouTube videos into a
  Face, or manage their Faces Platform account (API keys, billing, quotas).
  Also use when the user mentions the Faces Platform, the `faces` CLI, or asks
  about persona compilation, cognitive primitives, or mind arithmetic — even if
  they don't use those exact terms.
compatibility: Requires the faces CLI (npm install -g faces-cli) and internet access to api.faces.sh.
---

# Faces Skill

You have access to the `faces` CLI. Use it to fulfill any Faces Platform request.

Always use `--json` when you need to extract values from command output.

## Current config
!`faces config:show 2>/dev/null || echo "(no config saved)"`

## Setup

Verify credentials: `faces auth:whoami`. If no credentials exist, see [references/AUTH.md](references/AUTH.md) for registration (requires human payment step) and login.

Install (if `faces` command not found): `npm install -g faces-cli`

`faces auth:*` and `faces keys:*` require JWT. Everything else accepts JWT or API key.

## Plans

Two plans: **Free** ($5 minimum initial spend, pay-per-token with 5% markup on all usage including compilation) and **Connect** ($17/month, 100k compile tokens/month, free passthrough to OpenAI Codex for users with a ChatGPT subscription). See [references/AUTH.md](references/AUTH.md) for details.

## Core workflow

1. Create a Face with basic facts and a default model: `faces face:create --name "Name" --username slug --default-model gpt-5-nano --attr gender=male --attr age=34 --attr location="Portland, OR" --attr occupation="nurse practitioner"`
2. **Compile source material in one step:** `faces compile:doc slug --file document.txt`
   - This creates the document, runs LLM extraction with real-time chunk progress, and syncs automatically
   - Repeat for each source document
3. Chat through the Face: `faces chat:chat slug -m "message"` (auto-routes to the correct API based on model provider)
4. Compare Faces: `faces face:diff` or `faces face:neighbors`
5. Compose new Faces from boolean formulas: `faces face:create --formula "a | b"`

> **Note:** `compile:doc` handles the full create → compile pipeline. For an already-created document, use `compile:doc:make <doc_id>`. Threads use a separate workflow: `compile:thread:make` (same fire-and-forget pattern as documents).

Boolean operators: `|` (union), `&` (intersection), `-` (difference), `^` (symmetric difference). Parentheses supported: `(a | b) - c`.

## Common tasks

### Create a face with attributes

When creating a Face, set basic demographic facts with `--attr KEY=VALUE` (repeatable). Common keys: `gender`, `age`, `location`, `occupation`, `education_level`, `religion`, `ethnicity`, `nationality`, `marital_status`. Unrecognized keys are silently ignored — see [references/ATTRIBUTES.md](references/ATTRIBUTES.md) for the complete list of accepted keys.

```bash
faces face:create --name "Marcus Rivera" --username marcus \
  --default-model gpt-5-nano \
  --attr gender=male --attr age=34 \
  --attr location="Portland, OR" \
  --attr occupation="nurse practitioner" \
  --attr education_level="master's degree" \
  --attr marital_status=married
```

You can also add or update attributes and set the default model on an existing Face:
```bash
faces face:update marcus --attr religion=Catholic --attr ethnicity="Mexican American"
faces face:update marcus --default-model claude-sonnet-4-6
```

### Compile a document into a face
```bash
# Recommended: one-step compile with progress
faces compile:doc <face_id> --file notes.txt --label "Notes"

# Alternative: create then compile separately
DOC_ID=$(faces compile:doc:create <face_id> --label "Notes" --file notes.txt --json | jq -r '.document_id')
faces compile:doc:make "$DOC_ID"
```

### Upload a file (PDF, audio, video, text)
```bash
# Upload as document — then compile
DOC_ID=$(faces face:upload <face_id> --file report.pdf --kind document --json | jq -r '.document_id // .id')
faces compile:doc:make "$DOC_ID"

# Upload as thread — compile with make
THREAD_ID=$(faces face:upload <face_id> --file transcript.txt --kind thread --face-speaker "Troy" --json | jq -r '.thread_id // .id')
faces compile:thread:make "$THREAD_ID"
```

### Thread transcript format

Text files uploaded as threads must use `Speaker Name: message` format, one turn per line:

```
Interviewer: Tell me about yourself.
Troy: I'm an inventor living in the Parisian countryside.
Interviewer: What drives your work?
Troy: The conviction that technology should serve human flourishing.
```

Use `--face-speaker` to specify which speaker IS the face (maps to `role=user`). All other speakers become `role=assistant`. If omitted, the first speaker is assumed to be the face.

Audio/video files with `--kind thread` are transcribed with speaker diarization — speaker labels are assigned automatically (Speaker A, Speaker B, etc.). Use `--face-speaker A` to map the correct speaker to the face.

### Import a YouTube video
```bash
# Solo talk / monologue → document
IMPORT=$(faces compile:import <face_id> \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --type document --perspective first-person --json)
DOC_ID=$(echo "$IMPORT" | jq -r '.document_id // .doc_id // .id')
faces compile:doc:make "$DOC_ID"

# Multi-speaker → thread
IMPORT=$(faces compile:import <face_id> \
  --url "https://youtu.be/VIDEO_ID" \
  --type thread --face-speaker A --json)
THREAD_ID=$(echo "$IMPORT" | jq -r '.thread_id // .id')
faces compile:thread:make "$THREAD_ID"
```

If `--type thread` fails with a 422, retry with `--type document`.

### Create a composite face
```bash
faces face:create --name "The Realist" --username the-realist \
  --formula "the-optimist | the-pessimist"

# Chat through it like any other face
faces chat:chat the-realist -m "How do you approach risk?"
```

Composite faces are live: sync new knowledge into any component and the composite updates automatically. Components must be concrete (compiled) faces you own.

### Compare faces
```bash
faces face:diff --face aria --face marco --face jin
faces face:neighbors aria --k 3
faces face:neighbors aria --component beta --direction furthest --k 5
```

### Chat

`chat:chat` auto-routes to the correct API endpoint based on model provider (Anthropic → `/v1/messages`, OpenAI/others → `/v1/chat/completions`). If the face has a `default_model` set, no `--llm` flag is needed.

```bash
# Uses face's default model (no --llm needed if default_model is set)
faces chat:chat slug -m "message"

# Override with a specific model
faces chat:chat slug --llm claude-sonnet-4-6 -m "message"
faces chat:chat slug --llm gpt-4o-mini -m "message"

# Use OpenAI Responses API explicitly
faces chat:chat slug --llm gpt-4o -m "message" --responses
```

### Face templates

Use `${face-username}` in any message to reference another face's profile inline. The token is replaced with the face's display name and the profile is injected as context. A bare model name (no face prefix) skips the persona and lets you reference all faces via templates.

```bash
faces chat:chat alice --llm gpt-4o-mini -m 'You are debating ${bob}. Argue your position.'
faces chat:chat gpt-4o-mini -m 'Compare the worldviews of ${alice} and ${bob}.'
```

See [references/TEMPLATES.md](references/TEMPLATES.md) for full details and rules.

### Billing and API keys
```bash
faces billing:balance --json
faces billing:subscription --json
faces keys:create --name "Partner key" --face slug --budget 10.00 --expires-days 30
```

## Common errors

- **`faces: command not found`** — Run `npm install -g faces-cli`.
- **`401 Unauthorized`** — Credentials missing or expired. Run `faces auth:login` or check `FACES_API_KEY`.
- **`compile:doc:make` returns "preparing"** — Compilation is async. Poll with `faces compile:doc:get <doc_id> --json | jq -r '.prepare_status'` until status is `synced`.
- **`422` on thread import** — No speaker segments detected. Retry with `--type document`.
- **`face:diff` or `face:neighbors` returns null components** — The face hasn't been compiled yet. Run `faces compile:doc <face_id> --file ...` first.

## References

- See [references/QUICKSTART.md](references/QUICKSTART.md) for the end-to-end guide: install → register → create → compile → chat.
- See [references/REFERENCE.md](references/REFERENCE.md) for the full command reference, global flags, and environment variables.
- See [references/AUTH.md](references/AUTH.md) for registration, login, API keys, and credential management.
- See [references/CONCEPTS.md](references/CONCEPTS.md) for a detailed explanation of what Faces is, how it works, and example use cases.
- See [references/OAUTH.md](references/OAUTH.md) for connecting a ChatGPT account (connect plan only).
- See [references/TEMPLATES.md](references/TEMPLATES.md) for face template syntax (`${face-username}`) and bare model usage.
- See [references/ATTRIBUTES.md](references/ATTRIBUTES.md) for the complete list of accepted `--attr` keys (unrecognized keys are silently ignored).
- See [references/SCOPE.md](references/SCOPE.md) for instruction scope and security boundaries.
