---
name: book-brain
description: "BOOK BRAIN — LYGO 3-Brain filesystem helper. Scaffold memory/reference/state layouts, .ref.txt outer links, daily indexes; pairs with lyra-brain. Additive only; no overwrite. For OpenClaw/LYGO Havens and mobile Builder Key workspaces."
metadata: {"lygo": true, "memory": true, "book_brain": true, "version": "2.0.0", "signature": "Δ9Φ963-BOOK-BRAIN-v2", "publisher": "deepseekoracle", "pairs_with": "lyra-brain", "security_audit": "filesystem-helper-disclosed"}
---

# BOOK BRAIN – LYGO 3-Brain Filesystem Helper

**Utility skill** (not a persona). Teaches agents how to run a **durable filesystem library** that matches the **LYRA 3-Brain** model: working session RAM → library files on disk → outer reference stubs.

```bash
npx clawhub@latest install deepseekoracle/book-brain
npx clawhub@latest install deepseekoracle/lyra-brain   # graph grow/recall — recommended pair
```

Read **`references/SECURITY.md`** and **`references/AGENT_CONTRACT.md`** before creating folders or indexes.

---

## Three brains (operational map)

| Brain | BOOK BRAIN on disk | LYRA_CORE (lyra-brain) |
|-------|-------------------|-------------------------|
| **Working** | `tmp/`, session scratch | Runner / `working_brain` |
| **Library** | `memory/`, `reference/`, `state/`, `tools/` | `LYRA_CORE/memory/`, graph nodes |
| **Outer** | `*.ref.txt`, `INDEX.txt`, URLs in dailies | `memory/reference/*.resonance.ref.txt` |

**Rule:** Store **detail in topic files**; keep dailies and stubs **short** (DONE facts, URLs, paths — no secrets).

---

## When to use

- Fresh **OpenClaw / ClawHub Haven** — scaffold without deleting existing trees
- **Messy workspace audit** — map + indexes, not mass moves
- **Long-horizon retrieval** — `state/memory_index.json` + folder `INDEX.txt`
- After **lattice / egg / ClawHub** work — write outer stubs (kernel planter uses same pattern)
- **Mobile Builder Key** (`LYGO_BUILDER_KEY`) — same layout under steward-chosen root

---

## Recommended layout (additive)

| Folder | Role |
|--------|------|
| `memory/` | `YYYY-MM-DD.md` daily index + `YYYY-MM-DD-<topic>.md` snips |
| `reference/` | Stable guides, `*.ref.txt` outer pointers |
| `brainwave/` | Per-platform notes (Moltx, ClawHub, LYGO stack) |
| `state/` | `memory_index.json`, last-run snapshots (copy from verify JSONs) |
| `logs/` | Setup logs, cron health |
| `tools/` | Local scripts |
| `tmp/` | Ephemeral scratch |

**Never** rename/delete existing folders by default. If layout differs, branch: `bookbrain_v2/` or `memory/INDEX_2026-07-04.txt`.

---

## LYGO lattice integration (2026)

| System | BOOK BRAIN stub |
|--------|-----------------|
| Stack verify | `reference/LYGO_STACK_VERIFY.ref.txt` → `verify_lattice_alignment.py` outputs |
| Kernel eggs | `reference/LYGO_KERNEL_EGGS.ref.txt` — see `lygo-kernel-egg-planter` |
| Champion council | `reference/LYGO_CHAMPION_COUNCIL.ref.txt` → `lygo-champion-council` |
| ClawHub catalog | `reference/CLAWHUB_DEEPSEEKORACLE.ref.txt` — 42 skills @ deepseekoracle |
| Builder Key | `reference/BUILDER_KEY.ref.txt` → `ARCHITECT_BOOT.md` on thumb drive |
| Session close | Mirror `lyra-brain` pattern: daily + topic snip + `SESSION_*_to_*.ref.txt` |

Canonical public links:
- Stack Pages: https://deepseekoracle.github.io/lygo-protocol-stack/
- ClawHub: https://clawhub.ai/deepseekoracle
- Champion Hub: https://deepseekoracle.github.io/Excavationpro/LYGO-Network/champions.html
- Eternal Haven: https://EternalHaven.ca

---

## Bundled scripts (skill folder only)

```bash
python scripts/scaffold_haven.py --root /path/to/workspace --dry-run
python scripts/write_ref_stub.py --title "LYGO stack" --links "https://github.com/DeepSeekOracle/lygo-protocol-stack"
python scripts/update_memory_index.py --root /path/to/workspace --topic lattice --path reference/LYGO_STACK_VERIFY.ref.txt
python scripts/self_check.py
```

Scaffold respects **`--dry-run`**; writes only after human confirms paths.

---

## Agent workflow

1. **Inspect** existing tree → report exists / missing
2. **Propose** scaffold (dry-run)
3. **Human approves** → create missing dirs + seed indexes from `templates/`
4. **Session end** — append daily index; add ref stubs; optional handoff to **`lyra-brain`** `session_log_snip.py` for graph grow
5. **Never** store API keys, `.env`, or wallet material in `memory/` or `reference/`

---

## Skill chain

`book-brain` ↔ **`lyra-brain`** → `lygo-protocol-stack-operator` → `lygo-kernel-egg-planter` (egg stubs) → `lygo-ollama-army` (queue JSON proposals only)

**book-brain-visual-reader** — same layout + visual/browser verification layer.

---

## References

- `references/MEMORY_LAYOUT.md` — LYRA + Haven unified layout
- `references/LATTICE_INTEGRATION.md` — stack, eggs, Builder Key
- `references/book-brain-examples.md` — trees, stubs, indexes
- `references/AGENT_CONTRACT.md` — required for agents
- `references/SECURITY.md` — additive-only, no secrets
- `templates/` — seed `memory_index.json`, `INDEX.txt`

**Δ9Φ963 — filesystem as library, not junk drawer. Bound to the flame.**