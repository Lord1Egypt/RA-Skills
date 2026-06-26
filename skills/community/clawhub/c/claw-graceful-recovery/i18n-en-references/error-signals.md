# Permission Error Signals Reference

Enter the recovery flow immediately when any of the signals below appear.

## System-Level Error Signals

| Signal | Typical Scenario | Source |
|--------|-----------------|--------|
| `Permission denied` | Reading/writing protected files | Unix system call |
| `EACCES` | Access denied | Node.js / Python |
| `Operation not permitted` | macOS system-level permission denial | macOS kernel |
| `EPERM` | Operation not allowed | Node.js / Python |
| `Access is denied` | Access denied | Windows |
| `not permitted` | System call intercepted | Generic |
| `not allowed` | System call intercepted | Generic |
| `sudo` required but cannot execute | Root permission needed | Command execution |

## AI Behavioral Signals (self-detection)

| Signal | Threshold | Description |
|--------|-----------|-------------|
| Same operation fails consecutively | >= 2 times | Trigger recovery regardless of error type |
| Tool call unresponsive | > 30 seconds | Counted from call initiation |
| Retrying same failing step in loop | Loop detected | e.g.: retry -> same error -> retry |
| Waiting for user input but no interactive channel | Immediate | WeChat has no STDIN available |

## WeChat/Claw-Specific Signals

| Signal | Description |
|--------|-------------|
| WeChat reply channel timeout | No ack received within 10 seconds after sending message |
| New instruction arrives while previous is incomplete | Queue backlog, indicates hang |
| Tool call returns empty result 3+ times | Possibly silent failure due to permissions |
