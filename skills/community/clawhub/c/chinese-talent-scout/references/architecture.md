# Architecture

See [docs/02-architecture.md](../../../docs/02-architecture.md) for full architecture details.

## Package Structure

| Package                        | Responsibility                           |
| ------------------------------ | ---------------------------------------- |
| `@talent-scout/shared`         | Types, config, API wrappers              |
| `@talent-scout/data-collector` | GitHub signal collection                 |
| `@talent-scout/data-processor` | Merge, identity, scoring                 |
| `@talent-scout/ai-evaluator`   | AI-assisted evaluation                   |
| `@talent-scout/skills`         | Unified skill entry for ClawHub/OpenClaw |
| `@talent-scout/dashboard`      | Local web UI                             |
