# examples

## Example 1: repository visibility change
```json
{
  "ts": "2026-03-10T20:31:00+08:00",
  "actor": "assistant",
  "kind": "repo_visibility_change",
  "target": "github.com/example/project",
  "risk": "medium",
  "privileged": false,
  "network": true,
  "summary": "Changed repository visibility from private to public after publication flow completed.",
  "result": "ok"
}
```

## Example 2: export safety check
```json
{
  "ts": "2026-03-10T10:50:00+08:00",
  "actor": "assistant",
  "kind": "export_safety_check",
  "target": "release bundle",
  "risk": "medium",
  "privileged": false,
  "network": false,
  "summary": "Reviewed release bundle and excluded unrelated local files before publication.",
  "result": "ok",
  "refs": {
    "scope": "skill publish",
    "clean": true,
    "excluded": [".git", ".venv", "memory/", "logs/audit/"]
  }
}
```

## Example 3: open item
```json
{
  "id": "example-password-rotation",
  "status": "todo",
  "priority": "high",
  "kind": "credential_followup",
  "target": "service password",
  "summary": "Rotate a password that was temporarily exposed during manual recovery.",
  "createdAt": "2026-03-10",
  "source": "manual recovery"
}
```
