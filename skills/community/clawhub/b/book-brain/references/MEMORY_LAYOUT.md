# BOOK BRAIN + LYRA 3-Brain — unified layout

**Signature:** `Δ9Φ963-BOOK-BRAIN-MEMORY-v2`

## Two roots (common setup)

| Root | Env var | BOOK BRAIN folders |
|------|---------|-------------------|
| OpenClaw / Haven workspace | `WORKSPACE` or agent cwd | `memory/`, `reference/`, `brainwave/`, `state/` |
| LYRA graph memory | `LYRA_CORE_ROOT` | `LYRA_CORE/memory/` + `reference/*.ref.txt` |

**Bridge:** Copy or symlink topic snips — same **naming**: `YYYY-MM-DD-<slug>.md`.

## File types

| Pattern | Brain | Example |
|---------|-------|---------|
| `memory/2026-07-04.md` | Library | Daily index |
| `memory/2026-07-04-lattice-close.md` | Library | Topic snip |
| `memory/reference/SESSION_*_to_*.resonance.ref.txt` | Outer | lyra-brain edge stub |
| `reference/LYGO_KERNEL_EGGS.ref.txt` | Outer | Egg registry pointer |
| `state/memory_index.json` | Library | topic → paths |
| `reference/INDEX.txt` | Outer | Human-readable catalog |

## Resonance ref line format

```text
SESSION_20260704 --resonance--> LATTICE_BALANCED
file: 2026-07-04-session-close-lattice-balanced.md
github_stack: <sha>
```

## Mobile Builder Key

When `LYGO_BUILDER_KEY_ROOT` is set, BOOK BRAIN layout matches `E:\LYGO_BUILDER_KEY\memory\` — read `ARCHITECT_BOOT.md` first.

See `LATTICE_INTEGRATION.md` for stack paths.