# Download Guard - User Config

> This file is your single source of truth. The Agent reads and writes it directly.
> You can also edit it by hand - changes take effect immediately, no restart needed.

---

## Setup Status

```
SETUP_DONE: true
```

> `false` = first time, the Agent will guide you through setup on first trigger.
> `true`  = already configured, Agent will use your settings below.

---

## Download Root

DOWNLOAD_ROOT: F:\ProgramData\Workbuddy Data

> Where the Agent puts downloaded files (git clones, models, datasets, etc.).
> Example: `DOWNLOAD_ROOT: D:\AI-Downloads`
>
> - Safe to include spaces (for file storage only).
> - Do NOT point npm prefix or conda envs at a path with spaces (Windows compat issue).

---

## Disk Space Thresholds (GB)

```
MIN_FREE_GB: 5
WARN_FREE_GB: 15
C_DRIVE_WARN_GB: 5
```

> | Param | Meaning |
> |-------|---------|
> | `MIN_FREE_GB` | Below this -> download BLOCKED |
> | `WARN_FREE_GB` | Below this -> warning, but download proceeds |
> | `C_DRIVE_WARN_GB` | C: below this -> extra health warning |

---

## PATH Safety

```
ALLOW_SPACE_IN_TOOL_PATH: false
```

> Keep `false`. Spaces in npm prefix / conda envs paths cause known Windows bugs.

---

## Exempt Paths

```
EXEMPT_PATHS:
  # - D:\dev
  # - E:\projects
```

> Paths listed here are NOT guarded by this Skill. Add one per line.

---

## Log Cleanup

```
LOG_RETENTION_DAYS: 30
LOG_ARCHIVE_MAX_MB: 10
```

> | Param | Meaning |
> |-------|---------|
> | `LOG_RETENTION_DAYS` | Entries older than this many days get archived automatically |
> | `LOG_ARCHIVE_MAX_MB` | Archive files larger than this (MB) get deleted |
> | `0` | Set `LOG_RETENTION_DAYS` to `0` to **never** clean up |
