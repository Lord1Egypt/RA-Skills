# Call Script Coach

**Walk into every difficult phone call with a script, an objection tree, and a plan —
instead of a sinking feeling.**

People accept wrong fees, skip refund disputes, overpay for years, and avoid
negotiating because when the rep says "that's our policy," they have nothing ready.
The difference between resolved and capitulated is usually four things: goal, leverage,
prepared responses, and knowing when to escalate. This tool builds all four for your
specific call.

## What it does

- 📋 **10 pre-built scenarios** — billing disputes, late-fee waivers, rate negotiation,
  cancellations, landlord repairs, insurance denials, collections, vendor complaints,
  raise calls, sales cold calls
- 🌳 **Objection→response trees** — for every predictable "no," a modeled response in
  the acknowledge → bridge → ask pattern
- 📄 **Printable cheat sheet** — opening line, asks in order, escalation path,
  do-not-say list, notes field for the rep's name and ticket number
- 🎭 **Practice mode** — the script plays the other side with realistic pushback and
  scores your typed responses against the pattern (did you acknowledge? restate
  leverage? make a concrete ask?)
- ✍️ **Custom builds** — supply your own goal, leverage, fallback, and objection
  pairs for situations the library doesn't cover

## Quick start

```bash
python3 scripts/call_coach.py scenarios
python3 scripts/call_coach.py build --scenario billing-dispute \
    --goal "Remove the $80 tech-visit charge" \
    --leverage "Chat log where rep said visit was free; 3yr customer" \
    --fallback "File FCC + state AG complaint"
python3 scripts/call_coach.py practice --scenario cancellation
```

Scripts are saved to `~/.call-scripts/` (txt + json) — print the one-pager and keep it
next to the phone.

## Who needs this

- Anyone disputing a charge, fee, or bill hike by phone
- People canceling services who want to survive the retention gauntlet
- Renters demanding repairs with dates attached, not promises
- Anyone facing a collections call (validation-first, admit-nothing script)
- Sales folks and freelancers doing cold calls and rate negotiations
- Anyone who has rehearsed a call in their head three times — write it down instead

## Example (practice mode)

```
[1/5] REP: I can offer a partial credit as a one-time courtesy
YOU:  I appreciate that — is that against the full $80 or partial? If partial,
      I'm asking for the full amount because the visit was quoted as free.
      score: 3/3  [acknowledge + bridge + ask]
```

Deeper methodology: [`references/negotiation-playbook.md`](references/negotiation-playbook.md)

## License

MIT
