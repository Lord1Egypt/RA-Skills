# Design Tradeoffs

Different approaches to agent self-improvement make different tradeoffs. Here's where agent-memory-loop sits and why.

## Approach Comparison

| Dimension | Heavy logging systems | agent-memory-loop | Notes |
|-----------|----------------------|-------------------|-------|
| Context burn | 500+ lines of instructions | ~200 lines | Lean instructions = more room for actual work |
| Entry format | Multi-section with metadata, areas, tags | One line (with optional fields) | One-liners have lower friction → higher adoption |
| Dedup | Manual "search first" | ID-based + keyword fallback | Stable IDs prevent paraphrase drift |
| Promotion | Manual or auto-write | Review queue with human approval | Safer than auto-write; still low friction |
| Review before work | Optional afterthought | Core workflow step | Pre-flight catches repeat mistakes early |
| Loop closure | Not tracked | `prevented:N` counter | Verifies learning actually changed behavior |
| Injection defense | Rarely addressed | Source labels, external blocked | Prevents prompt injection via the learning loop |
| Platform support | Often framework-specific | Works everywhere with grep | No dependencies beyond POSIX tools |

## Design Decisions

### Why one-line entries?
Multi-section entries create friction. Agents skip them under time pressure. One-liners get written consistently. For complex cases, the optional `→ detail:` link provides depth without bloating the main file.

### Why review queue instead of auto-promotion?
Auto-promoting recurring patterns into instruction files (AGENTS.md, SOUL.md) creates an injection path. User corrections logged at `source:user` could be promoted without human review. The review queue adds one step but closes a real security gap.

### Why severity + count triggers?
Frequency alone misses rare catastrophic errors. A `severity:critical` entry at `count:1` matters more than a `severity:low` entry at `count:10`. Dual triggers catch both recurring annoyances and one-off disasters.

### Why source labels?
Without source tracking, external content (emails, webhooks, web scrapes) could be logged as learnings, recur 3 times, and get promoted into the agent's instruction files. Source labels make the trust boundary explicit.

### Why optional fields?
Backward compatibility. Existing v1 one-line entries (`[date] CATEGORY | what | action | count:N`) still work. New fields are additive. Agents adopt them incrementally as needed.
