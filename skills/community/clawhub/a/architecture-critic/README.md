# Architecture Critic

An adversarial pre-build agent that reviews your proposed architecture before a single line of code is written. It returns a verdict with specific, itemized findings — not encouragement, not alternatives, not vibes.

**Cost to run: ~$0.05. Cost of skipping: a rework cycle.**

## Requirements

- **Runtime:** OpenClaw (this skill uses OpenClaw's agent infrastructure)
- **Dependencies:** `python3` (3.8+), `bash` 4.0+, `anthropic` Python package (`pip install anthropic`)
- **Credentials:** Anthropic API key — set `ANTHROPIC_API_KEY` env var or configure in `openclaw.json`
- **Cost:** ~$0.03–$0.10 per review (Anthropic Sonnet, billed to your account)
- **Data:** Sends task brief + repo snapshot to your Anthropic account. See [SECURITY.md](SECURITY.md) for full details.

---

## Quick Start

```bash
# 1. Write your DONE_WHEN brief
cat > /tmp/brief.md << 'EOF'
Task: Add Stripe subscription checkout to the user settings page
Done when: User can upgrade from free to Pro ($49/mo), webhook updates DB, access gates work
Files touched: app/api/checkout/route.ts, app/settings/page.tsx, lib/stripe.ts, db/schema.sql
EOF

# 2. Run the critic
bash ~/.openclaw/workspace/skills/architecture-critic/scripts/run-critic.sh \
  --project my-project \
  --task "Add Stripe subscription checkout" \
  --done-when /tmp/brief.md

# 3. Read the verdict — build only if APPROVE
```

---

## How It Works

```
You write a brief
      │
      ▼
┌─────────────────────┐
│   Architecture      │
│   Critic Agent      │
│                     │
│  Sees only:         │
│  • Task spec        │
│  • Codebase state   │
│                     │
│  Never sees:        │
│  • Your enthusiasm  │
│  • Prior decisions  │
│  • Conversation     │
└─────────────────────┘
      │
      ▼
  ┌───────────┐   ┌────────────┐   ┌────────────┐
  │  APPROVE  │   │   REVISE   │   │   REJECT   │
  │           │   │            │   │            │
  │ Build it  │   │ Fix brief, │   │ Stop. Tell │
  │           │   │ re-run     │   │ stakeholder│
  └───────────┘   └────────────┘   └────────────┘
```

The critic is structurally isolated — it has no relationship to protect, no stake in the outcome, and no access to the conversation history that might bias a human reviewer.

---

## The Three Verdicts

| Verdict | Meaning | Action |
|---|---|---|
| **APPROVE** | No critical issues found. Proceed. | Start the build. |
| **REVISE** | Specific issues found that could cause rework. Address findings, re-run. | Fix the brief. Re-run critic (max 2 cycles). |
| **REJECT** | Fundamental flaw — wrong approach, security risk, or missing prerequisite. | Stop. Escalate to decision-maker. No build proceeds. |

---

## Example Verdict (REVISE)

```
VERDICT: REVISE

FINDINGS:

1. [PAYMENT] Amount passed from client
   The brief describes checkout creating a PaymentIntent with an
   amount from the frontend request body. This allows any user to
   set their own price. Amount must be calculated server-side from
   a product lookup, never trusted from the client.
   Fix: Server reads price from DB/config by plan ID; client sends
   only `planId`.

2. [RACE CONDITION] No idempotency on subscription creation
   If the user double-clicks or the network retries the checkout
   request, two subscriptions will be created. Stripe's idempotency
   keys must be used. Key should be deterministic from the user ID
   and plan ID, not random.
   Fix: Generate key as `sub-${userId}-${planId}`; pass as
   `idempotencyKey` to stripe.subscriptions.create().

3. [WEBHOOK] Missing invoice.payment_failed handler
   The brief lists checkout success and cancellation webhooks but
   omits `invoice.payment_failed`. Unpaid subscriptions will retain
   access indefinitely until someone notices.
   Fix: Add handler that suspends access or triggers dunning flow
   on first payment failure.

SUMMARY: 3 issues. Address all before proceeding. Re-run critic
after revisions.
```

---

## Reference Checklists

The critic draws on domain-specific checklists:

| Checklist | Use Case |
|---|---|
| `references/checklist-web.md` | General web app architecture |
| `references/checklist-general.md` | Any software build |
| `references/security.md` | Auth, secrets, injection, OWASP |
| `references/payment-flows.md` | Stripe, subscriptions, webhooks |
| `references/ai-builds.md` | LLM calls, prompt injection, token costs |

---

## Skip Only For

- Copy/style-only changes under 3 files with no logic
- Isolated bug fixes that don't touch payment or auth

When in doubt: run the critic. It costs less than a coffee.

---

## Contributing

This skill is published on [ClaWHub](https://clawhub.io). Contributions welcome:

- Add domain-specific reference checklists (`references/`)
- Improve the base SKILL.md prompt
- Add example verdicts for common patterns
- Report false positives / missed issues

See `SKILL.md` for the full skill specification.

---

## License

MIT — see `LICENSE`

Built in production by AxiomStream Group. Running since April 2026.
