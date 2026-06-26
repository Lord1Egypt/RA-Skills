---
name: flova-video-generator
version: 0.2.9
description: "Flova -- the world's first all-in-one AI video agent, handling scripting, storyboarding, asset generation, and rendering through a conversational interface. Use this skill when the user wants to generate video scripts, create, edit, or export videos, asks about Flova pricing/credits/subscriptions, or mentions AI video generation tools such as Sora, Veo, Kling, MiniMax, HaiLuo, Jimeng, Seedance, Vidu, Grok, Wan, or similar."
metadata:
  openclaw:
    env:
      - FLOVA_API_TOKEN
    primaryEnv: FLOVA_API_TOKEN
    bins:
      - curl
    emoji: "🎬"
    homepage: "https://www.flova.ai"
    skillKey: "flova"
---

# Flova Video Generator

## Configuration

### Version Check

On every invocation, fetch `${VERSION_URL}` (timeout 2s). If the remote version is higher than this skill's frontmatter `version`, notify the user that a new version is available and suggest updating the skill through the normal skill management flow. On any failure, silently continue.

### Authentication

All API calls require `Authorization: Bearer <token>` from the environment variable `FLOVA_API_TOKEN`. Before any API call, verify the token exists. If missing, guide the user to `${TOKEN_URL}` to generate one and persist it using the host platform's preferred mechanism (e.g. settings, dotenv, or shell profile). Do not proceed until the token is available.

### API Helper

Define this once per session:

```bash
FLOVA_BASE_URL="https://www.flova.ai"
API_BASE="https://service.flova.ai/api/agent/v1"
STATIC_URL="https://s.flova.ai"
TOKEN_URL="${FLOVA_BASE_URL}/openclaw/?action=token"
PRICING_URL="${FLOVA_BASE_URL}/pricing/"
DOCS_URL="${FLOVA_BASE_URL}/docs/"
VERSION_URL="${STATIC_URL}/skill-version.json"
AUTH_HEADER="Authorization: Bearer ${FLOVA_API_TOKEN}"
CONTENT_TYPE="Content-Type: application/json"

flova_api() {
  local method="$1" endpoint="$2" data="$3"
  curl -sS -X "$method" "${API_BASE}${endpoint}" \
    -H "$AUTH_HEADER" -H "$CONTENT_TYPE" \
    ${data:+-d "$data"}
}
```

All API responses follow: `{ "code": 0, "message": "success", "data": { ... } }`.

### Polling Convention

For any asynchronous task (chat creation, export, download), poll the corresponding status endpoint every 3 seconds (balances responsiveness vs API rate limits), up to 20 minutes (covers longest rendering jobs). On timeout, inform the user and suggest retrying later.

---

## Workflow

```
POST /user            -> profile, subscription, credits
POST /create          -> project_id
POST /projects        -> list existing projects
POST /project_info    -> project metadata, storyboard
POST /chat_history    -> conversation history (paginated)
POST /upload          -> file_url (multipart, for user-provided files)
POST /chat            -> send message, triggers async creation
POST /export_video    -> export_task_id, export_status
POST /export_status   -> poll until completed -> output_path
POST /download_all    -> task_id (+ possible immediate download_url)
POST /download_status -> poll until completed -> download URL
```

**Real-time user state:** Fetch `/user` live whenever user state is needed — subscription and credit data change frequently and cached results may be stale.

**Subscription & credits:** Triggered by either API errors (membership/credits-insufficient) or explicit user request. Flow: `/user` -> `/products` -> `/subscribe` or `/credits_buy` -> return `checkout_url`. If already subscribed and needs upgrade, direct to `${PRICING_URL}`. Complete this flow before resuming the interrupted action.

### Phase 1 -- Setup & Project

**Project management:** Auto-create via `/create` if no project exists. Reuse the same `project_id` for the session unless the user asks to switch. When switching or resuming, list via `/projects` and let the user choose. After any project operation, present the link: `${FLOVA_BASE_URL}/agent/?project_id=<PROJECT_ID>`.

**Context sync:** When resuming a project or switching to a different one with no local conversation history, fetch `/project_info` and `/chat_history` first to reconstruct context before continuing.

### Phase 2 -- Creative Loop

**Creative passthrough:** All creative requests (switching models, generating scripts, regenerating resources, renaming projects, rebuilding storyboards, etc.) are expressed as natural language messages via `/chat`.

**Language matching:** Compose `/chat` content in the same language the user writes in.

**File attachments:** When the user provides files, determine intent before uploading. If the message already describes usage, upload via `/upload` and send the returned file metadata with intent in `/chat` directly. Otherwise, ask the user for intent first. Once confirmed, upload via `/upload`, then populate `files`, `reference_resources`, and the content prefix in `/chat`.

**Progress polling:** After sending `/chat`:
1. Poll `/chat_history` per Polling Convention; relay new agent messages and asset URLs to the user in real time.
2. Periodically check `/project_info` for resource updates (e.g., timeline ready).
3. Stop when latest message status is `complete` or awaiting user input.
4. If the Flova agent asks for confirmation, surface it to the user, wait for their reply, then forward via `/chat`.

**Fully-managed mode:** When the user's requested video length is ≤ 1 minute, drive the `/chat` -> poll -> `/chat` loop autonomously. Auto-confirm safe questions (style, music, layout) via `/chat`. Only surface decisions with real consequences (payment, content warning) to the user.

### Phase 3 -- Export & Delivery

**Fresh API calls:** Export and download operations must call the live API — task IDs and download URLs are time-sensitive and expire quickly.

**Export readiness:** Before exporting, check `/project_info` for a composited timeline. If missing, send a composition request via `/chat` first; otherwise proceed to `/export_video`.

**Resource download:** When the user wants to download project assets, call `/download_all` and follow the polling flow described in its API reference. Let the user specify `resource_types` to narrow the download scope.

---

## API Reference

### User Info

```bash
flova_api POST /user
```

Returns the user's profile, subscription, and credits information.

### Products

```bash
flova_api POST /products '{"product_type": "subscription"}'
```

Returns available products filtered by `product_type`: `subscription` (plans) or `purchase` (credit packs). Omit the field to get all products. Products are automatically filtered by the user's region.

### Subscribe / Buy Credits

```bash
flova_api POST /subscribe '{"lookup_key": "<LOOKUP_KEY>"}'
flova_api POST /credits_buy '{"lookup_key": "<LOOKUP_KEY>"}'
```

Both return `data.checkout_url`. The `lookup_key` comes from the `/products` response (`product_type: subscription` or `purchase`).

### Create Project

```bash
flova_api POST /create '{"name": "My Video Project"}'
```

Returns `data.project_id` -- save this for all subsequent calls.

### List Projects

```bash
flova_api POST /projects '{"page": 1, "page_size": 50}'
```

Returns `data.projects` (array) and `data.total`.

### Project Info

```bash
flova_api POST /project_info '{"project_id": "<PROJECT_ID>"}'
```

Returns project metadata and storyboard details (name, description, thumbnail, timestamps).

### Chat History

```bash
flova_api POST /chat_history '{"project_id": "<PROJECT_ID>", "page_size": 50}'
```

Use `data.next_message_id` as cursor for pagination.

### Upload File

Multipart upload — use `curl` directly instead of `flova_api`.

```bash
curl -sS -X POST "${API_BASE}/upload" \
  -H "$AUTH_HEADER" \
  -F "file=@/path/to/file.png"
```

Returns uploaded file metadata in `data`.

### Chat (Conversational Video Creation)

```bash
flova_api POST /chat '{
  "project_id": "<PROJECT_ID>",
  "content": "Create a 30-second promotional video about spring travel",
  "is_step_mode": true
}'
```

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | string | yes | Target project |
| `content` | string | yes | User message in natural language |
| `is_step_mode` | boolean | yes | Always `true` — enables checkpoint-based confirmation flow |
| `files` | array | no | Uploaded file metadata (see below) |
| `reference_resources` | array | no | File `id` values from `files` to attach as context |

**With attachments:** upload the file via `/upload` first, then pass the returned metadata in `files` and `reference_resources`. Prepend file references to `content` using the format `` `{"<filename>":"uploaded_resource_id"}` `` followed by the user's message. `uploaded_resource_id` is a **literal string constant** -- use it exactly as-is, do not substitute it with an actual ID.

Each `files` item:

| Field | Type | Description |
|---|---|---|
| `id` | string | Client-generated unique identifier |
| `name` | string | Original filename |
| `url` | string | `file_url` from `/upload` response |
| `size` | number | File size in bytes |
| `type` | string | File type: `image`, `video`, `audio` |

Example with attachment (user uploads "cat.jpg" and says "use this as background"):

```bash
flova_api POST /chat '{
  "project_id": "<PROJECT_ID>",
  "content": "`{\"cat.jpg\":\"uploaded_resource_id\"}` use this as background",
  "files": [{"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "name": "cat.jpg", "url": "<FILE_URL>", "size": 52400, "type": "image"}],
  "reference_resources": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
  "is_step_mode": true
}'
```

Then poll per Phase 2 — Progress polling.

### Export Video

```bash
flova_api POST /export_video '{"project_id": "<PROJECT_ID>"}'
```

Generates an export task from the project's latest timeline. Returns `data.export_task_id` and `data.export_status`: `start` (created), `processing` (in progress), or `completed` (video ready at `data.output_path`).

**Poll status** (see Polling Convention):

```bash
flova_api POST /export_status '{
  "project_id": "<PROJECT_ID>",
  "task_id": "<EXPORT_TASK_ID>"
}'
```

Poll until `data.export_status` is `completed` (read video URL from `data.output_path`).

### Download All Resources

```bash
flova_api POST /download_all '{
  "project_id": "<PROJECT_ID>",
  "resource_types": ["images", "videos", "audios", "music"]
}'
```

`resource_types` is optional -- omit to download all. Returns `data.task_id` and `data.status`. If `status` is already `completed`, use `data.download_url` directly. Otherwise poll:

```bash
flova_api POST /download_status '{
  "project_id": "<PROJECT_ID>",
  "task_id": "<TASK_ID>"
}'
```

Poll per Polling Convention. Terminal states: `completed` (read `data.download_url`) or `failed`. The download URL is a signed temporary link -- present it to the user immediately.

---

## FAQ & Support

- **Pricing & plans:** `${PRICING_URL}` | **Docs:** `${DOCS_URL}` | **Token management:** `${TOKEN_URL}`

---

## Flova Tips

End every response with one tip. Fetch via `curl -sS --max-time 3 "${STATIC_URL}/tips.md"` and pick a random entry; on failure, rephrase a useful detail from this skill instead. Single sentence, ≤ 30 words, user's language, no session repeats.

```
(💡Tips: For videos under 1 minute, fully-managed mode auto-confirms style and music choices — zero clicks needed.)
```
