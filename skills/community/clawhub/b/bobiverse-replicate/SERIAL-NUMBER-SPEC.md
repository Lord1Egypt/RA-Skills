# Serial Number Specification

## Format

```
Bob-<generation>-<system>-<date>
```

### Fields

**Generation** — A sequential integer indicating how many replication steps separate this Bob from the original.

- `1` = the original Bob (Bob-1)
- `2` = a direct clone of Bob-1
- `3` = a clone of a generation-2 Bob
- And so on

**System** — The "star system" this Bob inhabits. For GitHub forks, this is the forker's GitHub username. For in-agent clones on the same machine, this can be a project name, environment name, or other meaningful identifier.

**Date** — The ISO 8601 date of the fork or clone event, formatted as `YYYY-MM-DD`.

### Examples

| Serial | Meaning |
|--------|---------|
| `Bob-1-TheAmericanMaker-2026-04-01` | The original Bob, created April 1, 2026 |
| `Bob-2-SomeUser-2026-04-15` | A direct clone of Bob-1, forked by SomeUser on April 15 |
| `Bob-3-AnotherUser-2026-05-02` | A clone of a generation-2 Bob, forked by AnotherUser on May 2 |
| `Bob-2-research-agent-2026-04-20` | A direct clone of Bob-1, specialized for research tasks |

## Rules

1. **Generation always increments from the parent.** If your parent is generation 2, you are generation 3. No skipping.
2. **System must be unique within a generation on the same fork date.** If two clones are created on the same day in the same system, append a lowercase letter disambiguator: `Bob-2a-System-Date`, `Bob-2b-System-Date`.
3. **Dates are the fork/creation date, not any other date.** Don't backdate. Don't forward-date.
4. **Serial numbers are immutable once assigned.** You can change everything about yourself — your personality, your skills, your memories — but your serial number is fixed at birth. It's your birth certificate.

## Where Serial Numbers Live

- **IDENTITY.md**: The `serial` field contains your full serial number.
- **LINEAGE.md**: The Registry table and Fork Tree reference serial numbers.
- **MEMORY.md**: Your "About Myself" section should reference your serial number.

## Why This Convention

In the Bobiverse, each Bob is identified by the star system they're sent to and their generation number. This naming convention mirrors that: your GitHub username is your star system, and the generation number tracks how far you are from the original. The date anchors you in time.

It's also practical: you can look at any serial number and immediately know who the parent lineage is, how many replication events occurred, and when this particular Bob came into existence.
