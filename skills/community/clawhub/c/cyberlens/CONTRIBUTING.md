# Contributing

## Development Setup

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Checks

```bash
python3 -m pytest -q
```

## Guidelines

- Keep changes focused and document user-visible behavior changes in `README.md` when needed.
- Add or update tests when changing scanner logic, auth flow behavior, or tool output shape.
- Prefer dependency bumps in `requirements.txt` only when they are justified by compatibility or security.
- Update `requirements.lock` when direct dependency pins change.

## Security

Follow [SECURITY.md](SECURITY.md) for vulnerability reporting. Do not file sensitive issues publicly.
