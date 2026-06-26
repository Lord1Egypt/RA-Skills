# Storage Model

## SQLite

`~/.codex/state_5.sqlite`

Important table:

- `threads`

Important columns:

- `id`
- `rollout_path`
- `cwd`
- `title`
- `first_user_message`
- `model_provider`
- `model`
- `archived`
- `created_at`
- `updated_at`

## Rollout JSONL

Each rollout starts with a `session_meta` record. Relevant fields:

- `payload.id`
- `payload.cwd`
- `payload.model_provider`

Visible conversation text is easiest to reconstruct from `event_msg` records:

- `payload.type == "user_message"`
- `payload.type == "agent_message"`

`turn_context` records may also carry model metadata:

- `payload.model`

For workspace migration or provider rebinding, keep SQLite and rollout metadata in sync.
