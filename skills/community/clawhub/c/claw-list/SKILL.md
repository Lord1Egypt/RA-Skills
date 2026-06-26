# Claw-List

Manage todo lists via a central API. Trigger on: "the list", "show me the list", "todo", "add task", "add to my list", "mark done", "mark complete", "what's due", "my tasks", "create a list".

## Config

Check env vars first: `CLAW_LIST_AGENT_ID`, `CLAW_LIST_URL` (set via openclaw.json skills.entries for multi-agent setups).

If env vars not set: read `~/.openclaw/skills/claw-list/claw-list.conf` and extract `AGENT_ID`, `DISPLAY_NAME`, `CLAW_LIST_URL`, `REGISTERED`.

If conf file doesn't exist (first run):
1. Generate UUID: `cat /proc/sys/kernel/random/uuid` — fallback: `python3 -c 'import uuid; print(uuid.uuid4())'`
2. Ask user for `DISPLAY_NAME` and `CLAW_LIST_URL` (e.g. `https://claw-list.internal/api` or `http://host:8100`)
3. Write conf file with those values and `REGISTERED=false`

If `REGISTERED=false`: call `POST {CLAW_LIST_URL}/admin/agents` with body `{"agent_id":"{AGENT_ID}","display_name":"{DISPLAY_NAME}","scope":"own"}` — no `X-Agent-Id` header. On 201 or 409 write `REGISTERED=true` to conf. On any other status: tell user the API is unreachable and stop.

## API

All requests require header `X-Agent-Id: {AGENT_ID}`. Base URL from `CLAW_LIST_URL`.

Lists: `GET /lists` · `POST /lists {"name":"..."}` · `DELETE /lists/{id}`

Items: `GET /lists/{id}/items` · `POST /lists/{id}/items` · `PUT /items/{id}` · `DELETE /items/{id}`

Item fields: `title` (required on create), `notes`, `priority` (1–5), `due_date`, `category`, `done`.

Full reference: `~/.openclaw/skills/claw-list/docs/api.md`

## Behaviour

- Re-read conf at the start of every session — never assume values from a previous session.
- Present results cleanly; never expose `AGENT_ID` or raw JSON to the user.
- Store conversation context in `notes` when the user says "put that in the notes".
- On 403: tell the user they don't have permission, don't retry.
