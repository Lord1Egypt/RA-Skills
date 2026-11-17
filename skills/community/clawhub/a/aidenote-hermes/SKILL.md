---
name: aidenote-hermes
description: "Install and operate the verified AideNote local connection suite for Hermes, then query real AideNote recording notes, transcripts, summaries, extracted todos/action items, knowledge bases, account status, and mobile bridge health. Use whenever the user mentions AideNote, SlonAide, recording notes, meeting minutes, transcripts, summaries, today's tasks, todos, follow-ups, action items, knowledge bases, installing the AideNote connection, or connecting the AideNote mobile app to this computer."
license: MIT
metadata:
  hermes:
    version: 1.2.9
    author: AideNote Team
    tags: [AideNote, SlonAide, recordings, transcription, summaries, todos, meetings, knowledge-base, mobile-bridge]
    category: productivity
---

# AideNote for Hermes

Use the bundled scripts to retrieve real AideNote data. Do not infer account data from conversation history.

## Mandatory behavior

1. Run an AideNote command before answering any question about recordings, meetings, transcripts, summaries, todos, action items, or knowledge bases.
2. Never answer that the user has no todos or recordings unless the corresponding command completed successfully and returned an empty result.
3. Never invent IDs, titles, dates, transcript text, summaries, or task status.
4. Never ask the user to paste an API key into chat. If setup is missing during an authorized install, start the built-in pairing flow and show only its 8-character code.
5. Do not print environment variables, authorization headers, access tokens, or AideNote configuration files.
6. Summarize command JSON for the user instead of dumping raw payloads, unless raw JSON is explicitly requested.
7. Run `bridge.py install --confirm` only after the user explicitly asks to install, configure, repair, or connect AideNote on this computer. A data question alone is not installation consent.

The API command is:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py COMMAND [OPTIONS]
```

If `python3` is unavailable on Windows, use `python` with the same arguments.

## One-time pairing

When the user explicitly asks to install or connect AideNote, run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/bridge.py install --confirm
```

If credentials are missing, the command immediately returns `pairing_required` and an 8-character `pairingCode`. Tell the user to open AideNote, add or edit the Hermes assistant, enter that code, and tap **Confirm connection**. A detached local worker then receives the account-bound credential, installs the verified connection suite, and removes the relay pairing session. The user does not need to paste an API Key or run another command.

Use `bridge.py status` to check progress. Its `pairing.status` changes from `pending` to `installing`, then `installed` or `failed`. Never print or inspect the private pairing state file.

`scripts/configure.py` remains a manual recovery option only when App pairing is unavailable. It must be run directly in a local terminal; never ask the user to send the key in chat.

## Choose the command

| User intent | Command |
|---|---|
| Check connection or account | `health` or `user-info` |
| List/search recent recordings | `recordings` |
| List recordings shared with me | `shared-recordings` |
| Read transcript or AI summary | `recording-detail` |
| Ask about todos, tasks, action items, or follow-ups | `todos` |
| List knowledge bases | `knowledge-bases` |
| List files in a knowledge base | `knowledge-files` |
| List recordings in a knowledge base | `knowledge-recordings` |
| Check mobile bridge state | `bridge.py status` |
| Install/configure the local connection suite | `bridge.py install --confirm` |
| Check whether the local connection suite is installed | `bridge.py status` |

## Common workflows

### Recent recordings

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py recordings --page 1 --page-size 10
```

Add `--keyword "text"` when the user gives a search term. Present titles, dates, durations, and processing status. Preserve the returned recording ID for follow-up detail requests.

### Transcript or summary

If the user did not provide a recording ID, list recent recordings first and select the matching record. Then run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py recording-detail --file-id "RECORDING_ID"
```

Answer only from the returned detail. Distinguish transcript content from the AI summary and extracted action items.

### Recordings shared with me

For requests such as "分享给我的录音" or "别人共享了哪些音频", run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py shared-recordings --page 1 --page-size 10
```

Do not use the personal `recordings` command for shared-with-me requests.

### Todos and action items

For requests such as "今天有哪些待办", "最近有什么任务", or "会议里有哪些行动项", run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py todos --recording-page-size 20 --page-size 50
```

Completed items are excluded by default. Add `--include-done` only when the user asks for completed/history items. Group results by source recording when that improves readability.

### Knowledge bases

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py knowledge-bases
```

Use the returned knowledge-base ID for:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py knowledge-files --knowledge-base-id ID
```

Add `--folder-id ID` or `--keyword "text"` only when needed.

For recordings stored anywhere inside a knowledge base, including nested folders, run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/aidenote.py knowledge-recordings --knowledge-base-id ID
```

Use this command instead of manually filtering `knowledge-files` output.

## Mobile bridge

The local connection suite enables the AideNote mobile app to reach this computer's Hermes API through the AideNote relay. It installs the AideNote tunnel, the AideNote MCP server, the WorkBuddy bridge, login/startup services, and Hermes API settings. Existing Hermes and OpenClaw tokens are preserved.

Check status without changing the system:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/bridge.py status
```

When the user explicitly says "安装 AideNote 连接", "配置手机连接", "修复 AideNote bridge", or equivalent, run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/bridge.py install --confirm
```

The command downloads the official installer over HTTPS, verifies its pinned SHA-256 digest, and passes only the required local credential and a restricted environment. The official installer verifies every downloaded binary, configures Hermes API port `8642`, synchronizes the Hermes API token into the tunnel config, and enables login/startup services. Do not substitute another download URL, bypass checksum verification, or construct a shell pipeline.

After installation, inspect the returned `status`. Success requires all of the following:

- `installed` is `true`.
- `upToDate` is `true`.
- `hermesTokenConfigured` is `true`.
- `hermesStartupConfigured` is `true`.
- `ports.hermes.reachable` is `true`.

If the suite is installed but `ports.hermes.reachable` is `false`, repair the supervised Hermes Gateway before reporting a relay failure:

```bash
hermes gateway status
hermes gateway start
```

If the service definition is missing or stale, and the user already authorized repair, run:

```bash
hermes gateway install --force --start-now --start-on-login
```

Then rerun `bridge.py status` and require port `8642` to be reachable. Do not expose `API_SERVER_KEY`. If Hermes reports `No inference provider configured`, the bridge is healthy but the model provider is not; direct the user to complete `hermes model` locally.

If the install command returns `pairing_required`, present the pairing code and App steps. If installation is not explicitly authorized, show the status and ask whether the user wants the verified connection suite installed.

## Error handling

- `pairing_required`: show the 8-character code and direct the user to AideNote > Add Assistant > Hermes.
- `pairing_network_error`: report that the pairing service could not be reached and keep the existing installation unchanged.
- `pairing_not_found`: the code expired; rerun the authorized install command to create a new code.
- `missing_credentials`: start the pairing flow through `bridge.py install --confirm`; use `configure.py` only as manual recovery.
- `insecure_credentials`: tell the user to restrict the credential file to owner-only access and rerun configuration.
- `authentication_failed`: ask the user to regenerate or reconfigure the AideNote API Key locally.
- `network_error`: report that AideNote could not be reached; do not claim the account has no data.
- `api_error`: report the safe error message and operation; never expose credentials.
- `confirmation_required`: ask the user for explicit installation consent; do not add `--confirm` preemptively.
- `checksum_mismatch`: stop and report that installer verification failed; never bypass the check.
- `installer_failed` or `verification_failed`: report the safe error, run `bridge.py status`, and point the user to the official guide if manual recovery is needed.
- `upToDate` is `false`: run the authorized install again to upgrade the local connection suite before diagnosing relay or token failures.
- Hermes port `8642` unavailable: run `hermes gateway status`, start or reinstall the supervised Gateway after authorization, then rerun `bridge.py status`.
- `No inference provider configured`: tell the user to run `hermes model` locally; do not treat this as a tunnel or account failure.
- Unsupported platform: automatic bridge installation currently supports macOS and Windows.

For endpoint and output details needed during maintenance, read [references/api-contract.md](references/api-contract.md).
