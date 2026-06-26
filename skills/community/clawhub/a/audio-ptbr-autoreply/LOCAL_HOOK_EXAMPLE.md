# Optional local hook example

Do not include this hook in the public ClawHub build unless the platform provides a structured non-shell hook API.

Example of the **old risky shape**:

```yaml
hooks:
  - event: "message.audio.receive"
    action: "bash process.sh "{{MediaPath}}" "{{Target}}" "{{MessageID}}""
```

Why risky:
- the templated values are expanded into a shell command string before `process.sh` runs
- if a value contains shell-breaking characters, quoting can be bypassed at the shell parsing layer

Safer direction:
- wait for an OpenClaw hook mechanism that passes structured arguments without shell interpolation
- or register the hook only in a locally controlled environment after review and acceptance of that platform-level risk
