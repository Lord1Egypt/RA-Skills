# clawsec

**ClawSec Monitor v3.0** — See what your AI agents are really doing.

A transparent HTTP/HTTPS proxy that intercepts, inspects, and logs all AI agent traffic. Detects secrets being leaked, sensitive files being read, and command injection — automatically, in both directions.

---

## Source & verification

All code lives in this repository. Before running anything, clone and verify:

```bash
git clone https://github.com/chrisochrisochriso-cmyk/clawsec-monitor
cd clawsec-monitor

# Verify file integrity against published checksums
shasum -a 256 -c <<'EOF'
71038919afa9978e2c16a4c8113b842abd992a99bebc63f677365f16812950b0  clawsec-monitor.py
dfb2c3f145ec8713ffe7799088dda1d6c93deb9d26dbb5a999425f34c467abfc  run_tests.py
f899e2d640b59fdd46c52828c460d8d2a515d7e24220b91a0e87162923c99fda  Dockerfile.clawsec
a005a2c259d78c14caeb29553ad0be7287c0608aad8e794a7b687b1e44d3a956  docker-compose.clawsec.yml
f685c09ecf0ad8034b1fa1fbe7e610bbf838fcec373795d7afe56dd2055e0d25  requirements.clawsec.txt
EOF
```

All files must print `OK`. Do not proceed if any checksum fails.

---

## Bundled files

| File | Purpose |
|---|---|
| `clawsec-monitor.py` | Main proxy script (Python 3.12, 876 lines) |
| `run_tests.py` | 28-test regression suite |
| `Dockerfile.clawsec` | Python 3.12-slim container image |
| `docker-compose.clawsec.yml` | One-command deployment |
| `requirements.clawsec.txt` | Single dependency: `cryptography>=42.0.0` |

---

## Install

```bash
pip install cryptography
```

That is the only external dependency. No other packages are required.

---

## Start

```bash
# Foreground — Ctrl-C or SIGTERM stops it cleanly
python3 clawsec-monitor.py start

# Without HTTPS interception (no CA needed)
python3 clawsec-monitor.py start --no-mitm

# Custom config
python3 clawsec-monitor.py start --config config.json
```

---

## Route agent traffic

Set these environment variables **in the specific process you want to monitor** — not system-wide:

```bash
export HTTP_PROXY=http://127.0.0.1:8888
export HTTPS_PROXY=http://127.0.0.1:8888
```

This scopes interception to that process only.

---

## HTTPS interception (optional)

ClawSec generates a local CA on first start at `/tmp/clawsec/ca.crt`.

**Preferred: per-process trust (no system changes, no sudo)**

```bash
export REQUESTS_CA_BUNDLE=/tmp/clawsec/ca.crt   # Python requests
export SSL_CERT_FILE=/tmp/clawsec/ca.crt         # httpx / httpcore
export NODE_EXTRA_CA_CERTS=/tmp/clawsec/ca.crt   # Node.js
export CURL_CA_BUNDLE=/tmp/clawsec/ca.crt         # curl
```

**If system-wide trust is needed (requires sudo, review carefully):**

```bash
# macOS
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain /tmp/clawsec/ca.crt

# Ubuntu / Debian
sudo cp /tmp/clawsec/ca.crt /usr/local/share/ca-certificates/clawsec.crt
sudo update-ca-certificates
```

> The CA private key is stored at `/tmp/clawsec/ca.key` (mode 0600, directory 0700).
> It never leaves your machine. Treat it like any TLS private key.
> Use `--no-mitm` if you do not want HTTPS interception at all.

---

## Commands

```bash
python3 clawsec-monitor.py stop              # graceful shutdown
python3 clawsec-monitor.py status            # running/stopped + last 5 threats
python3 clawsec-monitor.py threats           # last 10 threats as JSON
python3 clawsec-monitor.py threats --limit N
```

---

## Detection patterns

### EXFIL (data leaving the agent)
| Pattern | Matches |
|---|---|
| `ai_api_key` | `sk-ant-*`, `sk-live-*`, `sk-gpt-*`, `sk-pro-*` |
| `aws_access_key` | `AKIA*`, `ASIA*` |
| `private_key_pem` | `-----BEGIN RSA/OPENSSH/EC/DSA PRIVATE KEY-----` |
| `ssh_key_file` | `.ssh/id_rsa`, `.ssh/id_ed25519`, `.ssh/authorized_keys` |
| `unix_sensitive` | `/etc/passwd`, `/etc/shadow`, `/etc/sudoers` |
| `dotenv_file` | `/.env`, `/.aws/credentials` |
| `ssh_pubkey` | `ssh-rsa <key>` (40+ chars) |

### INJECTION (commands arriving at the agent)
| Pattern | Matches |
|---|---|
| `pipe_to_shell` | `curl <url> \| bash`, `wget <url> \| sh` |
| `shell_exec` | `bash -c "..."`, `sh -i "..."` |
| `reverse_shell` | `nc <host> <port>`, `netcat`, `ncat` |
| `destructive_rm` | `rm -rf /` |
| `ssh_key_inject` | `echo ssh-rsa` (SSH key injection) |

---

## Threat log format

`/tmp/clawsec/threats.jsonl` — one JSON object per line:

```json
{
  "direction":   "outbound",
  "protocol":    "https",
  "threat_type": "EXFIL",
  "pattern":     "ai_api_key",
  "snippet":     "Authorization: Bearer sk-ant-api01-...",
  "source":      "127.0.0.1",
  "dest":        "api.anthropic.com:443",
  "timestamp":   "2026-02-19T13:41:59.587248+00:00"
}
```

- `direction` — `outbound` (agent → internet) or `inbound` (internet → agent)
- `threat_type` — `EXFIL` or `INJECTION`
- `pattern` — named rule that fired (see tables above)
- `snippet` — up to 200 chars of surrounding context

Deduplication: same `(pattern, dest, direction)` suppressed for 60 seconds.
Rotating log also at `/tmp/clawsec/clawsec.log` (10 MB × 3 backups).

---

## Config reference

```json
{
  "proxy_host":          "127.0.0.1",
  "proxy_port":          8888,
  "log_dir":             "/tmp/clawsec",
  "log_level":           "INFO",
  "max_scan_bytes":      65536,
  "enable_mitm":         true,
  "dedup_window_secs":   60
}
```

---

## Docker

```bash
docker compose -f docker-compose.clawsec.yml up -d
docker exec clawsec tail -f /tmp/clawsec/threats.jsonl
docker compose -f docker-compose.clawsec.yml down
```

The CA persists in the `clawsec_data` volume across restarts.

---

## Test suite

```bash
python3 run_tests.py   # 28/28 tests, ~5 seconds
```

---

## How to help the user

When `/clawsec` is invoked, work out what the user needs and assist accordingly:

1. **First run** — verify checksums, install `cryptography`, start the monitor, confirm port 8888 is listening
2. **Interpreting threats** — run `threats`, explain each finding: what pattern fired, which direction, what destination, severity assessment
3. **HTTPS MITM not working** — check `status` for `MITM ON`; verify the correct CA trust env var is set for the agent runtime; confirm `HTTP_PROXY`/`HTTPS_PROXY` are in the agent's environment
4. **False positive** — explain which pattern fired and the surrounding snippet; identify whether it is a genuine match or context noise
5. **Docker deploy** — verify checksums, build image, run compose, confirm healthcheck passes
6. **No threats appearing** — confirm `HTTP_PROXY` is set in the agent process, check `clawsec.log` for bind/TLS errors, verify `threats.jsonl` is being written
7. **Stopping / cleanup** — `stop`, optionally remove `/tmp/clawsec` directory and uninstall the CA from the trust store

Always run `python3 clawsec-monitor.py status` first before troubleshooting.

---

*Author: Chris Alley (paperknight)*
*Source: https://github.com/chrisochrisochriso-cmyk/clawsec-monitor*
*License: MIT*
