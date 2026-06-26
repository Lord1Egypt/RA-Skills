# URL

Generate a claude-sessions web URL from a session ID.

## URL Format

```
http://localhost:5174/#project={project-key}&session={session-id}
```

## Project Key Conversion

| Environment | Path | Project Key |
|-------------|------|-------------|
| Windows | `C:\Users\es6kr\path\repo` | `C--Users-es6kr-path-repo` |
| WSL | `/mnt/c/Users/es6kr/path/repo` | `-mnt-c-Users-es6kr-path-repo` |
| macOS | `/Users/es6kr/path/repo` | `-Users-es6kr-path-repo` |

Rule: Replace all non-alphanumeric characters with `-`

## Procedure

### 1. Get Session ID

Use `/session id` for the current session, or receive an ID directly.

### 2. Generate Project Key

Derive from CWD automatically:

```bash
# Windows (Git Bash)
pwd | sed 's|^/c/|C--| ; s|/|-|g'

# WSL
pwd | sed 's|/|-|g'
```

### 3. Compose URL

```
http://localhost:5174/#project={project-key}&session={session-id}
```

## Usage

```bash
/session url                    # URL for current session
/session url <session-id>       # URL for a specific session
```

## Notes

- Active sessions may not load in claude-sessions (jsonl not yet closed)
- Project-only view: `http://localhost:5174/#project={project-key}` (omit session param)
