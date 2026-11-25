---
name: gdrive-nextcloud-migration
description: "Experimental. Use when migrating Google Drive to Nextcloud."
version: 0.3.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [experimental, nextcloud, rclone, google-drive, migration, heic, yunohost]
    related_skills: []
---

# Google Drive → Nextcloud Migration

Automates the Low-tech Lab procedure from "Vers un numérique souverain et résilient" (https://bureau.lowtechlab.org/apps/collectives/p/YmeZCDHbQnXqGEB/Vers-un-numerique-souverain-et-resilient-9/La-migration-des-donnees-713441): rclone copy from Drive to Nextcloud, then server-side cleanup of extensionless files and HEIC images, then an occ rescan. Three control levels: full-auto, granular (per-phase, dry-run, bandwidth/volume caps), and didactic interactive (per-file confirmation). Destructive phases are dry-run by default. Linux-only (GNU stat/find, apt, occ).

**Status: EXPERIMENTAL.** Logic validated on synthetic test fixtures (40 automated checks: dry-run, apply, interactive, collisions, failed conversions, log triage); not yet run end-to-end on a production migration. Always review the dry-run plan and keep a backup before `--apply`.

## When to Use

- Migrating a Google Drive tree into a self-hosted Nextcloud (YunoHost or bare metal).
- Post-migration cleanup: files without extensions (Nextcloud can't handle them), iPhone .heic images (no preview support).
- Re-parsing an rclone migration log to triage failed files (`--report-only`).
- Don't use for: Nextcloud→Nextcloud moves, client sync bugs, or Drive takeout imports.

## Prerequisites

- `rclone` on the copy machine; `file`, `heif-convert` (Debian: `apt install libheif-examples`) and PHP occ on the Nextcloud server; bash + coreutils everywhere.
- SSH access to the Nextcloud host and its data dir: YunoHost `/home/yunohost.app/nextcloud/data/USER/files`, bare metal typically `/var/www/nextcloud/data/USER/files` (check `datadirectory` in config.php).
- Backup/snapshot of the Nextcloud data dir before bulk renames. Estimate source size with `rclone size gdrive_remote:/FOLDER`; keep ≥20% free-space margin on the target.

### Credentials policy (ask only if necessary, never in chat)

- Scripts take remote NAMES only — never passwords, tokens or app passwords as arguments. No secret is ever requested or typed in chat.
- Check `rclone listremotes` first. If both remotes already exist, nothing is asked. Only for a missing remote, have the USER run `rclone config` themselves (Drive: interactive OAuth browser flow; Nextcloud: vendor `nextcloud`, WebDAV URL `https://HOST/remote.php/dav/files/USER/`, user + app password created in Nextcloud settings → Security).
- The migrate script re-checks remotes before copying and exits with the `rclone config` hint if one is missing. If a login form must be driven by the agent, use the credential vault (`browser_vault`), never typed secrets.

## Modes (user control)

- Full-auto: `migrate_gdrive.sh SRC DST LOG_DIR`, then `fix_nextcloud_files.sh --apply [--auto-office]`, then occ scan. Review the error report afterwards.
- Granular: run phases separately; copy folder-by-folder via SRC/DST subpaths; preview with `--dry-run` (nothing transferred); cap bandwidth with `--bwlimit 5M` (or timetable `"08:00,512k 23:00,off"`) and volume with `--max-transfer 10G`; re-triage an existing log with `--report-only LOG_DIR`; fix script dry-run → review plan → `--apply`.
- Didactic / interactive: `fix_nextcloud_files.sh --interactive` (needs a terminal; over SSH use `ssh -t`). Per file: `y` do it, `n` skip, `a` all remaining suggestions, `q` quit. Unknown MIME types: the `file` description is shown and the user types an extension by hand (empty = skip). As the agent in this mode: explain each command before running it, show the dry-run plan, and wait for the user's explicit go before each destructive phase — never chain phases without confirmation.

## How to Run

Scripts (Hermes substitutes `${HERMES_SKILL_DIR}` with the skill's absolute directory at load time; standalone users: replace it with the folder path):

- `scripts/migrate_gdrive.sh` — phase 1 copy + error report
- `scripts/fix_nextcloud_files.sh` — phase 2 fixes (dry-run by default)

Both are plain bash and also work standalone, without Hermes. Phase 1 runs on the copy machine; phases 2–3 on the Nextcloud server (scp the fix script over first):

    terminal(command="scp ${HERMES_SKILL_DIR}/scripts/fix_nextcloud_files.sh user@host:/tmp/")

Phase 1 — copy (long runs: `terminal(background=True, notify=True)`):

    terminal(command="bash ${HERMES_SKILL_DIR}/scripts/migrate_gdrive.sh gdrive_hello:/FOLDER nextcloud_LTL:/Google_Drive/FOLDER ~/migration-logs --exclude '/FOLDER/TO/EXCLUDE'", timeout=600)
    # preview / metered-link variants:
    #   ... --dry-run
    #   ... --bwlimit 5M --max-transfer 10G

Phase 2 — server-side fixes, INSIDE `data/USER/files`, as the Nextcloud system user (YunoHost: `nextcloud`, bare Debian: `www-data`; `yunohost app shell nextcloud` gives that shell):

    terminal(command="ssh user@host 'cd /home/yunohost.app/nextcloud/data/USER/files && sudo -u nextcloud bash /tmp/fix_nextcloud_files.sh'")            # dry-run
    terminal(command="ssh user@host 'cd /home/yunohost.app/nextcloud/data/USER/files && sudo -u nextcloud bash /tmp/fix_nextcloud_files.sh --apply'")
    terminal(command="ssh -t user@host 'cd /home/yunohost.app/nextcloud/data/USER/files && sudo -u nextcloud bash /tmp/fix_nextcloud_files.sh --interactive'")

Phase 3 — rescan as the Nextcloud user:

    YunoHost: yunohost app shell nextcloud  →  php occ files:scan --all
    Bare:     sudo -u www-data php /var/www/nextcloud/occ files:scan --all

## Procedure

1. Remotes: `rclone listremotes`; guide `rclone config` ONLY for missing ones (user runs it — see Credentials policy). Verify with `rclone lsd` on both. Criterion: both remotes list directories; no secret exchanged in chat.
2. Size check: `rclone size gdrive_remote:/FOLDER`; target free space ≥ size × 1.2. Criterion: numbers recorded before copying.
3. Run `migrate_gdrive.sh` (options: `--exclude PATTERN` repeatable, `--dry-run`, `--bwlimit`, `--max-transfer`). It copies with `--drive-export-formats ods,odt,odp --drive-skip-dangling-shortcuts --links`, logs to `LOG_DIR/rclone_gdrive.txt`, writes `LOG_DIR/errors_report.txt` split into name-too-long vs other. Criterion: report reviewed, rclone exit code noted.
4. Triage failures: name-too-long → rename at the Drive source (or `rclone moveto` to a shorter path) and re-run the copy (idempotent); other errors → fix individually. Criterion: a re-run yields 0 new errors.
5. Dry-run `fix_nextcloud_files.sh` on the server. Review the plan and the manual-review list (office/text/zip/unknown MIME types are NOT auto-renamed by default). Criterion: every planned rename looks right; choose `--apply`, `--apply --auto-office`, or `--interactive`.
6. Execute the chosen mode. HEIC files are converted with `heif-convert`, originals deleted only after a verified non-empty .jpg; collisions get `-1`, `-2`… suffixes, never overwrites. Criterion: summary shows 0 failures; report file kept.
7. Rescan: `php occ files:scan --all` as the Nextcloud user. Criterion: scan exits 0; spot-check the web UI — a converted HEIC and a renamed extensionless JPEG both preview.

## Pitfalls

- Drive-native Docs/Sheets/Slides export to ods/odt/odp; remaining native items (Forms, My Maps…) become small link files via `--links` — pointers, not data.
- Nextcloud rejects filenames over ~250 chars: per-file log failures ("Le nom de fichier est trop long" / "file name too long"), the rest continues. The report isolates them.
- The rclone log appends across runs; move it aside between attempts for a clean per-run report (`--report-only LOG_DIR` re-parses without copying).
- On metered links (tethering/4G), always `--bwlimit` and/or `--max-transfer` — a full Drive copy can be hundreds of GB. `--dry-run` first.
- Never run the fix script on the whole datadirectory (appdata, versions, uploads) — only `USER/files`. It refuses `/` and `$HOME` and warns outside a `*/files` path.
- Run as the Nextcloud user, not root: new files must be owned by it. As root the script chowns new files to the data-dir owner, but `sudo -u nextcloud` / `sudo -u www-data` is the correct path.
- `--interactive` refuses to run without a terminal (use `ssh -t`). In interactive mode, `a` applies all remaining suggestions INCLUDING office types; unknown types with no typed extension still land in the manual list.
- Multi-image HEIC (bursts, Live Photos): `heif-convert` can emit extra `NAME-1.jpg`, `NAME-2.jpg`… siblings — keep them.
- Disk-level renames are invisible to Nextcloud until `occ files:scan`; skipping phase 3 looks like "files disappeared".
- `find ! -name "*.*"` also skips dotfiles (`.hidden` matches `*.*`); intended.
- Unknown MIME types stay untouched by default and land in the manual list with a `file` description — decide by hand (or via `--interactive`), don't blanket-guess.

## Verification

- `errors_report.txt`: 0 untriaged errors.
- On the server in `USER/files`: `find . -type f ! -name "*.*" | wc -l` → only deliberate remainders; `find . -type f -iname "*.heic" | wc -l` → 0.
- `php occ files:scan --all` exit 0; UI previews work for converted/renamed samples.

## Install / Share

Self-contained and machine-independent: no local paths or host-specific data, standard YunoHost/Debian layouts, scripts need only bash + coreutils + `file` (+ `rclone` / `heif-convert` per phase).

- Folder copy: drop the `gdrive-nextcloud-migration/` directory into the target profile's `skills/` dir (`~/.hermes/skills/`, or `$HERMES_HOME/skills/` when set). Any category subdir or none.
- GitHub: push the folder to a repo, then `hermes skills install <owner>/<repo>/<path-to>/gdrive-nextcloud-migration`.
- Direct URL: host `SKILL.md` with its `scripts/` subtree on any web server, then `hermes skills install https://host/path/SKILL.md` — referenced `scripts/` files are fetched and security-scanned automatically.
- Without Hermes: run the two bash scripts directly as documented in How to Run.
- Scan note: Skills Guard rates this skill CAUTION — `privilege_escalation` findings on the `sudo -u` / chown / occ guidance, which are standard Nextcloud administration requirements (files must belong to the Nextcloud user; the skill explicitly discourages running as root). Community installs are blocked by default: review the findings, then install with `hermes skills install <identifier> --force`.
