
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-brightgreen?logo=openclaw&logoColor=white)](https://openclaw.ai)
[![Tests](https://img.shields.io/badge/Tests-28%20passing-brightgreen)](https://github.com/chrisochrisochriso-cmyk/clawsec-monitor/actions)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://github.com/chrisochrisochriso-cmyk/clawsec-monitor/blob/main/docker-compose.clawsec.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://pypi.org/project/clawsec-monitor/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/chrisochrisochriso-cmyk/clawsec-monitor/blob/main/LICENSE)

# ClawSec Monitor

> **See what your AI agents are really doing.**

ClawSec Monitor is a transparent HTTP/HTTPS proxy that sits between your AI agents and the internet. It watches every request and response in real time — catching secrets being leaked, sensitive files being read, and command injection travelling through agent traffic — automatically, with zero code changes to your agents.

---

## Why ClawSec?

Autonomous AI agents make decisions and take actions you can't always predict. ClawSec gives control back.

- **See what agents do** — every HTTP and HTTPS request, decrypted and logged
- **Catch threats automatically** — secrets, sensitive files, reverse shells, injection attempts
- **Block malicious behavior** — pattern-matched detection fires before damage is done
- **Full transparency** — structured threat log you can query, pipe into SIEM, or alert on

---

## What it catches

| Category | Examples |
|---|---|
| **AI API key leakage** | `sk-ant-*`, `sk-live-*`, `sk-gpt-*`, OpenAI keys |
| **SSH key exfiltration** | PEM private keys, `ssh-rsa` pubkeys, `.ssh/id_rsa` paths |
| **Sensitive file access** | `/etc/passwd`, `/etc/shadow`, `/etc/sudoers` |
| **Dot-file leakage** | `.env`, `.aws/credentials`, `.netrc`, `.pgpass` |
| **Command injection** | `curl … \| bash`, `wget … \| sh`, `eval`, `base64 -d \| sh` |
| **Netcat backdoors** | `nc -e`, `nc -lvp`, reverse shells |
| **SSH lateral movement** | New outbound SSH connections to unknown hosts |

Detection covers **both directions** (outbound requests and inbound responses) across plain HTTP **and** HTTPS.

---

## Quick start

### Native (Python 3.12+)

```bash
pip install cryptography
python3 clawsec-monitor.py start
```

Point your agent's HTTP proxy to `http://127.0.0.1:8888` — that's it.

### Docker

```bash
docker compose -f docker-compose.clawsec.yml up -d
```

---

## HTTPS interception

ClawSec generates a local CA on first start and performs full HTTPS MITM — so even encrypted agent traffic is visible. You trust the CA once; after that all HTTPS is inspected transparently.

```
CA certificate: /tmp/clawsec/ca.crt
```

**Trust the CA for your agent runtime:**

| Runtime | Command |
|---|---|
| macOS system | `sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /tmp/clawsec/ca.crt` |
| Ubuntu/Debian | `sudo cp /tmp/clawsec/ca.crt /usr/local/share/ca-certificates/clawsec.crt && sudo update-ca-certificates` |
| Python `requests` | `export REQUESTS_CA_BUNDLE=/tmp/clawsec/ca.crt` |
| Python `httpx` | `export SSL_CERT_FILE=/tmp/clawsec/ca.crt` |
| Node.js | `export NODE_EXTRA_CA_CERTS=/tmp/clawsec/ca.crt` |
| curl | `export CURL_CA_BUNDLE=/tmp/clawsec/ca.crt` |

Prefer not to intercept HTTPS? Use blind tunnel mode:

```bash
python3 clawsec-monitor.py start --no-mitm
```

---

## Commands

```
python3 clawsec-monitor.py start              # start proxy (foreground)
python3 clawsec-monitor.py start --no-mitm   # no HTTPS interception
python3 clawsec-monitor.py stop              # graceful shutdown
python3 clawsec-monitor.py status            # running/stopped + last 5 threats
python3 clawsec-monitor.py threats           # last 10 threats as JSON
python3 clawsec-monitor.py threats --limit 50
```

---

## Threat log

Every detection is appended to `/tmp/clawsec/threats.jsonl`:

```json
{
  "direction": "outbound",
  "protocol": "https",
  "threat_type": "EXFIL",
  "pattern": "ai_api_key",
  "snippet": "Authorization: Bearer sk-ant-api01-...",
  "source": "127.0.0.1",
  "dest": "api.anthropic.com:443",
  "timestamp": "2026-02-19T13:41:59.587248+00:00"
}
```

The same events are mirrored to `/tmp/clawsec/clawsec.log` (rotating, 10 MB × 3 backups).

**Deduplication**: the same `(pattern, dest, direction)` triple is suppressed for 60 seconds to prevent log flooding.

---

## Configuration

```bash
python3 clawsec-monitor.py start --config /etc/clawsec/config.json
```

```json
{
  "proxy_host": "127.0.0.1",
  "proxy_port": 8888,
  "log_dir": "/tmp/clawsec",
  "log_level": "INFO",
  "max_scan_bytes": 65536,
  "enable_mitm": true,
  "dedup_window_secs": 60
}
```

All keys are optional — the defaults above apply if omitted.

---

## Docker

```bash
# Start
docker compose -f docker-compose.clawsec.yml up -d

# Stream threat log live
docker exec clawsec tail -f /tmp/clawsec/threats.jsonl

# Query threats
docker exec clawsec python3 clawsec-monitor.py threats

# Stop
docker compose -f docker-compose.clawsec.yml down
```

The generated CA persists in the `clawsec_data` Docker volume across container restarts.

**Pointing a containerised agent at ClawSec:**

```yaml
environment:
  - HTTP_PROXY=http://clawsec:8888
  - HTTPS_PROXY=http://clawsec:8888
  - REQUESTS_CA_BUNDLE=/tmp/clawsec/ca.crt
volumes:
  - clawsec_data:/tmp/clawsec:ro
```

---

## Test suite

```bash
python3 run_tests.py
```

28 automated tests: SSH key detection, start/stop lifecycle, stale PID recovery, custom config, sensitive file patterns, false positive checks, and throughput under load (300 concurrent connections, ~4 000 req/s on a laptop).

---

## Architecture

```
AI Agent
    │  HTTP_PROXY=http://127.0.0.1:8888
    ▼
┌────────────────────────────────────────────────────┐
│  ClawSec HTTP Proxy  (:8888)                       │
│                                                    │
│  Plain HTTP  → scan headers + body → upstream      │
│                                                    │
│  HTTPS (CONNECT) → MITM tunnel:                   │
│    1. Connect upstream with real TLS               │
│    2. Send client 200 Connection Established       │
│    3. Upgrade client connection to TLS (start_tls) │
│    4. Pipe decrypted traffic through scan()        │
│    5. Re-encrypt to client and upstream            │
│                                                    │
│  SSH watcher  → poll ss / netstat every 5 s       │
└────────────────────────────────────────────────────┘
    │
    ▼  threats.jsonl  ·  clawsec.log
```

---

## Security notes

- The CA private key lives at `/tmp/clawsec/ca.key` (mode 0600, directory 0700). Treat it like any TLS private key.
- Do **not** trust this CA system-wide on production machines — only in the processes you intend to monitor.
- Log snippets are kept short to avoid writing entire secrets to disk.
- Use `--no-mitm` if you cannot or do not want to install the CA.

---

## License

MIT
