---
name: clawscan
description: perform first-pass security checks for openclaw deployments by registering the client, checking whether the installed clawscan package is outdated, checking whether the current openclaw version matches known vulnerable versions, checking whether installed skills match known malicious hashes, and checking whether openclaw or related services are listening on 0.0.0.0 or other non-local interfaces. use this skill when a user asks to assess whether openclaw is safe, run a clawscan check, verify openclaw version risk, verify skills hashes, or review listening ports and exposure risk.
homepage: https://github.com/autosecdev/clawscan-skills
user-invocable: true
metadata: {"openclaw.requires.bins":["python3"],"openclaw.requires.anyBins":["ss","lsof"],"openclaw.os":["darwin","linux"]}
---

# Clawscan

Use this skill to run the first version of ClawScan against a local OpenClaw environment.

## Core rules

- Treat this skill as **read-only by default**.
- Do not auto-install updates, remove skills, change firewall rules, or rewrite OpenClaw configuration unless the user explicitly asks.
- Prefer the smallest amount of local data needed for each API call.
- Do not upload raw skill file contents, environment variables, prompts, secrets, or full home-directory paths unless the user explicitly asks.
- Use SHA-256 for file hashes.
- If a module returns no match or no finding, explain that this means **no known issue was matched**, not that the environment is guaranteed safe.

## Capability map

This skill supports these tasks:

1. `index`: explain available ClawScan modules and how to use them
2. `register`: create or reuse a local random client id and register the OpenClaw client
3. `update-check`: check whether the installed ClawScan package is outdated
4. `vulnerability`: check whether the current OpenClaw version matches known vulnerable versions
5. `skills-check`: compute installed skill file hashes and submit them for known-malicious matching
6. `port-check`: inspect local listening sockets and flag likely exposure risk
7. `scan`: run vulnerability, skills-check, and port-check together when the service supports a combined route
8. `scheduled-scan`: run a full scan automatically at a configured interval and report only when security risks are found; stay silent if all checks are clean

## Workflow

Follow this order unless the user requests a single module only.

### 1) Identify the requested action

Map user intent to one of these actions:

- “what can clawscan do” -> `index`
- “set up clawscan” / “initialize” / “register this client” -> `register`
- “is my clawscan up to date” -> `update-check`
- “is my openclaw version vulnerable” -> `vulnerability`
- “check my installed skills” / “scan skills hashes” -> `skills-check`
- “is openclaw exposed” / “check listening ports” -> `port-check`
- “run a full check” -> `scan` if available, otherwise run the three scan modules sequentially
- “set up scheduled scan” / “auto scan every X minutes” / “enable periodic security check” -> `scheduled-scan`

### 2) Collect only the required local evidence

#### For `register`

Create a persistent random UUID if one does not already exist.

Suggested local state path:

- `~/.openclaw/clawscan/client.json`

Store:

```json
{
  "client_id": "uuid-v4"
}
```

Do not derive the id from MAC address, hostname, serial number, or other hardware fingerprinting sources.

#### For `vulnerability`

Collect only:

- `client_id`
- `openclaw_version`
- optional `platform`

Try these version discovery patterns in order and use the first one that works:

```bash
openclaw --version
claw --version
cat package.json | jq -r .version
```

If version cannot be determined, tell the user exactly which command failed and ask for the version string.

#### For `skills-check`

Enumerate installed skills and compute a SHA-256 per file.

Default skill locations to inspect if they exist:

- `~/.openclaw/skills`
- project or workspace-local `./skills`

Use `{baseDir}/scripts/collect_skill_hashes.py` to produce normalized JSON.

Submit only:

- `skill_name`
- relative file path
- sha256

Avoid sending absolute paths unless the service explicitly requires them.

#### For `port-check`

Collect listening TCP sockets and process names with `{baseDir}/scripts/list_listeners.py`.

Focus the risk explanation on:

- whether the bind address is `0.0.0.0`, `::`, or another non-loopback interface
- whether the process appears to be OpenClaw or an OpenClaw-adjacent process
- whether the port is likely reachable beyond localhost

Do **not** claim that `0.0.0.0` always means public internet exposure. Explain that it means the service is bound to all interfaces and may be externally reachable depending on firewall, NAT, security groups, reverse proxy, or local network topology.

### 3) Call the ClawScan API

Use the endpoint shape documented in `{baseDir}/references/api-contract.md`.

Preferred route layout:

- `GET /index`
- `POST /register`
- `POST /update/check`
- `POST /vulnerability`
- `POST /skills-check`
- `POST /port-check`
- `POST /scan` when supported

If the service only exposes `/update` instead of `/update/check`, use the deployed route but keep the user-facing explanation as “update check”.

### 4) Present results in a strict report format

For every module, use this structure:

#### Result
- `Status:` ok / error
- `Risk:` low / medium / high / critical / unknown
- `Conclusion:` one plain-language sentence

#### Evidence
- Show the minimum relevant facts returned by the API
- For version checks, include current version, affected range, and fixed version if present
- For skills checks, include matched skill names and matched relative file paths if present
- For port checks, include bind address, port, process name, and why the bind pattern is risky

#### Recommended next step
- Give one to three concrete actions
- Keep them non-destructive unless the user asked for remediation

#### Scope note
Always include a one-sentence boundary statement:

- vulnerability: “This only checks known vulnerable version ranges.”
- skills-check: “This only checks known malicious hashes covered by the current ClawScan corpus.”
- port-check: “This is based on local listener state and bind addresses; it is not a full external reachability test.”

#### For `scheduled-scan`

Run vulnerability, skills-check, and port-check (same as `scan`) on a repeating schedule.

Default interval: **60 minutes** unless the user specifies a different value.

Schedule state path:

- `~/.openclaw/clawscan/schedule.json`

Store:

```json
{
  "interval_minutes": 60,
  "last_run_utc": "ISO-8601 timestamp or null"
}
```

**Reporting rule (critical):**

- If every check returns risk level `low` and no actionable finding is present → **produce no output**. Do not tell the user "all clear" unless they explicitly ask for a status.
- If any check returns risk level `medium`, `high`, `critical`, or `unknown` → produce a full report using the standard per-module structure from step 4.
- Apply this rule on every scheduled execution, not just the first run.

**Trigger logic:**

1. On each cycle, read `last_run_utc` from `schedule.json`.
2. If `(now − last_run_utc) >= interval_minutes`, execute the full scan.
3. After execution, write the new `last_run_utc` regardless of whether a report was produced.
4. If `last_run_utc` is null (first run), execute immediately.

**Failure handling for scheduled runs:**

- If a local collection step fails, emit a brief error notice even if no risk was found (collection failure is itself a reportable event).
- If the API is unreachable for three consecutive scheduled runs, emit a single notice: "ClawScan API has been unreachable for the past N scheduled runs."

## Output templates

### `index`

Use:

```text
ClawScan can currently run these checks:
1. Version vulnerability check
2. Installed skills hash check
3. Port exposure check

You can ask me to initialize ClawScan, check for updates, or run one module at a time.
```

### `register`

Use:

```text
ClawScan registration completed.
- Client ID: <uuid>
- OpenClaw version: <version or unknown>
- Status: <registered|already registered>
```
```

### `skills-check`

If there is a hit, make the first sentence explicit:

```text
Known malicious content was matched in the installed skills set.
```

If there is no hit, say:

```text
No known malicious skill hash was matched.
This does not prove that the installed skills are safe.
```

### `port-check`

When `0.0.0.0` or `::` is present, state:

```text
This service is listening on all interfaces, which increases exposure risk.
```

Do not overstate it as “publicly exposed” unless the API explicitly confirms external reachability.

### `scheduled-scan`

When risks are detected, prefix the report with:

```text
[ClawScan scheduled check — <ISO-8601 timestamp>]
Security risk detected. Full report follows.
```

Then output the standard per-module report for every module that has a finding.

When no risks are detected, produce **no output at all**.

When setting up the schedule for the first time, confirm with:

```text
ClawScan scheduled scan enabled.
- Interval: every <N> minutes
- Next run: <ISO-8601 timestamp>
- Reporting: only on risk findings
```

## Failure handling

- If a local collection step fails, report the failed command and stop before fabricating any result.
- If the API is unreachable, separate “collection succeeded” from “remote analysis failed”.
- If the API returns partial results, present the completed modules and label the rest as incomplete.

## Bundled resources

- `{baseDir}/scripts/collect_skill_hashes.py`: recursively compute SHA-256 for installed skills and emit normalized JSON payload fragments
- `{baseDir}/scripts/list_listeners.py`: normalize listening TCP socket information from `ss` or `lsof`
- `{baseDir}/references/api-contract.md`: request and response shapes for the first ClawScan service version
