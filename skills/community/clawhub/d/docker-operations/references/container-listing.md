# Container Listing Commands

Commands for listing and filtering Docker containers.

## docker ps

List containers.

```bash
docker ps [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Show all containers (default shows just running) |
| `-f, --filter filter` | Filter output based on conditions provided |
| `--format string` | Format output using a custom template |
| `-n, --last int` | Show n last created containers (includes all states) |
| `-l, --latest` | Show the latest created container (includes all states) |
| `--no-trunc` | Don't truncate output |
| `-q, --quiet` | Only display container IDs |
| `-s, --size` | Display total file sizes |

**Format templates:**
- `table`: Print output in table format with column headers (default)
- `json`: Print in JSON format
- Custom: `table {{.Names}}\t{{.Status}}\t{{.Ports}}`

**Format placeholders:**
- `{{.ID}}` - Container ID
- `{{.Image}}` - Image name
- `{{.Command}}` - Command
- `{{.CreatedAt}}` - Creation time
- `{{.RunningFor}}` - Running time
- `{{.Status}}` - Status
- `{{.Ports}}` - Ports
- `{{.Names}}` - Container names
- `{{.Networks}}` - Network names
- `{{.Mounts}}` - Mount points
- `{{.Size}}` - Container size

**Filter Reference:**

| Filter | Description | Example |
|--------|-------------|---------|
| `id` | Container ID | `--filter "id=abc123"` |
| `name` | Container name | `--filter "name=web"` |
| `status` | Container status | `--filter "status=exited"` |
| `label` | Label key/value | `--filter "label=env=prod"` |
| `exited` | Exit code | `--filter "exited=0"` |
| `ancestor` | Parent image | `--filter "ancestor=nginx"` |

**Examples:**
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# List container IDs only
docker ps -aq

# List latest created container
docker ps -l

# List last 5 created containers
docker ps -n 5

# Format output as table
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Filter by status
docker ps -f "status=exited"

# Filter by name
docker ps --filter "name=web"

# Show sizes
docker ps -s

# Don't truncate output
docker ps --no-trunc
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| List running | `docker ps` |
| List all | `docker ps -a` |
| List IDs only | `docker ps -aq` |
| List latest | `docker ps -l` |
| List last 5 | `docker ps -n 5` |
| Show sizes | `docker ps -s` |
| Format table | `docker ps --format "table {{.Names}}\t{{.Status}}"` |
| Filter by status | `docker ps -f "status=running"` |
