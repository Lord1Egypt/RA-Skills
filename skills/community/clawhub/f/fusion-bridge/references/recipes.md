# Fusion Bridge Recipes

## Connectivity checks

### Ping

```bash
curl http://<bridge-host-or-ip>:8765/ping
curl http://<fusion-host-ip>:8765/ping
```

### State

```bash
curl http://<bridge-host-or-ip>:8765/state
```

### Logs

```bash
curl http://<bridge-host-or-ip>:8765/logs
```

## Raw Python examples

### Show a popup

```json
{
  "code": "ui.messageBox('Hi from the Fusion Bridge!')",
  "timeoutSeconds": 60
}
```

### Print active document name

```json
{
  "code": "print(document.name if document else 'no document')",
  "timeoutSeconds": 60
}
```

### Return structured data

```json
{
  "code": "result = {'documentName': document.name if document else None, 'hasDesign': design is not None}",
  "timeoutSeconds": 60
}
```

### List occurrences

```json
{
  "code": "items = []\nif rootComp:\n    for occ in rootComp.occurrences:\n        items.append(occ.name)\nresult = items",
  "timeoutSeconds": 60
}
```

## Recommended pattern

For reusable tasks:
1. send a small helper-style snippet first
2. inspect `stdout` or `result`
3. escalate to larger raw Python only when needed

For geometry creation:
1. confirm dimensions in words first
2. build base body first
3. add holes/features in separate passes
4. inspect resulting bodies after every pass
5. hide old attempts after a successful new revision
6. reserve popups for the end, not the middle

## Debugging heuristics

- If `/ping` fails remotely but works locally, suspect bind address or firewall.
- If `/exec` times out, inspect `/logs` and reduce UI-blocking code.
- If startup works but runtime pump fails, inspect logs for `runtime_pump_*` events.
- If UI feedback is needed, use `ui.messageBox(...)` deliberately.
- If the visual model looks wrong, check for overlapping old attempt bodies before assuming the latest build failed.
- If a Fusion API call fails in one style, switch to a more robust construction method instead of repeatedly forcing the same API path.
