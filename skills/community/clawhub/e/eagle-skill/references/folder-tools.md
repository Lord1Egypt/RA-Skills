# Folder Tools

Folder management - create, query, and update folder hierarchy

## folder_create

Batch create folders with support for nested structures and parent-child relationships. Supports creating multiple folders in one operation, including hierarchical folder trees.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| parentId | string | No | Shared parent folder ID for all folders. Individual folder parentId overrides this value. |
| folders | object[] | Yes | Array of folders to create |

### Example

```bash
node scripts/eagle-api-cli.js call folder_create --json '{"folders":[]}'
```

## folder_get

Retrieve Eagle folders based on various criteria. Supports querying by ID, selected status, recent usage, and hierarchical relationships. Perfect for folder management and organization tasks.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| ids | string[] | No | Array of specific folder IDs |
| isSelected | boolean | No | Retrieve currently selected folders |
| isRecent | boolean | No | Retrieve recently used folders |
| getAllHierarchy | boolean | No | Return complete hierarchical structure |
| fullDetails | boolean | No | Return complete folder information |

### Example

```bash
node scripts/eagle-api-cli.js call folder_get
```

## folder_update

Batch update multiple folders with new properties. Supports updating folder names, descriptions, icon colors, and parent folder assignments. Efficient for reorganizing and maintaining folder structures with visual organization and hierarchy management.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| parentId | string | No | Shared parent folder ID to move all folders under. Individual folder parentId overrides this value. Use null to move to root level. |
| folders | object[] | Yes | Array of folders to update |

### Example

```bash
node scripts/eagle-api-cli.js call folder_update --json '{"folders":[]}'
```
