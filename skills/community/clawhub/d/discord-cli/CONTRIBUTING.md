# Contributing

## Development

```bash
uv sync --extra dev --extra ai
uv run ruff check .
uv run python -m pytest
uv build
```

## Notes

- Keep the CLI behavior scriptable and stable.
- Prefer adding tests for CLI and SQLite behavior when changing commands.
- Discord auth uses user tokens from the local machine. Do not weaken the safety messaging around that flow.
