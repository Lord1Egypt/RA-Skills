# System Information Commands

Commands for getting Docker system information, version, and real-time events.

## docker version

Show the Docker version information.

```bash
docker version [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --format string` | Format output using a custom template |

**Format templates:**
- `json`: Print in JSON format
- Custom: `{{.Server.Version}}`, `{{.Client.Version}}`, etc.

**Examples:**
```bash
# Show version
docker version

# Show in JSON format
docker version --format '{{json .}}'

# Show specific information
docker version --format 'Server: {{.Server.Version}}\nClient: {{.Client.Version}}'

# Show client only
docker version --format '{{.Client.Version}}'

# Show server version
docker version --format '{{.Server.Version}}'
```

## docker info

Display system-wide information about Docker.

```bash
docker info [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --format string` | Format output using a custom template |

**Format templates:**
- `json`: Print in JSON format
- Custom: `{{.ServerVersion}}`, `{{.Containers}}`, `{{.Images}}`, etc.

**Examples:**
```bash
# Show system info
docker info

# Format output
docker info --format '{{.ServerVersion}}'
docker info --format 'Containers: {{.Containers}}\nImages: {{.Images}}'
docker info --format '{{json .}}'
```

## docker events

Get real time events from the Docker server.

```bash
docker events [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --filter filter` | Filter output based on conditions provided |
| `--format string` | Format output using a custom template |
| `--since string` | Show all events created since timestamp |
| `--until string` | Stream events until this timestamp |

**Event types:**
| Type | Description |
|------|-------------|
| `container` | Container events (create, start, stop, destroy, etc.) |
| `image` | Image events (pull, push, tag, remove, etc.) |
| `volume` | Volume events (create, mount, unmount, remove, etc.) |
| `network` | Network events (create, connect, disconnect, remove, etc.) |
| `daemon` | Daemon events |
| `plugin` | Plugin events |
| `service` | Service events |
| `node` | Node events |
| `secret` | Secret events |
| `config` | Config events |

**Filter keys:**
| Key | Description |
|-----|-------------|
| `type` | Event type (container, image, volume, network, daemon) |
| `container` | Filter by container name or ID |
| `image` | Filter by image name or ID |
| `volume` | Filter by volume name |
| `network` | Filter by network name |
| `event` | Event type (start, stop, die, create, destroy, etc.) |
| `label` | Filter by label |
| `plugin` | Filter by plugin |
| `config` | Filter by config |
| `secret` | Filter by secret |
| `service` | Filter by service |
| `node` | Filter by node |

**Examples:**
```bash
# Get all events (stream until Ctrl+C)
docker events

# Events since specific time
docker events --since '2024-01-01'
docker events --since '2h'
docker events --since 1704067200

# Events until specific time
docker events --until '2024-01-02'
docker events --until '1h'

# Filter by container
docker events --filter 'container=my_container'

# Filter by type
docker events --filter 'type=container'
docker events --filter 'type=image'
docker events --filter 'type=network'

# Filter by event type
docker events --filter 'event=start'
docker events --filter 'event=stop'
docker events --filter 'event=die'

# Combine filters
docker events --since '1h' --filter 'type=container' --filter 'event=start'

# Format output
docker events --format '{{.Time}} {{.Type}} {{.Action}} {{.Actor.ID}}'
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Show version | `docker version` |
| JSON version | `docker version --format '{{json .}}'` |
| Show system info | `docker info` |
| Show containers count | `docker info --format '{{.Containers}}'` |
| Stream events | `docker events` |
| Events since time | `docker events --since '1h'` |
| Filter by container | `docker events --filter 'container=<id>'` |
| Filter by type | `docker events --filter 'type=container'` |
| Filter by event | `docker events --filter 'event=start'` |
