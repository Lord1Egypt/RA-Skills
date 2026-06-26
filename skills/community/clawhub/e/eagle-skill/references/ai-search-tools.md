# Ai Search Tools

AI-powered semantic search (requires AI Search plugin)

## ai_search_status

Check AI Search plugin availability and status. Returns whether the plugin is installed, ready, starting, or syncing. This tool never fails — it always returns status information even if the plugin is not installed.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|

### Example

```bash
node scripts/eagle-api-cli.js call ai_search_status
```

## ai_search_by_text

Semantic search for Eagle items using natural language. Uses AI embeddings for meaning-based search rather than keyword matching. Requires the AI Search plugin to be installed and ready.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Natural language search query for semantic search (e.g., 'sunset over ocean', 'minimalist logo') |
| limit | number | No | Maximum number of results to return (default: 20, max: 100) |
| fullDetails | boolean | No | Return complete item details (default: false, returns only core fields + score) |

### Example

```bash
node scripts/eagle-api-cli.js call ai_search_by_text --json '{"query":"cat"}'
```

## ai_search_by_item

Find visually similar items to an existing Eagle item using AI. Provide an item ID from your Eagle library to discover similar images. Requires the AI Search plugin to be installed and ready.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| itemId | string | Yes | Eagle item ID to find similar items for |
| limit | number | No | Maximum number of results to return (default: 20, max: 100) |
| fullDetails | boolean | No | Return complete item details (default: false, returns only core fields + score) |

### Example

```bash
node scripts/eagle-api-cli.js call ai_search_by_item --json '{"itemId":"<string>"}'
```
