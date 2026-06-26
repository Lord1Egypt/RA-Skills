# Alert System

---

## Alert Levels

| Level | Threshold | Action |
|--------|-----------|--------|
| ✅ Normal | < 60% | Silent |
| 🟡 Watch | 60-79% | Suggest compression |
| 🔴 Critical | 80-94% | Pause auto-write, force suggestion |
| 🚨 Danger | ≥ 95% | Block writes, must compress |

---

## Alert Display

**Normal**: no output

**Watch (60-79%)**:
```
[🦅 Context: 67% / 80%]
  today.md: 156 lines (suggest compress)
  LanceDB Working: 23 memories
  → /hawk compress
```

**Critical (80-94%)**:
```
[🦅⚠️ Context: 84% / 80%] 🔴 Context high
  Largest block: today.md (156 lines)
  Auto-write paused. Compress before continuing.
  → /hawk compress today summarize
  → /hawk strategy A (high-importance mode)
```

**Danger (≥95%)**:
```
[🦅🚨 Context: 97% / 80%] 🚨 Context critical
  Writes blocked. Compress immediately.
  → /hawk compress all summarize --force
```

---

## Config

| Config key | Default | Description |
|-----------|---------|-------------|
| `hawk_alert_enabled` | `true` | Toggle alerts |
| `hawk_alert_threshold` | `60` | Watch threshold (%) |
| `hawk_critical_threshold` | `80` | Critical threshold (%) |
| `hawk_danger_threshold` | `95` | Danger threshold (%) |

---

## Auto-Defense at High Context

When context > 80%:
1. **Pause** today.md auto-append (prevent further inflation)
2. **Suggest** compression command
3. **Recommend** switching to strategy A (high-importance)
4. **Show** /hawk introspect for details

When context > 95%:
1. **Block** all non-essential content writes
2. **Force** compression prompt
3. **Show** emergency compress command

---

## Commands

```bash
hawk alert on         # Enable alerts
hawk alert off        # Disable alerts
hawk alert set 70    # Set watch threshold to 70%
hawk alert set 60 80 95  # Set all three thresholds
hawk alert status     # Show current config
```
