# Fact Table Schema

Standard fields for the release fact table (Step 3 of the main workflow). One row per release; fill `unknown` rather than guessing.

| Field | What to record | Source quality floor |
|---|---|---|
| Date | Announced date and general-availability date, if different | Official post or repo tag |
| Release status | Preview / beta / stable / deprecated | Official status label |
| License | Full license name and notable restrictions | LICENSE file or docs |
| Runtime architecture | Execution model, sandbox, process isolation | Architecture doc |
| Supported modes | CLI / IDE / API / headless / MCP | Official docs |
| Model & provider scope | Which models or providers are supported | Official docs |
| Session & logging | Event log, resume, replay support | Docs or verified demo |
| Sandbox & security | Isolation mechanism, approval gates, policy layer | Security doc or paper |
| Extensibility | Skills / plugins / hooks / custom tools | Developer docs |
| Known limitations | Officially acknowledged gaps | Release notes |

Rules:

- Never promote a community observation into an official field value; mark it `[community-reported]`.
- If a field cannot be sourced, write `unknown` — an empty cell invites invention.
- Dates use the platform's official timezone or state the timezone used.
