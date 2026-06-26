# Tags and Folders

---

## Tags Module

### list

List all tags in workspace.

```bash
affine-cli tags list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |

### create

Create a new tag.

```bash
affine-cli tags create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --name | -n | **Yes** | Tag name |
| --color | -c | No | Color hex code (e.g., `#3B82F6`) |
| --workspace | -w | No | Workspace ID |

**Examples:**
```bash
# Simple tag
affine-cli tags create --name important

# With color
affine-cli tags create --name urgent --color #EF4444
```

### add

Add tag to document.

```bash
affine-cli tags add [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --tag | -t | **Yes** | Tag name |
| --workspace | -w | No | Workspace ID |

### remove

Remove tag from document.

```bash
affine-cli tags remove [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc | -d | **Yes** | Document ID |
| --tag | -t | **Yes** | Tag name |
| --workspace | -w | No | Workspace ID |

### delete

Delete a tag entirely.

```bash
affine-cli tags delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --tag | -t | **Yes** | Tag name |
| --workspace | -w | No | Workspace ID |

### info

List documents with a specific tag.

```bash
affine-cli tags info [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --tag | -t | **Yes** | Tag name |
| --workspace | -w | No | Workspace ID |
| --ignore-case | -i | No | Case-insensitive search |

---

## Folder Module

### all

List all folders in workspace.

```bash
affine-cli folder all [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |

### list

List contents of a folder.

```bash
affine-cli folder list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Folder ID |
| --folder | -f | No | Return only subfolders (not documents) |
| --workspace | -w | No | Workspace ID |

### create

Create a new folder.

```bash
affine-cli folder create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --name | -n | **Yes** | Folder name |
| --parent | -p | No | Parent folder ID |
| --index | - | No | Sort order index |
| --workspace | -w | No | Workspace ID |

**Examples:**
```bash
# Create root folder
affine-cli folder create --name Projects

# Create subfolder
affine-cli folder create --name "2025" --parent PARENT_FOLDER_ID
```

### delete

Delete a folder.

```bash
affine-cli folder delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Folder ID |
| --workspace | -w | No | Workspace ID |

### update

Update folder properties.

```bash
affine-cli folder update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Folder ID |
| --name | -n | No | New folder name |
| --parent | -p | No | New parent folder ID. Use empty to move to root |
| --index | - | No | Sort order index |
| --workspace | -w | No | Workspace ID |

### clear

Remove all empty folders.

```bash
affine-cli folder clear [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |

### add

Add document to folder.

```bash
affine-cli folder add [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Folder ID |
| --doc | -d | **Yes** | Document ID to add |
| --index | - | No | Sort order index |
| --workspace | -w | No | Workspace ID |

### move

Move document from another folder to this folder.

```bash
affine-cli folder move [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Target folder ID |
| --doc | -d | **Yes** | Document ID to move |
| --workspace | -w | No | Workspace ID |

### remove

Remove document from folder (does not delete the document).

```bash
affine-cli folder remove [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Folder ID |
| --doc | -d | **Yes** | Document ID to remove |
| --workspace | -w | No | Workspace ID |