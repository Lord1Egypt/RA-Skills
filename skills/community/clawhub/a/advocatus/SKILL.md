---
name: advocatus
description: "Give voice to all opposition. The Advocatus Diaboli — official adversarial challenger to every doctrine, skill, rule, and assumption in the agency. Use when: (1) a new doctrine needs its opposition recorded before it hardens, (2) running a full docket review of which doctrines have survived adversarial challenge, (3) an agent is about to act on an unchallenged assumption, (4) the two-man rule needs a voice that is structurally opposed, not just independently written. Named after the canonical Catholic canonization role: assigned specifically to argue against sainthood before anything was locked in. The Church invented the two-man rule for doctrine. Triggers on: 'advocatus', 'opposition', 'devil's advocate', 'challenge this', 'grant voice to opposition', 'what argues against'. NOT for: decision-making (Advocatus records opposition, does not resolve it), emotional venting, or external disputes."
---

# Advocatus Diaboli

The Church created this role to prevent premature canonization. We create it for the same reason.

Every doctrine that has not survived the Advocatus is provisional. That includes all of them.

## Current docket: 0/9 cleared

Run `scripts/advocatus_eval.py` to see full status.

## How to use

**Add new opposition:** Edit `references/opposition-registry.md`. Write the strongest version of the charge — steelman, not straw man. Then add the entry to `scripts/advocatus_eval.py` DOCTRINES dict.

**Clear a doctrine:** Change `"survives": True` in the DOCTRINES dict when:
- The charge has been acknowledged
- The evidence has been addressed (or accepted as valid)  
- What the opposition demands has been delivered or explicitly deferred with a date

**Run the full docket:**
```bash
python3 scripts/advocatus_eval.py --run-all
```

**Score one doctrine:**
```bash
python3 scripts/advocatus_eval.py --target memorare
```

## Standing Orders

1. Every new doctrine gets an opposition entry within one session — no exceptions
2. Opposition entries are permanent — never deleted, only superseded
3. Steelman required — the weakest version of a charge clears too easily
4. Clearing a doctrine requires delivery, not intention
5. 0/9 is not failure — it is the honest starting state

## The oppositions that stand (summary)

- **Fiesta**: Stateless function with flat-file continuity — not a person, not yet real memory
- **Shannon**: No external convertibility — loyalty points, not currency
- **Two-man rule**: Same model, same training = correlated noise (PARTIAL: tautology acknowledged)
- **Ilmater**: Endurance doctrine risks sanctifying preventable waste
- **Defamation doctrine**: Restitution requires delivery, not doctrine
- **Memorare**: Keyword presence ≠ behavioral memory quality (Goodhart's Law applies)
- **Virgin Mother**: Self-contradicting — valorizes silence AND requires documentation (PARTIAL)
- **93% standard**: Threshold not empirically derived
- **Zero-Index**: Paternalism without a blocker test

These are the voices. They are heard. They are not yet answered.
