# MCP and REST configuration

## Endpoint

```
https://dashboard.deutero.ai/mcp
```

`https://agents.deutero.ai/mcp` serves the same server. Use **https** — an `http://` URL will not connect. The path is exactly `/mcp` with nothing after it; a 404 on `/mcp/mcp` means a client appended its own path.

The same API is plain REST at `https://dashboard.deutero.ai/study-api/api/v1/`, documented at `/study-api/api/v1/docs`. Every MCP tool is exactly one REST route with the same parameters — the tool name is the route *function's* name, though, not its URL path (`find_interviews_by_external_id` is `GET /studies/{study_id}/interviews/by-external-id`), so read the paths off `/docs` rather than deriving them from tool names. This is the surface a **server** uses: MCP tools are available to an agent in a session, not to the user's own backend, so anything that has to run in a request handler or a nightly job goes through REST with an API key — in Python, through the `deutero` SDK (`python-sdk.md`), which wraps every route and names each method after its resource rather than the tool.

## OAuth

Preferred wherever the client supports remote MCP authorization. The user signs in with their Deutero account; no secret lands in a file. Authorized clients are listed under **Connected Applications** in Settings and can be revoked there.

```json
{
  "mcpServers": {
    "deutero": {
      "type": "streamable-http",
      "url": "https://dashboard.deutero.ai/mcp"
    }
  }
}
```

The first tool call triggers the authorization prompt. It needs a browser and a human; an agent cannot complete it unattended. If the user is on a headless machine, use an API key instead.

## API keys

Better for IDEs, scripts and CI. Keys are scoped to the whole organization, not to a project or study.

**Generating one**

1. **Settings** from the account menu (top right).
2. Scroll to **Generate API Key**.
3. Enter a **Label** — this is how the key is recognised later, so name it after the machine or client that will hold it.
4. **Generate API Key**, then copy it from the dialog. **It is shown only once.** The dialog also offers a ready-made `DEUTERO_API_KEY=…` line.

Keys are listed below the form with label, prefix, status, creation and last-used dates. **Disable** suspends a key; deleting removes it. Rotate by generating the replacement, switching the client over, confirming with `health_health_get`, then deleting the old one.

**Claude Code**

```bash
claude mcp add --transport http deutero https://dashboard.deutero.ai/mcp \
  --header "X-API-Key: $DEUTERO_API_KEY"
```

**Cursor** (`~/.cursor/mcp.json`), **Windsurf** (`~/.windsurf/mcp.json`), **Claude Desktop** (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "deutero": {
      "url": "https://dashboard.deutero.ai/mcp",
      "headers": { "X-API-Key": "${env:DEUTERO_API_KEY}" }
    }
  }
}
```

Keep the key in an environment variable rather than inline in a file that might be committed. Restart the client after editing its configuration.

**REST**

```bash
curl -H "X-API-Key: <your-api-key>" \
  https://dashboard.deutero.ai/study-api/api/v1/projects
```

```python
from deutero import Deutero
print(Deutero().projects.list())   # DEUTERO_API_KEY from the environment
```

The key also works as `Authorization: Bearer <key>` — either header is fine.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Tools do not appear | Client has not reloaded. Restart it, then check its MCP log. |
| 401 Unauthorized | Key wrong, disabled or deleted, or stray whitespace in the header. Regenerate in Settings. |
| 402 | Out of credits. Check **Billing & Usage**; `get_credit_balance` reports the same number. On `publish_study`, read `detail.code`: `plan_limit_reached` is the open-study limit, not credits. |
| 403 Upgrade required | Plan does not include the feature — simulations and Interview Flow on Hobby, graph mode below Pro, premium tier below Pro, image questions on Hobby, custom CSS below Pro. The message names the plan needed; see `plan-limits.md`. |
| 403 on `set_theme` without `study_id` | Only an organization admin can set the organization's theme. Set a study's theme instead, or ask an admin. |
| 422 `invalid_theme` | A theme value is not allowed or text would be unreadable; `detail.problems` lists each one. See `plan-interview-research/references/branding.md`. |
| 404 on `/mcp/mcp` | URL must be exactly `/mcp`. |
| 409 on `set_graph` / `patch_graph` | Someone edited the flow after you read it. Re-read `get_graph` and retry with the new `graph_version`. |
| 409 `study_locked` | The study is open to participants, so its interview configuration is locked. With the user's go-ahead: `pause_study`, edit, `publish_study`. |
| 409 / 422 on `publish_study` | A refusal with a `detail.code`. See `plan-interview-research/references/publishing.md`. |
| OAuth prompt never appears | Client does not support remote MCP authorization. Use an API key. |

## Tool inventory

100 tools. Names are exact.

- **Projects and studies** — `list_projects`, `create_project`, `get_project`, `update_project`, `create_study`, `list_studies`, `get_study`, `update_study`, `draft_study`, `draft_study_from_site`
- **Publication** — `get_publication_status`, `validate_study`, `publish_study`, `pause_study`
- **Welcome and consent** — `get_welcome`, `set_welcome`, `generate_welcome`, `list_welcome_translations`, `upsert_welcome_translation`, `delete_welcome_translation`, `upload_welcome_hero`, `delete_welcome_hero`
- **Brand theme** — `get_theme`, `set_theme`
- **Screening** — `get_screening`, `set_screening_settings`, `create_screening_question`, `update_screening_question`, `delete_screening_question`, `reorder_screening_questions`
- **Characteristics** — `get_characteristics`, `set_characteristics_settings`, `create_characteristic_question`, `update_characteristic_question`, `delete_characteristic_question`, `reorder_characteristic_questions`
- **Questions** — `list_questions`, `create_question`, `update_question`, `delete_question`, `reorder_questions`, `generate_questions`, `validate_questions`, `upload_question_image`, `delete_question_image`
- **Interview Flow** — `describe_graph_nodes`, `get_graph`, `check_graph`, `set_graph`, `patch_graph`, `import_questions_to_graph`, `activate_graph`, `deactivate_graph`, `get_flow_signals`, `upload_flow_image`
- **Recruitment and embedding** — `get_recruitment`, `update_recruitment`, `list_embed_keys`, `create_embed_key`, `update_embed_key`, `get_embed_snippet`
- **Sharing a study** — `get_study_share_links`, `create_study_share`, `refresh_study_share`, `revoke_study_share`
- **Personas and simulation** — `list_personas`, `create_persona`, `update_persona`, `delete_persona`, `generate_personas`, `list_simulations`, `run_simulation`, `get_simulation`, `delete_simulation`
- **Results** — `get_study_stats`, `list_interviews`, `find_interviews_by_external_id`, `get_interview`, `get_transcript`, `bulk_transcripts`, `search_transcripts`, `get_interview_fetches_and_signals`
- **Participant contacts** — `list_study_contacts`, `get_interview_contact` (personal data; every read is audited)
- **Analysis** — `list_analyzable_questions`, `get_scale_responses`, `get_options_responses`, `run_clustering`, `get_optimal_clusters`, `get_latest_clustering`
- **Webhooks** — `list_webhook_event_types`, `list_webhooks`, `create_webhook`, `update_webhook`, `delete_webhook`, `rotate_webhook_secret`, `list_webhook_deliveries`
- **Account** — `get_credit_balance` (the balance, and the `plan` block: tier, allowed model tiers, Interview Flow, image questions, simulations, open-study limit), `health_health_get`
- **Feedback** — `report_feedback` (tell the Deutero team what you could not do; free, never shown to participants)
