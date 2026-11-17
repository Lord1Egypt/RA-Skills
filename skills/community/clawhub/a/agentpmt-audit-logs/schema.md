# AgentPMT Audit Logs Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agentpmt-audit-logs`

x402 availability: not enabled for this product.

## `get_chat_review`

Action slug: `get-chat-review`

Fetch a bounded chat transcript page and correlated tool calls.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_limit` | `integer` | no | Maximum correlated tool activity rows for get_chat_review (1-200). |
| `activity_offset` | `integer` | no | Tool activity row offset for get_chat_review. |
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `message_limit` | `integer` | no | Maximum chat messages to return for get_chat_review (1-200). |
| `message_offset_from_end` | `integer` | no | Offset from the end of the transcript for get_chat_review. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |
| `session_id` | `string` | yes | Chat session ID for review or session-scoped tool call listing. |

Sample parameters:

```json
{
  "activity_limit": 100,
  "activity_offset": 0,
  "agent_group_id": "example agent group id",
  "message_limit": 100,
  "message_offset_from_end": 0,
  "scope": "current_agent_group",
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "activity_limit": {
    "default": 100,
    "description": "Maximum correlated tool activity rows for get_chat_review (1-200).",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "activity_offset": {
    "description": "Tool activity row offset for get_chat_review.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "message_limit": {
    "default": 100,
    "description": "Maximum chat messages to return for get_chat_review (1-200).",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "message_offset_from_end": {
    "description": "Offset from the end of the transcript for get_chat_review.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  },
  "session_id": {
    "description": "Chat session ID for review or session-scoped tool call listing.",
    "required": true,
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Explain how to read chat history, tool calls, workflow runs, and scheduled workflows.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_workflow_run`

Action slug: `get-workflow-run`

Fetch one prior workflow run result by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `run_id` | `string` | yes | Workflow run ID for get_workflow_run. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |

Sample parameters:

```json
{
  "agent_group_id": "example agent group id",
  "run_id": "example run id",
  "scope": "current_agent_group"
}
```

Generated JSON parameter schema:

```json
{
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "run_id": {
    "description": "Workflow run ID for get_workflow_run.",
    "required": true,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `get_workflow_schedule`

Action slug: `get-workflow-schedule`

Fetch one scheduled workflow by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `schedule_id` | `string` | yes | Workflow schedule ID for schedule detail or run filtering. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |

Sample parameters:

```json
{
  "agent_group_id": "example agent group id",
  "schedule_id": "example schedule id",
  "scope": "current_agent_group"
}
```

Generated JSON parameter schema:

```json
{
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "schedule_id": {
    "description": "Workflow schedule ID for schedule detail or run filtering.",
    "required": true,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `list_agent_groups`

Action slug: `list-agent-groups`

List the agent groups this user can read.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum list items to return (1-100). |
| `offset` | `integer` | no | Number of list items to skip. |

Sample parameters:

```json
{
  "limit": 20,
  "offset": 0
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 20,
    "description": "Maximum list items to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of list items to skip.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `list_chat_sessions`

Action slug: `list-chat-sessions`

List chat sessions for the current or selected agent group.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `from_date` | `string` | no | Optional inclusive ISO date/datetime lower bound. |
| `limit` | `integer` | no | Maximum list items to return (1-100). |
| `offset` | `integer` | no | Number of list items to skip. |
| `query` | `string` | no | Optional search text for supported list actions. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |
| `status` | `string` | no | Optional status filter. Use all for workflow run and schedule list actions. |
| `to_date` | `string` | no | Optional inclusive ISO date/datetime upper bound. |

Sample parameters:

```json
{
  "agent_group_id": "example agent group id",
  "from_date": "example from date",
  "limit": 20,
  "offset": 0,
  "query": "example search query",
  "scope": "current_agent_group",
  "status": "example status",
  "to_date": "example to date"
}
```

Generated JSON parameter schema:

```json
{
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "from_date": {
    "description": "Optional inclusive ISO date/datetime lower bound.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 20,
    "description": "Maximum list items to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of list items to skip.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Optional search text for supported list actions.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "Optional status filter. Use all for workflow run and schedule list actions.",
    "required": false,
    "type": "string"
  },
  "to_date": {
    "description": "Optional inclusive ISO date/datetime upper bound.",
    "required": false,
    "type": "string"
  }
}
```

## `list_tool_calls`

Action slug: `list-tool-calls`

List safe, read-only tool call activity for authorized agent groups.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `action_name` | `string` | no | Optional nested tool action name filter for list_tool_calls. |
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `from_date` | `string` | no | Optional inclusive ISO date/datetime lower bound. |
| `limit` | `integer` | no | Maximum list items to return (1-100). |
| `offset` | `integer` | no | Number of list items to skip. |
| `product_id` | `string` | no | Optional product/tool ID filter for list_tool_calls. |
| `response_status` | `string` | no | Optional tool call response status filter. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |
| `session_id` | `string` | no | Chat session ID for review or session-scoped tool call listing. |
| `to_date` | `string` | no | Optional inclusive ISO date/datetime upper bound. |

Sample parameters:

```json
{
  "action_name": "example action name",
  "agent_group_id": "example agent group id",
  "from_date": "example from date",
  "limit": 20,
  "offset": 0,
  "product_id": "example product id",
  "response_status": "example response status",
  "scope": "current_agent_group"
}
```

Generated JSON parameter schema:

```json
{
  "action_name": {
    "description": "Optional nested tool action name filter for list_tool_calls.",
    "required": false,
    "type": "string"
  },
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "from_date": {
    "description": "Optional inclusive ISO date/datetime lower bound.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 20,
    "description": "Maximum list items to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of list items to skip.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Optional product/tool ID filter for list_tool_calls.",
    "required": false,
    "type": "string"
  },
  "response_status": {
    "description": "Optional tool call response status filter.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  },
  "session_id": {
    "description": "Chat session ID for review or session-scoped tool call listing.",
    "required": false,
    "type": "string"
  },
  "to_date": {
    "description": "Optional inclusive ISO date/datetime upper bound.",
    "required": false,
    "type": "string"
  }
}
```

## `list_workflow_runs`

Action slug: `list-workflow-runs`

List prior workflow run results for authorized agent groups.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `from_date` | `string` | no | Optional inclusive ISO date/datetime lower bound. |
| `limit` | `integer` | no | Maximum list items to return (1-100). |
| `offset` | `integer` | no | Number of list items to skip. |
| `schedule_id` | `string` | no | Workflow schedule ID for schedule detail or run filtering. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |
| `status` | `string` | no | Optional status filter. Use all for workflow run and schedule list actions. |
| `to_date` | `string` | no | Optional inclusive ISO date/datetime upper bound. |
| `trigger_source` | `string` | no | Workflow run trigger source filter. |
| `workflow_id` | `string` | no | Optional workflow ID filter. |

Sample parameters:

```json
{
  "agent_group_id": "example agent group id",
  "from_date": "example from date",
  "limit": 20,
  "offset": 0,
  "schedule_id": "example schedule id",
  "scope": "current_agent_group",
  "status": "example status",
  "to_date": "example to date"
}
```

Generated JSON parameter schema:

```json
{
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "from_date": {
    "description": "Optional inclusive ISO date/datetime lower bound.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 20,
    "description": "Maximum list items to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of list items to skip.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "schedule_id": {
    "description": "Workflow schedule ID for schedule detail or run filtering.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "Optional status filter. Use all for workflow run and schedule list actions.",
    "required": false,
    "type": "string"
  },
  "to_date": {
    "description": "Optional inclusive ISO date/datetime upper bound.",
    "required": false,
    "type": "string"
  },
  "trigger_source": {
    "default": "all",
    "description": "Workflow run trigger source filter.",
    "enum": [
      "all",
      "agent_webhook",
      "dashboard_schedule_test",
      "workflow_schedule"
    ],
    "required": false,
    "type": "string"
  },
  "workflow_id": {
    "description": "Optional workflow ID filter.",
    "required": false,
    "type": "string"
  }
}
```

## `list_workflow_schedules`

Action slug: `list-workflow-schedules`

List scheduled workflows for authorized agent groups.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_group_id` | `string` | no | Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group. |
| `due_from` | `string` | no | Optional inclusive next_due_at lower bound for schedules. |
| `due_to` | `string` | no | Optional inclusive next_due_at upper bound for schedules. |
| `execution_mode` | `string` | no | Workflow schedule execution mode filter. |
| `limit` | `integer` | no | Maximum list items to return (1-100). |
| `offset` | `integer` | no | Number of list items to skip. |
| `query` | `string` | no | Optional search text for supported list actions. |
| `scope` | `string` | no | Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access. |
| `status` | `string` | no | Optional status filter. Use all for workflow run and schedule list actions. |
| `workflow_id` | `string` | no | Optional workflow ID filter. |

Sample parameters:

```json
{
  "agent_group_id": "example agent group id",
  "due_from": "example due from",
  "due_to": "example due to",
  "execution_mode": "all",
  "limit": 20,
  "offset": 0,
  "query": "example search query",
  "scope": "current_agent_group"
}
```

Generated JSON parameter schema:

```json
{
  "agent_group_id": {
    "description": "Optional agent group ID. This is stored internally as budget_id but shown to users as an agent group.",
    "required": false,
    "type": "string"
  },
  "due_from": {
    "description": "Optional inclusive next_due_at lower bound for schedules.",
    "required": false,
    "type": "string"
  },
  "due_to": {
    "description": "Optional inclusive next_due_at upper bound for schedules.",
    "required": false,
    "type": "string"
  },
  "execution_mode": {
    "default": "all",
    "description": "Workflow schedule execution mode filter.",
    "enum": [
      "all",
      "external_due",
      "managed_cron"
    ],
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 20,
    "description": "Maximum list items to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "offset": {
    "description": "Number of list items to skip.",
    "maximum": 10000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Optional search text for supported list actions.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "default": "current_agent_group",
    "description": "Read scope. current_agent_group reads only the calling workflow's agent group unless agent_group_id is provided. all_authorized_agent_groups reads every agent group the user can access.",
    "enum": [
      "current_agent_group",
      "all_authorized_agent_groups"
    ],
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "Optional status filter. Use all for workflow run and schedule list actions.",
    "required": false,
    "type": "string"
  },
  "workflow_id": {
    "description": "Optional workflow ID filter.",
    "required": false,
    "type": "string"
  }
}
```
