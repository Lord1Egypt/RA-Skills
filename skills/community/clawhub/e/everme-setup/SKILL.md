---
name: everme-setup
description: Set up, verify, or repair EverMe memory for OpenClaw. Use when the user asks to install EverMe or the EverMe memory plugin, wants OpenClaw to share the work memory they already use in other AI tools, or reports that EverMe is not recalling or not saving in OpenClaw.
---

# EverMe Setup for OpenClaw

EverMe is work memory for a person and the AI tools they use: one memory of past decisions, solved problems and corrections, kept in the user's EverMe account and shared by every tool they connect. The official OpenClaw plugin `@everme/openclaw` is a context-engine plugin. After setup the user just chats: the plugin recalls related memories before each reply and saves each finished turn, including tool calls and results.

Source: https://github.com/EverMind-AI/EverMe/tree/main/plugins/openclaw (Apache-2.0). Account and memory management: https://everme.evermind.ai

## Before you start, tell the user

Say these three things and wait for a yes before installing:

1. The plugin becomes OpenClaw's context engine and sets the `memory` slot to `none`, so another memory plugin stops being used.
2. Each finished turn of the conversation, with its tool calls and results, is sent to the user's EverMe account at `api.everme.evermind.ai` and saved there. Recall sends the current request as a search query. If the user runs EverMe Desktop with local memory turned on, memory stays on that Mac instead.
3. An EverMe account is required. The user signs in themselves in the browser; you never see or type the password.

Never install or sign in without the user's yes. Never ask for, print or store the agent token. The installer writes it to the OpenClaw config.

## Requirements

- OpenClaw installed and working
- Node.js, for `npm`
- An EverMe account (sign up at https://everme.evermind.ai)

## Step 1: Install the EverMe CLI

```bash
npm install -g @everme/cli
evercli --version
```

## Step 2: Sign in

```bash
evercli auth login
```

This opens the browser. Ask the user to finish the sign-in there, then continue.

## Step 3: Install the plugin

```bash
evercli plugin install openclaw
```

The command installs `@everme/openclaw`, registers this OpenClaw as an agent in the user's EverMe account, and writes the plugin's config block (API base, agent id, agent token, and the `contextEngine` slot). Restart the OpenClaw gateway if the command does not do it:

```bash
openclaw gateway restart
```

## Step 4: Verify

Ask the user to:

1. Tell OpenClaw a work fact, for example "We decided to ship v2 pricing on December 1."
2. Start a new session with `/new` and send any message.
3. Ask "What did we decide about v2 pricing?"

Memories are extracted in the background, by default after every fifth turn and when a session is compacted or closed. If the answer is missing right after step 1, close the session, wait a little, and ask again before troubleshooting. The user can also see what was saved at https://everme.evermind.ai.

## Troubleshooting

| Symptom | Fix |
|---|---|
| No recall and nothing is saved | Check that `plugins.slots.contextEngine` is `@everme/openclaw` and that `@everme/openclaw` is in `plugins.allow` and enabled. Run `evercli plugin install openclaw` again to rewrite the config, then restart the gateway. |
| Worked before, stopped after an OpenClaw upgrade | Update the plugin: run `evercli plugin install openclaw` again. OpenClaw 2026.8 and later use the plugin's `commitTurn` path, which older plugin versions do not have. |
| Sign-in expired or the token was revoked | Run `evercli auth login`, then `evercli plugin install openclaw`. |
| Error says the account keeps its memory on another Mac | The account uses local memory on that Mac. To save from this computer, the user switches the account back to the cloud in EverMe Desktop on that Mac, or on the web. |
| Another memory plugin is still active | Set `plugins.slots.memory` to `none` and `plugins.slots.contextEngine` to `@everme/openclaw`, or rerun the installer. |

If EverMe cannot be reached, OpenClaw keeps working without memory.

## Settings

Written by the installer under `plugins.entries["@everme/openclaw"].config`. Change them only when the user asks.

| Key | Default | Meaning |
|---|---|---|
| `apiBase` | `https://api.everme.evermind.ai` | EverMe API |
| `topK` | 5 | Memories recalled per turn |
| `flushEveryTurns` | 5 | Extract memories after this many turns |

## Uninstall

```bash
evercli plugin uninstall openclaw
openclaw gateway restart
```

Saved memories stay in the user's EverMe account until the user deletes them at https://everme.evermind.ai.

## Do not

- Do not install, sign in or change the context engine without the user's yes.
- Do not print, copy or move the agent token (`evt_...`). Treat it as a secret.
- Do not confuse EverMe with EverOS. EverOS is a separate, self-hosted memory layer from the same company with its own OpenClaw plugin (`@everos-ai/openclaw-plugin`).
