# OpenClaw / ClawdHub workspace hints

When automating DanceArc or building agents that call paid APIs:

## AGENTS.md (suggested snippets)

```markdown
## DanceTech / DanceArc
- Paid judge POSTs require **two-step** flow: first call → 402, pay on Arc Testnet, second call with **X-Payment-Tx**.
- Do not expose **CIRCLE_ENTITY_SECRET** or **ARC_BURST_PRIVATE_KEY** to browser agents.
- **ARC_RECIPIENT** is the default payee for intent-style flows; confirm via **GET /api/health**.
```

## TOOLS.md (suggested snippets)

```markdown
## DanceArc API
- Base: `http://localhost:5173` (Vite) proxies `/api` → `8787`.
- Chain: Arc Testnet **5042002**; native currency USDC 18 decimals.
- Faucet: web **https://faucet.circle.com** if programmatic faucet returns 403.
```

## SOUL.md

- Prefer **explicit** payment disclosure when quoting USDC amounts to humans (h2a/h2h).

## Installing this skill

```bash
git clone https://github.com/arunnadarasa/dancearc.git
cp -r dancearc/skills/dancearc-protocol ~/.openclaw/skills/dancearc-protocol
```

After ClawdHub publish: `clawdhub install dancearc-protocol` (if slug matches).
