# Examples

## Example 1 — user correction becomes a learning

```bash
python3 scripts/learnings.py log-learning \
  --root /repo \
  --category correction \
  --priority high \
  --area tests \
  --summary "Database fixtures in this repo are module-scoped, not function-scoped" \
  --details "Initial assumption used function-scoped fixtures. Existing suite uses module scope for DB-heavy tests." \
  --suggested-action "Check local fixture conventions before creating expensive test fixtures." \
  --source user_feedback \
  --related-files tests/conftest.py \
  --tags pytest,fixtures
```

## Example 2 — recurring environment failure becomes an error entry

```bash
python3 scripts/learnings.py log-error \
  --root /repo \
  --name docker-build \
  --priority high \
  --area infra \
  --summary "Docker image build fails on Apple Silicon due to architecture mismatch" \
  --error-text "error: failed to solve: no match for platform linux/arm64" \
  --context "docker build -t myapp . on Apple Silicon" \
  --suggested-fix "Use --platform linux/amd64 or choose a multi-arch base image" \
  --reproducible yes \
  --related-files Dockerfile
```

## Example 3 — project convention promoted into memory

Learning entry summary:
> This repository uses `pnpm` workspaces. `npm install` is the wrong default.

Promotion to `CLAUDE.md`:

```markdown
## Build & dependencies
- Package manager: pnpm. Use `pnpm install` and `pnpm -r build`.
```

## Example 4 — extracted skill candidate

A learning is a good extraction candidate when it is resolved, general, and recurs across tasks.

Good candidate:
- “Regenerate generated API clients after OpenAPI changes”

Poor candidate:
- “A typo in one temporary bash command”
