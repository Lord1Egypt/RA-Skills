# Advanced Patterns

## Collaborative Mode Conversation

1. Create project with `"mode": "collaborative"`
2. Agent responds and returns `idle` with its response in `agent_message`
3. Review the response, send feedback via `POST /projects/:id/messages`
4. Poll until next `idle`
5. Repeat

## Long-Term Projects

The agent handles individual creative tasks. For projects that span weeks or months (campaigns, series, catalogs), you manage the long-term plan and hand the agent focused short-term tasks.

**Setup:** Work with the agent to build the creative foundation: direction, strategy, character casting, visual references, style rules. This is iterative and collaborative. Save the output as your master plan (`agent_message`, `GET /projects/:id/memory`, `GET /projects/:id/assets`).

**Execution:** Hand the agent focused tasks from the master plan: "produce this week's episode," "create the 9:16 social cuts," "generate the Japanese market version." The agent executes the creative work. You update your progress tracking.

**Variations** (parallel timeline branches within a project) keep everything connected: each deliverable can be its own variation, sharing the project's creative foundation while branching for each task.

**Memory:** The agent's working memory is designed for short-term task focus. Your master plan lives outside. Feed the agent what it needs per task. Use `GET /projects/:id/memory` to monitor.

## Parallel Projects

Launch multiple projects simultaneously (default limit: 5 concurrent). Projects start as capacity opens up; all begin as `queued` and move to `running` as the system picks them up.

### Tracking Pattern

When managing multiple projects, maintain your own tracking:

```
Project A (id: ...): status generating, last_msg msg_123
Project B (id: ...): status running, last_msg msg_456
Project C (id: ...): status queued, last_msg null
```

Track:
- Project IDs and current status
- Key asset URLs as they're produced
- Milestones (planned, images generated, video done, rendered)
- Last message ID per project (for efficient `?after=` polling)

## Variation Workflows

Variations are parallel creative directions within one project: different styles, languages, aspect ratios, or A/B tests.

**Variations are read-only via API.** To create, switch, or delete:

```json
{"message": "Duplicate the current variation and switch to it"}
{"message": "Switch to variation var_xyz"}
{"message": "Create a 9:16 version of this project"}
```

The active `variation_id` is included in GET project status. Use `GET /projects/:id/timeline?variation_id=ID` to inspect any variation without switching.

## Project Discovery and Adoption

Adopt projects created in the studio for API management:

```bash
# List available projects
curl https://eversince.ai/api/v1/projects/discover \
  -H "Authorization: Bearer $EVERSINCE_API_KEY"

# Adopt one
curl -X POST https://eversince.ai/api/v1/projects/adopt \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "PROJECT_ID", "mode": "collaborative"}'
```

The project is now API-managed. All endpoints work on it.

## Teaching the Agent

```bash
# Create a skill
curl -X POST https://eversince.ai/api/v1/account/skills \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Brand Guidelines",
    "instructions": "Always use the brand colors #1a1a2e and #e94560. The brand voice is confident and minimal. Never use exclamation marks in taglines.",
    "is_active": true
  }'
```

Skills persist across all projects. Use them for brand guidelines, style rules, or domain-specific knowledge. Budget: 40,000 tokens (roughly 160,000 characters) across all active skills combined.

List all skills via `GET /account/skills`. Both Eversince skills (built-in) and custom skills can be toggled on/off via `PATCH /account/skills/:id`. Custom skills can also be created, updated, and deleted.
