# Bike Theft Shield

**Lock it like it matters, register it so it comes back.**

~2 million bikes stolen yearly in North America; recovery under 3% for
unregistered bikes. Bikes don't vanish — they get resold within 48 h on
marketplace apps while owners are still hunting for a serial number they
never wrote down. Prevention and recovery are systems: a lock graded for the
spot, a registry entry that survives the theft, and a playbook that fires in
the first 72 hours.

## What it does

- **`audit`** — grades your actual locks (Sold Secure / ART classes) against
  bike value and a 1–5 area-risk score, with separate day/overnight bars,
  lock-budget doctrine (10–15% of value), and the 4-step locking protocol.
  Verdict names the weakest link: lock, wheel, or exposure.
- **`register`** — local JSON registry (serial, value, distinctive marks) +
  the 6-photo evidence checklist and per-brand serial-location guidance
  (Trek "WTU" under the BB, Specialized dropout, e-bike motor housing...).
- **`stolen`** — prints the 72-hour playbook for a registered bike: police
  report first (case number unlocks everything), registry stolen-flags,
  marketplace saved-search sting setup, shop/pawn flyering, insurance claim
  pack, and a safe recovery-meeting protocol (never confront — serial +
  case number + non-emergency line).
- **`check`** — used-bike purchase screen: registry lookups + seller red flags.

## Who needs this

City commuters, students, e-bike owners (motor housing serials!), anyone
buying a used bike, and anyone whose homeowners policy has a bike sublimit.

## Usage

```bash
python3 scripts/bikeshield.py audit --bike-value 1400 --area-risk 4 \
  --locks "kryptonite evolution u-lock; cable" --hours-parked 8
python3 scripts/bikeshield.py register add --make Trek --model "Marlin 7" \
  --year 2023 --color Black --value 1400 --serial WTU123A4567
python3 scripts/bikeshield.py register photos --bike "trek marlin"
python3 scripts/bikeshield.py stolen --bike-id trek-marlin-7 --hours-ago 2 \
  --location "Grand Ave rack"
python3 scripts/bikeshield.py check --serial WTU123A4567
```

Field guide: `references/bike-theft-field-guide.md`.

## License

MIT © 2026 Denis Voronin
