# Item Tools

Library item management - search, filter, add, update, tag, and organize

## item_query

Smart text search engine with comprehensive query syntax support. Supports complex search patterns like AND/OR/NOT operations, quoted phrases, and field-specific searches. Perfect for finding specific items when you know keywords or search terms.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Search query string with syntax support. Examples: 'cat', 'cat OR dog', '(cute OR adorable) cat -dog' |
| fullDetails | boolean | No | Return complete Item object details (default: false, returns only core fields: id, name, ext, tags, folders, width, height, thumbnailPath, filePath) |

### Example

```bash
node scripts/eagle-api-cli.js call item_query --json '{"query":"cat"}'
```

## item_get

Precision attribute filter for retrieving Eagle library items based on specific criteria. Supports filtering by ID, tags, folders, extensions, ratings, and more. Includes pagination support for large result sets. Use this when you need exact matching against specific item properties.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | No | Array of specific item IDs to retrieve |
| keywords | string[] | No | Array of keywords to search for |
| ext | string | No | File extension filter (e.g., 'jpg', 'png', 'gif') |
| tags | string[] | No | Array of tags to filter by |
| folders | string[] | No | Array of folder IDs to filter by |
| shape | "square" \| "portrait" \| "landscape" | No | Image shape filter |
| rating | number | No | Star rating filter (0-5 stars) |
| annotation | string | No | Annotation content filter |
| url | string | No | Source URL filter |
| isUnfiled | boolean | No | Retrieve items not in any folder |
| isUntagged | boolean | No | Retrieve items without any tags |
| fullDetails | boolean | No | Return complete item information (default: false) |
| limit | number | No | Maximum number of items to return (default: 100, max: 1000) |
| offset | number | No | Number of items to skip for pagination (default: 0) |

### Example

```bash
node scripts/eagle-api-cli.js call item_get
```

## item_get_selected

Get currently selected items in Eagle application. Perfect for working with items the user has manually selected. Returns empty array if no items are selected.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| fullDetails | boolean | No | Return complete item information (default: false) |

### Example

```bash
node scripts/eagle-api-cli.js call item_get_selected
```

## item_update

Batch update multiple items with new properties. Supports shared parameters (tags, folders, annotation, star) at top level that apply to all items - individual items can override these. Efficient for bulk operations with common metadata.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tags | string[] | No | Shared tags applied to all items (can be overridden per item) |
| folders | string[] | No | Shared folder IDs applied to all items (can be overridden per item) |
| annotation | string | No | Shared annotation applied to all items (can be overridden per item) |
| star | number | No | Shared star rating applied to all items (can be overridden per item) |
| items | object[] | Yes | Array of items to update, each containing id and properties to update |

### Example

```bash
node scripts/eagle-api-cli.js call item_update --json '{"items":[]}'
```

## item_count

High-performance counting tool for Eagle library items. Supports all the same filter criteria as item_get but returns only the count without loading full item data. Perfect for analytics and overview information.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No | Specific item ID to count |
| ids | string[] | No | Array of specific item IDs to count |
| keywords | string[] | No | Array of keywords to search for |
| ext | string | No | File extension filter (e.g., 'jpg', 'png', 'gif') |
| tags | string[] | No | Array of tags to filter by |
| folders | string[] | No | Array of folder IDs to filter by |
| shape | "square" \| "portrait" \| "landscape" | No | Image shape filter |
| rating | number | No | Star rating filter (0-5 stars) |
| annotation | string | No | Annotation content filter |
| url | string | No | Source URL filter |
| isUnfiled | boolean | No | Count items not in any folder |
| isUntagged | boolean | No | Count items without any tags |
| isSelected | boolean | No | Count currently selected items |

### Example

```bash
node scripts/eagle-api-cli.js call item_count
```

## item_add

Unified item addition tool with intelligent source type routing. Supports URL, Base64, file path, and bookmark sources in batch operations. Supports shared parameters (tags, folders, annotation) at top level that apply to all items - individual items can override these. Perfect for batch imports with common metadata.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tags | string[] | No | Shared tags applied to all items (can be overridden per item) |
| folders | string[] | No | Shared folder IDs applied to all items (can be overridden per item) |
| annotation | string | No | Shared annotation applied to all items (can be overridden per item) |
| items | object[] | Yes | Array of items to add |

### Example

```bash
node scripts/eagle-api-cli.js call item_add --json '{"items":[]}'
```

## item_move_to_trash

Batch move items to trash. Supports moving multiple items at once by providing their IDs. Items moved to trash can be restored from Eagle's trash folder. Use carefully as this affects the library organization.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of item IDs to move to trash |

### Example

```bash
node scripts/eagle-api-cli.js call item_move_to_trash --json '{"ids":[]}'
```

## item_add_tags

Incrementally add tags to multiple items without replacing existing tags. All specified items receive the same tags. Tags are merged with existing ones, duplicates are automatically handled.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of item IDs |
| tags | string[] | Yes | Tags to add to all specified items |

### Example

```bash
node scripts/eagle-api-cli.js call item_add_tags --json '{"ids":[],"tags":[]}'
```

## item_remove_tags

Incrementally remove specific tags from multiple items without affecting other tags. All specified items have the same tags removed. Non-existent tags are silently ignored.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of item IDs |
| tags | string[] | Yes | Tags to remove from all specified items |

### Example

```bash
node scripts/eagle-api-cli.js call item_remove_tags --json '{"ids":[],"tags":[]}'
```

## item_add_to_folders

Incrementally add multiple items to folders without replacing existing folder assignments. All specified items are added to the same folders. Folders are merged with existing ones, duplicates are automatically handled.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of item IDs |
| folders | string[] | Yes | Folder IDs to add all specified items to |

### Example

```bash
node scripts/eagle-api-cli.js call item_add_to_folders --json '{"ids":[],"folders":[]}'
```

## item_remove_from_folders

Incrementally remove multiple items from specific folders without affecting other folder assignments. All specified items are removed from the same folders. Non-existent folder assignments are silently ignored.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of item IDs |
| folders | string[] | Yes | Folder IDs to remove all specified items from |

### Example

```bash
node scripts/eagle-api-cli.js call item_remove_from_folders --json '{"ids":[],"folders":[]}'
```
