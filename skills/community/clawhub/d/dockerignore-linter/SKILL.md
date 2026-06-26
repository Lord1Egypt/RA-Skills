---
name: dockerignore-linter
description: Lint, validate, and audit .dockerignore files for syntax issues, security risks, missing patterns, and optimization opportunities. Use when asked to lint, validate, audit, or check .dockerignore files, optimize Docker build context, reduce Docker image size, or review what files are included in Docker builds. Triggers on "lint dockerignore", "check .dockerignore", "docker context", "docker build size", "audit dockerignore".
---

# Dockerignore Linter

Lint .dockerignore files for syntax issues, security risks, missing essential patterns, and optimization opportunities.

## Commands

All commands use the bundled Python script at `scripts/dockerignore_linter.py`.

### 1. Lint a .dockerignore file

```bash
python3 scripts/dockerignore_linter.py lint <file> [--strict] [--format text|json|markdown]
```

Run all validation rules.

### 2. Audit for security-sensitive files

```bash
python3 scripts/dockerignore_linter.py security <file> [--format text|json|markdown]
```

Check if secrets, credentials, and sensitive files are properly excluded.

### 3. Suggest missing patterns

```bash
python3 scripts/dockerignore_linter.py suggest [--project-type node|python|go|rust|java|ruby|generic] [--format text|json]
```

Generate recommended .dockerignore patterns for a project type.

### 4. Analyze Docker build context

```bash
python3 scripts/dockerignore_linter.py context <directory> [--dockerignore <file>] [--format text|json]
```

Show which files would be included in the Docker build context, with size breakdown.

## Lint Rules (18 total)

### Syntax (4 rules)
1. **empty-file** — .dockerignore is empty
2. **invalid-pattern** — Malformed glob pattern
3. **duplicate-pattern** — Same pattern appears twice
4. **negation-conflict** — Negation `!` overrides a previous exclusion (likely unintended)

### Security (6 rules)
5. **missing-env** — `.env` not excluded (may contain secrets)
6. **missing-secrets** — Common secret files not excluded (*.pem, *.key, id_rsa, etc.)
7. **missing-git** — `.git` directory not excluded (exposes history + credentials)
8. **missing-credentials** — Credential files not excluded (aws/credentials, .npmrc with tokens, etc.)
9. **missing-docker** — Docker-related files not excluded (docker-compose*.yml, Dockerfile*)
10. **missing-ide** — IDE config not excluded (.vscode, .idea, *.swp)

### Optimization (4 rules)
11. **missing-deps** — Dependency directories not excluded (node_modules, __pycache__, vendor, target)
12. **missing-build** — Build output not excluded (dist, build, *.o, *.pyc)
13. **missing-logs** — Log files not excluded (*.log, logs/)
14. **missing-test** — Test data/coverage not excluded (coverage, .nyc_output, htmlcov)

### Best Practices (4 rules)
15. **too-broad** — Pattern is overly broad (e.g., `*` without specific negations)
16. **commented-pattern** — Inline comment after pattern (not supported, treated as literal)
17. **trailing-space** — Pattern has trailing whitespace
18. **readme-excluded** — README/docs excluded (usually should be kept for reference)

## Output Formats

Text, JSON, Markdown — same structure as other linters.

## CI Integration

```yaml
- name: Lint Dockerignore
  run: python3 scripts/dockerignore_linter.py lint .dockerignore --strict
```

Exit codes: 0 = clean, 1 = issues found.
