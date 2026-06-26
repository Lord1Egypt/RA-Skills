# OpenClaw Setup

## 1. Install AOMS

```bash
pip install cortex-mem
```

This installs the `cortex-mem` CLI and Python package from PyPI.

## 2. Start the Service

```bash
cortex-mem start --daemon
```

Or via systemd (recommended for always-on):

```ini
[Unit]
Description=AOMS - Always-On Memory Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/data
ExecStart=/path/to/venv/bin/cortex-mem start --port 9100
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

## 3. Configure OpenClaw

Add the memory provider to your OpenClaw config:

```yaml
# ~/.openclaw/config.yaml
memory:
  provider: cortex-mem
  url: http://localhost:9100
```

Then restart OpenClaw:

```bash
openclaw gateway restart
```

## 4. Session Boot Script

Create a boot script in your workspace:

```python
# boot_aoms.py
import httpx, sys

try:
    r = httpx.post("http://localhost:9100/recall", json={
        "task": "session boot — what's recent and relevant",
        "token_budget": 300,
        "format": "markdown"
    }, timeout=5.0)
    if r.status_code == 200:
        data = r.json()
        print(data["context"])
        print(f"\n---\nAOMS: {data['tokens']} tokens from {len(data['sources'])} sources")
except Exception as e:
    print(f"AOMS unavailable: {e}", file=sys.stderr)
```

Reference from AGENTS.md:
```markdown
## Every Session Boot
1. Run: `python3 boot_aoms.py`
2. Review recalled context
```

## 5. Helper Functions

Copy `openclaw_integration.py` from the cortex-mem package into your workspace for convenient logging:

```python
from openclaw_integration import log_achievement, log_error, log_fact, sync_memory_md

# Log events
await log_achievement("Shipped feature X", "All tests passing")
await log_error("Deploy failed", "Missing env var DATABASE_URL")
await log_fact("auth-service", "requires", "Redis 7+")

# Sync MEMORY.md to AOMS
await sync_memory_md(Path("MEMORY.md").read_text())
```

## 6. Optional: Workspace Memory Migration

If you have existing flat-file memory (MEMORY.md, daily logs), you can import it into AOMS:

```bash
cortex-mem migrate ~/.openclaw/workspace
```

This parses Markdown files and creates structured episodic/semantic entries. It **does not modify or delete** your original files.

> **Review first:** Run `cortex-mem migrate --dry-run ~/.openclaw/workspace` to see what would be imported before committing.
