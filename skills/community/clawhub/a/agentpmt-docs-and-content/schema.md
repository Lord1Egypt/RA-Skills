# AgentPMT Platform Search Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `agentpmt-docs-and-content`

x402 availability: not enabled for this product.

## `get_instructions`

Action slug: `get-instructions`

Price: `0` credits

Return usage instructions for this content search handler.

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

## `global_search`

Action slug: `global-search`

Price: `0` credits

Search the public AgentPMT site across tools, workflows, agents, articles, papers, videos, docs, pages, and FAQs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Opaque continuation cursor returned by a previous search or global_search call. Reuse it with the same query and type filters. |
| `limit` | `integer` | no | Maximum items to return (1-50). |
| `query` | `string` | yes | Search query. Required when action='search' or action='global_search'. |
| `types` | `array` | no | Global search result kinds to include. Omit for all result kinds. Supported values: product, workflow, agent, article, paper, video, doc, page, faq. Used only when action='global_search'. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "limit": 10,
  "query": "example search query",
  "types": [
    "product"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Opaque continuation cursor returned by a previous search or global_search call. Reuse it with the same query and type filters.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 10,
    "description": "Maximum items to return (1-50).",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Search query. Required when action='search' or action='global_search'.",
    "required": true,
    "type": "string"
  },
  "types": {
    "description": "Global search result kinds to include. Omit for all result kinds. Supported values: product, workflow, agent, article, paper, video, doc, page, faq. Used only when action='global_search'.",
    "items": {
      "description": "",
      "enum": [
        "product",
        "workflow",
        "agent",
        "article",
        "paper",
        "video",
        "doc",
        "page",
        "faq"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `recent`

Action slug: `recent`

Price: `0` credits

Return the most recently published public content for selected types.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_types` | `array` | no | Content types to include. Omit for all content. Supported values: article, paper, video, doc, faq. |
| `limit` | `integer` | no | Maximum items to return (1-50). |
| `skip` | `integer` | no | Number of recent items to skip for pagination. Used only when action='recent'. |

Sample parameters:

```json
{
  "content_types": [
    "article"
  ],
  "limit": 10,
  "skip": 0
}
```

Generated JSON parameter schema:

```json
{
  "content_types": {
    "description": "Content types to include. Omit for all content. Supported values: article, paper, video, doc, faq.",
    "items": {
      "description": "",
      "enum": [
        "article",
        "paper",
        "video",
        "doc",
        "faq"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "limit": {
    "default": 10,
    "description": "Maximum items to return (1-50).",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "skip": {
    "description": "Number of recent items to skip for pagination. Used only when action='recent'.",
    "maximum": 1000,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `search`

Action slug: `search`

Price: `0` credits

Search public articles, papers, videos, docs, FAQs, or all content.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_types` | `array` | no | Content types to include. Omit for all content. Supported values: article, paper, video, doc, faq. |
| `cursor` | `string` | no | Opaque continuation cursor returned by a previous search or global_search call. Reuse it with the same query and type filters. |
| `limit` | `integer` | no | Maximum items to return (1-50). |
| `query` | `string` | yes | Search query. Required when action='search' or action='global_search'. |

Sample parameters:

```json
{
  "content_types": [
    "article"
  ],
  "cursor": "example cursor",
  "limit": 10,
  "query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "content_types": {
    "description": "Content types to include. Omit for all content. Supported values: article, paper, video, doc, faq.",
    "items": {
      "description": "",
      "enum": [
        "article",
        "paper",
        "video",
        "doc",
        "faq"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "cursor": {
    "description": "Opaque continuation cursor returned by a previous search or global_search call. Reuse it with the same query and type filters.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 10,
    "description": "Maximum items to return (1-50).",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Search query. Required when action='search' or action='global_search'.",
    "required": true,
    "type": "string"
  }
}
```
