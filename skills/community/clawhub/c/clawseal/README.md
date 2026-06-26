# ClawSeal OpenClaw Plugin

**Cryptographic memory for AI agents with QSEAL tamper-evidence.**

Zero-config demo mode. Auto-start daemon. Production-ready in under 5 minutes.

---

## What This Is

ClawSeal adds persistent, tamper-evident memory to OpenClaw agents:

- **Cryptographically signed memories** — HMAC-SHA256 QSEAL signatures
- **Tamper detection** — Any modification breaks signature immediately
- **Zero database dependencies** — Pure YAML files, Git-friendly
- **Auto-start daemon** — Runs on boot, restarts on failure (launchd/systemd)
- **Demo mode by default** — Works immediately without setup

---

## Quick Start

### Installation

```bash
# Clone or download this plugin
cd clawseal-openclaw-plugin

# Run installation script (installs package + registers daemon)
bash install.sh
```

**That's it.** The server is now running on `http://localhost:5002` and will auto-start on boot.

### Test Health

```bash
curl http://localhost:5002/health
# {"status": "ok", "service": "clawseal-openclaw-server"}
```

### Run Demo

Follow the [demo_conversation.md](demo_conversation.md) script for a complete 2-minute walkthrough showing:
1. Storing memories with QSEAL signatures
2. Recalling memories with verification
3. Detecting tampering (manual corruption)

---

## How It Works

### Architecture

```
OpenClaw Agent
    ↓ (curl/JSON)
ClawSeal Server (Flask, port 5002)
    ↓ (Python)
ClawSeal Package (PyPI: pip install clawseal)
    ↓
YAML Scrolls (signed with QSEAL)
```

### API Endpoints

1. **POST /remember** — Store memory with QSEAL signature
2. **POST /recall** — Retrieve memories with verification
3. **POST /verify** — Explicitly verify signature
4. **GET /health** — Health check

Full API documentation in [SKILL.md](SKILL.md).

---

## Demo Mode vs Production Mode

### Demo Mode (Default)

- **Secret**: Auto-generated persistent secret at `~/.clawseal/demo_secret` (chmod 600)
- **Artifacts**: Marked with `"qseal_mode": "demo_ephemeral"`, `"qseal_production": false`
- **Use case**: Testing, development, demos
- **Security**: NOT production-ready (ephemeral secret)

### Production Mode

- **Secret**: User-managed `QSEAL_SECRET` environment variable
- **Artifacts**: Marked with `"qseal_mode": "production"`, `"qseal_production": true`
- **Use case**: Production deployments, compliance scenarios
- **Security**: Rotate secrets regularly, store in secure vaults

**Upgrade to production:**
```bash
# Generate production secret
clawseal init

# Restart server (will detect QSEAL_SECRET)
# macOS:
launchctl unload ~/Library/LaunchAgents/com.mvar.clawseal.plist
launchctl load ~/Library/LaunchAgents/com.mvar.clawseal.plist

# Linux:
systemctl --user restart clawseal-server
```

---

## Auto-Start Daemon

The `install.sh` script automatically registers ClawSeal as a system service:

### macOS (launchd)

- **Service file**: `~/Library/LaunchAgents/com.mvar.clawseal.plist`
- **Logs**: `~/Library/Logs/clawseal-server.log`
- **Management**:
  ```bash
  # Stop
  launchctl unload ~/Library/LaunchAgents/com.mvar.clawseal.plist

  # Start
  launchctl load ~/Library/LaunchAgents/com.mvar.clawseal.plist

  # View logs
  tail -f ~/Library/Logs/clawseal-server.log
  ```

### Linux (systemd)

- **Service file**: `~/.config/systemd/user/clawseal-server.service`
- **Logs**: `journalctl --user -u clawseal-server`
- **Management**:
  ```bash
  # Stop
  systemctl --user stop clawseal-server

  # Start
  systemctl --user start clawseal-server

  # View logs
  journalctl --user -u clawseal-server -f
  ```

---

## Memory Types

ClawSeal supports 5 memory types with visual glyphs:

- `preference` 🎯 — User preferences
- `fact` 📌 — Factual information
- `insight` ✨ — Insights/observations
- `decision` ⚖️ — Decision records
- `general` 📝 — General notes

---

## Integration with OpenClaw

See [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md) for detailed integration guide.

**TL;DR**: OpenClaw agents call ClawSeal via standard `curl` commands. No special integration required.

---

## Security Notes

### QSEAL Signatures

- **Algorithm**: HMAC-SHA256
- **Secret management**: Demo mode (persistent local file) or production mode (env var)
- **Tampering detection**: Any content modification breaks signature immediately
- **Chain linking**: Optional Merkle-like chains via `qseal_prev_signature`

### Threat Model

- **Tamper-evident**: Signatures break on modification
- **Verifiable**: Anyone with QSEAL_SECRET can verify
- **Auditable**: Chain structure provides temporal lineage
- **Fail-closed**: Missing QSEAL_SECRET = hard error (no silent fallbacks)

**NOT designed for**:
- Protection against secret theft (if attacker has QSEAL_SECRET, they can forge)
- Network-level attacks (use HTTPS for remote deployments)
- Multi-party verification (single shared secret model)

---

## Troubleshooting

### Server not starting

**Check logs:**
```bash
# macOS
tail -f ~/Library/Logs/clawseal-server.log

# Linux
journalctl --user -u clawseal-server -f
```

**Common issues:**
- Port 5002 already in use → Change port in service file
- Python dependencies missing → Re-run `pip install -r backend/requirements.txt`
- ClawSeal package not installed → Run `pip install clawseal>=1.1.3`

### Health check fails

```bash
curl http://localhost:5002/health
```

If this fails:
1. Check if server is running (see logs above)
2. Verify port 5002 is accessible
3. Try manual start: `python3 backend/clawseal_server.py`

### Import errors

```bash
python3 -c "from clawseal import ScrollMemoryStore"
```

If this fails:
```bash
pip install --upgrade clawseal
```

---

## Files

- **SKILL.md** — OpenClaw skill metadata + LLM instructions
- **backend/clawseal_server.py** — Flask HTTP bridge
- **backend/requirements.txt** — Python dependencies
- **demo_conversation.md** — Agent interaction demo script
- **install.sh** — Installation + daemon registration
- **package.json** — npm metadata
- **README.md** — This file
- **OPENCLAW_INTEGRATION.md** — OpenClaw ecosystem integration guide

---

## Links

- **PyPI**: https://pypi.org/project/clawseal/
- **GitHub**: https://github.com/mvar-security/ClawSeal
- **Documentation**: https://github.com/mvar-security/ClawSeal#readme
- **Issues**: https://github.com/mvar-security/ClawSeal/issues

---

## License

Apache 2.0 — See [LICENSE](LICENSE) for full text.

---

**This isn't theory. This is running code. Dated today.**

Install it. Run the demo. Record the video. That video goes viral.
