# Food Recall Radar

**Check whether food you actually bought is under recall — before you eat it.**

Thousands of FDA food recalls happen every year, and almost nobody hears about the one
affecting *their* pantry. News covers outbreaks, not the quiet store-brand recalls.
This tool keeps a personal pantry inventory and matches it against **live FDA recall
data** (openFDA) so you get a ranked action list: check the package / discard / return
for refund.

## What it does

- 🧾 **Pantry inventory** — record brand + product (UPC/lot optional), or paste a whole
  receipt in one shot
- 📡 **Live recall matching** — pulls ongoing Class I/II/III recalls from openFDA and
  fuzzy-matches them against your items (brand containment, product-token overlap,
  sequence similarity, UPC equality)
- 🏷️ **Store-brand aware** — `audit` mode catches the co-packer case: your "Simple
  Truth" spinach recalled under the manufacturer's name
- 🔍 **Lot intelligence** — extracts lot-code and best-by patterns from recall notices
  and tells you exactly what to look for on the package
- 🚨 **Ranked by severity** — Class I (Listeria, Salmonella, undeclared allergens)
  first, with the FDA notice URL for every hit
- 📴 **Offline-first** — pantry is local JSON; recall data can be cached
  (`--offline --data <file>`); pure stdlib, no dependencies

## Quick start

```bash
python3 scripts/recall_radar.py add --brand "Pillsbury" --product "Golden Layer Biscuits" --upc 018000000000
python3 scripts/recall_radar.py match          # against live openFDA
python3 scripts/recall_radar.py audit          # weekly: + store-brand heuristics
python3 scripts/recall_radar.py match --offline --data references/sample-recalls.json
```

## Who needs this

- Families with young children, pregnant household members, elderly parents, or anyone
  immunocompromised — for whom a Class I Listeria recall is not an abstraction
- People with serious food allergies — undeclared-allergen recalls are the ones that
  never make the news
- Anyone who buys store brands (i.e., everyone) — the hardest recalls to match
- Bulk buyers and freezer-stockers — recalled lots sit in freezers for months

## How it works

1. Your pantry lives in `~/.pantry.json` (brand, product, UPC, lot).
2. `match` queries openFDA's food enforcement endpoint for `status:"Ongoing"` recalls.
3. Each pantry item is scored against each recall (fuzzy brand containment, product
   token overlap, string similarity; UPC equality is a near-exact `MATCH`).
4. Hits print with classification, reason, firm, lot intel, recommended action, and
   the FDA notice URL — always read the notice before discarding.

Full matching methodology: [`references/recall-matching.md`](references/recall-matching.md)

## Safety

This tool over-notifies by design — a false "go check the fridge" costs 10 seconds.
It is not a substitute for reading the FDA notice, and never a substitute for medical
advice.

## License

MIT
