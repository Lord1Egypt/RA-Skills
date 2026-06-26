# OpenClaw Gateway Manager

🦞 Unified Multi-Cloud OpenClaw Gateway Manager

---

## 💡 Philosophy

**Problem:** Users deploy OpenClaw across multiple platforms and clouds (local, JVS Claw, QClaw, cloud instances, etc.), but lack a unified management tool.

**Solution:** This skill automatically detects different configuration paths and provides unified management for all OpenClaw variants, regardless of where they're deployed.

**Core Principles:**
- 🔍 **Auto-Discovery** - Scan all possible configuration paths
- 🎯 **Unified Interface** - One set of commands for all instances
- ☁️ **Multi-Cloud** - Local, cloud, multi-vendor distributions
- 🛡️ **Safe Management** - Triple confirmation + automatic backup

---

## ✨ Features

- 🔍 **Smart Status Query** - Auto-detect all OpenClaw instances
- ✏️ **Modify Ports** - Automatically update config files + LaunchAgent plist
- 🔄 **Restart Gateways** - Safely restart specific or all gateways
- ✅ **Verify Configuration** - Check config consistency and port status
- ➕ **Create Instances** - One-click creation with LaunchAgent setup
- 🗑️ **Safe Deletion** - Triple confirmation + automatic backup
- 📡 **Port Scanning** - Intelligently identify all instances

---

## 🎯 Supported Distributions

| Distribution | Config Directory | Default Port | Developer | Status |
|--------------|-----------------|--------------|-----------|--------|
| **OpenClaw (Original)** | `~/.openclaw/` | 18789 | OpenClaw Community | ✅ |
| **JVS Claw (Alibaba)** | `~/.jvs/.openclaw/` | 18789 | Alibaba Cloud Wuying | ✅ |
| **QClaw (Tencent)** | `~/.qclaw/` | 28789 | Tencent | ✅ |
| **Cloud Claw** | `~/.claw-cloud/` | Custom | Cloud Service | 🔜 |
| **Custom Instance** | `~/.openclaw-<name>/` | Custom | User | ✅ |

**Identification:** Different distributions are identified by their configuration file paths.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/seastaradmin/openclaw-gateway-manager.git ~/.jvs/.openclaw/skills/gateway-manager
```

### Usage

```bash
# Check all gateway status (auto-detect all instances)
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-status.sh

# Check dependencies
~/.jvs/.openclaw/skills/gateway-manager/scripts/check-dependencies.sh

# Scan ports
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-scan-ports.sh

# Modify port
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-set-port.sh local-shrimp 18888

# Restart all gateways
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-restart.sh all

# Verify config
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-verify.sh local-shrimp

# Create new instance
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-create.sh test-bot 18899 openim

# Delete instance (triple confirmation)
~/.jvs/.openclaw/skills/gateway-manager/scripts/gateway-delete.sh test-bot
```

---

## 📝 Example Output

```
=== OpenClaw Gateway Instances ===
💡 Unified Management Platform - Multi-Cloud Support

🔍 Scanning all OpenClaw configuration paths...

🔹 Local Shrimp (JVS Claw)
   Main Port: 18789
   Aux Ports: 18791(Browser) 18792(Canvas)
   Config: ~/.jvs/.openclaw
   Status: ✅ Running (PID: 6512)
   Channel: openim
   Dashboard: http://127.0.0.1:18789/

🔹 Feishu Bot
   Main Port: 18790
   Aux Ports: 18792(Browser) 18793(Canvas)
   Config: ~/.openclaw
   Status: ✅ Running (PID: 76822)
   Channel: feishu
   Dashboard: http://127.0.0.1:18790/

🔹 QClaw (Tencent)
   Main Port: 28789
   Aux Ports: 28791(Browser) 28792(Canvas)
   Config: ~/.qclaw
   Status: ✅ Running (PID: 87107)
   Channel: wechat-access
   Dashboard: http://127.0.0.1:28789/

📊 Statistics:
   Detected ports: 9
```

---

## 🛡️ Safety Features

- **Triple confirmation for deletion** - Prevents accidental deletion
- **Automatic backup** - Backs up to `~/.openclaw-deleted-backups/`
- **Port availability check** - Verifies port is free before modification
- **Configuration validation** - Auto-verifies after changes
- **Dependency checker** - Auto-checks system dependencies

---

## 📦 Scripts

| Script | Function | Risk Level |
|--------|----------|------------|
| `gateway-status.sh` | Query status | 🟢 Safe |
| `gateway-scan-ports.sh` | Port scanning | 🟢 Safe |
| `gateway-set-port.sh` | Modify ports | 🟡 Medium |
| `gateway-restart.sh` | Restart gateway | 🟢 Safe |
| `gateway-verify.sh` | Verify config | 🟢 Safe |
| `gateway-create.sh` | Create instance | 🟡 Medium |
| `gateway-delete.sh` | Delete instance | 🔴 Dangerous |
| `check-dependencies.sh` | Check dependencies | 🟢 Safe |

---

## 🎯 Instance Aliases

| Alias | Config Directory | Default Port |
|-------|-----------------|--------------|
| `local-shrimp` / `本地虾` / `18789` | `~/.jvs/.openclaw/` | 18789 |
| `feishu` / `飞书` / `18790` | `~/.openclaw/` | 18790 |
| `qclaw` / `腾讯` / `28789` | `~/.qclaw/` | 28789 |

---

## ⚙️ System Requirements

### Operating System

- ✅ **macOS** (Required)
- ❌ Windows / Linux (Not supported)

Reason: Uses macOS-specific LaunchAgent, launchctl, and plutil.

### Dependencies

Run to check dependencies:

```bash
~/.jvs/.openclaw/skills/gateway-manager/scripts/check-dependencies.sh
```

**Required Tools:**

| Tool | Purpose | Install Command |
|------|---------|----------------|
| `jq` | JSON processing | `brew install jq` |
| `lsof` | Port check | Built-in macOS |
| `plutil` | plist editing | Built-in macOS |
| `launchctl` | LaunchAgent management | Built-in macOS |
| `curl` | HTTP requests | Built-in macOS |
| `node` | OpenClaw runtime | `brew install node` |

---

## ⚠️ Safety Notes

### Deletion Operation

- ✅ **Triple confirmation** - Requires 3 confirmations
- ✅ **Automatic backup** - Backs up before deletion
- ⚠️ **Destructive** - Uses `rm -rf` to delete config directories

**Recommendation:** Manually backup important data before first use

### Path Security

✅ **Fixed** - All paths use `$HOME` instead of hardcoded user paths

### LaunchAgent Permissions

- Creates user-level LaunchAgent only (`~/Library/LaunchAgents/`)
- No system-level permissions or sudo required
- Each user managed independently

---

## 📄 License

MIT

## 🔗 Links

- **GitHub**: https://github.com/seastaradmin/openclaw-gateway-manager
- **Author**: @seastaradmin
- **Version**: 1.0.1
