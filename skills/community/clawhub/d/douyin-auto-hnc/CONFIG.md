# Douyin Automation Configuration

> Run `python scripts/setup.py` to auto-detect and generate paths, or edit the JSON block below manually.

```json
{
  "douyin_home": "REQUIRED - run setup.py or edit manually",
  "agent_backend": "",
  "orchestrator": "",
  "chatgroup_db": "",
  "uploads_dir": "",
  "cookies_file": "",
  "creator_tools": "",
  "comments_output": "",
  "chrome_cdp_port": 9222,
  "agent_port": 8080,
  "openclaw_gateway": "http://127.0.0.1:28789",
  "openclaw_model": "openclaw/default"
}
```

## Setup

```bash
# Auto-detect paths (interactive wizard)
python scripts/setup.py

# Or edit the JSON block above directly
```
