# EchoMemory Normal Usage

Use this reference for everyday EchoMemory requests after setup is already working.

## Current command surface

- `/echo-memory onboard`
- `/echo-memory view`
- `/echo-memory status`
- `/echo-memory search <query>`
- `/echo-memory graph`
- `/echo-memory graph public`
- `/echo-memory sync`
- `/echo-memory whoami`
- `/echo-memory help`

## Natural-language routing

Use onboarding when the user asks how to install, configure, authenticate, connect with email, sign up, use the manual API key fallback, or troubleshoot the plugin.

Use the local UI when the user asks to:

- open local memories
- browse markdown memories
- launch the localhost viewer
- get the local workspace URL
- check the installed plugin version in the UI
- check whether a packaged install has an update available

Use search when the user asks to:

- remember prior notes
- find stored context on a topic
- look up plans, dates, people, preferences, or decisions from imported memories

Use status when the user asks:

- whether EchoMemory is working
- when the last sync ran
- what the current import state is

Use sync when the user asks to:

- sync now
- refresh the cloud copy
- upload local markdown files

Use graph commands when the user explicitly wants the cloud graph or public memory page.

## Local UI versus graph

Do not confuse these two surfaces:

- local UI: localhost viewer for local markdown files
- graph: iditor.com pages for private or public cloud graph views

If the user says "view my memories" without saying graph, iditor, or public page, prefer the local UI.

Do not confuse local UI with cloud sync either:

- local UI can show the wider OpenClaw workspace markdown structure
- cloud retrieval depends on what was actually imported from `memoryDir`
- a file being browsable locally does not guarantee it will appear in cloud search
- packaged installs can also expose plugin version and update controls in the setup sidebar

Common local file expectations:

- `workspace/MEMORY.md` for curated long-term memory
- `workspace/memory/YYYY-MM-DD.md` for daily logs
- topic or project subfolders for local organization

## Tool mapping

- `echo_memory_onboard`: setup, onboarding, commands, troubleshooting
- `echo_memory_local_ui`: localhost viewer URL and optional browser open
- `echo_memory_search`: semantic cloud memory retrieval
- `echo_memory_status`: local sync summary plus backend import status
- `echo_memory_sync`: push local markdown memories into EchoMemory cloud
- `echo_memory_graph_link`: private graph login link or public memories link

## Update-panel guidance

When users ask about the new `Plugin updates` section:

- treat packaged installs as the intended update target
- treat linked repos and local checkouts as development installs
- if the update panel shows route `404` errors or mismatched version behavior, verify which active plugin copy OpenClaw is actually loading
