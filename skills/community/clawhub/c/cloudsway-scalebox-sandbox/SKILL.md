# ScaleBox Sandbox Skill

Create and manage isolated cloud sandboxes for secure code execution.

## When to Use

- Running untrusted code in an isolated environment
- Browser automation (browser-use, computer-use templates)
- Testing scripts that may have side effects
- Remote code execution without local resource impact
- Creating temporary development environments

---

## Prerequisites

### 1. Get API Key

Register at [ScaleBox Dashboard](https://www.scalebox.dev) to get your API key.

Set environment variable:
```bash
export SCALEBOX_API_KEY="your-api-key-here"
```

### 2. Install CLI

Download the official CLI from [ScaleBox Documentation](https://www.scalebox.dev/docs/en/cli/installation):

```bash
# Visit official docs for platform-specific downloads
# https://www.scalebox.dev/docs/en/cli/installation

# After installation, authenticate:
scalebox-cli auth login --api-key $SCALEBOX_API_KEY --server-url https://api.scalebox.dev
```

**Security Note**: Always download CLI from official sources. Verify checksums when available.

### 3. Server URL

```
https://api.scalebox.dev
```

---

## Port Access URL Format

**Important**: ScaleBox uses port prefixes, not port suffixes.

### Method 1: Specify ports at creation time (Recommended)

Use API to specify `custom_ports` when creating the sandbox:

```bash
curl -X POST "https://api.scalebox.dev/v1/sandboxes" \
  -H "X-API-Key: $SCALEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "base",
    "name": "my-sandbox",
    "timeout": 3600,
    "custom_ports": [
      {"port": 8080, "name": "web-server", "protocol": "TCP"}
    ]
  }'
```

### Method 2: Add port to running sandbox

If you need to add a port after creation:

```bash
# CLI
scalebox-cli sandbox port add <sandbox-id> --port 8080 --name web-server --protocol TCP

# API
curl -X POST "https://api.scalebox.dev/v1/sandboxes/{sandbox_id}/ports" \
  -H "X-API-Key: $SCALEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"port": 8080, "name": "web-server", "protocol": "TCP"}'
```

### Access URL Format

**Format**: `https://{port}-{sandbox_domain}/path`

**Example**:
- Sandbox domain: `sbx-abc123.k27xn5o3lnw5dan3x.scalebox.dev`
- Port: 8080
- **Correct URL**: `https://8080-sbx-abc123.k27xn5o3lnw5dan3x.scalebox.dev/`
- ❌ **Wrong**: `https://sbx-abc123.k27xn5o3lnw5dan3x.scalebox.dev:8080/`

---

## Available Templates

| Template | CPU | Memory | Use Case |
|----------|-----|--------|----------|
| base | 2 | 512MB | Basic sandbox |
| code-interpreter | 2 | 1GB | Jupyter environment |
| browser-use | 2 | 2GB | Browser automation (VNC) |
| browser-use-headless | 4 | 4GB | Browser automation (headless) |
| desktop | 8 | 8GB | Desktop environment (VNC) |
| computer-use-preview | 2 | 2GB | Google Computer Use |

---

## Three Ways to Use ScaleBox

| Method | Best For | Notes |
|--------|----------|-------|
| **CLI** | File operations, command execution | Most powerful, cross-platform |
| **REST API** | Lifecycle management | Auth via `X-API-Key` header |
| **Python SDK** | Programmatic access | `pip install scalebox-sdk` |

---

## Method 1: CLI Commands

### 1.1 Sandbox Lifecycle

```bash
# Create sandbox
scalebox-cli sandbox create --template <name> --name <name> --timeout <seconds>

# List sandboxes
scalebox-cli sandbox list

# Get sandbox details
scalebox-cli sandbox get <sandbox-id>

# Pause sandbox (preserves state)
scalebox-cli sandbox pause <sandbox-id>

# Resume paused sandbox
scalebox-cli sandbox resume <sandbox-id>

# Terminate sandbox immediately
scalebox-cli sandbox terminate <sandbox-id>

# Delete sandbox and resources
scalebox-cli sandbox delete <sandbox-id>
```

**Create parameters**:
- `--template`: Template name or ID (default: `base`)
- `--name`: Sandbox name (optional, auto-generated)
- `--timeout`: Timeout in seconds (default: 300)
- `--cpu`: CPU count (minimum: 2)
- `--memory`: Memory in MB
- `--storage`: Storage in GB
- `--async`: Fire-and-forget mode - returns immediately, sandbox may still be starting. **You must poll status yourself.**
- `--auto-pause`: Pause on timeout instead of terminate

**Important: async vs sync**:
- **Sync mode** (default, no `--async`): Waits for sandbox to be fully running before returning. The returned sandbox is ready to use.
- **Async mode** (`--async`): Returns immediately after creating the request. The sandbox may still be starting. You must poll `sandbox get <id>` until `status: running` before using it.

```bash
# Sync mode (recommended) - sandbox is ready when command returns
scalebox-cli sandbox create --template base --timeout 600
# Output includes sandbox ID, ready to use

# Async mode - need to wait
scalebox-cli sandbox create --template base --timeout 600 --async
# Returns immediately, sandbox may still be starting
# Must poll: scalebox-cli sandbox get <id> until status is "running"
```

### 1.2 File Operations

```bash
# Upload file
scalebox-cli sandbox upload <sandbox-id> <local-path> <remote-path>

# Upload directory recursively
scalebox-cli sandbox upload <sandbox-id> ./project /workspace/project --recursive

# Download file
scalebox-cli sandbox download <sandbox-id> <remote-path> <local-path>

# List files
scalebox-cli sandbox ls <sandbox-id> <remote-path>
```

**Note**: Remote path must be absolute (e.g., `/workspace/file.py`).

### 1.3 Command Execution

```bash
# Execute command
scalebox-cli sandbox exec <sandbox-id> "<command>"

# With working directory
scalebox-cli sandbox exec <sandbox-id> "python3 script.py" --cwd /workspace

# With timeout
scalebox-cli sandbox exec <sandbox-id> "npm install" --timeout 120
```

---

## Method 2: REST API

### 2.1 Authentication

All requests require `X-API-Key` header:
```bash
curl -H "X-API-Key: $SCALEBOX_API_KEY" https://api.scalebox.dev/v1/sandboxes
```

### 2.2 Sandbox Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create sandbox | POST | `/v1/sandboxes` |
| List sandboxes | GET | `/v1/sandboxes` |
| Get sandbox | GET | `/v1/sandboxes/{id}` |
| Delete sandbox | DELETE | `/v1/sandboxes/{id}` |
| Pause sandbox | POST | `/v1/sandboxes/{id}/pause` |
| Resume sandbox | POST | `/v1/sandboxes/{id}/resume` |

**Note**: File operations (upload/download/exec) are only available via CLI or SDK.

### 2.3 API Example

```bash
# Create sandbox
curl -X POST "https://api.scalebox.dev/v1/sandboxes" \
  -H "X-API-Key: $SCALEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"template": "base", "name": "my-sandbox", "timeout": 600}'
```

---

## Method 3: Python SDK

### 3.1 Installation

```bash
pip install scalebox-sdk
```

Module name: `scalebox` (not `scalebox_sdk`)

### 3.2 Basic Usage

```python
import scalebox
import os

# Create sandbox
sandbox = scalebox.Sandbox.create(
    template="base",
    timeout=600,
    api_key=os.environ.get("SCALEBOX_API_KEY")
)

print(f"Sandbox ID: {sandbox.sandbox_id}")

# Get signed URLs for file operations
upload_url = sandbox.upload_url(path="/workspace/test.py")
download_url = sandbox.download_url(path="/workspace/output.json")

# Kill sandbox
sandbox.kill()
```

---

## Typical Workflow

```bash
# 1. Create sandbox
sandbox_id=$(scalebox-cli sandbox create --template code-interpreter --name my-task --async | grep "Sandbox ID:" | awk '{print $3}')

# 2. Upload code
scalebox-cli sandbox upload $sandbox_id ./script.py /workspace/script.py

# 3. Execute
scalebox-cli sandbox exec $sandbox_id "python3 /workspace/script.py"

# 4. Download results
scalebox-cli sandbox download $sandbox_id /workspace/output.json ./output.json

# 5. Cleanup
scalebox-cli sandbox delete $sandbox_id
```

---

## Security Notes

- Sandboxes are completely isolated from local machine
- All file paths must be absolute (no `..` traversal)
- Internet access enabled by default (disable with `--internet=false`)
- Credentials never stored in database
- **Minimum CPU**: 2 cores
- **Always download CLI from official sources**

---

## Error Handling

| Error | Solution |
|-------|----------|
| `CPU count must be at least 2` | Use `--cpu 2` or higher |
| `health check timeout` | Check status with `sandbox get` |
| `Sandbox not found` | Verify sandbox ID |
| `Timeout exceeded` | Create new sandbox |

---

## Links

- **Official Website**: https://www.scalebox.dev
- **Documentation**: https://www.scalebox.dev/docs
- **CLI Installation**: https://www.scalebox.dev/docs/en/cli/installation
- **API Reference**: https://www.scalebox.dev/docs/en/api

---

## Version

- Skill: 1.0.5
- CLI: v1.3.4
- SDK: v0.1.9
- API: v1

Last updated: 2026-03-21