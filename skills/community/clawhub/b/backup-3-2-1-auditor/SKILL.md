---
name: backup-3-2-1-auditor
description: "Use when you realize your photos/code/documents exist in exactly one place (or your 'backup' is a external drive in the same room as the computer) — audits your actual data-loss risk against the 3-2-1 rule (3 copies, 2 media, 1 offsite) asset by asset, scores blast radius (ransomware encrypts synced copies too), prices honest recovery (professional recovery lab $300-3000 vs $0), generates the minimum-cost redundancy plan for YOUR asset list, and produces a restore-test drill because an untested backup is a hope, not a backup."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [backup, data-loss, ransomware, photos, digital-safety, 3-2-1]
---

# Backup 3-2-1 Auditor

**An untested backup is a hope, not a backup.** Most people discover
their backup strategy failed at the exact moment they need it: the
external drive died two years ago, the cloud sync encrypted along
with the laptop (ransomware follows sync), the "backup" was the same
disk. This tool audits what you ACTUALLY have, asset by asset,
against the 3-2-1 rule and scores the real risk.

## Overview

1. **audit** — register assets (family photos, code repos, tax
   documents, password vault...), declare where each lives
   (laptop + Time Machine + Google Drive...), get a per-asset
   3-2-1 verdict with copy count, media diversity, offsite status.
2. **blast** — ransomware blast-radius analysis: which "backups" are
   reachable/synced from your main machine and die with it.
3. **price** — honest loss pricing per asset class: irrecoverable
   (baby photos), recoverable-at-cost (professional lab $300-3000,
   ~40% success), re-creatable (OS, apps, streamed media).
4. **plan** — minimum-cost redundancy plan from your audit: which
   assets need what (versioned cloud + unplugged offline copy vs
   sync is enough), with concrete product classes, not brands.
5. **drill** — the quarterly restore test: pick a random file class,
   actually restore it, log the result. The drill finds the silent
   failures (encrypted backups, expired accounts, full drives).

Stdlib Python, offline, local JSON registry.

## When to Use

- New Year / tax season / post-vacation "where do my photos actually
  live" moments
- After a scare (drive clicking, phone in the lake, ransomware in
  the news at your employer)
- Setting up a family member's first real backup
- Before a big life event: moving, kid going to college with the
  family photo library, relative's estate (their accounts die with
  them)

**Don't use for:** enterprise backup policy (different tool class),
or after active ransomware detection (isolate from network first,
then this tool for the post-mortem).

## How It Works — Numbered Steps

1. Register your assets and where each currently lives:
   ```
   python3 scripts/backup_auditor.py add --asset "family photos 2009-2026" \
       --copies "laptop,icloud photos,external HDD in desk drawer" --value irreplaceable
   python3 scripts/backup_auditor.py add --asset "code repos" \
       --copies "github,workstation" --value recreate-cheap
   ```
2. Audit against 3-2-1:
   ```
   python3 scripts/backup_auditor.py audit
   ```
   Per asset: copies count ✓/✗, media diversity ✓/✗, offsite ✓/✗,
   overall PASS / FRAGILE / FAIL.
3. Check ransomware blast radius:
   ```
   python3 scripts/backup_auditor.py blast
   ```
   Any copy that syncs from, or mounts on, your main machine is NOT
   an independent copy under ransomware. Verdicts per copy.
4. Price the downside honestly:
   ```
   python3 scripts/backup_auditor.py price
   ```
5. Get the minimum-cost fix plan:
   ```
   python3 scripts/backup_auditor.py plan
   ```
6. Run the restore drill quarterly and log it:
   ```
   python3 scripts/backup_auditor.py drill --asset "family photos" --result "restored 3 random files OK"
   python3 scripts/backup_auditor.py drill --due
   ```

## The Rules Behind The Verdicts

| Rule | Means | Common failure |
|---|---|---|
| 3 copies | primary + 2 backups | "iCloud IS my backup" = 1.5 copies (sync ≠ backup) |
| 2 media | different device types | laptop + external SSD plugged into the laptop = 1 media for surge/ransomware purposes |
| 1 offsite | survives fire/theft/flood | external drive in the same desk ≠ offsite; cloud sync counts as offsite ONLY if versioned |
| Versioned | can roll back before encryption event | plain sync mirrors ransomware's damage in seconds |
| Air-gapped | unreachable from the network | rotate two offline drives; one always unplugged |

Asset value classes:
- **irreplaceable** — baby photos, family video, life documents
  originals. Recovery lab $300-3000 at ~40% success if media intact.
- **painful** — tax records, contracts, thesis drafts: rebuildable
  at days of work or agency-request loops.
- **recreate-cheap** — code on GitHub, music re-ripped, OS/apps.

## Common Pitfalls

1. **Sync is not backup.** Dropbox/Drive/iCloud sync the encrypted
   versions too. You need VERSIONING (roll back) or an offline
   copy. This is the #1 ransomware loss pattern.
2. **The drawer drive.** Two copies in one room = one fire/theft
   away from zero. Offsite can be: versioned cloud, bank safe
   deposit, relative's house (rotating drive).
3. **No media diversity.** Laptop SSD + external SSD on the same
   desk, same power strip: surge takes both. HDD + cloud, or SSD +
   tape-class cold storage, count; two identical SSDs on one desk
   don't.
4. **Never tested restore.** Backup software says "success" for
   years while writing garbage or the account expired. The drill
   (restore 3 random files, open them) is the only proof.
5. **Forgetting the phone.** For most families the phone IS the
   primary photo library now. Audit it as an asset with its own
   copy plan, not as a satellite of the laptop.
6. **Backup drive always plugged in.** Convenience kills the air
   gap. Rotate two drives: one attached this month, one in the
   drawer. Ransomware can't encrypt what isn't mounted.
7. **Estate blindness.** Cloud accounts with the only copy die with
   the owner (or lock behind 2FA). For irreplaceable family data,
   one copy must exist that doesn't require any account.

## Example

```
$ backup_auditor.py audit
ASSET: family photos 2009-2026 [irreplaceable]
  copies: laptop, iCloud Photos
  3 copies: FAIL (2)   media: FAIL (both live-sync from phone/laptop)
  offsite: PARTIAL (cloud but unversioned tier)
  ransomware blast: BOTH copies reachable from phone/laptop — no rollback
  VERDICT: FAIL — one device-loss or ransomware event from zero
  recovery if lost: lab $300-3000, ~40% (photos on dead phone)

$ backup_auditor.py plan
MINIMUM-COST PLAN:
  family photos: add (a) versioned cloud tier OR rotated 2-drive
    offline pair — one unplugged at all times; (b) annual copy to
    relative/bank. Result: 3 copies / 2 media / 1 offsite / rollback.
  code repos: PASS (GitHub + workstation = fine for recreate-cheap).
NEXT DRILL DUE: 2026-12-10 (quarterly)
```

## Verification Checklist

- [ ] Every irreplaceable asset registered with real copy locations
- [ ] Audit run: no FAIL/FRAGILE on irreplaceable assets
- [ ] Blast radius: at least one copy unreachable from main machine
- [ ] Versioned or offline rollback path exists per irreplaceable asset
- [ ] Restore drill done this quarter — files OPENED, not just copied
- [ ] One asset copy exists that requires no account (estate rule)
