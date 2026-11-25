# Chest Freezer Inventory

**Problem.** Chest freezers are black holes by design: you load from
the top, gravity buries the old, and nothing shows a date. Households
end up with $100+ of forgotten stock aging past its quality window
(fatty fish dies at ~3 months, cooked dishes ~3, while roasts hold
10), buying duplicates of what's already buried, and excavating
"mystery bags" during defrost day. The USDA's "safe indefinitely when
frozen" is true — and useless without a quality clock and a record.

**What it does.** `scripts/freezer_inventory.py` — a 6-command
inventory built around how chest freezers actually stratify:

- `add` (10 seconds at freeze time, layer-aware, optional unit value);
- `list` — depth map TOP/MIDDLE/BOTTOM + per-item aging verdicts
  (PRIME / FADING / USE-FIRST / BURN RISK with days left);
- `dig` — FIFO "what's for dinner" with the **dig-past list**: what
  you'll physically excavate to reach each target;
- `plan --days 7` — dated FIFO week menu with variety caps,
  night-before thaw moves, and dollars-consumed tally;
- `use` — consumption logging (partial OK);
- `stats` — stock value, **value-at-risk in dollars**, burn report,
  and the DEFROST DAY trigger when >30% of entries are past their
  quality windows.

**Why broadly useful.** Roughly 40% of US households own a chest
freezer, and household frozen-food waste is a structural multi-billion
dollar problem. Every batch-cooker, hunter, angler, gardener and
bulk-buyer runs the same failure mode — the tool's 10-second `add`
habit is the entire behavioral ask.

**Example.**

```bash
python3 scripts/freezer_inventory.py add --item "salmon fillets" \
    --class fish-fatty --qty 4 --date 2025-12-01 --layer middle --value 12
python3 scripts/freezer_inventory.py dig --count 2
# → oldest-first picks + "dig past: peas, turkey chili, whole chicken"
python3 scripts/freezer_inventory.py stats
# → Value in USE-FIRST/BURN $130 (94% of stock) → DEFROST DAY trigger
```

stdlib only; JSON store beside you; USDA windows documented in
references. MIT license.
