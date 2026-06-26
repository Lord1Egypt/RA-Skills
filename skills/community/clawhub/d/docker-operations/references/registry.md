# Registry Commands

Commands for managing Docker registries - logging in, pushing/pulling images, and searching.

## docker login

Log in to a Docker registry.

```bash
docker login [OPTIONS] [SERVER]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-p, --password string` | Password or Personal Access Token (PAT) |
| `--password-stdin` | Take the Password or Personal Access Token (PAT) from stdin |
| `-u, --username string` | Username |

**Examples:**
```bash
# Interactive login (prompts for password)
docker login

# Login to specific registry
docker login myregistry.com

# Non-interactive login
docker login -u "username" -p "password" myregistry.com

# Non-interactive from file or pipe (recommended for security)
echo "$PASSWORD" | docker login -u "$USER" --password-stdin myregistry.com
```

> ⚠️ Using `--password-stdin` is recommended for scripting to avoid saving passwords in shell history.

## docker logout

Log out from a Docker registry.

```bash
docker logout [SERVER]
```

**Examples:**
```bash
# Logout from default registry (Docker Hub)
docker logout

# Logout from specific registry
docker logout myregistry.com
```

## docker search

Search Docker Hub for images.

```bash
docker search [OPTIONS] TERM
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --filter filter` | Filter output based on conditions provided |
| `--format string` | Pretty-print search using a Go template |
| `--limit int` | Max number of search results (default: 25, max: 100) |
| `--no-trunc` | Don't truncate output |

**Filter values:**
| Filter | Description |
|--------|-------------|
| `stars=<n>` | Images with at least n stars |
| `is-automated=<true\|false>` | Automated builds |
| `is-official=<true\|false>` | Official images |

**Format placeholders:**
- `{{.Name}}` - Image name
- `{{.Description}}` - Image description
- `{{.Stars}}` - Number of stars
- `{{.Official}}` - Is official ("OK" or "")
- `{{.Automated}}` - Is automated ("OK" or "")

**Examples:**
```bash
# Search for images
docker search nginx

# Search with filters
docker search --filter "stars=100" nginx
docker search --filter "is-official=true" ubuntu
docker search --filter "is-automated=true" nginx

# Limit results
docker search --limit 10 nginx

# Format output
docker search --format "table {{.Name}}\t{{.Stars}}\t{{.Official}}" nginx

# No truncation
docker search --no-trunc nginx
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Login to registry | `docker login <server>` |
| Login with user/pass | `docker login -u <user> -p <pass> <server>` |
| Secure login | `echo $PASS \| docker login -u <user> --password-stdin` |
| Logout | `docker logout <server>` |
| Search images | `docker search <term>` |
| Search official | `docker search --filter "is-official=true" <term>` |
| Search top stars | `docker search --filter "stars=100" <term>` |
| Limit results | `docker search --limit 10 <term>` |
