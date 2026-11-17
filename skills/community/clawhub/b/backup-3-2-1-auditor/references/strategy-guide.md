# Backup 3-2-1 Auditor — Reference

The model, threat classes, and product-class guidance behind the
verdicts in `scripts/backup_auditor.py`.

## 1. Why 3-2-1 (and what each number actually defends)

| # | Rule | Threat it defends |
|---|---|---|
| 3 | three copies of the data | any single failure: disk death, theft, loss, accidental deletion discovered late |
| 2 | two different media/device classes | correlated hardware failure (batch defect), power surge killing everything on one strip, house-level events |
| 1 | one copy offsite | fire, flood, burglary, regional disaster |
| + | versioned / rollback | ransomware, crypto-lockers, accidental overwrite, sync poisoning (a bad edit propagates) |
| + | air gap (offline copy) | ransomware that enumerates mounts; compromised credentials; malicious deletion of cloud data |
| + | restore-tested | silent backup corruption, expired accounts, full drives, format drift |

3-2-1 is the floor, not the goal: for irreplaceable data the working
standard is 3-2-1-1-0 (…one offline copy, zero errors on test).

## 2. Copy classification (how the script thinks)

Each declared copy is tagged:

- **live-sync** — mirror of primary on another device (cloud sync
  folder, NAS sync). Good against disk loss; USELESS against
  deletion/encryption events (it replicates them).
- **versioned-cloud** — keeps N days/versions of history
  (snapshot-capable services, versioned object storage). Good
  against deletion/encryption within the version window.
- **offline-attached** — external drive, attached now. Good against
  primary disk death; dies with surge/ransomware while attached.
- **offline-rotated** — external drive, currently unplugged/stored.
  The air gap. Ransomware cannot reach it.
- **offsite-physical** — drive/media at another location (relative,
  bank box, office). Good against room/house-level events.
- **remote-repo** — Git host etc. Fine as one copy for code-class
  assets.

Counting rules:
- Copies on the same physical device don't count separately.
- live-sync copies do NOT count toward the "ransomware-safe" copy —
  they count for disk-loss only.
- The audit reports BOTH plain 3-2-1 and 3-2-1-under-ransomware so
  you can see the gap.

## 3. Blast radius analysis

For each asset, the script asks: if my main machine is compromised
TODAY, which copies survive?

- Survives: offline-rotated, offsite-physical, versioned-cloud
  (within window), remote-repo (if attacker lacks creds).
- Dies: live-sync copies (seconds to minutes), offline-attached
  (mounted = reachable), unversioned cloud mirrors.
- Verdict per asset: N surviving copies. For irreplaceable assets
  the target is ≥ 1 surviving + rollback window ≥ 30 days.

## 4. Honest recovery pricing

| Asset class | If lost | Cost |
|---|---|---|
| irreplaceable photos/docs on dead media | professional recovery lab | $300-3000, ~40% success if media physically intact; near $0% after head crash + reuse |
| phone-only photos | lab on flash is harder | $400+, lower success |
| painful docs (tax, contracts) | rebuild via agencies/banks | days-weeks of requests, some originals unrecoverable |
| code | clone from remote | minutes |
| OS/apps/media | reinstall/relurp | hours, $0 marginal |

The point of the price view: spend protection effort where recovery
is expensive/impossible, not uniformly.

## 3-2-1 minimum-cost patterns (product classes, not brands)

1. **The rotated pair.** Two external HDDs. One attached, one in a
   drawer/relative's house. Swap monthly. Cheapest air gap; covers
   ransomware + room events. Weakness: no automation, no versioning.
2. **Versioned cloud + offline.** One versioned cloud tier (rollback
   ≥ 30 days) + one offline drive. Covers everything except
   credential theft of the cloud account → offline drive covers that.
3. **NAS + snapshot + offsite.** Local NAS with snapshots counts as
   versioned + separate media IF the NAS is not mounted 24/7 on the
   main machine (or has its own credentials). Pair with cloud or
   rotated offsite drive for the offsite leg.
4. **Phone-first families.** Phone auto-uploads to versioned cloud
   (not plain sync), quarterly dump to the family offline drive.
   Laptop optional. This matches how photos actually die.

## 5. The restore drill (the part everyone skips)

Quarterly, per irreplaceable asset:
1. Pick 3 random files (use the drill command's random pick habit —
   different years/folders each time).
2. Restore them to a scratch folder from the BACKUP, not the primary.
3. OPEN each file. Photos render, docs open, video plays.
4. Note the time it took. If restore takes > 1 h of fiddling, your
   recovery under stress will be worse — simplify.
5. Log result. Two missed quarters in a row = treat the backup as
   unverified.

Silent failures the drill catches: expired cloud account (billing
card lapsed), backup software writing 0-byte files since the last OS
update, drive full since March, encrypted-by-ransomware-and-nobody-
noticed backups.

## 6. Estate rule

For each irreplaceable asset, at least one copy must be accessible
WITHOUT any account: a physical drive a family member can plug in.
Cloud accounts lock behind 2FA/death; crypto-lockers don't matter to
the dead, but probate does. Record where the physical copies are in
a place your executor will find (not only in the password vault that
dies with you).

## 7. Ransomware-era specifics

- Rotating offline media is the only reliable defense vs modern
  lockers that enumerate all mounts and stored cloud credentials.
- Cloud versioning windows vary (30 days typical, some 30 min for
  sync tiers) — know your window; it is your rollback horizon.
- After an event: don't rush re-sync. Restore OFFLINE copy to a
  clean machine first, then re-point sync. Re-syncing a poisoned
  client has re-encrypted restored data in documented incidents.
- Isolation before investigation: pull the network cable; a live
  attacker keeps working.
