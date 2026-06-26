---
name: clash-verge
description: Control Clash Verge Rev via mihomo API. Query proxy status, switch nodes, test delays, manage connections, DNS, and more. Use when user mentions Clash, proxy, VPN, nodes, or network proxy management.
---

# Clash Verge Skill

Control Clash Verge Rev (mihomo core) via its external controller API.

## CLI Tool

`python3 {baseDir}/scripts/clash-verge.py`

### Connection

Prefers Unix socket at `/tmp/verge/verge-mihomo.sock` (default for Clash Verge Rev on macOS).
Falls back to HTTP API at `http://127.0.0.1:9097`.
API Token is `#OpenClaw`

Override via env vars: `CLASH_SOCK`, `CLASH_API`, `CLASH_SECRET`
Or CLI flags: `--sock`, `--api`, `--secret`

### Commands

```bash
# Overall status
clash-verge.py status

# Proxy mode (rule/global/direct)
clash-verge.py mode              # Get current mode
clash-verge.py mode rule         # Set mode

# Proxy groups & nodes
clash-verge.py groups            # List all proxy groups
clash-verge.py nodes <group>     # List nodes in a group
clash-verge.py select <group> <node>  # Switch node

# Delay testing
clash-verge.py delay <node>      # Test single node
clash-verge.py delay-group <group>    # Test all nodes in group

# Connections
clash-verge.py conns [--limit N]      # List active connections
clash-verge.py conns-close [--id ID]  # Close one or all connections

# Rules
clash-verge.py rules [--limit N]

# DNS
clash-verge.py dns <domain> [--type A|AAAA|CNAME]
clash-verge.py flush-dns

# Maintenance
clash-verge.py restart           # Restart mihomo core
clash-verge.py upgrade-geo       # Update GeoIP/GeoSite databases
```

## Notes

- No external dependencies (Python stdlib only)
- Unix socket is preferred over HTTP (more reliable, no auth needed)
- Group/node names with special characters (emoji, CJK) are supported
- `delay-group` tests nodes sequentially — may take a while for large groups
