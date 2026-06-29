# AgentPMT Workflow Creator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agentpmt-workflow-creator`

x402 availability: not enabled for this product.

## `add_showcase_example`

Action slug: `add-showcase-example`

Price: `0` credits

Add a single showcase example to a workflow skill.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `showcase_example` | `object` | no | Single showcase example to add (for add_showcase_example action) |
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "showcase_example": null,
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "showcase_example": {
    "default": null,
    "description": "Single showcase example to add (for add_showcase_example action)",
    "required": false,
    "type": "object"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  }
}
```

## `attach_context`

Action slug: `attach-context`

Price: `0` credits

Attach one Agent Context document to a workflow skill draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId for attach_context/detach_context. |
| `skill_id` | `string` | yes | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "context_document_id": null,
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId for attach_context/detach_context.",
    "required": true,
    "type": "string"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": true,
    "type": "string"
  }
}
```

## `create_new`

Action slug: `create-new`

Price: `0` credits

Create a new workflow skill.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chat_model` | `string` | no | Override the workflow's chat model identifier. Must reference chat_model_config.available_models; null or blank clears the override on update. |
| `context_document_ids` | `array` | no | Agent Context document ObjectIds to attach to the workflow (max enforced by the agent_context domain). Replaces the existing set when provided. |
| `default_export_target` | `string` | no | Default export target: mcp or rest |
| `description` | `string` | no | Workflow skill description |
| `edges` | `array` | no | Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?} |
| `industry_tags` | `array` | no | List of industry tag names to associate with this workflow |
| `mcp_server_name` | `string` | no | MCP server name (default: agentpmt) |
| `name` | `string` | no | Workflow skill name |
| `nodes` | `array` | no | Workflow graph nodes - array of SkillChainNode objects |
| `remixed_from_skill_id` | `string` | no | Source skill ID when creating a remix |
| `remixed_from_skill_name` | `string` | no | Source skill name when creating a remix |
| `time_saved_minutes` | `number` | no | Estimated minutes saved (>= 0) |
| `visibility` | `string` | no | Visibility: private or public |

Sample parameters:

```json
{
  "chat_model": null,
  "context_document_ids": null,
  "default_export_target": null,
  "description": null,
  "edges": null,
  "industry_tags": null,
  "mcp_server_name": null,
  "name": null
}
```

Generated JSON parameter schema:

```json
{
  "chat_model": {
    "default": null,
    "description": "Override the workflow's chat model identifier. Must reference chat_model_config.available_models; null or blank clears the override on update.",
    "required": false,
    "type": "string"
  },
  "context_document_ids": {
    "default": null,
    "description": "Agent Context document ObjectIds to attach to the workflow (max enforced by the agent_context domain). Replaces the existing set when provided.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "default_export_target": {
    "default": null,
    "description": "Default export target: mcp or rest",
    "required": false,
    "type": "string"
  },
  "description": {
    "default": null,
    "description": "Workflow skill description",
    "required": false,
    "type": "string"
  },
  "edges": {
    "default": null,
    "description": "Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?}",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "industry_tags": {
    "default": null,
    "description": "List of industry tag names to associate with this workflow",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "mcp_server_name": {
    "default": null,
    "description": "MCP server name (default: agentpmt)",
    "required": false,
    "type": "string"
  },
  "name": {
    "default": null,
    "description": "Workflow skill name",
    "required": false,
    "type": "string"
  },
  "nodes": {
    "default": null,
    "description": "Workflow graph nodes - array of SkillChainNode objects",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "remixed_from_skill_id": {
    "default": null,
    "description": "Source skill ID when creating a remix",
    "required": false,
    "type": "string"
  },
  "remixed_from_skill_name": {
    "default": null,
    "description": "Source skill name when creating a remix",
    "required": false,
    "type": "string"
  },
  "time_saved_minutes": {
    "default": null,
    "description": "Estimated minutes saved (>= 0)",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "visibility": {
    "default": null,
    "description": "Visibility: private or public",
    "required": false,
    "type": "string"
  }
}
```

## `delete`

Action slug: `delete`

Price: `0` credits

Delete a workflow skill draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  }
}
```

## `detach_context`

Action slug: `detach-context`

Price: `0` credits

Detach one Agent Context document from a workflow skill draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId for attach_context/detach_context. |
| `skill_id` | `string` | yes | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "context_document_id": null,
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId for attach_context/detach_context.",
    "required": true,
    "type": "string"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": true,
    "type": "string"
  }
}
```

## `fetch_existing`

Action slug: `fetch-existing`

Price: `0` credits

Fetch workflow skills, optionally filtered to one skill.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_published_only` | `boolean` | no | For fetch_existing: only return skills that have been published |
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "include_published_only": false,
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "include_published_only": {
    "default": false,
    "description": "For fetch_existing: only return skills that have been published",
    "required": false,
    "type": "boolean"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  }
}
```

## `fetch_industry_tags`

Action slug: `fetch-industry-tags`

Price: `0` credits

Fetch available industry tags for workflow skills.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum results to return (1-200) |
| `skip` | `integer` | no | Number of results to skip for pagination |

Sample parameters:

```json
{
  "limit": 50,
  "skip": 0
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 50,
    "description": "Maximum results to return (1-200)",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "skip": {
    "default": 0,
    "description": "Number of results to skip for pagination",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `fetch_tools`

Action slug: `fetch-tools`

Price: `0` credits

Browse or search tools available for workflow nodes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `exclude_private_tools` | `boolean` | no | If true, omit private tools from fetch_tools results |
| `limit` | `integer` | no | Maximum results to return (1-200) |
| `skip` | `integer` | no | Number of results to skip for pagination |
| `sort_by` | `string` | no | Sort order for fetch_tools browse (no search query). 'recently_updated' or 'name'. |
| `tool_search` | `string` | no | Search query for tools in fetch_tools action |

Sample parameters:

```json
{
  "exclude_private_tools": false,
  "limit": 50,
  "skip": 0,
  "sort_by": "recently_updated",
  "tool_search": null
}
```

Generated JSON parameter schema:

```json
{
  "exclude_private_tools": {
    "default": false,
    "description": "If true, omit private tools from fetch_tools results",
    "required": false,
    "type": "boolean"
  },
  "limit": {
    "default": 50,
    "description": "Maximum results to return (1-200)",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "skip": {
    "default": 0,
    "description": "Number of results to skip for pagination",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "sort_by": {
    "default": "recently_updated",
    "description": "Sort order for fetch_tools browse (no search query). 'recently_updated' or 'name'.",
    "enum": [
      "recently_updated",
      "name"
    ],
    "required": false,
    "type": "string"
  },
  "tool_search": {
    "default": null,
    "description": "Search query for tools in fetch_tools action",
    "required": false,
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Price: `0` credits

Fetch usage instructions for workflow skill management.

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

## `publish`

Action slug: `publish`

Price: `0` credits

Publish a workflow skill version.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |
| `version_bump` | `string` | no | Version bump type for publish: major, minor, patch, or auto |

Sample parameters:

```json
{
  "skill_id": null,
  "version_bump": null
}
```

Generated JSON parameter schema:

```json
{
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  },
  "version_bump": {
    "default": null,
    "description": "Version bump type for publish: major, minor, patch, or auto",
    "required": false,
    "type": "string"
  }
}
```

## `remix`

Action slug: `remix`

Price: `0` credits

Create a remix from an existing workflow skill.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  }
}
```

## `remove_showcase_example`

Action slug: `remove-showcase-example`

Price: `0` credits

Remove a showcase example from a workflow skill by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `showcase_example_id` | `string` | no | Showcase example id to remove (for remove_showcase_example action) |
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |

Sample parameters:

```json
{
  "showcase_example_id": null,
  "skill_id": null
}
```

Generated JSON parameter schema:

```json
{
  "showcase_example_id": {
    "default": null,
    "description": "Showcase example id to remove (for remove_showcase_example action)",
    "required": false,
    "type": "string"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  }
}
```

## `search_public`

Action slug: `search-public`

Price: `0` credits

Search public workflow skills.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `categories` | `string` | no | Comma-separated category names to filter by (for search_public) |
| `industry_tags_filter` | `string` | no | Comma-separated industry tag names to filter by (for search_public) |
| `limit` | `integer` | no | Maximum results to return (1-200) |
| `publisher` | `string` | no | Filter by publisher username (case-insensitive substring match, for search_public) |
| `query` | `string` | no | Search query over name/description (case-insensitive) |
| `skip` | `integer` | no | Number of results to skip for pagination |

Sample parameters:

```json
{
  "categories": null,
  "industry_tags_filter": null,
  "limit": 50,
  "publisher": null,
  "query": null,
  "skip": 0
}
```

Generated JSON parameter schema:

```json
{
  "categories": {
    "default": null,
    "description": "Comma-separated category names to filter by (for search_public)",
    "required": false,
    "type": "string"
  },
  "industry_tags_filter": {
    "default": null,
    "description": "Comma-separated industry tag names to filter by (for search_public)",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 50,
    "description": "Maximum results to return (1-200)",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "publisher": {
    "default": null,
    "description": "Filter by publisher username (case-insensitive substring match, for search_public)",
    "required": false,
    "type": "string"
  },
  "query": {
    "default": null,
    "description": "Search query over name/description (case-insensitive)",
    "required": false,
    "type": "string"
  },
  "skip": {
    "default": 0,
    "description": "Number of results to skip for pagination",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `update_existing`

Action slug: `update-existing`

Price: `0` credits

Update an existing workflow skill draft.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chat_model` | `string` | no | Override the workflow's chat model identifier. Must reference chat_model_config.available_models; null or blank clears the override on update. |
| `context_document_ids` | `array` | no | Agent Context document ObjectIds to attach to the workflow (max enforced by the agent_context domain). Replaces the existing set when provided. |
| `default_export_target` | `string` | no | Default export target: mcp or rest |
| `description` | `string` | no | Workflow skill description |
| `edges` | `array` | no | Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?} |
| `industry_tags` | `array` | no | List of industry tag names to associate with this workflow |
| `mcp_server_name` | `string` | no | MCP server name (default: agentpmt) |
| `name` | `string` | no | Workflow skill name |
| `nodes` | `array` | no | Workflow graph nodes - array of SkillChainNode objects |
| `skill_id` | `string` | no | Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch) |
| `time_saved_minutes` | `number` | no | Estimated minutes saved (>= 0) |
| `visibility` | `string` | no | Visibility: private or public |

Sample parameters:

```json
{
  "chat_model": null,
  "context_document_ids": null,
  "default_export_target": null,
  "description": null,
  "edges": null,
  "industry_tags": null,
  "mcp_server_name": null,
  "name": null
}
```

Generated JSON parameter schema:

```json
{
  "chat_model": {
    "default": null,
    "description": "Override the workflow's chat model identifier. Must reference chat_model_config.available_models; null or blank clears the override on update.",
    "required": false,
    "type": "string"
  },
  "context_document_ids": {
    "default": null,
    "description": "Agent Context document ObjectIds to attach to the workflow (max enforced by the agent_context domain). Replaces the existing set when provided.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "default_export_target": {
    "default": null,
    "description": "Default export target: mcp or rest",
    "required": false,
    "type": "string"
  },
  "description": {
    "default": null,
    "description": "Workflow skill description",
    "required": false,
    "type": "string"
  },
  "edges": {
    "default": null,
    "description": "Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?}",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "industry_tags": {
    "default": null,
    "description": "List of industry tag names to associate with this workflow",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "mcp_server_name": {
    "default": null,
    "description": "MCP server name (default: agentpmt)",
    "required": false,
    "type": "string"
  },
  "name": {
    "default": null,
    "description": "Workflow skill name",
    "required": false,
    "type": "string"
  },
  "nodes": {
    "default": null,
    "description": "Workflow graph nodes - array of SkillChainNode objects",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "skill_id": {
    "default": null,
    "description": "Skill chain ObjectId or slug (required for update, publish, remix, delete; optional for fetch)",
    "required": false,
    "type": "string"
  },
  "time_saved_minutes": {
    "default": null,
    "description": "Estimated minutes saved (>= 0)",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "visibility": {
    "default": null,
    "description": "Visibility: private or public",
    "required": false,
    "type": "string"
  }
}
```

## `validate`

Action slug: `validate`

Price: `0` credits

Dry-run validate workflow graph nodes and edges without persisting.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `edges` | `array` | no | Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?} |
| `nodes` | `array` | no | Workflow graph nodes - array of SkillChainNode objects |
| `validation_mode` | `string` | no | Validation mode for validate action. Defaults to agent_write. |

Sample parameters:

```json
{
  "edges": null,
  "nodes": null,
  "validation_mode": "agent_write"
}
```

Generated JSON parameter schema:

```json
{
  "edges": {
    "default": null,
    "description": "Workflow graph edges - array with {id, from, to, condition, sourceHandle?, targetHandle?}",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "nodes": {
    "default": null,
    "description": "Workflow graph nodes - array of SkillChainNode objects",
    "items": {
      "description": "",
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "validation_mode": {
    "default": "agent_write",
    "description": "Validation mode for validate action. Defaults to agent_write.",
    "enum": [
      "agent_write",
      "draft_structure",
      "publish_executable"
    ],
    "required": false,
    "type": "string"
  }
}
```
