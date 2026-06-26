# Comments

---

## Comments Module

### list

List comments on a document.

```bash
affine-cli comments list [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc-id | -d | **Yes** | Document ID |
| --workspace | -w | No | Workspace ID |
| --first | -n | No | Number of results (default: 20) |
| --offset | -o | No | Offset for pagination |
| --full | -f | No | Return full comment data |

### create

Create a comment on a document.

```bash
affine-cli comments create [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --doc-id | -d | **Yes** | Document ID |
| --content | -c | **Yes** | Comment text |
| --workspace | -w | No | Workspace ID |
| --selection | -s | No | Text being commented on (will auto-link) |
| --doc-title | - | No | Document title |
| --doc-mode | -m | No | Document mode: `page` or `edgeless` |

### update

Update comment text.

```bash
affine-cli comments update [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Comment ID |
| --content | -c | **Yes** | New comment text |

### delete

Delete a comment.

```bash
affine-cli comments delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Comment ID |
| --workspace | -w | No | Workspace ID |
| --doc-id | -d | No | Document ID (auto-detected if not provided) |

### resolve

Mark comment as resolved/unresolved.

```bash
affine-cli comments resolve [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Comment ID |
| --resolved | -r | **Yes** | `true` or `false` |