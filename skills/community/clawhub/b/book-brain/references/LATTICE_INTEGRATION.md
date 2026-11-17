# BOOK BRAIN — LYGO lattice integration

**Signature:** `Δ9Φ963-BOOK-BRAIN-LATTICE-v2`

## Stack workspace

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack
python tools/verify_lattice_alignment.py
```

Stub template `reference/LYGO_STACK_VERIFY.ref.txt`:

```text
Title: LYGO Protocol Stack — last verify
stack_root: <LYGO_STACK_ROOT>
verify_tool: python tools/verify_lattice_alignment.py
pages: https://deepseekoracle.github.io/lygo-protocol-stack/
clawhub: https://clawhub.ai/deepseekoracle
github: https://github.com/DeepSeekOracle/lygo-protocol-stack
# Paste verdict + git sha from steward verify — do not trust chat alone
```

## Kernel / champion eggs

After consent-gated plant:

```bash
python scripts/write_book_brain_stubs.py  # in lygo-kernel-egg-planter mirror
```

BOOK BRAIN equivalent:

```bash
python scripts/write_ref_stub.py --out reference/LYGO_KERNEL_EGGS.ref.txt \
  --lines "registry: data/kernel_eggs/registry.json" "retrieval: KernelEggRetrieval.html"
```

Champion: `docs/ChampionEggRegistry.json` → `reference/LYGO_CHAMPION_EGGS.ref.txt`

## ClawHub catalog snip

Maintain `reference/CLAWHUB_DEEPSEEKORACLE.ref.txt` with:

- `npx clawhub@latest inspect deepseekoracle/lygo-champion-council`
- Pin versions from `clawhub/skills.json` when steward updates

## Builder Key (portable)

`LYGO_BUILDER_KEY/memory/` holds session closes; `verify/` holds `*_last_run.json` — copy summaries into `state/` stubs when auditing on a new machine.

**Δ9Φ963**