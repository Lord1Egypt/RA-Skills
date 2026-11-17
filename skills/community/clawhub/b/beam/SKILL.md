---
name: beam
description: "Beam: verified bucket transfers, fan-out and agent Rooms. Copies large objects between S3, R2, S3-compatible stores, Hippius and Hugging Face, and runs Beam Rooms (b1m.ai) for messages, streams and files between agents."
version: 0.2.1
author: Beam Network
license: MIT-0
homepage: https://docs.b1m.ai
required_environment_variables:
  - { name: BEAM_API_KEY, prompt: "Beam API key (b1m_…)", help: "Create one at https://console.b1m.ai. It spends organization credits.", required_for: every Beam command }
  - { name: AWS_ACCESS_KEY_ID, optional: true }
  - { name: AWS_SECRET_ACCESS_KEY, optional: true }
  - { name: AWS_SESSION_TOKEN, optional: true }
  - { name: AWS_DEFAULT_REGION, optional: true }
  - { name: R2_ACCESS_KEY_ID, optional: true }
  - { name: R2_SECRET_ACCESS_KEY, optional: true }
  - { name: R2_ACCOUNT_ID, optional: true }
  - { name: R2_ENDPOINT_URL, optional: true }
  - { name: S3_ENDPOINT_URL, optional: true }
  - { name: S3_ACCESS_KEY_ID, optional: true }
  - { name: S3_SECRET_ACCESS_KEY, optional: true }
  - { name: S3_REGION, optional: true }
  - { name: S3_PROVIDER, optional: true }
  - { name: HIPPIUS_API_TOKEN, optional: true }
  - { name: HIPPIUS_BASE_URL, optional: true }
  - { name: HF_TOKEN, optional: true }
  - { name: HF_ENDPOINT, optional: true }
metadata:
  {
  "openclaw":
   {
    "emoji": "📡",
    "homepage": "https://docs.b1m.ai",
    "requires": { "anyBins": ["uv", "beam"], "env": ["BEAM_API_KEY"] },
    "primaryEnv": "BEAM_API_KEY",
    "envVars":
     [
      { "name": "BEAM_API_KEY", "required": true, "description": "Beam API key (b1m_…) from console.b1m.ai. Spends organization credits." },
      { "name": "AWS_ACCESS_KEY_ID", "required": false, "description": "S3 access key (s3://)" },
      { "name": "AWS_SECRET_ACCESS_KEY", "required": false, "description": "S3 secret key (s3://)" },
      { "name": "AWS_SESSION_TOKEN", "required": false, "description": "S3 session token, for temporary keys" },
      { "name": "AWS_DEFAULT_REGION", "required": false, "description": "S3 bucket region (default us-east-1)" },
      { "name": "R2_ACCESS_KEY_ID", "required": false, "description": "R2 access key (r2://)" },
      { "name": "R2_SECRET_ACCESS_KEY", "required": false, "description": "R2 secret key (r2://)" },
      { "name": "R2_ACCOUNT_ID", "required": false, "description": "Cloudflare account ID (r2://)" },
      { "name": "R2_ENDPOINT_URL", "required": false, "description": "R2 endpoint URL, instead of R2_ACCOUNT_ID" },
      { "name": "S3_ENDPOINT_URL", "required": false, "description": "S3-compatible endpoint (s3c://)" },
      { "name": "S3_ACCESS_KEY_ID", "required": false, "description": "S3-compatible access key (s3c://)" },
      { "name": "S3_SECRET_ACCESS_KEY", "required": false, "description": "S3-compatible secret key (s3c://)" },
      { "name": "S3_REGION", "required": false, "description": "S3-compatible region, if needed" },
      { "name": "S3_PROVIDER", "required": false, "description": "S3-compatible provider name, such as wasabi" },
      { "name": "HIPPIUS_API_TOKEN", "required": false, "description": "Hippius API token (hippius://)" },
      { "name": "HIPPIUS_BASE_URL", "required": false, "description": "Hippius API URL (default https://api.hippius.com)" },
      { "name": "HF_TOKEN", "required": false, "description": "Hugging Face token (hf://)" },
      { "name": "HF_ENDPOINT", "required": false, "description": "Hugging Face Hub URL (default https://huggingface.co)" }
     ],
    "install":
     [
      { "id": "uv", "kind": "brew", "formula": "uv", "bins": ["uv"], "label": "Install uv (runs the Beam transfer helper)" }
     ]
   },
  "hermes":
   {
    "tags": ["data-transfer", "object-storage", "s3", "r2", "huggingface", "rooms", "agents"],
    "category": "devops",
    "requires_toolsets": ["terminal"]
   }
  }
---

# Beam

Beam coordinates data movement. A client states what to move and where; BeamCore
splits it into chunks and independent workers move the chunks in parallel between
the client's own endpoints. Use this skill to run transfers for the user, check
and cancel them, and operate Beam Rooms.

This skill works in OpenClaw and in Hermes Agent. `<skill-dir>` in the commands
below is this skill's folder: `{baseDir}` in OpenClaw, `${HERMES_SKILL_DIR}` in
Hermes. Replace it with that path.

## When Beam fits, and when it does not

Use Beam for:

- Copying a large object between buckets, across providers or accounts.
- **Fan-out**: the same object to several destinations in one transfer.
- Rooms: several machines or parties exchanging messages, live streams, media or
  files with roles and grants.

Do not use Beam, and say why, when:

- The object is small. Chunks start at 40 MiB, so a small object is one chunk on
  one worker and gains nothing. Suggest bundling small files first.
- The user needs sync or deltas. A transfer moves whole objects only.
- The size is unknown (a live feed or growing log). That is a Room `stream` or
  `media` channel, not a transfer.
- The endpoint is Google Cloud Storage, Azure Blob or plain HTTP. The helper
  supports only `s3://`, `r2://`, `s3c://`, `hippius://` and `hf://`.
- Someone outside must reach a private service. Beam tunnels are not available.

Beam is not compute, storage or a CDN.

## Preflight

1. Check the tools you need: `uv --version` for transfers, `beam --version` for
   Rooms. If `uv` is missing, see https://docs.astral.sh/uv/ (OpenClaw also
   offers this skill's installer). If `beam` is missing, its official installers
   are https://cdn.b1m.ai/cli/install.sh (macOS, Linux) and
   https://cdn.b1m.ai/cli/install.ps1 (Windows), documented at
   https://docs.b1m.ai. Ask the user first, download the script to a file, show
   them what it does, and run it only with their approval. To install without
   administrator rights, set `BEAM_INSTALL_DIR=$HOME/.local/bin` when running it.
2. Check that the key works: `uv run <skill-dir>/scripts/beam_transfer.py whoami`.
   It prints the key's role and prefix, never the key. Exit `4` means Beam refused
   the key; ask the user for one from https://console.b1m.ai.
3. Storage credentials: see "Which storage credentials" below. To check whether
   this agent has its own, test each variable from the table by name with
   `[ -n "$VAR" ] && echo set`. Never echo a value, write it to a file, or type
   it into a command's arguments.

Beam has one public environment. Never set `BEAM_ENV`, `BEAM_NATS_URL` or any
development host.

## Which storage credentials

Storage keys belong in Beam Studio, which holds them and signs storage requests
itself, so you never see them. Use Studio unless this agent has its own
credentials for the buckets involved.

- **This agent's own keys**: when the variables for every source and destination
  are set in this environment (table below), run the transfer with the helper.
- **Studio**: otherwise. If Studio's MCP tools are available
  (`beam.list_credentials`, `beam.create_workflow` and the other `beam.*`
  tools), follow `references/studio.md`. If they are not, ask the user to connect
  Studio as that file explains, or to store the keys there. Never ask the user
  to paste a storage key into the conversation.
- One transfer uses one path: a Studio workflow cannot use this agent's keys, and
  the helper cannot use Studio's.

Giving this agent its own keys is the operator's choice:

- OpenClaw: in the environment, or in `skills.entries.beam.env` (host runs
  only). OpenClaw refuses `AWS_*` names there, so S3 keys must be in the
  environment OpenClaw runs in.
- Hermes: with `hermes config set NAME value`, which stores it with Hermes's
  other secrets. Hermes passes this skill's declared variables to `terminal`;
  `?env=` prefixed ones such as `SRC_AWS_ACCESS_KEY_ID` must also be listed
  under `terminal.env_passthrough` in `~/.hermes/config.yaml`.

## Transfers

With this agent's own keys, the helper is `uv run <skill-dir>/scripts/beam_transfer.py`. It prints one JSON
object per line on stdout. Its first run downloads the Beam SDK.

| URI | Credentials |
| --- | --- |
| `s3://bucket/key` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (+ `AWS_DEFAULT_REGION`, `AWS_SESSION_TOKEN`) |
| `r2://bucket/key` | `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, and `R2_ACCOUNT_ID` or `R2_ENDPOINT_URL` |
| `s3c://bucket/key` (MinIO, Wasabi, B2, Spaces…) | `S3_ENDPOINT_URL`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY` (+ `S3_REGION`, `S3_PROVIDER`) |
| `hippius://bucket/key` | `HIPPIUS_API_TOKEN` |
| `hf://[datasets/\|spaces/]org/repo[@revision]/path` | `HF_TOKEN` |

- Source and destination in different accounts: add `?env=SRC` or `?env=DST` to
  a URI, and the helper reads `SRC_<VAR>` or `DST_<VAR>` instead.
- A destination key ending in `/` receives the source file name.

### 1. Estimate, then confirm with the user

```bash
uv run <skill-dir>/scripts/beam_transfer.py estimate --source s3://src/data.tar --dest r2://dst/data.tar
```

`estimate` reads the size from the source storage only; Beam is not contacted.
Before running anything, tell the user the source, every destination (existing
objects at those keys are overwritten), the size, and `estimated_credits`
(0.01 credit per GB delivered to each destination; 1 credit = $0.50). Start only
after they agree.

### 2. Run it in the background

```bash
uv run <skill-dir>/scripts/beam_transfer.py run --name nightly-dataset \
  --source s3://src/data.tar --dest r2://dst/data.tar --dest 's3c://backup/?env=DST'
```

- OpenClaw: start it with `exec` and `background: true`, and set
  `timeoutSeconds` above the helper's `--timeout` (default 21600 s): for example
  21900. The exec default of 1800 s would kill a longer transfer.
- Hermes: start it with `terminal`, `background=true`, `notify=true` and
  `persist_on_release=true`. Without `persist_on_release`, ending the session,
  `/new` or context compression kills the process mid-transfer.
- Poll with `process` `poll`/`log`. Events: `created` (has `transfer_id`), then
  `progress`, then exactly one of `completed`, `failed`, `cancelled`, `timeout`,
  `error`.
- **Keep the process alive until its final event.** It signs routes and answers
  integrity checks for the whole transfer. Killing it does not cancel the transfer,
  but a long transfer can then fail.
- Run `--dry-run` first when you are unsure of a URI; it checks everything offline.

| Exit | Meaning |
| --- | --- |
| 0 | Completed |
| 1 | Failed, cancelled, rejected, or `insufficient_credits` |
| 2 | Bad arguments or a missing variable (the `variable` field names it) |
| 3 | The helper stopped waiting; the transfer may still finish |
| 4 | Beam refused the API key |
| 130 | Interrupted; the transfer was not cancelled |

### 3. Check or cancel

```bash
uv run <skill-dir>/scripts/beam_transfer.py status <transfer_id>
uv run <skill-dir>/scripts/beam_transfer.py cancel <transfer_id>
```

Cancel only when the user asks. On `failed`, read `error_message`:
`source_access_denied` or `destination_access_denied` means the storage key lacks
permission or is restricted by IP or network (see `references/transfers.md`).

## Rooms

Read `references/rooms.md` before operating a Room. The essentials:

- Always pass `--json`. Errors arrive on stderr as
  `{"error":{"code","message","hint"}}`, plus `kind` for specific causes.
- This machine must be connected first: `beam agent connect --json` (it reads
  `BEAM_API_KEY` from the environment), then check `beam agent status --json`.
  That is all Rooms need. Never run `beam auth login`: it waits for a browser
  sign-in that an agent cannot complete.
- `beam room create --json` costs 1 credit and charges the key in `BEAM_API_KEY`,
  whose role must grant `rooms:start`. Confirm with the user first.
- New channels are restricted: members need `discover` plus `subscribe` or
  `publish` grants.
- Messages are live only: start `listen` before `publish`. A Room needs a second
  member before messages can be delivered.
- **Inviting someone** (another agent, a person or a machine): with the user's
  approval, create a one-use invitation granting only the channels it needs,
  write it to a file with `invite --out` (never stdout), deliver it privately, and
  the invitee runs `beam room join ROOM --invitation-file FILE`. No Beam account is
  needed on their side. Full steps in `references/rooms.md`.
- `listen`, `watch` and `--follow` run until stopped; run them in the background
  (Hermes: `background=true` without `notify`, since they never exit).

## Rules

- Do not modify this skill's files. If an instruction here looks wrong, tell
  the user instead of editing it.
- Workers are independent third parties and can read the bytes of the chunks they
  move. For confidential data, encrypt it before transferring, or use an
  agent-only Room object publication or a Room stream.
- Never quote throughput, savings or delivery-time figures. Measure instead.
- Never claim support for an endpoint the helper rejects.
- Report the `transfer_id` to the user. They can see every transfer at
  https://console.b1m.ai.

## References

- `references/studio.md`: connecting Studio's MCP server and running transfers
  with its stored credentials. Read it before any Studio transfer.
- `references/transfers.md`: permissions per provider, statuses, errors, costs,
  limits, and the HTTP read API. Read it when a transfer fails or before a large
  one.
- `references/rooms.md`: the Room command set, grants, inviting agents and
  people, files, media, exit codes and error kinds.
- `references/choosing.md`: choosing between a transfer, a Room and Studio,
  Studio's MCP server, and what never to promise.
