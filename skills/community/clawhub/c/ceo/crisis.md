# Crisis — The First 24 Hours, By Type

A crisis is any event where the cost of a slow decision exceeds the cost of a wrong one. The generic moves are below; the per-type playbooks are what actually differ.

## The Universal First Three

1. **Name the clock.** What forces the deadline — cash, a regulator, a journalist's deadline, a customer's board meeting? Every crisis has one, and until you name it you will optimize the wrong thing.
2. **Assign one decision-maker and one scribe.** Committees dissolve in crisis. The scribe timestamps every fact learned and every decision made; you will need that timeline for the board, counsel, or the post-mortem, and reconstructing it later is how people misremember themselves into trouble.
3. **Separate facts from inferences in writing** before you communicate anything. Every crisis that got worse in public did so by asserting an inference that later turned out false.

Then set a cadence: internal sync every 4 hours on day one, daily by day three. A crisis without a cadence becomes a permanent state.

## Cash Crisis

1. Freeze: no new hires, no new vendors, no discretionary spend, all POs through you. Same day, before the plan exists.
2. Get the real number: cash in bank, committed payables, payroll dates for the next 90 days. Collections chased personally — a receivable is cash that already exists.
3. Compute the bear case (revenue flat, nothing new closes) and size the cut to hold months-to-milestone + 6 (SKILL.md rule 5). Cut once (→ SKILL.md Quick Reference: layoffs).
4. Call the two investors most likely to bridge before you call anyone else — insider willingness is the market signal, and if they decline you have your answer about the priced round too (→ SKILL.md Quick Reference: fundraising).
5. Payroll and payroll taxes are not a lever. Missing payroll converts a business problem into a personal-liability problem for officers and ends the company's ability to hire again (→ SKILL.md Quick Reference: shutdown).
6. Tell the board before the cut is designed, not after — a board that learns of a cash cliff at the meeting stops advising and starts governing.

## Security Breach / Data Incident

1. Contain before you diagnose: rotate credentials, revoke sessions and tokens, isolate the affected system. Preserve logs and images first — containment that destroys evidence costs you the investigation.
2. Engage counsel early, and route the technical investigation through counsel where privilege is available; get the forensics firm in the same call.
3. Notification clocks are legal, not editorial: the EU GDPR requires notifying the supervisory authority within 72 hours of becoming aware (Art. 33); US state breach laws, sector rules, and enterprise contracts each impose their own, and customer contracts are often stricter than statute. Pull the actual clauses from your top contracts on day one.
4. Communicate what is confirmed, when it was confirmed, what customers should do, and when the next update lands. Never estimate the record count out loud before forensics does.
5. The follow-through is the reputation event: publish the root cause and the systemic fix. Silence after the incident reads as concealment (→ SKILL.md Quick Reference: communication).

## Executive Misconduct or Fraud

1. Do not investigate it yourself. Notify the board chair or audit committee, retain independent counsel, preserve documents and issue a litigation hold.
2. Suspend access — systems, banking, signing authority — before the conversation, not after.
3. Assume the person will contact employees, customers, or investors. Decide the internal message before the rumor does.
4. Where money moved: separate the personnel question from the recovery question and from the disclosure question. They have different deadlines and different audiences (investors, insurer, bank, auditor).
5. Do not settle quietly to avoid embarrassment when the conduct affected employees; a suppressed pattern surfaces later at ten times the cost.

## Outage / Product Failure

1. Status page inside 30 minutes, updated on a fixed interval even when there is nothing new — the interval is the message.
2. One voice externally, one incident commander internally, engineering left alone to fix it.
3. Customer-impact list first, root cause second. Your top accounts hear from a human, not from the status page.
4. Credits and SLA: apply them proactively before customers ask; the ones who ask were already leaving.
5. Post-mortem published to affected customers within a week: timeline, cause, what changes. Blameless internally, specific externally.

## Key Person Leaves or Is Incapacitated

1. Name an interim owner the same day, in writing, with decision authority — ambiguity here is what causes second and third departures.
2. Knowledge transfer while you have goodwill: credentials, in-flight commitments, relationships, the undocumented things.
3. Tell the team before the market does, and tell them who to go to now. Tell customers who own the relationship yourself.
4. Then decide interim-versus-search deliberately (→ SKILL.md Quick Reference: people); a rushed exec hire in a shaken org is the classic double failure.
5. Prevention has a name: no single person holds the only copy of a credential, a customer relationship, or a critical system's knowledge. Audit the bus factor quarterly.

## Press / Public Attack

1. Verify the claim before you respond to it. Half of crises are a true fact framed badly, which is a very different response from a false claim.
2. One spokesperson, one written line, no improvisation. Every employee gets the line and the instruction to forward inquiries.
3. Correct facts, do not fight framing. Arguing framing extends the story by a news cycle; new facts end it.
4. Respond where the audience is, not where the attack is; a thread does not require a press release.
5. Employees and customers hear from you before or at the same time as the public — never after (→ SKILL.md Quick Reference: communication).

## Losing the Largest Customer

1. Get the real reason within 48 hours from the economic buyer, not from your champion, and not from the account manager who wants it to be price.
2. Save attempt or dignified exit — decide fast. A save that costs a roadmap quarter and a 40% discount is often a loss with extra steps (→ SKILL.md Quick Reference: customers).
3. Re-run the plan without them: revenue, runway, the covenant or milestone they were carrying. This is a board notification, immediately.
4. Then fix the concentration, not just the account.

## Regulatory Inquiry or Legal Demand

1. Litigation hold first: suspend deletion policies company-wide, in writing, the day you learn of it.
2. Single point of contact; no employee responds directly. Instruct the team not to speculate in writing — internal messages are discoverable, and a joke becomes evidence.
3. Distinguish inquiry from action; do not volunteer scope. Answer what is asked, completely and accurately.
4. Notify insurers (D&O, cyber) within the policy's notice window — late notice voids coverage more often than the claim itself fails (→ SKILL.md Quick Reference: governance).

## Crisis Principles

- The team mirrors your demeanor — move fast, never visibly panic; do the panicking with your confidants (→ SKILL.md Quick Reference: ceo-operating-system).
- Communicate more than feels necessary; silence creates a rumor vacuum, and the rumor is always worse than the fact.
- Deal with the cash crisis first regardless of what else is burning: cash converts any other crisis into a fatal one.
- One decision-maker, stated by name, for the duration.
- Document everything contemporaneously; memory reorganizes itself in your favor within a week.
- Set the exit condition when you enter: what has to be true for this to stop being run as a crisis. Wartime mode with no declared end erodes the team faster than the crisis did (SKILL.md rule 8).
