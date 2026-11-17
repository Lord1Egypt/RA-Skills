# Security Policy

## Data handling

| Data | Where | Protection | Needed for |
|---|---|---|---|
| Chess-Results personal number + password | macOS Keychain (service `chess-results`), Windows Credential Manager or Linux Secret Service — or, where none exists, `~/.config/chess-results/credentials.json` | the system store; the file must be mode `0600` and the user's own, or it is refused | result entry only |
| Chess-Results session cookie | memory of the running process | never written to disk | result entry only |
| Public pages (searches, tournament pages) | `~/.cache/chess-results/pages` (or the host's plugin data folder) | plain cache of public HTML | queries |
| Club settings | `chess-results.json` in the project | no secrets | result entry only |

All queries read public pages and need no login.

## What the skill accesses — and what it does not

- **Credentials:** only its own entry. On macOS it runs
  `/usr/bin/security find-generic-password -s chess-results` and
  `add-generic-password -s chess-results` (written by `cli.py login`), nothing else.
  It does not read SSH keys, cloud credentials, browser passwords, iCloud Keychain or
  other Keychain items. Scanners that flag "credential access" are seeing this.
- **Agent configuration:** the code never reads `~/.claude`, `~/.codex`, `~/.openclaw`
  or similar. SETUP.md *tells the user* which lines to add to their own Codex or
  OpenClaw configuration; the skill does not do it.
- **Network:** `chess-results.com` and its `s1`–`s3` nodes only, over HTTPS. Nothing is
  sent anywhere else. Requests are spaced and retried with back-off; the site is not
  crawled.
- **Code:** no remote code is fetched or executed; no shell commands other than the
  `security` tool on macOS.

## The password never reaches the agent

`cli.py login` asks for it with a hidden prompt in the user's own terminal and writes
it straight to the store. No command or tool prints it: `status` reports only whether
a login exists, where, and the personal number. Agents should never ask for the
password in chat (SKILL.md says so).

## Writes to Chess-Results need an explicit yes

Saving team results publishes them to the whole league, so every write path checks
first and saves only on an explicit confirmation:

- MCP: `enter_match_report` refuses unless called with `confirm=true`, which the skill
  instructs agents to pass only after the user approved the checked results.
- Command line: `cli.py enter` checks, shows the result, and saves only after the
  user types `yes`; without a terminal it refuses unless given `--yes`.
- In both, a match is saved only when Chess-Results' own check ("Eingabe Prüfen")
  reports no error or notice, every player matches the sheet, the score agrees, and
  the entry window is open. The overview is re-read afterwards to confirm.

Saved results can be changed again on Chess-Results, which logs who saved them.

## Reporting a vulnerability

Open an issue at https://github.com/odrobnik/chess-results-skill/issues, or for
anything sensitive contact the author through GitHub privately.
