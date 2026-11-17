# AideNote API contract

The bundled `scripts/aidenote.py` is the only supported API entry point for this Skill.

| Command | AideNote endpoint | Output focus |
|---|---|---|
| `health` | token exchange, then recording list | Authentication and data access |
| `user-info` | `/api/audiofileMstr/getUserInfo` | Current account information |
| `recordings` | `/api/audiofileMstr/audiofileseleUserAllList` | Recording IDs, titles, dates, durations, processing state |
| `shared-recordings` | `/api/audiofileMstr/audiofileseleUserAllList` with `screeningType=2` | Recordings shared with the current account |
| `recording-detail` | `/api/audiofileMstr/audiofileToText` | Transcript, AI summary, and recording detail |
| `todos` | recording list plus `/api/audiofileTodo/listByFile` | Extracted action items with source recording |
| `knowledge-bases` | `/api/userfolderMstr/AllList` | Available knowledge bases |
| `knowledge-files` | `/api/userfolderMstr/FolderList` | Files and folders in one knowledge base |
| `knowledge-recordings` | recursive `/api/userfolderMstr/FolderList` | Audio recordings in a knowledge base and its nested folders |

The preferred first-run flow uses the relay's short-lived `/agent-pair/start`, `/status`, `/approve`, and `/complete` endpoints. The AideNote App approves the 8-character code only after confirming that its signed-in account owns the dedicated API Key. The local worker stores that key in `aidenote-credentials.json` under the active Hermes profile with owner-only permissions, then destroys the relay pairing session. `scripts/configure.py` remains the manual recovery path.

All commands emit JSON. Successful output has `"ok": true`; failures have `"ok": false`, a stable `error` code, and a safe `message`. A nonzero process exit means the requested data was not retrieved and must not be interpreted as an empty result.

## Local connection suite

`scripts/bridge.py status` is read-only. `scripts/bridge.py install --confirm` is the only supported automatic installation entry point and requires explicit user intent. It accepts no alternate installer URL and verifies a pinned SHA-256 digest before execution. The verified installer then validates the SHA-256 digest of each tunnel, MCP, and WorkBuddy bridge binary before installing it.

The installer writes the local Hermes API key to Hermes' owner-only `.env` and writes the same key as `hermesToken` in `~/.aidenote/openclaw-tunnel.json`. Secret values are never included in command arguments or command output.
