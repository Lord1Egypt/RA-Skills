# Live MCP tools (honesty)

Only these names exist on the live Artifact Publisher MCP surface
(`ARTIFACT_RELAY_TOOLS` in `packages/mcp/src/contracts.ts` / `tools/list`).
Do **not** invent tools. Do **not** name `get_platform_capabilities` until that
tool ships in contracts (ADR 0026 is architecture-only today).

| Tool | Role |
| --- | --- |
| `publish_artifact` | Publish self-contained HTML → stable unlisted share link |
| `update_artifact` | Replace HTML behind the **same** URL (new version retained) |
| `set_artifact_access` | Change who can open / comment on an artifact |
| `get_feedback` | Pull anonymous page / passage comments (pull-only) |
| `reply_to_feedback` | Reply to a feedback item from the agent |
| `list_artifacts` | List artifacts visible to the connected workspace |
| `revoke_artifact` | Stop serving an artifact URL |
| `configure_workspace` | Workspace-level settings for the connected account |
| `get_artifact_board` | **Deprecated alias** — prefer state tools |
| `reset_artifact_board` | **Deprecated alias** — prefer state tools |
| `get_artifact_state` | Read artifact shared state |
| `set_artifact_state` | Set state keys atomically (null stored, not deleted) |
| `reset_artifact_state` | Clear all state (HTML unchanged) |
| `get_authoring_guide` | Themes / authoring guidance before large styling |

Server name: `artifact-publisher` · skill/server version aligned to `0.1.0`.
Endpoint: `https://app.artifactpublisher.com/mcp` (streamable HTTP).

## Hard rules (repeat)

1. After `publish_artifact` / `update_artifact`, report **`artifact.url`** first.
   Use `artifact.viewer_url` when a version pin helps. Never make the raw
   artifact-origin URL the primary share link.
2. Never print/paste/commit credentials (`ar_pk_…`, `ar_oat_…`, tokens, cookies,
   Authorization headers).
3. Do not invent HTML when a real file exists — read the file and pass contents.
4. Call `get_authoring_guide` before large styling; prefer
   `<meta name="ap-theme" content="firn">`.
5. Feedback is optional/secondary; `get_feedback` is pull-only.
6. Thin MCP wiring only — no shell/curl wrappers, no binary downloads.
