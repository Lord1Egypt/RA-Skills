# Structured Output Schema

`discord-cli` uses a shared agent-friendly envelope for machine-readable output.

## Success

```yaml
ok: true
schema_version: "1"
data: ...
```

## Error

```yaml
ok: false
schema_version: "1"
error:
  code: channel_resolution_error
  message: Channel 'gen' matches multiple local channels.
```

## Notes

- `--yaml` and `--json` both use this envelope
- non-TTY stdout defaults to YAML
- query commands return arrays or dicts under `data`
- `status` returns `data.authenticated` plus `data.user`
- `whoami` returns `data.user`
