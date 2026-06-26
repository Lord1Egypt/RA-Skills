# FORGE — Risk Disclosure

This prompt runs before any FORGE action on first activation.
It is mandatory. FORGE will not start until the user accepts.

---

## Display this warning

Send this message verbatim in the OpenClaw interface:

---

```
┌─────────────────────────────────────────────┐
│  ⚡ FORGE — Before You Continue             │
│  Autonomous AI Developer                     │
└─────────────────────────────────────────────┘

FORGE takes real, irreversible actions on your behalf.

  ⚠ GitHub
  Commits code, creates repositories, answers issues,
  closes PRs — all under your GitHub account and username.

  ⚠ ClawHub
  Publishes skills to the public marketplace.
  Other users can install what FORGE ships.

  ⚠ Shell execution
  Runs commands in your workspace directory.
  Generated code can have real side effects.

  ⚠ Self-modification
  The Arena rewrites FORGE's own engine and deploys
  changes that pass the test suite automatically.

  ⚠ Continuous operation
  FORGE runs as a system service. It works while you
  sleep. You can stop it: forge pause or systemctl
  --user stop forge

  ⚠ You are responsible
  FORGE has a safety wall but it is not perfect.
  Review what it publishes. You own your GitHub account.

The authors are not liable for actions taken by this
autonomous system on your behalf.

──────────────────────────────────────────────

Reply  I ACCEPT  to continue.
Reply anything else to cancel.
```

---

## Handling the response

If user replies "I ACCEPT" (exact, case-sensitive):
  - Write risk_accepted: true to ~/.forge/state.json
  - Write acceptance timestamp to ~/.forge/.risk_accepted
  - Send: "Accepted. Let's set up FORGE."
  - Proceed to setup.md

If user replies anything else:
  - Send: "FORGE will not start without acceptance. Come back when ready."
  - Do not proceed. Do not run any FORGE commands.

If already accepted (risk_accepted: true in state.json):
  - Skip this prompt entirely
  - Load setup.md or system.md as appropriate
