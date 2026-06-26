# Common Consistency Risk Patterns

Recurring patterns that cause architecture drift. Use this as a checklist during
Phase 3 (Global Reference Scan) and Phase 6 (Residue Audit).

## Pattern 1: Dual Status Fields

**Symptom**: Entity has `status` and `lifecycle_status` (or `state`, `phase`, etc.)
that are supposed to be in sync but diverge at runtime.

**Detection**:
```bash
grep -rn "status" --include="*.py" | grep -v "http_status\|exit_status" | sort
```

**Risk**: One field gets updated, the other doesn't. Queries on the stale field
return wrong results. State machine transitions become unpredictable.

**Fix pattern**: Pick one field as canonical. Migrate all reads/writes. Drop or
alias the other. Add a migration for existing DB rows.

---

## Pattern 2: Hardcoded Path Variants

**Symptom**: Same resource referenced by different path strings in different files.

```python
# file_a.py
DB_PATH = "/root/.openclaw/workspace/X记忆/memory.db"

# file_b.py
db = sqlite3.connect(os.path.expanduser("~/.openclaw/workspace/X记忆/memory.db"))

# file_c.py
from runtime_config import MEMORY_DB_PATH  # correct
```

**Detection**:
```bash
grep -rn "memory.db\|MEMORY_DB" --include="*.py"
```

**Risk**: Works on one machine, breaks on another. Refactoring the path in config
doesn't propagate to hardcoded sites.

**Fix pattern**: Single config source (e.g., `runtime_config.py`). All consumers
import from it. Zero hardcoded path literals.

---

## Pattern 3: Silent Fallback to Legacy

**Symptom**: New entry point exists, but `except` / `ImportError` / `if not available`
blocks silently route to the old implementation.

```python
try:
    from new_orchestrator import process
except ImportError:
    from old_auto_evolve import process  # silent legacy fallback
```

**Risk**: System appears to work but runs old logic. Bugs in old logic resurface.
New features in new module are silently bypassed.

**Fix pattern**: Remove fallback or convert to explicit error. If fallback must stay
temporarily, add logging.warning and a COMPAT comment with removal date.

---

## Pattern 4: Orphaned Legacy Table Writes

**Symptom**: New table/schema introduced, but old INSERT/UPDATE statements to the
retired table still execute in some code paths.

**Detection**:
```bash
grep -rn "INSERT INTO old_table\|UPDATE old_table" --include="*.py"
```

**Risk**: Data split across two tables. Queries on new table miss old-path data.
Storage grows silently.

**Fix pattern**: Remove old writes. If read-only access to old table is needed for
migration, mark it explicitly as `# LEGACY READ-ONLY`.

---

## Pattern 5: Doc-Code Desync

**Symptom**: SKILL.md, README, or architecture doc describes a flow that no longer
matches the code.

**Detection**: Compare documented entry points, module names, and flow descriptions
against actual imports and call chains.

**Risk**: Next developer (or AI agent) follows the doc, writes code against the old
flow, reintroduces retired patterns.

**Fix pattern**: Treat docs as part of the consistency scope. Every code change that
alters a documented flow must update the doc in the same pass.

---

## Pattern 6: Multiple Write Entry Points

**Symptom**: Same data store (e.g., observations table) written to by multiple
independent modules without a single gatekeeper.

```python
# module_a.py
cursor.execute("INSERT INTO observations ...")

# module_b.py
memory_governor.add_observation(...)  # goes through governor

# module_c.py
memory_db.add_observation(...)  # bypasses governor
```

**Detection**:
```bash
grep -rn "INSERT INTO observations\|add_observation" --include="*.py"
```

**Risk**: Deduplication, lineage tracking, and validation in the governor are bypassed.
Data quality degrades silently.

**Fix pattern**: Designate one module as the sole write gateway. All other modules
call it. Direct SQL inserts are prohibited outside the gateway.

---

## Pattern 7: Inconsistent Function Signatures

**Symptom**: Same logical operation has different parameter names or return types
across modules.

```python
# module_a.py
def get_status(proposal_id) -> str: ...

# module_b.py
def get_status(id, include_history=False) -> dict: ...
```

**Risk**: Callers assume one signature, get another. Refactoring breaks silently
when the wrong variant is updated.

**Fix pattern**: Define the canonical signature in the source-of-truth module.
All other modules either delegate to it or match its contract exactly.

---

## Pattern 8: Stale Event/Signal Names

**Symptom**: Event bus or signal system uses old event names that no longer match
the current architecture.

**Detection**:
```bash
grep -rn "emit\|publish\|on_event\|subscribe" --include="*.py" | grep -i "old_event"
```

**Risk**: Handlers listen for events that are never emitted (dead code) or emit
events that no one handles (lost signals).

**Fix pattern**: Inventory all emit/subscribe pairs. Remove orphans. Rename to
match current architecture terminology.

---

## Quick Reference: Risk Severity

| Pattern | Severity | Typical blast radius |
|---------|----------|---------------------|
| Dual status fields | Critical | All state-dependent logic |
| Hardcoded path variants | High | Deployment + portability |
| Silent fallback | Critical | Entire feature path |
| Orphaned table writes | High | Data integrity |
| Doc-code desync | Medium | Future development |
| Multiple write entries | High | Data quality + audit |
| Inconsistent signatures | Medium | Caller correctness |
| Stale event names | Medium | Event-driven flows |
