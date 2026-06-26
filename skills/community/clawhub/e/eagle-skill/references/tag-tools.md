# Tag Tools

Tag management - query, count, rename, and merge tags

## tag_get

Query Eagle tags with filtering capabilities. Supports searching by name, usage count, and returns tag statistics. Perfect for tag management and analysis.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Specific tag name to search for |
| names | string[] | No | Array of specific tag names |
| minCount | number | No | Minimum usage count filter |
| coreFieldsOnly | boolean | No | Return only core fields (name, count) |

### Example

```bash
node scripts/eagle-api-cli.js call tag_get
```

## tag_count

High-performance counting tool for Eagle tags. Returns only the count without loading full tag data. Perfect for analytics, dashboards, and checking tag statistics efficiently.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| minCount | number | No | Only count tags with at least this many items |

### Example

```bash
node scripts/eagle-api-cli.js call tag_count
```

## tag_update

Batch rename tags across the entire Eagle library. This operation affects all items using the renamed tags. Use carefully as changes are global and permanent.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tags | object[] | Yes | Array of tag rename operations |

### Example

```bash
node scripts/eagle-api-cli.js call tag_update --json '{"tags":[]}'
```

## tag_merge

Merge tags by renaming source tag to target tag. All items using the source tag will be updated to use the target tag. Also updates tag groups, starred tags, and history tags. This operation is irreversible.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| operations | object[] | Yes | Array of tag merge operations |

### Example

```bash
node scripts/eagle-api-cli.js call tag_merge --json '{"operations":[]}'
```
