# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 3.x     | ✅ Yes    |
| < 3.0   | ❌ No     |

## Reporting a Vulnerability

If you discover a security vulnerability in Apple Music DJ, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, email: **<and3rn3t@icloud.com>**

Include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment (what data could be exposed, etc.)
- Any suggested fix (optional)

### What qualifies as a security issue

- Token exposure (dev token or user token leaked in logs, output, or cache files)
- Cache files containing sensitive data beyond what's documented
- Scripts making network requests to undocumented endpoints
- File permission issues allowing unauthorized access to cached data
- Code injection via user-supplied arguments (artist names, playlist names, etc.)

### What does NOT qualify

- Apple Music API rate limiting (expected behavior)
- Token expiration (documented, not a vulnerability)
- Missing features or bugs that don't expose data

## Response Timeline

- **Acknowledgment:** Within 48 hours
- **Assessment:** Within 7 days
- **Fix (if confirmed):** Targeted within 14 days, depending on severity

## Security Best Practices for Users

1. **Never commit tokens** — Use environment variables, not hardcoded values
2. **Keep `.env` in `.gitignore`** — The repo ships with this configured
3. **Rotate tokens periodically** — Dev tokens support up to 6-month lifetime
4. **Review cache contents** — `~/.apple-music-dj/` contains your taste profile
5. **Clear the cache when sharing machines** — list it first (`ls -la ~/.apple-music-dj`), then delete
   the folder yourself. It holds your taste profile, snapshots, playlist history and cron logs, and
   deleting it can't be undone. An agent should never do this without being asked.

## How the skill handles local data

- **Owner-only files and directories.** Everything it writes about your listening (profile cache,
  `--output` files, snapshots, playlist history, config, cron logs) is mode `0600`, and
  directories it creates are `0700`. The mode is enforced on every write, so a file that already
  existed with looser permissions is tightened rather than left as it was. `~/.apple-music-dj/` itself
  is tightened to `0700`. Directories you pointed it at that already exist (e.g. `~/Documents`) are
  never changed.
- **No writing through symlinks.** An `--output` (or cache/profile) path that is a symlink, or an
  existing file owned by another user, is refused *before* anything is truncated or chmod'ed — a
  planted symlink can't be used to clobber an unrelated file. Pass the real path instead. (Stream
  devices such as `/dev/stdout` still work.)
- **No tokens on disk unless you ask.** Tokens come from environment variables. The temporary curl
  config that carries them is created `0600`, deleted right after each request, and removed on
  Ctrl-C / `kill`. `setup_auth.py` prints the tokens; it writes them to a file only with
  `--env-file PATH`, and then `0600` (same symlink/ownership checks as above). For the renewal
  reminder, `~/.apple-music-dj/user_token_seen.json` holds a 16-hex-digit SHA-256 fingerprint of the
  user token and the date it was first seen — never the token.

## Guided setup (`setup_auth.py`)

- The sign-in page is served on `127.0.0.1` only (any free port), at a random 32-character path,
  with `Cache-Control: no-store` and `Referrer-Policy: no-referrer`.
- Requests with a non-loopback `Host` header are refused (DNS rebinding), and the token `POST`
  must come from the page's own origin (a different site in the same browser can't submit one).
  Bodies over 8 KB or tokens containing whitespace are rejected; the first valid token wins.
- The server stops as soon as the token arrives, on Ctrl-C, or after `--timeout` (300 s).
- The page loads Apple's MusicKit JS from `js-cdn.music.apple.com`; the user token is created by
  Apple's sign-in and only ever posted back to the local script.

## Demo mode (`demo.py`)

The Apple tokens are declared in `SKILL.md` under `metadata.openclaw.envVars` with
`required: false`, not in `requires.env`. OpenClaw hides a skill whose `requires.env` variables are
missing, which would keep new users from ever reaching the demo. This doesn't loosen anything: each
script that calls Apple still refuses to run without both tokens (`require_env_tokens`,
`apple_music_api.sh`), and every environment variable the scripts read is declared there.


- The sample API listens on `127.0.0.1` only, for the duration of one command (`serve` aside).
- The scripts it runs get a sandbox `HOME` (`~/.apple-music-dj-demo/`), placeholder tokens, and an
  environment with every real `APPLE_*` variable removed, so a real token can't reach even the
  local mock.
- Only plain skill scripts run (by bare name); `setup_cron.py` (which would edit the real
  crontab), `setup_auth.py` and `generate_dev_token.py` are refused, as is any argument pointing
  into the real `~/.apple-music-dj/`.

## Scheduled jobs (cron)

Automation is **opt-in**: nothing is scheduled unless you run `setup_cron.py install`. The default
set is report-only (new releases, daily drop, health check). The two jobs that write or snapshot
(`weekly-mix`, which creates a playlist unattended, and `monthly-drift`) have to be named with `--jobs`. Because a crontab entry keeps running
until removed, the installer is deliberately strict:

- **Installing requires confirmation, enforced in code.** `install --dry-run` prints the exact
  crontab lines and a short digest of them; `install` only proceeds when re-run with
  `--confirm <digest>`. A bare `install` changes nothing and exits 2, and a digest only matches the
  lines it was printed for, so approving one set of jobs/paths can't authorize another.
- `--jobs` must name at least one known job (an empty value is an error, never "all jobs"; unknown
  names are rejected up front, including for `remove`).
- `--profile`, `--log-dir`, `--python`, `--storefront` and `--jobs` are validated: paths must not
  contain newlines, control characters or `%` (cron turns `%` into a newline, even inside quotes),
  `--python` must be an executable file, and the storefront must be a two-letter code.
- Every value is shell-quoted, including the log path, and a finished line containing a newline or
  `%` is refused.
- Jobs run under `umask 077`. Log files are created `0600` in a `0700` directory *before* cron
  writes to them (they contain playlist names, track picks and artist preferences). A symlinked log
  directory or file, a directory or file owned by someone else, or a directory other users can
  write to is rejected.
- `setup_cron.py status` shows what is installed; `setup_cron.py remove` takes it out again.
