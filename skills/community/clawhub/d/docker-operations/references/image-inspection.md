# Image Inspection Commands

Commands for inspecting Docker objects - containers, images, volumes, networks, and more.

## docker inspect

Return low-level information on Docker objects.

```bash
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --format string` | Format output using a custom template |
| `-s, --size` | Display total file sizes if the type is container |
| `--type string` | Return JSON for specified type |

**Format templates:**
- `json`: Print in JSON format
- Custom: `{{.Id}}`, `{{.Config}}`, `{{.NetworkSettings}}`, etc.

**Examples:**
```bash
docker inspect my_container
docker inspect --format '{{.Config.Image}}' my_container
docker inspect --format '{{json .}}' my_container
docker inspect -s my_container
docker inspect --type container my_container
```

## docker inspect Reference

### Common Data Types

- **Container**: Config, NetworkSettings, Mounts, State, Created
- **Image**: Config, Architecture, Os, RootFS, History
- **Volume**: Mountpoint, Driver, Labels, Scope
- **Network**: IPAM, Driver, Scope, Options
- **Daemon**: ServerVersion, OS, Arch, KernelVersion

### Useful Format Examples

```bash
# Get container IP address
docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my_container

# Get container log path
docker inspect --format '{{.LogPath}}' my_container

# Get image entrypoint
docker inspect --format '{{.Config.Entrypoint}}' my_image

# Get all exposed ports
docker inspect --format '{{json .Config.ExposedPorts}}' my_container

# Get mount points
docker inspect --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' my_container

# Get container status
docker inspect --format '{{.State.Status}}' my_container

# Get restart count
docker inspect --format '{{.RestartCount}}' my_container
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Inspect container | `docker inspect <container>` |
| Inspect image | `docker inspect <image>` |
| Format JSON | `docker inspect --format '{{json .}}' <id>` |
| Show size | `docker inspect -s <container>` |
| Specific type | `docker inspect --type container <id>` |
