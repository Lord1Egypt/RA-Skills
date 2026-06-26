# Structured Output Schema

`bilibili-cli` uses a shared agent-friendly envelope for machine-readable output.

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
  code: api_error
  message: 未找到用户: foo
```

## Notes

- `--yaml` and `--json` both use this envelope
- non-TTY stdout defaults to YAML
- command payloads are normalized at the CLI layer
- list-like results are typically returned under `data.items`
- `status` returns `data.authenticated` plus `data.user`
- `whoami` returns `data.user` and `data.relation`
- `video` returns `data.video`, `data.subtitle`, `data.ai_summary`, `data.comments`, `data.related`, and `data.warnings`
- write commands return normalized action payloads with `data.success` and `data.action`

## Error Codes

Common structured error codes:

- `not_authenticated`
- `permission_denied`
- `invalid_input`
- `network_error`
- `upstream_error`
- `not_found`
- `internal_error`
