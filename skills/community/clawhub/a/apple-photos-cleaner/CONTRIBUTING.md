# Contributing

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

1. **Fork** the repository
2. **Create a branch** from `main` (see [Branch Naming](#branch-naming))
3. **Make your changes** with clear, focused commits
4. **Push** your branch and open a **Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/apple-photos-cleaner.git
cd apple-photos-cleaner

# Create a virtualenv on a supported Python (see the policy below) and install the dev toolchain
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run the checks CI runs
ruff check . && ruff format --check . && mypy && pytest
```

### Python version policy

- The floor is **Python 3.10**. Stock macOS `/usr/bin/python3` (Command Line Tools, 3.9) is too old;
  install a current Python with `brew install python` or python.org.
- CI tests the floor plus the latest two releases.
- The floor rises when a version reaches end-of-life. A floor change is called out in the CHANGELOG
  and moves `requires-python`, ruff's `target-version`, and the CI matrix together.

### Deprecation policy

Agents depend on the CLI flags and JSON output, so breaking them silently is a bug.

- A flag or JSON field gets **at least one minor release of warnings** before it is removed or
  renamed, and the removal itself ships in a **major** release (see [RELEASING.md](RELEASING.md)).
  For example, deprecated in 1.2 and removed in 2.0 at the earliest.
- During that release the old form keeps working. Using it adds an entry to the result's
  `warnings` list (`{"code": "deprecated", "message": "...", "replacement": "..."}`) and logs
  to stderr. JSON stdout stays parseable.
- The deprecation and the removal each get a CHANGELOG entry, under **Deprecated** and
  **Removed** respectively.

**Exception: safety fixes.** If the old behavior lets something be deleted or written without
the user's informed approval, it can be removed immediately, with no warning period, and in
whatever release the fix lands in, including a minor or patch release. Waiting for a major would
leave the hole open. Call it out under a **Breaking (safety)** heading in the CHANGELOG, saying
what replaces it. See
[docs/threat-model.md](docs/threat-model.md).

## Branch Naming

Use the format `type/short-description`:

- `feature/user-authentication`
- `fix/login-redirect-loop`
- `docs/update-api-reference`
- `chore/upgrade-dependencies`

See [git-conventions.instructions.md](.github/instructions/git-conventions.instructions.md) for full details.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): short description

Optional longer body explaining what and why.

Refs: #123
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`

**Examples:**

```
feat(auth): add OAuth2 login flow
fix(api): handle null response from user endpoint
docs: update contributing guide
test(cart): add edge case tests for empty cart
```

## Pull Request Process

1. Fill out the [PR template](.github/pull_request_template.md) completely
2. Ensure all checks pass (lint, tests, build)
3. Request a review from at least one maintainer
4. Address review feedback
5. A maintainer will merge your PR once approved

Keep PRs focused on a single logical change. Large changes should be split into smaller PRs.

## Code Style

This project uses shared code style guidelines enforced through:

- [`.editorconfig`](.editorconfig) — Cross-editor formatting
- [Code style instructions](.github/instructions/code-style.instructions.md) — Naming, formatting, and organization conventions

Run the linter before submitting:

```bash
ruff check . && ruff format --check . && mypy
```

## Testing

All new code should include tests. Follow the patterns documented in:

- [Testing instructions](.github/instructions/testing.instructions.md) — Unit test patterns and conventions

```bash
pytest
```

## AI-Assisted Development

This repository includes configuration files for AI coding assistants (Copilot, Cursor, Windsurf, Cline, Claude Code). These files define project conventions so AI tools produce consistent, high-quality code.

- See [docs/AI-CUSTOMIZATION-GUIDE.md](docs/AI-CUSTOMIZATION-GUIDE.md) for details
- AI instructions in `.github/instructions/` are auto-loaded based on file patterns
- Prompts in `.github/prompts/` provide reusable task templates

You can use AI tools while contributing — the config files ensure generated code aligns with project standards.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Report unacceptable behavior to the project maintainers.

## Questions?

<!-- TODO: Add your preferred communication channel. -->

Open a [GitHub Discussion](https://github.com/YOUR_ORG/YOUR_REPO/discussions) or file an issue.
