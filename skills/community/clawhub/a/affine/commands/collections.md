# Collections

---

## Collection Module

### list

List all collections (favorites) in workspace.

```bash
affine-cli collection list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |

### info

List documents in a collection.

```bash
affine-cli collection info [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Collection ID |
| --workspace | -w | No | Workspace ID |

### create

Create a new collection.

```bash
affine-cli collection create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --name | -n | **Yes** | Collection name |
| --workspace | -w | No | Workspace ID |

### update

Rename a collection.

```bash
affine-cli collection update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Collection ID |
| --name | -n | **Yes** | New name |
| --workspace | -w | No | Workspace ID |

### delete

Delete a collection.

```bash
affine-cli collection delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Collection ID |
| --workspace | -w | No | Workspace ID |

### add

Add document to collection.

```bash
affine-cli collection add [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Collection ID |
| --doc | -d | **Yes** | Document ID to add |
| --workspace | -w | No | Workspace ID |

### remove

Remove document from collection.

```bash
affine-cli collection remove [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Collection ID |
| --doc | -d | **Yes** | Document ID to remove |
| --workspace | -w | No | Workspace ID |