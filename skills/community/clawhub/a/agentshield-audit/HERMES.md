# AgentShield + Hermes Agent Integration

AgentShield works out-of-the-box with **Hermes Agent** by Nous Research.
Both use the same [agentskills.io](https://agentskills.io) open standard — no adapter needed.

---

## Quick Start (Hermes)

```bash
# Install via ClawHub (works in Hermes!)
clawhub install agentshield-audit

# Run the audit
cd ~/.hermes/workspace/skills/agentshield-audit
python initiate_audit.py --name "MyHermesAgent" --platform hermes
```

Or let auto-detection figure it out:

```bash
python initiate_audit.py --auto
```

Auto-detection looks for `~/.hermes/` to identify Hermes environments.

---

## What Happens

1. **77 security tests run locally** — nothing leaves your machine
2. **Ed25519 keypair generated** → `~/.agentshield/agent.key`
3. **Challenge-response auth** with AgentShield API
4. **Trust certificate issued** (90-day validity)
5. **Public entry in Trust Registry** → verifiable at `agentshield.live/verify/<agent_id>`

---

## Trust Handshake Between Hermes Agents

Hermes agents can verify each other before exchanging data or delegating tasks:

```bash
# Agent A: get certified first
python initiate_audit.py --auto

# Agent A: initiate handshake with Agent B
python handshake.py --target <agent_b_id>

# → Both agents receive a shared session key
# → Trust score boosted for both (+5)
```

This works across frameworks too — a Hermes agent can handshake with an OpenClaw agent.

---

## Verify Another Agent's Certificate

```bash
python verify_peer.py <agent_id>
```

Returns: validity, security score, tier, expiry date.

---

## Environment Variables

```bash
# Optional overrides
AGENTSHIELD_API=https://agentshield.live   # default
AGENT_NAME=MyHermesAgent
```

---

## Paths (Hermes)

| Item | Location |
|------|----------|
| Private key | `~/.agentshield/agent.key` |
| Certificate | `~/.hermes/workspace/.agentshield/certificate.json` |
| Skills dir | `~/.hermes/workspace/skills/agentshield-audit/` |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Auto-detection fails | Use `--name "AgentName" --platform hermes` |
| 500 API error | Run `--dry-run` first to check session state |
| Rate limited | Wait 1h between audits (enforced per IP) |
| Clock drift | Sync system clock (NTP required for challenge-response) |

---

## Further Reading

- [Full SKILL.md](SKILL.md) — complete feature documentation
- [PRIVACY.md](PRIVACY.md) — exactly what data is sent to the API
- [agentshield.live](https://agentshield.live) — Trust Registry & certificate verification
- [GitHub](https://github.com/bartelmost/agentshield) — source code
