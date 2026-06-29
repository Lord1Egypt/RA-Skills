# Conventional Commits Reference

Changelog Weaver parses commits following the [Conventional Commits](https://www.conventionalcommits.org/) specification (v1.0.0).

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Recognized Types

| Type | Category | When to Use |
|------|----------|-------------|
| `feat` | Features | A new feature for the user or application |
| `fix` | Bug Fixes | A bug fix |
| `docs` | Documentation | Documentation-only changes |
| `style` | Styling | Formatting, missing semicolons, etc. — no code change |
| `refactor` | Refactoring | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance | A code change that improves performance |
| `test` | Tests | Adding or correcting tests |
| `build` | Build System | Changes to the build system or external dependencies |
| `ci` | CI/CD | Changes to CI configuration files and scripts |
| `chore` | Chores | Other changes that don't modify src or test files |
| `revert` | Reverts | Reverts a previous commit |
| `security` | Security | Security-related fixes or improvements |
| `deps` | Dependencies | Dependency updates |

## Breaking Changes

Breaking changes are detected in two ways:

### 1. `!` suffix (recommended)
```
feat(api)!: remove deprecated /v1/users endpoint
```

### 2. BREAKING CHANGE footer
```
feat(api): add /v2/users endpoint

BREAKING CHANGE: /v1/users has been removed. Migrate to /v2/users.
```

## Scope (Optional)

A scope provides additional contextual information:

```
feat(auth): add OAuth2 login
fix(parser): handle unicode edge case
```

The scope is preserved in the structured JSON output but not shown by default in generated changelogs. The AI can incorporate scopes when rewriting descriptions.

## Non-Conforming Commits

Commits that don't match the Conventional Commits pattern (e.g., `"WIP"`, `"fix stuff"`, `"update"`) are classified as `other`. The AI can reclassify these by analyzing the commit message and code diff context.

## Why Conventional Commits?

- **Automated classification**: No manual tagging needed — the commit prefix determines the category
- **Semantic versioning**: Tools can auto-determine the next version number (fix → patch, feat → minor, breaking → major)
- **Structured changelogs**: Deterministic grouping makes changelog generation reliable
- **Machine-readable**: Tools like `standard-version` and `semantic-release` consume the same format
