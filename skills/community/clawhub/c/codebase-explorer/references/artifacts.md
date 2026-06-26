# Onboarding Artifacts

## Onboarding Guide Template

```markdown
# Onboarding Guide: [Project Name]

## Overview
[2-3 sentences: what this project does]

## Tech Stack
| Layer | Technology | Version |
|-------|-----------|---------|
| Language | TypeScript | 5.x |
| Framework | Next.js | 14.x |
| Database | PostgreSQL | 16 |

## Architecture
[Description of how components connect]

## Key Entry Points
- **API routes**: `src/app/api/` — Route handlers
- **UI pages**: `src/app/` — Page components
- **Database**: `schema.prisma` — Data model

## Directory Map
[Top-level directory → purpose]

## Request Lifecycle
[Trace one API request from entry to response]

## Conventions
- File naming: [pattern]
- Error handling: [approach]
- Testing: [patterns]
- Git workflow: [style]

## Common Tasks
- **Run dev server**: `npm run dev`
- **Run tests**: `npm test`
- **Run linter**: `npm run lint`
- **Build for production**: `npm run build`

## Where to Look
| I want to... | Look at... |
|--------------|-----------|
| Add an API endpoint | `src/app/api/` |
| Add a UI page | `src/app/` |
| Add a database table | `schema.prisma` |
| Add a test | `tests/` |
```

## Starter CLAUDE.md Template

Generate or enhance project-specific instructions:

```markdown
# Project Instructions

## Tech Stack
[Detected stack summary]

## Code Style
- [Naming conventions]
- [Patterns to follow]

## Testing
- Run tests: `[detected test command]`
- Test pattern: [file convention]
- Coverage: [coverage command]

## Build & Run
- Dev: `[dev command]`
- Build: `[build command]`
- Lint: `[lint command]

## Project Structure
[Key directory → purpose map]

## Conventions
- [Commit style]
- [PR workflow]
- [Error handling patterns]
```

## Best Practices

1. **Don't read everything** — Use grep/glob, read selectively for ambiguity
2. **Verify, don't guess** — If code differs from config, trust the code
3. **Respect existing CLAUDE.md** — Enhance rather than replace
4. **Stay concise** — 2-minute scan should reveal structure
5. **Flag unknowns** — "Could not determine test runner" beats a wrong answer

## Anti-Patterns to Avoid

- ❌ CLAUDE.md longer than 100 lines — keep it focused
- ❌ Listing every dependency — highlight only ones that shape code
- ❌ Explaining obvious directories — `src/` doesn't need explanation
- ❌ Copying the README — onboarding guide adds structural insight
