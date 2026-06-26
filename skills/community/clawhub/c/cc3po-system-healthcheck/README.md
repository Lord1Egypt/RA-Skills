# system-healthcheck

**Three-tier system health monitoring for OpenClaw**

[English](SKILL.md) | [简体中文](README.zh-CN.md)

---

## Features

- **L1 Fast Check** (<200ms): Definition file existence check
- **L2 Hourly Check** (<5s): System resources, services, logs
- **L3 Daily Audit** (<60s): Comprehensive system audit
- **Heartbeat Mechanism**: Quiet when healthy, alert on issues
- **i18n Support**: Auto-detect language (en/zh-CN)
- **Zero External Dependencies**: Works out of the box

---

## Installation

```bash
clawhub install system-healthcheck
```

Or manually:

```bash
git clone https://github.com/your-username/system-healthcheck.git ~/.openclaw/skills/system-healthcheck
```

---

## Quick Start

### 1. L1 Fast Check (Manual)

```bash
cd ~/.openclaw/skills/system-healthcheck
python scripts/l1_fast_check.py
```

**Example Output:**
```
L1 Fast Check · 2026-03-23 09:00:00

✅ SOUL.md (2KB)
✅ IDENTITY.md (1KB)
✅ AGENTS.md (5KB)
✅ TOOLS.md (2KB)
✅ MEMORY.md (15KB)

━━━━━━━━━━━━━━━━━━━━━━━━
✅ All definition files OK
Duration: 45ms
```

### 2. L2 Hourly Check (Manual)

```bash
python scripts/l2_hourly_check.py
```

**Example Output:**
```
🦞 System Health Check · 2026-03-23 09:00:00

✅ Disk Usage: 45% (threshold: 80%)
✅ Memory Usage: 1.2GB / 8GB
✅ Cron Service: Running
✅ OpenClaw Gateway: Healthy
✅ Log Files: 12MB

━━━━━━━━━━━━━━━━━━━━━━━━
✅ All checks passed
Duration: 1.2s
```

### 3. Setup Crontab

```bash
# View example
cat templates/crontab_example.txt

# Edit crontab
crontab -e
```

### 4. Heartbeat Check

```bash
python scripts/heartbeat.py
```

**Output when healthy:**
```
HEARTBEAT_OK
```

**Output when issues detected:**
```
🦞 Heartbeat Check · 2026-03-23 14:30:00

⚠️ Disk Usage: 85% (exceeds 80%)
✅ Memory Usage: 2.1GB / 8GB
...
```

---

## Configuration

Edit `config/default_config.yaml`:

```yaml
# Internationalization
i18n:
  auto_detect: true  # Auto-detect system language
  # locale: zh-CN    # Or specify manually
  fallback: en       # Fallback language

# Thresholds
thresholds:
  disk_warning: 80      # Disk warning (%)
  disk_critical: 95     # Disk critical (%)
  memory_warning_mb: 500  # Memory warning (MB)
  log_size_mb: 100      # Log size warning (MB)

# L1 Fast Check
l1:
  enabled: true
  timeout_ms: 200
  critical_files:
    - SOUL.md
    - IDENTITY.md
    - AGENTS.md
    - TOOLS.md
    - MEMORY.md

# L2 Hourly Check
l2:
  enabled: true
  interval_minutes: 60
  timeout_seconds: 5

# L3 Daily Audit
l3:
  enabled: true
  schedule: "0 8 * * *"  # Daily at 08:00
  timeout_seconds: 60

# Heartbeat
heartbeat:
  enabled: true
  work_hours_start: 9
  work_hours_end: 18
  quiet_on_ok: true  # Silent when all OK
```

---

## Scripts Reference

### l1_fast_check.py

**Purpose**: Fast definition file check (<200ms)

**Options**:
- `--json`: JSON output
- `--quiet`: Silent mode (exit code only)

**Exit Codes**:
- `0`: All files exist and readable
- `1`: Missing or unreadable files

---

### l2_hourly_check.py

**Purpose**: System health check

**Checks**:
- Disk usage
- Memory usage
- Cron service status
- OpenClaw Gateway status
- Log file sizes
- Python environment

**Options**:
- `--json`: JSON output
- `--quiet`: Silent mode

**Exit Codes**:
- `0`: All checks passed
- `1`: One or more checks failed

---

### l3_daily_audit.py

**Purpose**: Comprehensive daily audit

**Status**: Coming in v1.1.0

---

### heartbeat.py

**Purpose**: Work-hours heartbeat mechanism

**Behavior**:
- During work hours (9-18): Output on issues, `HEARTBEAT_OK` when healthy
- Outside work hours: Silent (no output)

**Options**:
- `--force`: Force output (ignore work hours)
- `--json`: JSON output

---

## Internationalization

### Supported Languages

- `en` - English
- `zh-CN` - 简体中文

### Auto-Detection

Automatically detects from system locale:

```bash
echo $LANG  # e.g., zh_CN.UTF-8 or en_US.UTF-8
```

### Manual Override

```bash
# Set via environment
export OPENCLAW_LOCALE=zh-CN
python scripts/l2_hourly_check.py

# Or edit config
# i18n.locale: zh-CN
```

### Adding New Languages

1. Create `locales/<locale>.yaml`
2. Copy structure from `locales/en.yaml`
3. Translate all values

---

## File Structure

```
system-healthcheck/
├── SKILL.md                    # Skill metadata & description
├── README.md                   # English documentation
├── README.zh-CN.md             # Chinese documentation
│
├── config/
│   └── default_config.yaml     # Default configuration
│
├── locales/
│   ├── en.yaml                 # English translations
│   └── zh-CN.yaml              # Chinese translations
│
├── scripts/
│   ├── i18n.py                 # Internationalization module
│   ├── l1_fast_check.py        # L1 fast check
│   ├── l2_hourly_check.py      # L2 hourly check
│   ├── l3_daily_audit.py       # L3 daily audit (TODO)
│   └── heartbeat.py            # Heartbeat mechanism
│
└── templates/
    └── crontab_example.txt     # Crontab configuration example
```

---

## FAQ

### Q: How do I disable a specific check?
A: Edit `config/default_config.yaml` and set `enabled: false` for that check.

### Q: How do I change thresholds?
A: Modify the `thresholds` section in `config/default_config.yaml`.

### Q: Why is heartbeat not outputting?
A: During work hours, it outputs `HEARTBEAT_OK` when healthy (quiet mode). Outside work hours, it's silent.

### Q: Can I add custom checks?
A: Yes! Add a function to `scripts/l2_hourly_check.py` and call it in `run_l2_check()`.

### Q: Does this work on macOS?
A: Yes! Both Linux and macOS are supported. Some checks adapt to the platform.

---

## Requirements

- Python 3.8+
- Linux or macOS
- No external dependencies

**Optional**:
- `rich`: Colorful console output
- `pyyaml`: YAML configuration parsing

---

## License

MIT

---

## Contributing

Contributions welcome! Please open an issue or PR.

---

## Changelog

### v1.0.0 (2026-03-23)
- ✨ Initial release
- ✅ L1/L2 checks implemented
- ✅ Heartbeat mechanism
- ✅ i18n support (en/zh-CN)
- 📝 Documentation

### Planned

- v1.1.0: L3 daily audit
- v1.2.0: Custom check plugins
- v1.3.0: More languages (ja, ko, zh-TW)
