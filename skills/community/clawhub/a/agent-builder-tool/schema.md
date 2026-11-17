# Agent Builder Tool Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agent-builder-tool`

x402 availability: not enabled for this product.

## `add_product`

Action slug: `add-product`

Attach a product to the agent. Routes through file manager auto-attach.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `product_id` | `string` | no | Product ObjectId for add_product/remove_product. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "product_id": "example product id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "product_id": {
    "description": "Product ObjectId for add_product/remove_product.",
    "required": false,
    "type": "string"
  }
}
```

## `add_showcase_example`

Action slug: `add-showcase-example`

Add a chat preview example to the agent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `showcase_example` | `object` | no | Showcase example object for add_showcase_example. See get_instructions for shape. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "showcase_example": {}
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "showcase_example": {
    "description": "Showcase example object for add_showcase_example. See get_instructions for shape.",
    "required": false,
    "type": "object"
  }
}
```

## `add_workflow`

Action slug: `add-workflow`

Attach a workflow to the agent. Routes through file manager auto-attach.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `workflow_id` | `string` | no | Workflow (skill chain) ObjectId for add_workflow/remove_workflow. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "workflow_id": "example workflow id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "workflow_id": {
    "description": "Workflow (skill chain) ObjectId for add_workflow/remove_workflow.",
    "required": false,
    "type": "string"
  }
}
```

## `archive`

Action slug: `archive`

Soft-delete the agent. If forward_to is supplied, issue 301 redirects from the agent's canonical paths to that internal destination.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `forward_to` | `string` | no | Internal path to redirect the archived agent's URLs to. Must start with /. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "forward_to": "example forward to"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "forward_to": {
    "description": "Internal path to redirect the archived agent's URLs to. Must start with /.",
    "required": false,
    "type": "string"
  }
}
```

## `attach_context`

Action slug: `attach-context`

Attach an Agent Context document to the agent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `context_document_id` | `string` | no | Agent Context document ObjectId for attach_context/detach_context. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "context_document_id": "example context document id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "context_document_id": {
    "description": "Agent Context document ObjectId for attach_context/detach_context.",
    "required": false,
    "type": "string"
  }
}
```

## `create_new`

Action slug: `create-new`

Create a private draft agent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chat_model` | `string` | no | Override the agent's chat model identifier. |
| `context_document_ids` | `array` | no | Full set of Agent Context document ObjectIds to attach on create_new/update_existing (replaces the existing set). Use attach_context/detach_context to mutate a single id. |
| `description` | `string` | no | Free-text description shown in the marketplace. |
| `draft_slug` | `string` | no | Admin-only when slug_unlocked=true. Editable URL slug intent before activation. |
| `name` | `string` | no | Agent display name. Required on create_new. |
| `remixed_from_agent_id` | `string` | no | Source agent id to remix from. Used by create_new/remix. |
| `remixed_from_agent_name` | `string` | no | Override the remix source name attribution. |
| `slug` | `string` | no | Admin-only when slug_unlocked=true. Final URL slug for active agents. |
| `slug_unlocked` | `boolean` | no | Admin-only flag required before changing slug or draft_slug manually. |

Sample parameters:

```json
{
  "chat_model": "example chat model",
  "context_document_ids": [
    "example context document id"
  ],
  "description": "example description",
  "draft_slug": "example draft slug",
  "name": "example name",
  "remixed_from_agent_id": "example remixed from agent id",
  "remixed_from_agent_name": "example remixed from agent name",
  "slug": "example slug"
}
```

Generated JSON parameter schema:

```json
{
  "chat_model": {
    "description": "Override the agent's chat model identifier.",
    "required": false,
    "type": "string"
  },
  "context_document_ids": {
    "description": "Full set of Agent Context document ObjectIds to attach on create_new/update_existing (replaces the existing set). Use attach_context/detach_context to mutate a single id.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "description": {
    "description": "Free-text description shown in the marketplace.",
    "required": false,
    "type": "string"
  },
  "draft_slug": {
    "description": "Admin-only when slug_unlocked=true. Editable URL slug intent before activation.",
    "required": false,
    "type": "string"
  },
  "name": {
    "description": "Agent display name. Required on create_new.",
    "required": false,
    "type": "string"
  },
  "remixed_from_agent_id": {
    "description": "Source agent id to remix from. Used by create_new/remix.",
    "required": false,
    "type": "string"
  },
  "remixed_from_agent_name": {
    "description": "Override the remix source name attribution.",
    "required": false,
    "type": "string"
  },
  "slug": {
    "description": "Admin-only when slug_unlocked=true. Final URL slug for active agents.",
    "required": false,
    "type": "string"
  },
  "slug_unlocked": {
    "description": "Admin-only flag required before changing slug or draft_slug manually.",
    "required": false,
    "type": "boolean"
  }
}
```

## `detach_context`

Action slug: `detach-context`

Detach an Agent Context document from the agent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `context_document_id` | `string` | no | Agent Context document ObjectId for attach_context/detach_context. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "context_document_id": "example context document id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "context_document_id": {
    "description": "Agent Context document ObjectId for attach_context/detach_context.",
    "required": false,
    "type": "string"
  }
}
```

## `fetch_existing`

Action slug: `fetch-existing`

List your agents (recently updated first), or fetch one by id/slug.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `limit` | `integer` | no | Maximum results for list/search actions (1-100). |
| `query` | `string` | no | Substring search over name and description for fetch_existing/search_public. |
| `skip` | `integer` | no | Pagination offset for list/search actions. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "limit": 1,
  "query": "example search query",
  "skip": 0
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum results for list/search actions (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Substring search over name and description for fetch_existing/search_public.",
    "required": false,
    "type": "string"
  },
  "skip": {
    "description": "Pagination offset for list/search actions.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Return the handler reference guide.

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

Transition DRAFT to ACTIVE; stamps published_at the first time.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |

Sample parameters:

```json
{
  "agent_id": "example agent id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  }
}
```

## `remix`

Action slug: `remix`

Create a private copy of a viewable agent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `name` | `string` | no | Agent display name. Required on create_new. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "name": "example name"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "name": {
    "description": "Agent display name. Required on create_new.",
    "required": false,
    "type": "string"
  }
}
```

## `remove_product`

Action slug: `remove-product`

Detach a product from the agent. Routes through file manager auto-attach.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `product_id` | `string` | no | Product ObjectId for add_product/remove_product. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "product_id": "example product id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "product_id": {
    "description": "Product ObjectId for add_product/remove_product.",
    "required": false,
    "type": "string"
  }
}
```

## `remove_showcase_example`

Action slug: `remove-showcase-example`

Remove a showcase example by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `showcase_example_id` | `string` | no | Showcase example id for remove_showcase_example. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "showcase_example_id": "example showcase example id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "showcase_example_id": {
    "description": "Showcase example id for remove_showcase_example.",
    "required": false,
    "type": "string"
  }
}
```

## `remove_workflow`

Action slug: `remove-workflow`

Detach a workflow from the agent. Routes through file manager auto-attach.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `workflow_id` | `string` | no | Workflow (skill chain) ObjectId for add_workflow/remove_workflow. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "workflow_id": "example workflow id"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "workflow_id": {
    "description": "Workflow (skill chain) ObjectId for add_workflow/remove_workflow.",
    "required": false,
    "type": "string"
  }
}
```

## `search_public`

Action slug: `search-public`

Search active public agents.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum results for list/search actions (1-100). |
| `query` | `string` | no | Substring search over name and description for fetch_existing/search_public. |
| `skip` | `integer` | no | Pagination offset for list/search actions. |

Sample parameters:

```json
{
  "limit": 1,
  "query": "example search query",
  "skip": 0
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "Maximum results for list/search actions (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Substring search over name and description for fetch_existing/search_public.",
    "required": false,
    "type": "string"
  },
  "skip": {
    "description": "Pagination offset for list/search actions.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `update_existing`

Action slug: `update-existing`

Update editable fields on an agent you own. is_template is admin-only.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_id` | `string` | no | Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions. |
| `chat_model` | `string` | no | Override the agent's chat model identifier. |
| `context_document_ids` | `array` | no | Full set of Agent Context document ObjectIds to attach on create_new/update_existing (replaces the existing set). Use attach_context/detach_context to mutate a single id. |
| `description` | `string` | no | Free-text description shown in the marketplace. |
| `draft_slug` | `string` | no | Admin-only when slug_unlocked=true. Editable URL slug intent before activation. |
| `is_template` | `boolean` | no | Admin-only. Mark the agent as a public template; non-admin writes are silently dropped. |
| `name` | `string` | no | Agent display name. Required on create_new. |
| `slug` | `string` | no | Admin-only when slug_unlocked=true. Final URL slug for active agents. |
| `slug_unlocked` | `boolean` | no | Admin-only flag required before changing slug or draft_slug manually. |
| `status` | `string` | no | Lifecycle status. Use the dedicated publish/archive actions where possible. |
| `system_prompt` | `string` | no | System prompt persisted on the agent. |

Sample parameters:

```json
{
  "agent_id": "example agent id",
  "chat_model": "example chat model",
  "context_document_ids": [
    "example context document id"
  ],
  "description": "example description",
  "draft_slug": "example draft slug",
  "is_template": true,
  "name": "example name",
  "slug": "example slug"
}
```

Generated JSON parameter schema:

```json
{
  "agent_id": {
    "description": "Agent ObjectId hex string or slug. Required for update/publish/archive/composition/showcase actions.",
    "required": false,
    "type": "string"
  },
  "chat_model": {
    "description": "Override the agent's chat model identifier.",
    "required": false,
    "type": "string"
  },
  "context_document_ids": {
    "description": "Full set of Agent Context document ObjectIds to attach on create_new/update_existing (replaces the existing set). Use attach_context/detach_context to mutate a single id.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "description": {
    "description": "Free-text description shown in the marketplace.",
    "required": false,
    "type": "string"
  },
  "draft_slug": {
    "description": "Admin-only when slug_unlocked=true. Editable URL slug intent before activation.",
    "required": false,
    "type": "string"
  },
  "is_template": {
    "description": "Admin-only. Mark the agent as a public template; non-admin writes are silently dropped.",
    "required": false,
    "type": "boolean"
  },
  "name": {
    "description": "Agent display name. Required on create_new.",
    "required": false,
    "type": "string"
  },
  "slug": {
    "description": "Admin-only when slug_unlocked=true. Final URL slug for active agents.",
    "required": false,
    "type": "string"
  },
  "slug_unlocked": {
    "description": "Admin-only flag required before changing slug or draft_slug manually.",
    "required": false,
    "type": "boolean"
  },
  "status": {
    "description": "Lifecycle status. Use the dedicated publish/archive actions where possible.",
    "enum": [
      "draft",
      "active",
      "archived"
    ],
    "required": false,
    "type": "string"
  },
  "system_prompt": {
    "description": "System prompt persisted on the agent.",
    "required": false,
    "type": "string"
  }
}
```
