---
name: application-manager
description: Manage a shared Windows application registry and control which agents may run registered apps. Use when the user asks for the application manager, application registry, app registry, register an application, list registered apps, add or edit an app entry, change which agents may run an app, change app mode (full, allowlist, off), or launch a registered Windows application through the registry.
---

# Application Manager

Operate a chat-first manager for a shared application registry.

Treat the registry file as the source of truth.
Prefer updating the registry over inventing one-off launch rules in chat.
Keep the interaction menu-driven when the user asks to manage the registry directly.
Also use the registry to resolve natural-language application launch requests like `open last z`.

## Core rules

- Use one shared registry file for registered applications.
- Treat each app entry as a policy object, not just a path shortcut.
- Do not guess executable paths.
- Prefer storing enough information to both start and stop an app reliably.
- For Windows apps, a shortcut path alone may be enough to launch but not enough to stop.
- When known, store the real runtime executable path and process name.
- Show the current stored values before editing an existing entry.
- Confirm before saving additions, edits, deletions, or policy changes.
- When asked to launch a registered app, first check whether the requesting agent is allowed by the app entry.
- If mode is `off`, do not launch the app.
- If mode is `allowlist`, only agents listed in `allowed_agents` may launch it.
- If mode is `full`, any agent may launch it.
- Prefer stable launcher shapes for Windows execution, such as `cmd.exe /c start "" "<path>"`, rather than ambiguous interpreter-style launch forms.
- Keep entries human-readable and pretty-printed in JSON.

## Canonical registry location

Preferred registry path:

- `~/.openclaw/registries/application_registry.json`

If the registry file does not exist yet:
- say so plainly
- offer to create it
- initialize it as an empty JSON object: `{}`

## Trigger phrases

Treat requests like these as a request to open this skill's wizard:

- `application manager`
- `open application manager`
- `show application manager`
- `application registry`
- `open application registry`
- `show application registry`
- `app registry`
- `register an application`
- `add application`
- `edit application`
- `change application policy`
- `who can run this app`
- `list registered apps`

Also treat natural-language app-launch requests as a request to use this skill's registry lookup and launch behavior, for example:

- `open last z`
- `launch last z`
- `run last z`
- `start last z`
- `open <registered app name>`
- `launch <registered app name>`
- `run <registered app name>`
- `start <registered app name>`

## Start menu

When this skill is triggered for registry management, open an app-first menu.

If the registry has entries, show the apps first as numbered launch targets.
Choosing an app number should launch it directly.
Management actions should be typed as words, not numbered.

Preferred shape:

```text
Application Manager
Registry file: ~/.openclaw/registries/application_registry.json

Applications
1. Last Z

Commands
- add
- edit
- delete
- policy
- validate
- quit

Reply with an app number to launch it, or type `add`, `edit`, `delete`, `policy`, `validate`, or `quit`.
```

If multiple apps exist, continue numbering only the app list.

If the registry file exists but is empty, show:

```text
Application Manager
Registry file: ~/.openclaw/registries/application_registry.json
Status: no applications registered yet

Commands
- add
- quit

Reply with `add` or `quit`.
```

If the registry file does not yet exist, say:

```text
Application Manager
Registry file: ~/.openclaw/registries/application_registry.json
Status: not created yet

Commands
- create
- quit

Reply with `create` or `quit`.
```

## Menu behavior

### Start screen app launching

On the start screen, list registered applications as numbered launch targets.
Choosing an app number launches that app directly from the menu.
Treat only app numbers as numeric choices.
Treat management commands as words like `add`, `edit`, `delete`, `policy`, `validate`, and `quit`.

When launching from the start screen:
- read the registry fresh
- map the chosen number to the selected app
- evaluate launch access using the current agent id
- if mode is `off`, refuse launch plainly
- if mode is `allowlist`, allow launch only when the current agent id is in `allowed_agents`
- if mode is `full`, allow launch
- if access is allowed, prefer a stable Windows launcher shape:
  - `cmd.exe /c start "" "<launch_path>"`
- report success or the exact launcher error
- after the result, repeat the start menu

If the user wants details instead of launch, the skill may show the selected app entry before acting only when needed for confirmation or troubleshooting.

### Add application

Prompt for:
- friendly app name
- Windows launch path to executable or shortcut
- optional real runtime executable path
- optional process name used to stop the app
- mode: `full`, `allowlist`, or `off`
- allowed agents if mode is `allowlist`

Rules:
- use the friendly app name as the registry key unless a different stable key is already established
- reject duplicate names unless the user explicitly switches to Edit
- if mode is `full`, store an empty `allowed_agents` array
- if mode is `off`, store an empty `allowed_agents` array
- if mode is `allowlist`, require at least one allowed agent

Before saving, show the proposed entry and ask for explicit confirmation.
After save, repeat the start menu.

### Edit application

Show the numbered list of apps.
The user chooses an entry number.
Allow `back` or `quit`.

Then show:

```text
Edit Application
Selected: Last Z

Current values:
- launch_path: C:\Users\greg\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Last Z\Last Z.lnk
- runtime_exe: C:\Users\greg\AppData\Local\Last Z\Game\Survival.exe
- process_name: Survival.exe
- mode: allowlist
- allowed_agents: system_engineer

Reply with:
1. Edit launch path
2. Edit runtime executable path
3. Edit process name
4. Edit mode
5. Edit allowed agents
6. Edit all
Type `back` to go back or `quit` to exit.
```

Show the proposed updated entry before writing.
Ask for explicit confirmation.
Then repeat the start menu.

### Delete application

Show the numbered list.
The user chooses an entry number.
Allow `back` or `quit`.

Then show the selected entry and ask for explicit confirmation.
Do not delete without confirmation.
After delete, confirm success and repeat the start menu.

### Change launch policy

Show the numbered list.
The user chooses an entry number.
Allow `back` or `quit`.

Then offer:

```text
Change Launch Policy
Selected: Last Z
Current mode: allowlist
Current allowed_agents: system_engineer

Reply with:
1. Set mode to full
2. Set mode to allowlist
3. Set mode to off
4. Edit allowed agents only
Type `back` to go back or `quit` to exit.
```

Rules:
- if switching to `full`, clear `allowed_agents`
- if switching to `off`, clear `allowed_agents`
- if switching to `allowlist`, require at least one allowed agent
- always show the final proposed policy before saving
- ask for explicit confirmation before writing

### Validate registry

Read the registry fresh and validate each entry.

For each app, check:
- entry is a JSON object
- `launch_path` exists and is non-empty
- `runtime_exe` is optional
- `process_name` is optional
- `mode` is one of `full`, `allowlist`, `off`
- `allowed_agents` is an array
- `allowed_agents` is non-empty when mode is `allowlist`

Display grouped results:
- valid
- incomplete
- malformed
- policy mismatch

Do not guess repairs.
If JSON is malformed, stop and report the parse error clearly.
After reporting, repeat the start menu.

### Quit

Exit cleanly with a short completion message.

## Registry shape

Use this JSON shape:

```json
{
  "Last Z": {
    "launch_path": "C:\\Users\\greg\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Last Z\\Last Z.lnk",
    "runtime_exe": "C:\\Users\\greg\\AppData\\Local\\Last Z\\Game\\Survival.exe",
    "process_name": "Survival.exe",
    "mode": "allowlist",
    "allowed_agents": [
      "system_engineer"
    ]
  }
}
```

Keep the schema simple unless a stronger need appears later.
Do not add extra metadata fields by default.

## Launch behavior guidance

When a user asks to run a registered app, including natural-language requests like `open last z`:
- read the registry fresh
- match the requested app name against friendly names in the registry, preferring exact case-insensitive match before looser contains matching
- if one clear match is found, use it
- if multiple plausible matches are found, ask a short disambiguation question
- if no match is found, say so plainly and offer to open the Application Manager menu
- evaluate access using the current agent id
- if access is denied, say so plainly
- if access is allowed, prefer a stable Windows launcher shape such as:
  - `cmd.exe /c start "" "<launch_path>"`
- report success or the exact launcher error

When a user asks to stop or close a registered app:
- read the registry fresh
- match the requested app name against friendly names in the registry
- if `process_name` is present, prefer stopping by that process name or PID discovery based on that process
- if only `runtime_exe` is present, identify the running process from that executable path, then stop it
- if neither `process_name` nor `runtime_exe` is present, say the app can be launched but does not yet have enough stop metadata stored
- report success or the exact stop error

If a direct `.lnk` or interpreter-style launch fails due to execution-policy shape, retry with a stable launcher executable before concluding the app cannot be opened.

## Implementation guidance

When reading or writing the registry:
- create `~/.openclaw/registries/` if needed
- read the current JSON fresh each time before mutation
- preserve valid existing entries
- write pretty-printed JSON for readability
- never leave the file partially written

If JSON is malformed:
- stop
- report the parse error clearly
- do not guess repairs without approval

## Optional reference

If needed for future expansion, add references under `references/` for:
- registry schema notes
- launcher patterns
- agent-policy examples
