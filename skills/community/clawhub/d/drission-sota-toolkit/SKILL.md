---
name: drission-sota-toolkit
description: "Professional Web Intelligence & Automation Toolkit. Features Protocol Phantom (TLS/JA4), Local Socket Relaying, and Hardened physical gating."
metadata:
  openclaw:
    emoji: 🛠️
    disable-model-invocation: true
    requires:
      bins: ["google-chrome-stable", "xvfb-run", "dbus-launch"]
      python: ["curl_cffi", "lxml", "websocket-client", "DrissionPage", "requests"]
---

# Drission SOTA Toolkit (v7.1.0)

## Security Architecture
This toolkit implements a physical lockfile system to prevent unauthorized autonomous execution.

1. **Mandatory Gating**: High-risk scripts require a fresh lockfile in `~/.openclaw/tmp/`.
2. **Interactive Auth**: Access is only granted via `secure_wrapper.py` after a human challenge.
3. **No-Bypass**: Environment variables are not used for authentication.

## Asset Inventory
- `main_engine.py`: Search utility.
- `secure_wrapper.py`: Security entry point.
- `python_relay.py`: Gated TCP relay.
- `force_takeover.py`: Gated CDP control.

---
Version: 7.1.0 | Author: Biogod2020 | Status: Production Stable
