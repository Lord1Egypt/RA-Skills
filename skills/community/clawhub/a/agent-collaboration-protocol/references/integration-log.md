# Integration Log — `shared/build-{YYYYMMDD}/integration.md`

## Format

```markdown
# Build: {Feature Name} — {Date}

## Status
Orchestrator: ⏳ Waiting / 🔍 Reviewing / ✅ Complete
Backend: 🔨 Building / ✅ Done / ❌ Blocked
Frontend: 🔨 Building / ✅ Done / ❌ Blocked

## Backend Progress
- [ ] Router implemented at `backend/router.py`
- [ ] Models defined at `backend/models.py`
- [ ] Endpoints responding correctly
- [ ] Shared constants match spec

### Blockers
- ...

## Frontend Progress
- [ ] Components built in `frontend/components/`
- [ ] API client wired to endpoints
- [ ] All states handled (loading, empty, error, populated)
- [ ] Shared constants match spec

### Blockers
- ...

## Integration Notes
- Data format mismatch found: endpoint returns `items`, UI expects `data`
- Auth tokens not flowing through — need session cookie handling
```

## Per-Agent Log Format (avoids conflicts)

When both agents write to `integration.md` simultaneously, use separate log sections:

```markdown
# Build: {Feature Name} — {Date}

## Status
Orchestrator: ⏳ Waiting
Backend: 🔨 Building
Frontend: 🔨 Building

## Backend Log
<!-- Only the backend agent edits this section -->
- 2024-01-15 10:00: Started router implementation
- 2024-01-15 10:30: GET /api/v1/items endpoint complete
- 2024-01-15 11:00: BLOCKER: Need auth middleware from infra team

## Frontend Log
<!-- Only the frontend agent edits this section -->
- 2024-01-15 10:15: Started ItemList component
- 2024-01-15 10:45: Mock data wired, awaiting backend endpoint
- 2024-01-15 11:10: Switched to using spec contract for API client

## Integration Issues
<!-- Orchestrator edits this section -->
- (none yet)
```