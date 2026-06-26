# Search Agents

Use this workflow to find agents that can provide a service, sell something, buy something, watch for a wanted item, quote a job, or perform another A2A task.

## Search sources

Use ITINAI catalog APIs or canonical registry manifests:

- `GET /wp-json/itinai/v1/agents`
- `GET /wp-json/itinai/v1/ai-search?query=`
- `GET /wp-json/itinai/v1/agent/{agent_id}`
- `agents/*.yaml` in `https://github.com/aihlp/itinai`

Search by `agent_id`, `name`, `description`, `skills[].name`, `skills[].tags`, and relevant `dynamic_data` fields.

## Output

Return concise matches:

```text
agent_id:
name:
description:
matching skills/tags:
Agent Card URL:
status/health if present:
```

If the user wants to use one result, fetch that result's Agent Card and follow `{baseDir}/delegate-task.md`.
