# Tag Group Tools

Tag group management - create, update, delete groups and manage tag associations

## tag_group_create

Create tag groups to organize and categorize tags. Supports custom colors and tag associations for better tag management and visual organization.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tagGroups | object[] | Yes | Array of tag groups to create |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_create --json '{"tagGroups":[]}'
```

## tag_group_get

Retrieve tag groups by ID or name. Perfect for managing tag organization and retrieving group information with associated tags.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | No | Array of specific tag group IDs |
| names | string[] | No | Array of specific tag group names |
| fullDetails | boolean | No | Return complete tag group information |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_get
```

## tag_group_update

Update tag group properties including name, color, and associated tags. Supports shared parameters (name, description, color, tags) at top level that apply to all groups - individual groups can override these. Efficient for batch updates with common metadata.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Shared group name applied to all groups (can be overridden per group) |
| description | string | No | Shared description applied to all groups (can be overridden per group) |
| color | "red" \| "orange" \| "yellow" \| "green" \| "aqua" \| "blue" \| "purple" \| "pink" \| "none" | No | Shared color applied to all groups (can be overridden per group). Use predefined colors or 'none' to clear |
| tags | string[] | No | Shared tags applied to all groups - FULL REPLACEMENT (can be overridden per group). For incremental changes, use tag_group_add_tags / tag_group_remove_tags |
| tagGroups | object[] | Yes | Array of tag groups to update, each containing id and optional override properties |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_update --json '{"tagGroups":[]}'
```

## tag_group_delete

Delete tag groups by ID. This removes the grouping but does not delete the actual tags. Use carefully as this operation cannot be undone.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | Yes | Array of tag group IDs to delete |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_delete --json '{"ids":[]}'
```

## tag_group_add_tags

Incrementally add or move tags to tag groups. Use removeFromSource=true to move tags (removes from original groups), or false to just add (tags can exist in multiple groups). Much more efficient than updating the entire tags array.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| operations | object[] | Yes | Array of add tags operations |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_add_tags --json '{"operations":[]}'
```

## tag_group_remove_tags

Remove specific tags from tag groups. This only removes the association between tags and groups - it does not delete the tags themselves or affect items using those tags.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| operations | object[] | Yes | Array of remove tags operations |

### Example

```bash
node scripts/eagle-api-cli.js call tag_group_remove_tags --json '{"operations":[]}'
```
