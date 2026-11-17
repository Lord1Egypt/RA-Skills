# Backup 3-2-1 Auditor

**Your backup passed 3-2-1? Now check what ransomware leaves of it.**

Most people discover their backup strategy failed at the moment they
need it: the external drive died two years ago, the cloud sync
encrypted along with the laptop, the "backup" shared a power strip
with the machine. This tool audits what you ACTUALLY have, asset by
asset — and then goes one step further than 3-2-1: it computes the
ransomware blast radius, because a synced copy is not a copy when
the encryptor can reach it.

## What it does

- **audit** — per-asset 3-2-1 verdicts (copy count, media diversity,
  offsite) with an explicit rollback/versioning check
- **blast** — ransomware reachability per copy: synced and mounted
  copies DIE with the machine; rotated/offline/versioned copies
  survive. Zero-survivor assets are flagged as total-loss exposure.
- **price** — honest recovery pricing: lab $300-3000 at ~40% for
  irreplaceable data on dead media vs minutes for code-class assets
- **plan** — minimum-cost fixes per asset (versioned tier, rotated
  pair, offsite leg, air gap, estate rule) — product classes, not
  brands
- **drill** — quarterly restore-test log: 3 random files, OPENED not
  copied. An untested backup is a hope, not a backup.

## Quick start

```bash
python3 scripts/backup_auditor.py add --asset "family photos" \
    --copies "phone,icloud photos,laptop" --value irreplaceable
python3 scripts/backup_auditor.py audit
python3 scripts/backup_auditor.py blast
python3 scripts/backup_auditor.py plan
```

Stdlib-only Python 3, offline, local JSON registry. Not enterprise
backup tooling — this is the audit instrument for a household.

## License

MIT
