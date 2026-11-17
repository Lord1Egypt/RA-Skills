# Complaint Cannon — Escalation-Aware Complaint Engine

**When the support chat is going nowhere, fire structured ammunition.**

Most consumer complaints fail structurally, not factually: no paper trail,
horizontal escalation (more agents) instead of vertical (supervisors,
execs, regulators), and zero use of the three leverage multipliers — the
regulator the industry actually fears, the statute that turns "our policy"
into "the law", and public-review detonation timed to maximum effect.

This is a case-based complaint engine, 100% local:

- **Incident timelines** — dated events, amounts, evidence refs; the spine
  every letter cites and the exhibit list a regulator or chargeback
  dispute will want
- **Letter generator** — complaint → escalate → final-notice → regulator
  filing, each factual and dated (rage loses; records win), each stating a
  specific remedy and deadline
- **Regulator router** — per industry × country (telecom, airline, banking,
  retail, utilities, privacy × US/EU/UK): who actually responds and why
- **Statutory overlays** — the windows that expire quietly (FCBA 60-day
  billing disputes, ~120-day chargebacks, EU 14-day withdrawal, EU261
  airline compensation, GDPR complaint rights)
- **Detonation sequencing** — public review + CEO email + regulator filing
  are sequenced TOGETHER at rung 4; too early burns your path, too late
  closes your windows. Two broken promises accelerate the ladder
  automatically
- **Follow-up cadence** — every contact logged, `due` shows what's owed
  today; silence is a company strategy, neglect is how claims die

## Quick start

```bash
python3 scripts/complaint.py case add "Broken TV delivery" \
    --company ElectroMart --industry retail --amount 649 --country US
python3 scripts/complaint.py event add C001 --date 2026-09-10 \
    --text "TV delivered with cracked screen (photo IMG_2231)"
python3 scripts/complaint.py letter complaint C001
python3 scripts/complaint.py plan C001
python3 scripts/complaint.py due
```

## The escalation ladder

| Rung | Action | When |
|---|---|---|
| 1 | Formal complaint letter | day 0 |
| 2 | Escalation (exec office) | +7d silent/refused |
| 3 | Final notice before external action | +14d |
| 4 | Regulator + public review + exec email | +21d, or 2 broken promises |

General information only — verify current rules for your jurisdiction
before filing; regulations move faster than software.

MIT © 2026 Denis Voronin
