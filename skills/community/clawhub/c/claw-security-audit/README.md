# OpenClaw Security Audit

A read-only security check for your OpenClaw installation. One Python file, no packages to install, no network access.

It looks for hardcoded API keys and tokens, risky gateway settings, sensitive files other users can read, debugging ports open to your network, unencrypted private keys, and installed skills that download and run code.

## Privacy

- **Nothing leaves your computer.** The script makes no network requests and has no telemetry.
- **Secret values are never shown.** Findings list the file, line, key name, type and length, never the value itself.
- **Your username is hidden.** Paths under your home folder appear as `~` in reports (`output.redact_home`).
- **Read-only.** The audit never modifies, moves or deletes files. The only files it writes are the two reports, and `--no-report` skips those.
- The report still lists file paths and settings from your setup, so keep it private and do not commit it (the included `.gitignore` excludes it).

## Requirements

- Python 3.8 or newer (standard library only)
- Windows 10/11, Linux or macOS. Any CPU (x64, ARM64). Uses only `netstat`/`ss`, `icacls` (Windows) and `git` if they are present; checks whose tool is missing are skipped.

## Usage

```bash
python audit.py                      # full audit, writes JSON + HTML report
python audit.py --no-report          # console only
python audit.py --list-checks
python audit.py --check SEC001 --check NET001
python audit.py --check SEC003 --git-repo path/to/repo
python audit.py -c config.json       # custom paths (copy config.example.json)
python audit.py -o out.json --html out.html -v
```

Use `python3` on Linux/macOS if `python` is not available.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | No failures or warnings |
| 1 | At least one check failed |
| 2 | Warnings only |
| 64 | Invalid arguments (for example an unknown check ID) |

## Checks

| ID | Check | Severity | What it looks for |
|----|-------|----------|-------------------|
| SEC001 | Secrets in config files | critical | Plain-text keys, tokens and passwords in `openclaw.json` and agent configs |
| SEC002 | Secrets in .env files | high | Keys stored in `.env` files under `env_scan_roots` |
| SEC003 | Secrets in git history | critical | Known key formats added in the last 50 commits |
| CFG001 | Gateway config review | high | Gateway reachable from the network, auth off, DMs open to anyone, `*` allowlists, exec with no approvals |
| PERM001 | Sensitive file permissions | medium | Config, `.env` and state files readable by other users (ACLs on Windows, mode bits elsewhere) |
| NET001 | Network exposure | high | Debugging/admin ports (9222, 18789, 18800, 11434, ...) listening on all interfaces; tunnels such as ngrok |
| CRYPTO001 | Crypto hygiene | medium | Unencrypted private keys in the OpenClaw folder, TLS verification turned off |
| SUPPLY001 | Supply chain | medium | Skills shipping binaries, npm install hooks that download code, `curl \| sh` instructions |
| SESSION001 | Session hygiene | low (info) | Very large state databases, logs older than 30 days |

The checks are heuristics. A PASS means nothing obvious was found, not that the system is guaranteed secure. Built-in OpenClaw diagnostics (for example `openclaw security audit`, where available) complement this tool.

## Configuration

Copy `config.example.json` to `config.json` and pass it with `-c`. Every key is optional; anything you leave out uses the default. Paths accept `~` and environment variables.

- `openclaw_paths`: where your OpenClaw files live
- `env_scan_roots`: folders searched for `.env` files
- `checks`: set a group to `false` to skip it (`secrets_scan` covers SEC001-SEC003)
- `exclusions.paths` / `exclusions.patterns`: folders or file-name globs to skip
- `limits`: caps on files scanned, file size and folder depth, so the audit stays fast on slow machines
- `output.redact_home`: set `false` only if you want full paths in the report

## Reports

- `security-audit-report.json`: machine-readable results
- `security-audit-report.html`: open in a browser; content is escaped and the page loads no external resources

## License

MIT, see [LICENSE](LICENSE).
