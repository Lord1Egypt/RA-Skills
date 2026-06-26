# Contributing

Thanks for the interest. This skill is a practical tool — contributions that
make it work better for marketers and sales teams using ActiveCampaign are
warmly welcomed.

## Ways to contribute

- **Report a bug** — open an issue with the `bug` template
- **Suggest a new script or recipe** — open an issue with the `idea` template
- **Improve documentation** — README, INSTALL.md, frameworks, or recipes
- **Add tests** — coverage isn't 100%; help close the gap
- **Submit a PR** — see the workflow below

## Local development setup

```bash
git clone https://github.com/ji282h7/activecampaign-claw
cd activecampaign-claw

# Install dev dependencies (pytest, coverage, ruff)
pip install -e ".[dev]"

# Run the test suite
pytest

# Lint
ruff check scripts/ tests/
```

You don't need an ActiveCampaign account to run the unit tests — they all use
mocked HTTP. To run integration tests against a real account, set
`AC_API_URL` and `AC_API_TOKEN` and run the relevant script directly.

## Pull request workflow

1. **Open an issue first** for non-trivial changes so we can align on
   approach before you spend time on it.
2. Branch from `main`. Use a topic branch name like `feat/segment-builder` or
   `fix/automation-funnel-pagination`.
3. Match the existing code style:
   - All scripts start with a top-level docstring describing what they do
     and a usage block
   - `from __future__ import annotations` at the top
   - Use `_ac_client.ACClient` for HTTP — never inline `urllib`
   - Standard CLI flags: `--format markdown|json`, `--output <path>`, plus
     domain-specific filters
   - Render markdown reports with `render_markdown(report)`; render JSON
     with `json.dumps(report, indent=2)`
4. Write tests:
   - One test file per new script under `tests/test_<scriptname>.py`
   - Use the fixtures in `tests/conftest.py` (`mock_client`, `tmp_state_dir`,
     `sample_state`)
   - Avoid making real API calls in tests
5. Update docs:
   - Add a new entry in `SKILL.md`'s decision tree
   - Add an entry in `CHANGELOG.md` under "Unreleased"
   - If the script needs new dependencies (we prefer none), call it out in the PR
6. Run the full test suite locally before opening the PR
7. Open the PR; the CI workflow will run on Linux + macOS across Python 3.9-3.12

## Code review expectations

- Reviewers will look for: behavior under edge cases (empty data, 403 / 404
  feature gates, very large accounts), security (no shell metacharacter
  interpolation, sanitize API data before rendering), and consistency with
  the existing patterns
- Small PRs land faster than large ones — split unrelated changes
- A passing CI run is required before merge

## Reporting security issues

Please do **not** open public issues for security-relevant problems. See
[SECURITY.md](SECURITY.md) for the private disclosure process.

## Adding a new script — checklist

When adding a new script, your PR should include:

- [ ] `scripts/<name>.py` with module docstring + usage block + `--format` and `--output` flags
- [ ] `tests/test_<name>.py` with at least: import test, render test, edge cases
- [ ] Entry in `SKILL.md`'s decision tree
- [ ] Entry in the relevant `recipes/` if it slots into a workflow
- [ ] Entry in `CHANGELOG.md`
- [ ] Entry in `README.md`'s "What it can do" section if it's a headline capability

## Adding a new recipe

A recipe is a markdown file in `recipes/` that orchestrates one or more scripts
into a workflow the agent can invoke. See `recipes/quarterly-review.md` as a
reference for the structure: when-to-use, what-it-produces, how-the-agent-runs-it,
sample output, related links.

## License

By contributing you agree that your contribution is licensed under the
project's MIT license.
