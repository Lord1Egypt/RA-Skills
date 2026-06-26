# clinical-doc-assistant

> **ClawHub Skill** — Clinical Documentation Assistant for OpenClaw  
> Generate SOAP notes, referrals, prior auths, discharge summaries, and after-visit summaries from FHIR R4 data.

---

## Files in This Package

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill itself — publish this to ClawHub |
| `FHIR-REFERENCE.md` | Supporting reference for FHIR queries and EHR-specific notes |
| `backend.py` | FastAPI scaffold for the hosted credit-based backend |
| `README.md` | This file |

---

## Publishing to ClawHub

### 1. Install the ClawHub CLI
```bash
npm i -g clawhub
```

### 2. Log in with GitHub
```bash
clawhub login
```

### 3. Update SKILL.md author field
Edit `SKILL.md` and replace `your-clawhub-handle` with your actual handle.

### 4. Publish
```bash
clawhub publish ./clinical-doc-assistant
```

### 5. Verify
```bash
clawhub inspect your-handle/clinical-doc-assistant
```

---

## Monetization Setup

### Free Tier (Local Mode)
The skill works out of the box with FHIR sandbox — no backend needed.
This gets you installs and builds trust.

### Paid Tier (Hosted Backend)
1. Deploy `backend.py` to Render, Railway, or Fly.io
2. Add your `ANTHROPIC_API_KEY` as an env var on the server
3. Set up Supabase (free tier) for accounts + credit tracking
4. Integrate Stripe for credit purchases (uncomment the Stripe code in backend.py)
5. Update `CLINICAL_DOC_API_URL` in SKILL.md to point to your deployed backend

### Suggested Credit Pricing
| Package | Credits | Price | Per-doc cost |
|---------|---------|-------|-------------|
| Starter | 10 | $9 | $0.90 |
| Pro | 50 | $39 | $0.78 |
| Team | 200 | $129 | $0.65 |

At $0.78/doc and 100 users generating 10 docs/month = **$780 MRR from one skill.**

---

## Recommended Launch Sequence

1. **Day 1** — Publish to ClawHub with sandbox mode working perfectly
2. **Day 2** — Post in OpenClaw Discord `#skills` channel + Reddit r/OpenClaw
3. **Day 3** — Tweet/post on X with a demo video (screen record a SOAP note being generated)
4. **Week 2** — Deploy hosted backend, announce paid tier to early installers
5. **Month 2** — Publish Skill #2 (Drug Interaction Checker) and cross-link both skills

---

## HIPAA Note

This skill is a documentation *drafting* tool. For production use with real PHI:
- Deploy the backend on HIPAA-eligible infrastructure (AWS, Azure, GCP)
- Sign a BAA with your cloud provider
- Do not log PHI in your backend — audit IDs only
- Review with your organization's compliance team

---

## License

MIT — fork, modify, and build on this freely.
