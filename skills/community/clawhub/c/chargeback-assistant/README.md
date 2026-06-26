# chargeback-assistant

**Win your payment disputes. Know the right reason code, gather the right evidence, and submit a letter that actually gets approved.**

Most consumers lose chargebacks not because their case is weak — but because they submit a vague complaint instead of a structured case matching exactly what their bank needs to see. This skill fixes that.

---

## What it does

Describe your situation in plain language. The skill:

1. **Identifies your dispute type** — unauthorized, item not received, not as described, duplicate charge, cancelled subscription, credit not processed, or services not rendered
2. **Maps it to the correct reason code** — Visa, Mastercard, Amex, or PayPal/Stripe, each with their own codes and evidence standards
3. **Generates a tailored evidence checklist** — specific to your dispute type and network, not generic advice
4. **Writes a complete dispute letter** — ready to copy-paste into your bank's portal or send by mail, with the right framing for the reason code
5. **Tells you the deadline** — because a late dispute is automatically denied regardless of merit

## Example situations it handles

- *"I ordered something 3 weeks ago and it never arrived. The merchant stopped responding."*
- *"Someone used my card online — I don't recognize this charge."*
- *"I cancelled my subscription in January and they charged me again in February and March."*
- *"The item I received looks nothing like the photos. The merchant won't accept a return."*
- *"They charged me twice for the same order."*
- *"The merchant said they'd refund me two weeks ago. Nothing has appeared."*

## Networks covered

Visa · Mastercard · American Express · PayPal · Stripe

Each has its own reference file with reason codes, evidence requirements, filing timelines, and network-specific tips.

## Honest limits

The skill will tell you when a dispute is unlikely to succeed — digital goods already downloaded, past the filing deadline, buyer's remorse, or already refunded. For weak cases, it suggests alternatives: merchant escalation to a supervisor, BBB complaint, state attorney general, or small claims court.

## Install

```bash
npx clawhub@latest install howie-ge/chargeback-assistant
```

## License

MIT
