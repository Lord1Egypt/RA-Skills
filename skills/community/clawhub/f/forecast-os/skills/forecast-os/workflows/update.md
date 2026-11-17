# Workflow: update the skill and CLI

Refresh the skill and/or its pinned CLI binary from `github.com/precog-markets/forecast-os`.

These move independently. GitHub **Releases** are CLI binaries only. Skill-only
patches land on the default branch (`skills/forecast-os/`) without a new release.

**Load when** the user asks to update, or when `check_updates.py` exits **3** (CRITICAL). Periodic checks use `python scripts/check_updates.py --periodic` from SKILL defaults (at most once per week) and do not load this file on exit 0 or 1.

| Exit | Meaning | Agent |
| --- | --- | --- |
| 0 | Current, or stamp still fresh | Say nothing about updates |
| 1 | Stale skill and/or CLI, non-critical | Suggest update; show printed notes; keep working. Do not apply until the user asks |
| 2 | Both channels failed | Tell the user the check failed; continue the task |
| 3 | CRITICAL on skill and/or CLI | Apply this workflow now without waiting for the user to ask, then tell them a critical update was forced |

**Done when:** local `forecast-os-metadata.json` matches the remote skill version (and CLI pin if the CLI channel was stale), and `forecast --version` runs when a CLI install was required.

Force a check (ignore the stamp):

```bash
python scripts/check_updates.py
```

## Channels

| Channel | Source of truth | Suggest when | CRITICAL when |
| --- | --- | --- | --- |
| Skill | `skills/forecast-os/forecast-os-metadata.json` on the default branch (`skill`, optional `notes`, optional `critical`) | local `skill` ≠ remote `skill` | remote `critical` is true and versions differ |
| CLI | GitHub Releases (binaries) vs local `cli` pin | pin behind latest release | a newer release name/body has `CRITICAL…` or `[CRITICAL]` |

## CRITICAL (publishers)

**Skill-only** (no new binary). On the default branch, bump `skill` in `forecast-os-metadata.json`, set `"critical": true`, and put a short reason in `"notes"`. Leave `cli` unchanged. Clear `"critical"` on a later skill bump once the force window is over (clients that already match `skill` stay quiet even if `critical` is still true).

**CLI.** Cut a GitHub Release for the new binary. Put either of these in the release **name** or **body**:

- A line starting with `CRITICAL` (example: `CRITICAL: fix signature bypass`)
- The token `[CRITICAL]` anywhere in the name or body

Also bump `cli` in `forecast-os-metadata.json` on that same commit/tag so the pin matches.

## Steps

Run after the user asked to update, confirmed a suggestion (exit 1), or on CRITICAL (exit 3). Apply only the channels that were stale in the check output.

1. Update the skill when the skill channel was stale. For a git checkout, pull the default branch. For a skills.sh install, re-run it:

```bash
git pull
npx skills add precog-markets/forecast-os
```

2. Install the CLI only when the CLI channel was stale (or the new skill pin points at a CLI tag you do not have). `scripts/install.sh` reads the pin from `forecast-os-metadata.json`:

```bash
INSTALL_DIR="$PWD" sh scripts/install.sh
./forecast --version
```

3. Confirm. Run from a directory that resolves config if further commands are needed.

4. On CRITICAL only: tell the user the update was forced, name skill version and/or CLI tag, and quote `notes` or the CRITICAL line.

## Completion check

- `check_updates.py` exits 0, or each stale channel it reported was refreshed.
- If the CLI was updated, `forecast --version` prints a version.
- On CRITICAL, the user was notified that the force update ran.
