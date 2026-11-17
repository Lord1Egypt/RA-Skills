---
name: appointment-scheduling-rules
description: Writes appointment and cancellation rules plus CAN-SPAM and TCPA ready reminder copy for US service businesses. Use when the user asks for appointment policy template, cancellation and no show policy, email reminder template compliance. For US dental, salon, clinic, auto repair and field service owners who schedule appointments and send reminder messages.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Appointment Scheduling Rules

**Writes appointment and cancellation rules plus CAN-SPAM and TCPA ready reminder copy for US service businesses.** Written for US dental, salon, clinic, auto repair and field service owners who schedule appointments and send reminder messages.

Use this skill when someone asks for:

- appointment policy template
- cancellation and no show policy
- email reminder template compliance
- sms appointment reminder rules
- scheduling policy small business

---

## The job

Scheduling rules live in the owner's head and in whatever message the last employee wrote, so cancellations get waived for the wrong customers and reminder texts go out without the consent record the rules require.

## What you get

1. Collect the service types, the notice period, the cancellation fee, the deposit rules and the states the business serves.
2. Write the policy in the order the customer meets it: booking, confirmation, reminder, cancellation, no show and the refund of a deposit.
3. Draft the email and text reminders and run each one against the CAN-SPAM, TCPA and HIPAA points that the reminder touches.
4. Add the consent record the business has to keep for a text reminder, and the STOP keyword handling that goes with it.
5. Mark the state-specific items, such as a paid sick leave note or a deposit rule, for the owner's attorney to confirm.

Output contract:

- policy - the booking, reminder, cancellation, no show and deposit rules in customer order
- reminder_templates - the email and text copy with the required disclosures and the opt-out wording in place
- consent_record - what the business has to capture and keep before a text reminder goes out
- fee_schedule - the cancellation and no show amounts, each marked for approval before use
- state_items - the rules that change by state, listed for the owner or counsel to confirm

## US specifics that matter

- The CAN-SPAM Act (15 USC 7701 to 7713) covers commercial email and requires a valid physical postal address and a working opt-out, and the sender has to honor the opt-out within 10 business days.
- The TCPA and the FCC rules (47 USC 227 and 47 CFR 64.1200) require prior express consent for marketing text messages sent with an autodialer, and a written consent record for a telemarketing text.
- A consumer can revoke consent at any time in any reasonable way, and 47 CFR 64.1200(a)(10) stops all messages to that number, so a reminder program needs STOP handling and a suppression list.
- Florida's Telephone Solicitation Act (Fla. Stat. 501.059) requires prior express written consent for automated calls and texts, and Oklahoma's Telephone Solicitation Act of 2022 (15 OK Stat. 775C) and Washington law add their own consent and registration rules, so the state text rules differ.
- The FTC Cooling-Off Rule (16 CFR part 429) gives a three-day right to cancel certain sales made away from the seller's place of business, but it does not cover every service appointment.
- The HIPAA Privacy Rule (45 CFR part 164) allows appointment reminders when the information stays to the minimum necessary and carries no clinical detail, so a reminder template holds no diagnosis.
- Numbers in the 555-0100 through 555-0199 range are reserved for fictional use, so a sample phone number in a policy template has to come from that range.

## Guardrails (hard rules)

- Never send a reminder, a confirmation or a no-show notice; the business sends the message from its own system.
- Never put a customer name, phone number, email address or appointment detail into a shared policy or checklist file.
- Never quote a cancellation fee, a deposit amount or a waiver the business has not approved, and never waive one for a customer.
- Never present the policy as legal advice or as a final legal document; it is a draft for the owner and for state counsel.

## Quickstart

### 1. Fill in the brief

`templates/appointment-policy.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_reminder_copy.py --input appointment-policy.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/appointment-and-reminder-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Email reminders under CAN-SPAM**

- A commercial email has to identify the sender and include a valid physical postal address.
- The opt-out has to be clear, and the sender has 10 business days to honor it.
- A message about an existing appointment is usually transactional, but a message that also markets a service is not.
- Keep the address and the sender details in the template footer, not in a signature line that gets cut.

**Text messages and consent**

- Marketing texts need prior express consent, and a telemarketing text needs a written consent record under 47 CFR 64.1200.
- A STOP reply stops every message to that number, so the suppression list is part of the process.
- Florida (Fla. Stat. 501.059), Oklahoma (15 OK Stat. 775C) and Washington each set their own consent and registration rules.
- An appointment reminder and a marketing text are treated differently, so keep them in separate campaigns.

**Cancellation, deposits and no shows**

- A cancellation fee is a contract term, and the policy has to say how much, when it applies and how it is waived.
- The FTC Cooling-Off Rule (16 CFR part 429) gives three days to cancel certain sales made away from the seller's location, which is not the same as a no-show fee.
- Some states and cities require paid sick leave or set a different fee for a missed appointment, so those go in the state items list.
- A fee the business has not approved never belongs in a customer-facing draft.

**Privacy limits on what a reminder says**

- Under HIPAA (45 CFR part 164) a reminder stays to the minimum necessary and carries no clinical detail.
- Use the 555-0100 to 555-0199 range for sample numbers so a template is not mistaken for a live contact.
- Never copy a real customer's details into an example; use the appointment type and the time only.
- Keep the policy, the templates and the consent records in the business's own system and not in a shared document.

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
- `references/appointment-and-reminder-rules.md` - US appointment, reminder and cancellation rules
- `templates/appointment-policy.yaml` - the brief to fill in
- `scripts/lint_reminder_copy.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_reminder_copy.py --input appointment-policy.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
