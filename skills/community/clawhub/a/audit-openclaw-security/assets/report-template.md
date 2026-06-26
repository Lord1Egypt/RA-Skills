# OpenClaw Security Audit Report

## Executive summary

- **Overall risk rating:** (Critical / High / Moderate / Low / Informational)
- **OpenClaw version:** (`openclaw --version`)
- **Most urgent issues:** (1-3 bullets)
- **Big picture:** What is exposed, who can talk to the bot, what the bot can do.

## Environment overview

- **Host type:** (macOS host / laptop / Docker / EC2 / VPS / other)
- **OS + version:**
- **Gateway bind + access method:** (loopback / tailnet / reverse proxy / LAN / public)
- **Gateway auth mode:**
- **Control UI origin posture:**
- **Trusted proxies / real-IP policy:**
- **Session dmScope:**
- **DM policy / group policy:**
- **Tool profile and notable denies/allows:**
- **Key sensitive paths:** (`~/.openclaw`, auth profiles, sessions, logs)

## Findings

| Severity | Check ID / finding | Evidence (redacted) | Why it matters | Recommended fix | Verify |
|---|---|---|---|---|---|
| Critical |  |  |  |  |  |
| High |  |  |  |  |  |
| Medium |  |  |  |  |  |
| Low |  |  |  |  |  |

## Remediation plan

### Phase 1 — Stop the bleeding (same day)

1.
2.
3.

### Phase 2 — Reduce blast radius (this week)

1.
2.
3.

### Phase 3 — Operationalise (ongoing)

- update cadence (OS + OpenClaw)
- token/password rotation policy
- backup/restore routine
- transcript/log retention and pruning

## Verification checklist

- [ ] `openclaw security audit --deep --json` shows no critical findings
- [ ] `openclaw gateway probe --json` matches the intended listener/auth path
- [ ] `openclaw channels status --probe` shows the expected ready/connected channels
- [ ] Gateway is not reachable from untrusted networks
- [ ] DM pairing/allowlists are in place
- [ ] Group mention gating is enabled where required
- [ ] File permissions are tightened for OpenClaw state and config
- [ ] Tools are limited to what is actually required

## Residual risk notes

Even a well-hardened agent that can read messages and call tools still carries prompt-injection and social-engineering risk. Record which surfaces remain intentionally open, which tools remain enabled, and how recovery works if the Gateway host or credentials are compromised.
