# Repository Guidelines

## Project Structure & Module Organization
`scripts/` contains the CLI entry points for identity, messaging, groups, storage, and listener management. Shared SDK logic lives in `scripts/utils/`. `tests/` holds `pytest` suites and should mirror the module under test, for example `tests/test_local_store.py`. `service/` contains listener deployment templates, and `references/` stores protocol, schema, and integration notes. Top-level docs such as `README.md`, `README_zh.md`, `SKILL.md`, and `CLAUDE.md` explain user flows and agent-facing behavior.

## Build, Test, and Development Commands
Use `uv` for all local development tasks.

- `uv sync` installs and locks project dependencies from `pyproject.toml` and `uv.lock`.
- `uv run pytest` runs the unit test suite.
- `uv run python scripts/setup_identity.py --list` checks that the CLI and credential loading work.
- `uv run python scripts/check_inbox.py --limit 5` is a quick functional smoke test for message retrieval.
- `uv run python scripts/ws_listener.py run --credential default --mode smart --verbose` runs the WebSocket listener in the foreground for debugging.

## Coding Style & Naming Conventions
Target Python 3.10+ and follow Google-style Python conventions. Use 4-space indentation, explicit type hints on public functions, and short English docstrings where behavior is not obvious. Keep files and functions in `snake_case`, classes in `PascalCase`, and constants in `UPPER_SNAKE_CASE`. Keep CLI wrappers thin; move reusable logic into helper modules such as `scripts/utils/` or storage/service helpers.

## Testing Guidelines
Tests use `pytest`. Name files `test_*.py` and test functions `test_*`. Prefer focused unit tests with `tmp_path`, `monkeypatch`, and temporary SQLite state instead of relying on shared local data. No coverage threshold is enforced in the repository, so contributors should add or update tests whenever they change database schema, query behavior, message routing, or environment-variable based configuration.
When changing feature behavior in this repository, also update the corresponding system tests in the sibling repository at `../awiki-system-test/tests/`. Match the system-test location to the changed module's parent area whenever possible, such as `tests/cli/`, `tests/did/`, or `tests/listener/`.

## Commit & Pull Request Guidelines
Recent commits favor short, imperative subjects with conventional prefixes when useful, such as `feat:` and `fix:`. Keep the first line concise and scoped to one change. Pull requests should summarize the behavioral change, link any related issue, and list the verification commands you ran, typically `uv run pytest`. Include sample CLI output or config snippets when changing listener flows, settings, or user-facing commands.

## Security & Configuration Tips
Do not commit real credentials, generated data, or local runtime state from `.credentials/`, `.data/`, or custom `settings.json` files. Start from `service/settings.example.json` for new listener setups, and prefer `AWIKI_DATA_DIR` to isolate local test data.
