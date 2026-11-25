---
name: everos-setup
description: Set up, verify, or repair EverOS memory for OpenClaw. Use when the user asks to install EverOS or the EverOS memory plugin, wants OpenClaw to remember things across sessions with a self-hosted EverOS, or reports that EverOS memory is not recalling or not saving.
---

# EverOS Setup for OpenClaw

EverOS is an open-source memory layer for AI agents that the user runs on their own machine. The official OpenClaw plugin `@everos-ai/openclaw-plugin` connects OpenClaw's memory slot to a local EverOS server at `http://127.0.0.1:8000`. After setup the user just chats: the plugin recalls relevant memories before each reply and saves each finished turn. There are no memory tools to call.

Source: https://github.com/EverMind-AI/Plugins/tree/main/openclaw (Apache-2.0). EverOS: https://github.com/EverMind-AI/EverOS

## Before you start, tell the user

Say these three things and wait for a yes before installing:

1. The plugin takes OpenClaw's exclusive `memory` slot. It replaces the stock `memory-core` plugin or any other memory plugin in that slot.
2. The plugin needs conversation access. Recall and saving both read the conversation, and OpenClaw blocks them until the user grants this.
3. Conversation turns go to the local EverOS server. EverOS then sends text to the LLM and embedding providers the user configured in `~/.everos/everos.toml`. Nothing else leaves the machine.

Never grant conversation access or switch the memory slot without the user's yes. Never write API keys yourself; ask the user to add them to `~/.everos/everos.toml`.

## Requirements

- OpenClaw 2026.8.1 (2.0) or later
- EverOS 1.2.3 or later
- Node.js for `npx`, and `uv` if EverOS is installed from source

## Step 1: Check whether EverOS is installed and running

```bash
curl -s http://127.0.0.1:8000/health
```

- A JSON answer means EverOS is running. Go to step 3.
- No answer: check whether the `everos` command exists (`everos --help`). If it exists, the plugin can start EverOS by itself; go to step 3. If it does not exist, do step 2.

## Step 2: Install EverOS (only if it is missing)

```bash
git clone https://github.com/EverMind-AI/EverOS.git
cd EverOS
uv sync
uv run everos init
```

`everos init` creates `~/.everos/everos.toml`. It is required before the first start. Ask the user to open that file and fill in the `api_key` fields (LLM, and optionally embedding and rerank). Then start the server:

```bash
uv run everos server start
```

Confirm with the health check from step 1.

## Step 3: Install the plugin

Recommended, interactive:

```bash
npx --yes --package @everos-ai/openclaw-plugin everos-setup
```

The installer asks before it accepts the memory capability and before it grants conversation access, points the plugin at the EverOS checkout when `everos` is not on the gateway's PATH, restarts the gateway, and runs a health check. Let the user answer its questions.

Manual alternative, only after the user agreed to the three points above:

```bash
openclaw plugins install @everos-ai/openclaw-plugin --accept-capabilities
openclaw config set 'plugins.entries.evermind-ai-everos.hooks.allowConversationAccess' true
openclaw gateway restart
```

If EverOS lives in a project virtualenv, also set `EVEROS_OC_START_CMD` to the absolute path of the `everos` binary and `EVEROS_OC_EVEROS_DIR` to the EverOS checkout, or use `everos-setup`, which sets both.

## Step 4: Verify

Ask the user to:

1. Send a fact about themselves, for example "My favorite coffee is espresso."
2. Start a new session with `/new` and send any message.
3. Ask "What coffee do I like?"

Extraction in EverOS runs in the background. Wait a few seconds between the steps. If the answer is wrong on the first try, wait and ask once more before troubleshooting.

## Troubleshooting

| Symptom | Fix |
|---|---|
| No recall and nothing is saved | Conversation access is not granted. With the user's yes, run `openclaw config set 'plugins.entries.evermind-ai-everos.hooks.allowConversationAccess' true`, then `openclaw gateway restart`. |
| Saving works, recall does not | `hooks.allowPromptInjection` is set to `false`. Remove that override or set it to `true`, then restart the gateway. |
| Backend connection failed | Check `EVEROS_OC_BASE_URL`, then `curl <baseUrl>/health`. |
| EverOS never starts by itself | The gateway cannot find `everos`. Set `EVEROS_OC_START_CMD` to the absolute binary path and `EVEROS_OC_EVEROS_DIR` to the EverOS checkout. |
| Asked right after telling, no memory yet | Extraction is asynchronous. Wait a few seconds. |
| Warning "user-track memory is DISABLED" | No user id was resolved. Set `EVEROS_OC_USER_ID`. |
| Another memory plugin is active | Check that `plugins.slots.memory` is `evermind-ai-everos`. |
| An image, audio file or document shows as a placeholder | In the EverOS checkout run `uv sync --extra multimodal`, configure `[multimodal]` in `~/.everos/everos.toml`, restart EverOS, and check `/health`. |

If EverOS is down, OpenClaw keeps working; memory pauses until EverOS is back.

## Settings

All optional, set in the plugin's config:

| Key | Default | Meaning |
|---|---|---|
| `EVEROS_OC_BASE_URL` | `http://127.0.0.1:8000` | Where EverOS listens |
| `EVEROS_OC_USER_ID` | resolved automatically | Identity for the user's memories |
| `EVEROS_OC_AGENT_ID` | `openclaw` | Identity for the agent's memories |
| `EVEROS_OC_START_CMD` | `everos server start` | Command used to start EverOS |
| `EVEROS_OC_EVEROS_DIR` | none | EverOS checkout, when `everos` runs from a virtualenv |

## Do not

- Do not install, switch the memory slot or grant conversation access without the user's yes.
- Do not set `hooks.allowPromptInjection` to `false`; recall needs it.
- Do not put API keys in the OpenClaw config or in chat. They belong in `~/.everos/everos.toml`, edited by the user.
- Do not confuse EverOS with EverMe. EverMe is a separate cloud product from the same company with its own plugin and account.
