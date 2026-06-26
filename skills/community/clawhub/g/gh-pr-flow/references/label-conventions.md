# Label Conventions

## Standard Labels

| Label | Color | Description |
|-------|-------|-------------|
| `breaking` | `#B60205` | Breaking change |
| `feature` | `#0E8A16` | New feature |
| `enhancement` | `#84B6EB` | Improvement to existing feature |
| `bug` | `#FC2929` | Bug fix |
| `fix` | `#FC2929` | Bug fix (alias) |
| `docs` | `#5319E7` | Documentation |
| `documentation` | `#5319E7` | Documentation (alias) |
| `refactor` | `#FEF2C0` | Code refactoring |
| `experimental` | `#E99695` | Experimental work |
| `test` | `#BFDADC` | Tests |
| `testing` | `#BFDADC` | Tests (alias) |
| `perf` | `#FF78CB` | Performance |
| `performance` | `#FF78CB` | Performance (alias) |
| `chore` | `#BFD4F2` | Maintenance, deps |
| `deps` | `#BFD4F2` | Dependencies update |
| `dependencies` | `#BFD4F2` | Dependencies update (alias) |
| `ci` | `#BFD4F2` | CI/CD |


## Workflow Labels

| Label | Color | Description |
|-------|-------|-------------|
| `needs-review` | `#FFA500` | Ready for code review |
| `needs-testing` | `#FFA500` | Needs QA/testing |
| `needs-design` | `#FFA500` | Needs design review |
| `wip` | `#C5DEF5` | Work in progress |
| `blocked` | `#B60205` | Blocked by something else |
| `ready` | `#0E8A16` | Ready to merge |
| `auto-merge` | `#0E8A16` | Enable auto-merge |

## Priority Labels

| Label | Color | Description |
|-------|-------|-------------|
| `priority-critical` | `#B60205` | Must fix ASAP |
| `priority-high` | `#D93F0B` | Should be done next |
| `priority-medium` | `#FBCA04` | Normal priority |
| `priority-low` | `#0E8A16` | Nice to have |

## Setting up labels via gh CLI

```bash
# Add standard labels to a repo
for label in "breaking:#B60205" "feature:#0E8A16" "bug:#FC2929" "docs:#5319E7" \
  "refactor:#FEF2C0" "test:#BFDADC" "perf:#FF78CB" "chore:#BFD4F2" \
  "needs-review:#FFA500" "wip:#C5DEF5" "ready:#0E8A16" "blocked:#B60205"; do
  name="${label%%:*}"
  color="${label##*:}"
  gh label create "$name" --color "$color" --force 2>/dev/null || true
done
```
