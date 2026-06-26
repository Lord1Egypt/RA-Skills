# Progress Tracking for Long-Running Tasks

## When to Use

Tasks that:
- Have many items to process (reading files, processing data)
- Span multiple sessions
- Need deduplication (don't re-do completed work)
- Accumulate insights over time

## Template

```markdown
# <Task Name> Progress

- **Start Date**: YYYY-MM-DD
- **Total Items**: N
- **Completed**: M
- **Progress**: X%
- **Last Session**: YYYY-MM-DD HH:MM

## Completed Items (dedup list)
1. ✅ `path/to/item1` — one-line summary
2. ✅ `path/to/item2` — one-line summary

## Current Position
- Last completed: item N
- Next: item N+1

## Key Findings (accumulated insights)
### Finding 1: Title
Details...

### Finding 2: Title
Details...

## Next Steps
- [ ] Do this
- [ ] Then that
```

## Rules

1. **Always use the same file** — don't create session-specific progress files
2. **Update at session end** — write progress before the session dies
3. **Include dedup list** — so next session knows what's done
4. **Log current position** — so next session knows where to resume
5. **Extract key findings** — raw notes → curated insights over time

## Multi-Session Workflow

### Session A (starts task)
1. Read progress file (if exists, resume; if not, create)
2. Process items from current position
3. Update completed list + position
4. Write key findings
5. Save file

### Session B (continues)
1. Read progress file → sees completed items + position
2. Resume from last position
3. Repeat update cycle

## Example: Source Code Reading

```markdown
# Chromium Extensions Source Progress

- **Total Files**: 3,137
- **Completed**: 220
- **Progress**: 7.01%
- **Last Session**: 2026-03-17 00:19

## Completed Files (dedup)
1. ✅ `README.md` — extension system overview
2. ✅ `BUILD.gn` — build config
...

## Architecture Notes
### Layer 1: Browser Process
- EventRouter: event dispatch
- ExtensionFunction: API implementation
...

### Layer 2: Renderer Process  
- Dispatcher: IPC message handling
- ModuleSystem: require() pattern
...

## Next Files to Read
1. `browser/event_router.cc` — EventRouter implementation
2. `browser/process_manager.cc` — ProcessManager implementation
...
```

## Anti-Patterns

❌ **Don't**: Put progress in daily log files (hard to aggregate)
❌ **Don't**: Use multiple progress files for one task (fragmentation)
❌ **Don't**: Skip dedup info (next session re-does work)
❌ **Don't**: Forget to save at session end (progress lost)

✅ **Do**: One progress file per long-running task
✅ **Do**: Clear completed/pending state
✅ **Do**: Save at natural boundaries
