# Agent Context Manager Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agent-context-manager`

x402 availability: not enabled for this product.

## `archive`

Action slug: `archive`

Price: `0` credits

Archive an Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |
| `expected_revision` | `integer` | yes | Required CAS revision for update/archive. |

Sample parameters:

```json
{
  "context_document_id": null,
  "expected_revision": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  },
  "expected_revision": {
    "default": null,
    "description": "Required CAS revision for update/archive.",
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `clone_template`

Action slug: `clone-template`

Price: `0` credits

Clone a public Agent Context template into private context.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```

## `create`

Action slug: `create`

Price: `0` credits

Create an Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_edit_approval_required` | `boolean` | no | When true, agents need a user-approved temporary unlock before editing this document. |
| `body` | `string` | yes | Document body for create/update. |
| `document_scope` | `string` | no | Create-only scope. public_template requires admin JWT. |
| `summary` | `string` | no | Optional short summary for create/update. |
| `tags` | `array` | no | Optional tags for create/update. |
| `title` | `string` | yes | Document title for create/update. |

Sample parameters:

```json
{
  "agent_edit_approval_required": null,
  "body": null,
  "document_scope": "private",
  "summary": null,
  "tags": null,
  "title": null
}
```

Generated JSON parameter schema:

```json
{
  "agent_edit_approval_required": {
    "default": null,
    "description": "When true, agents need a user-approved temporary unlock before editing this document.",
    "required": false,
    "type": "boolean"
  },
  "body": {
    "default": null,
    "description": "Document body for create/update.",
    "required": true,
    "type": "string"
  },
  "document_scope": {
    "default": "private",
    "description": "Create-only scope. public_template requires admin JWT.",
    "enum": [
      "private",
      "public_template"
    ],
    "required": false,
    "type": "string"
  },
  "summary": {
    "default": null,
    "description": "Optional short summary for create/update.",
    "required": false,
    "type": "string"
  },
  "tags": {
    "default": null,
    "description": "Optional tags for create/update.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "default": null,
    "description": "Document title for create/update.",
    "required": true,
    "type": "string"
  }
}
```

## `fetch`

Action slug: `fetch`

Price: `0` credits

Fetch one readable Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Price: `0` credits

Return Agent Context Manager usage guidance.

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

## `list`

Action slug: `list`

Price: `0` credits

List readable Agent Context documents.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_archived` | `boolean` | no | When true, include archived documents in list results. |
| `limit` | `integer` | no | Maximum documents to return for list. |
| `query` | `string` | no | Optional search over title, summary, and tags for list. |
| `scope` | `string` | no | List scope. Use all to include owned private documents and public templates. |

Sample parameters:

```json
{
  "include_archived": false,
  "limit": 100,
  "query": null,
  "scope": "private"
}
```

Generated JSON parameter schema:

```json
{
  "include_archived": {
    "default": false,
    "description": "When true, include archived documents in list results.",
    "required": false,
    "type": "boolean"
  },
  "limit": {
    "default": 100,
    "description": "Maximum documents to return for list.",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "default": null,
    "description": "Optional search over title, summary, and tags for list.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "default": "private",
    "description": "List scope. Use all to include owned private documents and public templates.",
    "enum": [
      "private",
      "public_template",
      "all"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `request_unlock`

Action slug: `request-unlock`

Price: `0` credits

Request a temporary 30-minute edit unlock for a locked Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```

## `restore_version`

Action slug: `restore-version`

Price: `0` credits

Restore a retained Agent Context version using CAS.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |
| `expected_revision` | `integer` | yes | Required CAS revision for update/archive. |
| `version_id` | `string` | yes | Agent Context document version ObjectId. Required for version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null,
  "expected_revision": null,
  "version_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  },
  "expected_revision": {
    "default": null,
    "description": "Required CAS revision for update/archive.",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "version_id": {
    "default": null,
    "description": "Agent Context document version ObjectId. Required for version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```

## `update`

Action slug: `update`

Price: `0` credits

Update editable fields on an Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `agent_edit_approval_required` | `boolean` | no | When true, agents need a user-approved temporary unlock before editing this document. |
| `body` | `string` | no | Document body for create/update. |
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |
| `expected_revision` | `integer` | yes | Required CAS revision for update/archive. |
| `summary` | `string` | no | Optional short summary for create/update. |
| `tags` | `array` | no | Optional tags for create/update. |
| `title` | `string` | no | Document title for create/update. |

Sample parameters:

```json
{
  "agent_edit_approval_required": null,
  "body": null,
  "context_document_id": null,
  "expected_revision": null,
  "summary": null,
  "tags": null,
  "title": null
}
```

Generated JSON parameter schema:

```json
{
  "agent_edit_approval_required": {
    "default": null,
    "description": "When true, agents need a user-approved temporary unlock before editing this document.",
    "required": false,
    "type": "boolean"
  },
  "body": {
    "default": null,
    "description": "Document body for create/update.",
    "required": false,
    "type": "string"
  },
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  },
  "expected_revision": {
    "default": null,
    "description": "Required CAS revision for update/archive.",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "summary": {
    "default": null,
    "description": "Optional short summary for create/update.",
    "required": false,
    "type": "string"
  },
  "tags": {
    "default": null,
    "description": "Optional tags for create/update.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "default": null,
    "description": "Document title for create/update.",
    "required": false,
    "type": "string"
  }
}
```

## `version_detail`

Action slug: `version-detail`

Price: `0` credits

Fetch one retained Agent Context version detail with its snapshot.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |
| `version_id` | `string` | yes | Agent Context document version ObjectId. Required for version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null,
  "version_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  },
  "version_id": {
    "default": null,
    "description": "Agent Context document version ObjectId. Required for version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```

## `versions`

Action slug: `versions`

Price: `0` credits

List retained versions for a readable Agent Context document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context_document_id` | `string` | yes | Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version. |

Sample parameters:

```json
{
  "context_document_id": null
}
```

Generated JSON parameter schema:

```json
{
  "context_document_id": {
    "default": null,
    "description": "Agent Context document ObjectId. Required for fetch/update/archive/clone_template/versions/version_detail/restore_version.",
    "required": true,
    "type": "string"
  }
}
```
