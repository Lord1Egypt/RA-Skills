# Dropbox Download Skill

A V7 Go skill for downloading files from Dropbox.

## Files

- `SKILL.md` - Skill documentation and metadata
- `run.py` - V7 Go Python implementation
- `schema.json` - V7 Go tool schema for integration
- `example.json` - Example invocation

## Example Invocation

```json
{
  "path": "/documents/report.pdf",
  "rev": null
}
```

## Requirements

- Dropbox OAuth2 integration with `files.content.read` scope
- V7 Go runtime with Pipedream compatibility layer

## Implementation Notes

Uses the official Dropbox API endpoint `/2/files/download` with POST method.

The `rev` parameter is supported but deprecated; it's better to specify the revision directly in the file path.

## License

MIT
