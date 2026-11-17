# Plan documents

## Order of work (read this table first)

The number is the order of work. It appears in three places — **file name, title, and this table** — and all three must match.

| Order | Plan | Status | Depends on |
|---|---|---|---|
| **01** | (to fill in) | 📋 not started | — |

**Done** (only plans finished with no loose ends go here):

| No. | Plan | Completed |
|---|---|---|
| **D01** | (to fill in) | YYYY-MM-DD |

## Naming

```
PLAN-<NN>-<topic>.md     work queue
PLAN-D<NN>-<topic>.md    done
```

A `TASK-` prefix is recognised too, with the same rules (`TASK-D<NN>` means done). Pick one prefix per project.

Digits sort before uppercase letters in ASCII, so in the file tree the work queue sits above the done plans, each in order.

One title format, no variants:

```markdown
# [No.] Topic — Plan

Sequence: `No.` — why it sits at this position (which goal / which wave / what it depends on)

Status: `in_progress` / `planned` / `completed` — one sentence on how far along it is
```

⚠️ `Status` is checked by machine: if it says in progress but the file hasn't been touched in a long time, one of the two is false.

## Maintenance

- **When a plan is done, move it to the next `D` number**; the number it frees in the work queue can stay empty
- **Anything with loose ends does not go to `D`** — that tier has to mean actually done
- **The single source of truth for status and priority** is the project's execution entry document (e.g. `docs/PLAN.md`); this table only answers "what comes first". If the two disagree, the entry document wins and you come back to fix this table
