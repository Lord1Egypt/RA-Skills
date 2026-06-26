# ClawShorts — Per-Device Config & Auto-Detection Spec

## Goal

Replace hardcoded detection constants with a database-backed, per-device configurable system. Screen resolution is auto-detected via ADB on first setup, and detection thresholds are stored in SQLite with global defaults and per-device overrides.

---

## 1. Database Schema

### 1.1 `config` table — global system defaults

```sql
CREATE TABLE IF NOT EXISTS config (
    key          TEXT PRIMARY KEY,
    value        REAL NOT NULL,
    description  TEXT,
    updated_at   TEXT DEFAULT (datetime('now'))
);
```

**Initial rows (inserted on first run / migration):**

| key | value | description |
|-----|-------|-------------|
| `shorts_width_threshold` | 0.30 | player width must be < this ratio of screen width |
| `shorts_max_aspect_ratio` | 1.3 | portrait aspect ratio cap; ar < this = portrait |
| `shorts_fallback_height_ratio` | 0.4 | fallback: player height must exceed this ratio of screen height |
| `shorts_delta_cap` | 300 | max seconds accumulated per poll (prevents clock jumps) |
| `default_screen_width` | 1920 | fallback assumed screen width (used if auto-detect fails) |
| `default_screen_height` | 1080 | fallback assumed screen height |

### 1.2 `devices` table — add new columns

All 6 detection parameters are per-device. Every column is nullable — NULL means "use the global default from the `config` table."

```sql
ALTER TABLE devices ADD COLUMN screen_width              INTEGER;  -- pixels, auto-detected or manually set
ALTER TABLE devices ADD COLUMN screen_height             INTEGER;  -- pixels, auto-detected or manually set
ALTER TABLE devices ADD COLUMN width_threshold          REAL;    -- e.g. 0.30; NULL = global default
ALTER TABLE devices ADD COLUMN max_aspect_ratio         REAL;    -- e.g. 1.3; NULL = global default
ALTER TABLE devices ADD COLUMN fallback_height_ratio    REAL;    -- e.g. 0.4; NULL = global default
ALTER TABLE devices ADD COLUMN delta_cap               REAL;    -- e.g. 300; NULL = global default
ALTER TABLE devices ADD COLUMN updated_at TEXT DEFAULT (datetime('now'));
```

### 1.3 Full per-device config keyspace

Each of these 6 parameters can be set per-device (in `devices` table) or globally (in `config` table):

| key | default | per-device column | description |
|-----|---------|------------------|-------------|
| `shorts_width_threshold` | 0.30 | `width_threshold` | player width must be < this ratio of screen width |
| `shorts_max_aspect_ratio` | 1.3 | `max_aspect_ratio` | portrait if ar < this value |
| `shorts_fallback_height_ratio` | 0.4 | `fallback_height_ratio` | fallback: player height must exceed this ratio of screen height |
| `shorts_delta_cap` | 300 | `delta_cap` | max seconds accumulated per poll (prevents clock jumps) |
| `default_screen_width` | 1920 | `screen_width` | screen width in pixels |
| `default_screen_height` | 1080 | `screen_height` | screen height in pixels |

### 1.4 Schema migration function

- If `config` table doesn't exist, create it and seed with defaults
- If `devices` columns don't exist, add them with `NULL` defaults
- Existing devices keep `NULL` for all new columns → fall back to global defaults
- This makes the migration zero-downtime for existing installations

---

## 2. Screen Auto-Detection (ADB)

### 2.1 Detection command

```python
def detect_screen_resolution(ip: str) -> tuple[int, int] | None:
    """Query screen size via ADB. Returns (width, height) or None on failure."""
    result = subprocess.run(
        ["adb", "-s", ip, "shell", "dumpsys", "display"],
        capture_output=True, text=True, timeout=5
    )
    # Parse mDisplayWidth / mDisplayHeight from output
    # Fallback: use global default_screen_width/height from config
```

### 2.2 When auto-detect runs

| Event | Action |
|-------|--------|
| `shorts setup <IP>` (first time) | Detect screen resolution, store in `devices.screen_width/height` |
| `shorts add <IP>` | Detect and store |
| `shorts connect <IP>` | Re-detect and update stored values |
| Auto-detect fails | Use `default_screen_width/height` from `config` table |

---

## 3. Config Resolution (Priority Order)

For any device, values are resolved as:

```
per-device column (if not NULL)
    ?? global config key (from config table)
        ?? hardcoded Python default (last resort, for migration safety)
```

### Example

| Device | `width_threshold` col | Resolution |
|--------|----------------------|------------|
| loft (192.168.1.239) | NULL | global default: 0.30 |
| sofa (192.168.1.202) | 0.35 | per-device: 0.35 |

All 6 keys follow the same per-device / global precedence. If a per-device column is NULL, the global `config` table value is used.

---

## 4. Daemon Changes (`clawshorts-daemon.py`)

### 4.1 Load config at startup

```python
def _load_global_config() -> dict[str, float]:
    """Load all config keys from SQLite into a dict."""
    rows = db.get_all_config()
    return {key: value for key, value in rows}

def _get_device_config(ip: str, global_cfg: dict) -> dict:
    """Merge per-device overrides onto global config."""
    dev = db.get_device(ip)
    return {
        key: getattr(dev, key, None) or global_cfg.get(key)
        for key in ["screen_width", "screen_height", "width_threshold",
                    "max_aspect_ratio", "fallback_height_ratio", "delta_cap"]
    }
```

### 4.2 Per-device state

The per-device state dict (line ~78) currently has `screen_w` / `screen_h` as cached scalars. These should be loaded from device config and refreshed on reconnect.

```python
# Before: screen_w/screen_h were hardcoded 1920/1080
# After: loaded from db, or global config defaults
state.screen_w = device_cfg.get("screen_width", 1920)
state.screen_h = device_cfg.get("screen_height", 1080)
state.width_threshold   = device_cfg.get("width_threshold", 0.30)
state.max_aspect_ratio = device_cfg.get("max_aspect_ratio", 1.3)
state.fallback_height_ratio = device_cfg.get("fallback_height_ratio", 0.4)
state.delta_cap = device_cfg.get("delta_cap", 300)
```

### 4.3 Live config reload (optional, future)

Add a SIGHUP handler or a `shorts reload-config` command that re-reads from DB without restarting the daemon.

---

## 5. CLI Changes

### 5.1 New commands

```bash
shorts config                    # show global defaults
shorts config get <key>          # get a specific global config value
shorts config set <key> <value>  # set a global config value
shorts config show [IP]          # show all config keys (global defaults); or per-device effective values if IP given
shorts config set <IP> <key> <value>  # set per-device override
shorts config reset <IP>         # clear per-device overrides → use globals
shorts detect <IP>               # re-detect screen resolution via ADB, update DB
```

### 5.2 `shorts list` output (update)

```
  loft
     IP: 192.168.1.239 | Limit: 600/day
     Screen: 1920x1080 | w=0.30 (global) | ar=1.3 (global) | h=0.4 (global) | cap=300 (global)

  sofa
     IP: 192.168.1.202 | Limit: 300/day
     Screen: 1920x1080 | w=0.35 (per-device) | ar=1.3 (global) | h=0.4 (global) | cap=300 (global)
```

### 5.3 `shorts setup` / `shorts add` (update)

Both commands should:
1. Auto-detect screen resolution via ADB
2. Store in `devices.screen_width/height`
3. Use global defaults for threshold columns (NULL → fallback to global)

---

## 6. Files to Modify

| File | Changes |
|------|---------|
| `scripts/clawshorts_db.py` | Add `get_config`, `set_config`, `get_device_config`, `update_device_screen`, `update_device_threshold` functions |
| `scripts/clawshorts-daemon.py` | Replace hardcoded constants with DB-loaded values; add `_load_global_config()` |
| `src/clawshorts/cli.py` | Add new `config` subcommand with get/set/show/reset; add `detect` command; update `list` output |
| `scripts/clawshorts.sh` | Route new `config` and `detect` commands |
| `src/clawshorts/constants.py` | Keep only truly universal constants (e.g. poll interval range limits); remove detection thresholds |

---

## 7. Migration Plan

### Phase 1: Schema migration
- Add `config` table if not exists; seed with defaults
- Add columns to `devices` if not exist
- Existing devices: columns are NULL → use global defaults
- **Risk:** Low — only additive schema changes

### Phase 2: Config loading
- Modify daemon to load global config at startup
- Falls back to hardcoded defaults if DB read fails
- Existing devices with NULL columns still work exactly as before

### Phase 3: Per-device overrides
- Add per-device column writes/reads
- Implement config resolution priority
- Update `shorts list` display

### Phase 4: CLI commands
- Implement `shorts config` and `shorts detect`

### Phase 5: Cleanup
- Remove threshold constants from `constants.py`
- Keep only non-detection constants (poll interval bounds, etc.)

---

## 8. Backward Compatibility

- **Existing installations:** Migration adds new columns with NULL → existing behavior unchanged
- **New installs:** Schema created with all columns from day one
- **Config file (`devices.yaml`):** Already migrated to SQLite; no yaml code remaining
- **LaunchAgent restart:** Required to pick up new daemon binary

---

## 9. Testing Checklist

- [ ] Fresh install on new device → screen auto-detected and stored
- [ ] Existing device shows NULL thresholds → uses global defaults
- [ ] `shorts config set global shorts_width_threshold 0.25` → all devices use new threshold
- [ ] `shorts config set <IP> shorts_width_threshold 0.35` → only that device uses 0.35
- [ ] `shorts config reset <IP>` → device falls back to global
- [ ] `shorts detect <IP>` → re-runs ADB detection and updates DB
- [ ] Daemon restart → picks up latest DB config (not stale in-memory)
- [ ] `shorts list` → shows effective config per device
- [ ] Offline ADB → uses `default_screen_width/height` from config table
