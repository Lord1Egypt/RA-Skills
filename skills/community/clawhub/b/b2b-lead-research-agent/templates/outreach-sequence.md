# Outreach sequence - [Company Name]

**Tier:** [A]  **Contact role:** [role]  **Business contact:** [address used for business inquiries]
**Sender:** [name, company]  **Reply-to domain:** [your sending domain]

> Each draft is sent manually after a human read. No bulk automation. Verify
> every fact before it goes out - a wrong fact is worse than no email.

---

## Touch 1 - Email, day 1

**Subject:** [specific, under 60 chars, no fake Re:/Fwd:]

```
Hi [First name],

[Line 1 - the trigger: "Saw you posted 9 field tech roles last month."]

[Line 2 - their words: "Your site says you run dispatch from a single
coordinator across 4 territories."]

[Line 3 - the problem hypothesis, one sentence.]

Worth 15 minutes to compare how other multi-territory service teams handle
scheduling?

[Sender name]
[Title]
[Company]
[Phone]
[Physical street address]
[City, ST ZIP]

Unsubscribe: [one-click link or mailto:optout@yourdomain.com]
```

**Personalization note:** [which source each line came from]

## Touch 2 - LinkedIn (manual), day 3

```
[Connect note, under 300 characters, no pitch.]

Hi [First name] - noticed [Company] is [trigger]. I work with [similar
companies] on [outcome]. Open to comparing notes?
```

**Personalization note:** [source]

## Touch 3 - Email, day 8

**Subject:** [different angle, no fake Re:]

```
Hi [First name],

[One line - new proof point, benchmark, or customer result relevant to their
trigger. Date it.]

[One line - what changed since the first email, or a different entry point.]

Still worth 15 minutes?

[Sender name]
[Company]
[Phone]
[Physical street address]
[City, ST ZIP]

Unsubscribe: [link]
```

**Personalization note:** [source]

## Touch 4 - Email, day 18 (breakup)

**Subject:** [short, no fake Re:]

```
Hi [First name],

Closing the loop - if [specific problem] is not on your list this quarter, no
reply needed and I will not follow up again.

If it is, one line here and I will send the two-minute breakdown.

[Sender name]
[Company]
[Phone]
[Physical street address]
[City, ST ZIP]

Unsubscribe: [link]
```

**Personalization note:** [source]

---

## Compliance checklist (run `scripts/compliance_check.py`)

- [ ] From address is a real person at a business domain, not a freemail account
- [ ] Subject is truthful and not deceptive
- [ ] Physical postal address present in the body
- [ ] Opt-out line present, monitored, and connected to the suppression list
- [ ] No "guaranteed", "risk-free", or false-urgency claims
- [ ] One clear call to action per message
- [ ] Every personalization line traces to a cited source
- [ ] Volume and pace are within the account's daily limit
- [ ] No prior opt-out for this contact or domain

## Rules for this sequence

- Maximum 4 touches over 18 days, then stop.
- One follow-up after a reply stop.
- If they opt out, suppress permanently - no exception, no "last email".
- Never send the same sequence to two people at the same company.
- If the trigger goes cold, the sequence stops.

## SMS / call variant (only with documented consent)

- [ ] Prior express written consent captured and stored
- [ ] Consent record attached (timestamp, source, exact wording)
- [ ] STOP handling confirmed
- [ ] Number is a business line published for contact, or a mobile with consent
