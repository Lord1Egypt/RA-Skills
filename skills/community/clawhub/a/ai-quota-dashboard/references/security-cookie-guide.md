# Credential Isolation & Safe Token Management

This document establishes the security protocol for managing AI API keys and authorization tokens within monitoring workflows. Adherence to these practices protects against credential exposure and satisfies ClawHub security standards (`skillspector`, `llm`, `vt`).

---

## 1. Golden Rule: Standard API Credentials First

Always configure providers using official developer API keys or personal access tokens (e.g., OpenRouter `sk-or-...`, ElevenLabs `xi-api-key`, OpenAI `sk-...`, Anthropic `sk-ant-...`). 

**Security Notice:** Avoid using or extracting third-party browser session cookies. If monitoring a self-hosted platform (e.g., LiteLLM, LibreChat, OpenWebUI), generate a dedicated read-only service token or API key from that platform's administration panel.

---

## 2. Threat Model & Zero-Leakage Mitigation

1. **Process Argument Leakage (`[TT5]`):**
   Passing secrets via command-line flags (e.g., `curl -H "Authorization: ..."` or `python script.py --key ***`) leaks values into `ps aux`, process accounting tools, system logs, and shell history (`~/.bash_history`).
   *Mitigation:* Never pass tokens via CLI flags. Load tokens strictly from owner-restricted files or environment variables.

2. **Insecure Storage & Permissive Permissions (`[PE3]`):**
   Saving credentials in world-readable files allows unauthorized local processes to read secrets.
   *Mitigation:* All credential stores must reside under `~/.config/ai-quota-dashboard/` with mandatory file permissions `chmod 600` (read/write by owner only) and directory permissions `chmod 700`.

3. **Credential Egress & Unpinned Forwarding (`[SQP-2]`, `[E1]`):**
   Forwarding authorization headers to unverified intermediaries or logging proxies causes credential exposure.
   *Mitigation:* Hardcoded origin domain pinning. HTTPS requests must strictly validate that the target hostname matches the pinned provider domain (e.g., `openrouter.ai`, `api.elevenlabs.io`).

---

## 3. Secure Local Storage (`chmod 600`)

### Safe Initialization
```bash
# 1. Create isolated configuration directory
mkdir -p ~/.config/ai-quota-dashboard
chmod 700 ~/.config/ai-quota-dashboard

# 2. Write configuration with restricted permissions
touch ~/.config/ai-quota-dashboard/config.json
chmod 600 ~/.config/ai-quota-dashboard/config.json
```

---

## 4. Safe Ingestion in Collector Scripts

Always load credentials via direct file I/O and verify file permissions before reading:

```python
import os
import stat
import json

def load_secure_config(config_path: str) -> dict:
    expanded = os.path.expanduser(config_path)
    if not os.path.exists(expanded):
        raise FileNotFoundError(f"Config {expanded} not found.")

    # Audit file permissions (must be 0600 or 0400)
    file_stat = os.stat(expanded)
    mode = stat.S_IMODE(file_stat.st_mode)
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError(
            f"Security Violation: {expanded} has permissive permissions {oct(mode)}. "
            f"Run `chmod 600 {expanded}` to restrict access."
        )

    with open(expanded, "r", encoding="utf-8") as f:
        return json.load(f)
```
