# Examples

> By default the skill runs in SAFE PREVIEW: the exact coze request envelope is shown but NOT sent/computed. On the coze engine the natural-language trigger ("please compute directly" / 请直接计算) fires the compute — **no `--yes` needed**; `--show-code` displays the coze request JSON (no send), `--dry-run` previews only. The legacy `--yes` flag applies only to the optional local-R dev backend. **** R **** `--yes`(legacy local-R only) `--show-code` `--dry-run`

---

## Example 1: Two Proportion Comparison

**User query:**
> "20%35%α=0.05power=0.8"

### Step 1 — Run (compute, returns R code) — R

```bash
python scripts/samplesize_power.py --test proportion_two --p1 0.35 --p2 0.20 --power 0.8
```

Output: coze computes and returns the R code plus the result (a request is sent to the coze endpoint; use `--dry-run` to preview the envelope without sending).

### Step 2 — Execute (after review) —

```bash
python scripts/samplesize_power.py --test proportion_two --p1 0.35 --p2 0.20 --power 0.8 -y
```

### Results
- **Per-group N**: 138 → Total 276
- Adjusted for 10% dropout: 154/group → Total 308

---

## Example 2: Group Sequential

**User query:**
> "2HR=0.7α=0.025power=0.91236"

### Preview (dry-run)

```bash
python scripts/samplesize_power.py --test survival --hazard_ratio 0.7 --alpha 0.025 --power 0.9
```

### Execute (after review)

```bash
python scripts/samplesize_power.py --test survival --hazard_ratio 0.7 --alpha 0.025 --power 0.9 -y
```

---

## Example 3: Non-inferiority

**User query:**
> "70%65%10%α=0.025power=0.8"

### Preview (dry-run)

```bash
python scripts/samplesize_power.py --test non_inferiority --p1 0.65 --p2 0.70 --margin 0.1 --alpha 0.025 --power 0.8
```

### Execute (after review)

```bash
python scripts/samplesize_power.py --test non_inferiority --p1 0.65 --p2 0.70 --margin 0.1 --alpha 0.025 --power 0.8 -y
```

---

## Execution Notes

1. **Default behavior**: R code is executed and results returned; code hidden (add `--show-code` to show, `--dry-run` to preview only)
2. **To show code while executing**: Add `--show-code` (after reviewing a `--dry-run` preview if desired)
3. **All examples**: Follow the same pattern — preview first, then execute with `-y`

> All R code blocks follow `references/report_template.md` standards.
