---
name: customer-complaint-escalation
description: Builds a US complaint escalation path with severity tiers, response deadlines, repeat issue flags and review request limits. Use when the user asks for customer complaint escalation template, complaint response timeline, complaint log spreadsheet. For US customer service managers, e-commerce support leads and shop owners handling complaints, refunds and payment disputes.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Customer Complaint Escalation

**Builds a US complaint escalation path with severity tiers, response deadlines, repeat issue flags and review request limits.** Written for US customer service managers, e-commerce support leads and shop owners handling complaints, refunds and payment disputes.

Use this skill when someone asks for:

- customer complaint escalation template
- complaint response timeline
- complaint log spreadsheet
- service recovery policy
- chargeback complaint process

---

## The job

Every complaint is handled the same way, so a safety issue waits behind a refund request, repeat reports of the same defect never reach the person who can fix it, and agents start offering refunds to make the ticket go away.

## What you get

1. Collect the complaint sources, the products involved, the current response times and the people who can approve a remedy.
2. Set the severity tiers, and put the first response time and the resolution target in each tier.
3. Define what may be offered at each tier, and mark every remedy that needs approval from a named role.
4. Add the rules for a repeat issue, for a safety complaint and for a complaint that involves a payment.
5. Write the record rule: the original complaint stays as written, and any later action is a dated addendum.

Output contract:

- escalation_tiers - the severity levels with the trigger, the owner, the first response time and the resolution target
- remedy_menu - the options at each tier, each marked approved or pending approval
- repeat_issue_flags - the complaints that match an earlier report of the same issue and the count
- deadline_calendar - the response and resolution dates that apply to each complaint, with the rule behind each one
- record_note - the dated addendum language for the complaint record, without changing the original text

## US specifics that matter

- The FTC's rule on consumer reviews and testimonials (16 CFR part 465), effective October 21, 2024, bans giving an incentive that is conditioned on the sentiment of a review, and the rule's statement of basis says review gating can still violate Section 5 of the FTC Act (15 USC 45).
- The same rule bars a business from suppressing a review because of its rating or sentiment, so a complaint record and a review the customer leaves are two separate records.
- For a credit card billing error, Reg E (12 CFR 1005.11) requires the issuer to investigate promptly, to determine whether an error occurred within 10 business days, to report the result within 3 business days of finishing the investigation, and to correct an error within 1 business day.
- The FTC Telemarketing Sales Rule (16 CFR part 310) requires material disclosures, including a statement of the refund, cancellation or exchange policy, before a customer consents to pay, and it requires the seller to keep the records behind those disclosures.
- The FTC Mail Order Rule (16 CFR part 435) requires a reasonable basis to expect to ship within the promised time, and when the seller cannot, it has to offer a delay or a prompt refund, generally within 7 working days.
- California's Automatic Renewal Law (Bus. and Prof. Code 17600 et seq.) as amended by AB 2863, effective July 1, 2025, requires a clear cancellation path for auto-renewing subscriptions, so a subscription complaint carries its own state rule.

## Guardrails (hard rules)

- Never reply to the customer; the plan produces the path and the draft language, and a person sends the message.
- Never offer a refund, a credit, a discount or a replacement that the approval matrix does not authorize, and never promise a date the service level does not support.
- Never tie a remedy to a review, a rating or a positive statement from the customer.
- Never delete or rewrite the original complaint; add a dated note to the record instead.

## Quickstart

### 1. Fill in the brief

`templates/complaint-escalation.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/dedupe_complaints.py --input complaint-escalation.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/complaint-escalation-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Reviews, incentives and escalation**

- 16 CFR part 465, effective October 21, 2024, bans incentives that are conditioned on the sentiment of a review.
- The rule's statement of basis also says review gating can violate Section 5 of the FTC Act.
- A remedy in the escalation path is given for the service failure, not for a review or a rating.
- A complaint record stays intact whatever the customer writes publicly.

**Payment and billing disputes**

- 12 CFR 1005.11 sets the error resolution clock: 10 business days to decide, 3 business days to report the result, 1 business day to correct an error.
- 16 CFR part 435 sets the shipping promise rule and the 7 working day prompt refund when a shipment is late.
- 16 CFR part 310 requires material disclosures, including the refund and cancellation terms, before a customer consents to pay.
- A card dispute and a service complaint follow different clocks, so the tier names the rule it relies on.

**Tiers, owners and deadlines**

- Each tier names a trigger, an owner role, a first response target and a resolution target.
- A safety complaint goes to the top tier whatever the order value is, because the trigger is the harm.
- A repeat issue counts against the same fault and not against the customer, and it moves up the tiers.
- A deadline that a service level does not support is a problem to fix, not a number to print.

**Records and state rules**

- The original complaint text is never edited; a later action is a dated addendum in the same record.
- California's Auto-Renewal Law as amended by AB 2863, effective July 1, 2025, changes the cancellation path for subscriptions, so a subscription complaint gets a state check.
- State gift card, rebate and price advertising rules differ and change, so a state item goes to legal.
- Keep the complaint log, the response records and the approvals together for the period the business has to retain them.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/complaint-escalation-rules.md` - US complaint, refund and dispute rules
- `templates/complaint-escalation.csv` - the brief to fill in
- `scripts/dedupe_complaints.py` - the working script

## Verify the bundle

```bash
python3 scripts/dedupe_complaints.py --input complaint-escalation.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
