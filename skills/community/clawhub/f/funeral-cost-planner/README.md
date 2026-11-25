# Funeral Cost Planner

Funerals are bought in 48 hours of grief against a seller whose default is a package.
The median US funeral runs $8,300–$11,000 — the same dignity costs $2,500–$4,000 when
itemized and shopped. This toolkit itemizes funeral home quotes against NFDA median
bands, flags the classic padding patterns (embalming pushed on direct cremation, "state
law requires a vault" — false in every state, hidden basic-services fees, package deltas),
prices the cemetery half separately, and prints the FTC Funeral Rule rights card with
exact citations to read aloud.

## The real-world problem

- ~2.6M US deaths/yr; the median family spends $7,000-12,000 on arrangements, and
  funeral-industry surveys show most families use the FIRST funeral home they call.
- The FTC Funeral Rule (16 CFR 453) gives every family: an itemized General Price List
  on request (including by phone), the right to decline embalming, the right to bring
  an outside casket with NO fee — rights almost nobody invokes at the worst moment.
- Cemetery costs (plot, opening, vault, marker) are half of burial cost and appear on
  no funeral home price list.

## What it does

`scripts/funeral_compare.py` — Python stdlib, no dependencies:

- Per-home itemized comparison vs 13 NFDA-style median/fair bands
- **Padding detectors:** embalming on cremation plans (REFUSE with citation), vault-
  claimed-as-law, casket above retail-replacement price, package-vs-à-la-carte delta,
  basic-services fee over band
- **Path comparison:** direct cremation / cremation+viewing (rental casket) / burial
  with cemetery cost stack / green burial option
- **Rights card** — the six FTC sentences to read aloud, plus complaint routes
- Prepaid-contract review checklist in the references (portability, item-lock
  inflation, trust vs insurance, Medicaid exemption use)

## Quick start

```bash
python3 scripts/funeral_compare.py examples/two-homes.json
```

Example output (real run):

```
HOME: Fairhaven FH
  direct cremation (w/ container)    $  1,495   median $2,500 [ok]
  non-declinable basic services fee  $  1,950   median $2,300 [ok]
  embalming                          $    695   median $775 [ok]
      ⚠ EMBALMING NOT REQUIRED for this plan (no viewing): REFUSE this line (FTC 453.4(f))
  TOTAL (quoted package)             $  4,995
  TOTAL (sum of listed items)        $  8,395
      ⚠ package costs $3,400 LESS than its own items à la carte — demand the GPL and re-price
```

## Reference

`references/funeral-rule-playbook.md` — full price anchor table, the exact FTC phone
script for collecting 3 GPLs in 15 minutes, cemetery cost breakdown, body-donation and
private-land burial routes, prepaid-contract traps, UK/CA notes.

## License

MIT © Denis Voronin
