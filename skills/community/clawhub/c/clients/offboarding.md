# Offboarding — Ending an Engagement

Scope: closing out cleanly, whether the ending is a success, a pause, or a firing. Getting the next thing out of it is `retention.md`; the decision to end a bad relationship is `difficult-clients.md`.

Read the project file at `~/Clawic/data/projects/<project>.md`, the access list in `roster/<client-slug>.md`, and `## Receivables` before starting a handover — the two things that go wrong are unrevoked access and an unpaid balance, and both are in the record.

**Contents:** [The Closing Sequence](#the-closing-sequence) · [The Handover Pack](#the-handover-pack) · [Access, Both Directions](#access-both-directions) · [Final Invoice](#final-invoice) · [Endings That Are Pauses](#endings-that-are-pauses) · [Cancellations Mid-Project](#cancellations-mid-project) · [The Post-Mortem](#the-post-mortem) · [What to Keep, and For How Long](#what-to-keep-and-for-how-long)

## The Closing Sequence

Order matters, and every inversion has a cost:

1. **Confirm the end date in writing**, with what will be delivered before it.
2. **Final invoice raised** for everything outstanding, including work in progress and any approved change orders — before the handover is delivered, not after.
3. **Handover pack** written and delivered.
4. **Walkthrough call**, 30 minutes, recorded or summarised. A pack nobody was walked through gets three months of unpaid questions.
5. **Access revoked**, both directions.
6. **Testimonial and referral asked for**, at the walkthrough, while the value is visible (`retention.md`).
7. **Re-contact date set** in `## Due`.
8. **Post-mortem written**, and the roster row closed.

The frequent inversion is delivering everything and invoicing afterwards. Final deliverables are the only leverage remaining at the end of an engagement; spend them on payment, not on goodwill you already have.

## The Handover Pack

One document, at `artifacts/handover-<client>.md`, written for the person who will inherit this — usually someone less familiar with it than the client contact.

| Section | Content |
|---|---|
| What exists now | The current state in plain language, plus where each thing lives |
| How to run it | The routine operations, step by step, at the reader's level and not yours |
| Credentials | **Pointers only** — system, account name, and where the secret lives (`1password:Clients/Acme/wp-admin`). Never a value, in this file or any other |
| Decisions and why | The three or four choices a successor would otherwise reverse, each with its reason |
| Known issues | What is unfinished, what is fragile, what you would do next — honestly |
| Dependencies | Third-party services, licences, renewal dates and who holds each account |
| Contacts | Who at their end knows what; anyone external who was involved |
| What is not included | The support that ends with the engagement, and what it costs to buy (`pricing.md`) |

Write it as the engagement runs, not at the end. Retrofitting a handover from memory takes a day and misses the things only you knew, which are exactly the things worth writing down.

## Access, Both Directions

- **Theirs to you**: ask them to disable your accounts, and confirm in writing that you have asked. Access you still hold to a former client's systems is a liability with no upside, and it is the finding that appears in their next security review.
- **Yours to them**: transfer ownership of anything in your accounts that is theirs — domains, repositories, ad accounts, analytics properties, design files, DNS. Do this before the last day, because ownership transfers frequently need both sides to act while both are still engaged.
- **Delete the credential pointers** from `roster/<client-slug>.md` when access ends, and remove the actual secrets from the user's password manager or move them to an archived vault. The pointer surviving the access is how a stale credential lives for years.
- **Licences and subscriptions bought in your name** for their work get transferred or cancelled on a named date, and the date goes in `## Due`. A subscription nobody cancelled is a small recurring donation.
- Confirm the whole revocation list in one closing email. It reads as professional and it is the record if anything is questioned later.

## Final Invoice

- Raise it against the agreed schedule, not against goodwill. "I'll invoice once everything settles" is how a final invoice reaches 90 days.
- Include approved change orders, expenses with receipts, and any cancellation amount owed under the agreement.
- If a balance remains unpaid at the end date, the ladder applies unchanged (`getting-paid.md`). Endings do not suspend rungs; the relationship being over is precisely why the schedule has to be mechanical.
- Where the contract allows it, final deliverables transfer on final payment, and that was stated in the proposal so it is a known term rather than a surprise.
- Note the intellectual-property and licence position in the closing email — what they own, what they license, what you may show in a portfolio. This is the cheapest moment to settle it and an expensive one to leave ambiguous (`contract`).

## Endings That Are Pauses

Most "endings" are pauses that nobody labelled, which is why they turn into silence:

- **Name it as a pause with a date**: "let's stop here and pick up in October when the budget resets" is a much better ending than a project that trails off.
- Do the full handover anyway. A pause with no handover becomes an unpaid support obligation.
- Put the re-contact date in `## Due` and set the roster status to `paused` with the reason in the row.
- Keep the access question honest: if they want you back in three months, ask whether it is cheaper to keep a dormant account than to re-provision. Usually it is not, and the security answer is clear.

## Cancellations Mid-Project

- **Invoice work completed plus the current phase**, per the cancellation term in the proposal. If nothing was written, work completed plus notice is the defensible position.
- **Deliver what has been paid for.** Withholding paid work converts a cancellation into a dispute you will not win.
- **Find out why, once, without arguing.** Budget cuts, a reorg, or a change of direction are the usual causes and none of them are about you; if it is about you, this is the only chance to learn it (`retention.md`).
- **Cancellation for cause on your side** — non-payment, abuse, illegality — follows the exit procedure in `difficult-clients.md`, in that order, with the invoice first.

## The Post-Mortem

Twenty minutes, to `artifacts/postmortem-<client>.md`, on every engagement over a certain size. It is the only mechanism by which the user's practice actually improves.

```markdown
# Post-mortem — Acme, 2026 rebrand
*Read before quoting anything like this again, and before any win-back.*

Sold: 25,000 EUR fixed, 12 weeks.
Delivered: 14 weeks, 25,000 EUR plus a 5,000 EUR change order.
Effective rate: 25,000 + 5,000 over 240 hours = 125 EUR/h against a 150 EUR/h target.
Where the hours went: 38 outside scope, 22 of them billed.
First signal, and how early: approvals slowed in week 3, three weeks before the date slipped.
What worked: consolidated feedback rounds; the change order that moved the date with the price.
Do differently: quantify "brand guidelines" in the scope; deposit per phase, not per project.
Would take again: yes, at 30,000 EUR.
```

The last line is the one that matters. Recorded at the end of every engagement, it turns into a pricing model within a year.

## What to Keep, and For How Long

- **Keep**: the roster row, the closed project file, the contact log, the handover, the post-mortem, revenue lines, and any consented case study. This is the corpus that answers "what do I charge for this" and "who do I know who needs this".
- **Delete**: credential pointers whose access has ended, and any client material you are contractually required to return or destroy — check the agreement, because confidentiality obligations routinely outlast the engagement.
- **Do not delete the client's row when they leave.** A past client is the highest-converting lead source there is (`retention.md`), and the row is what makes the re-contact possible.
- Personal data about their staff is kept only while it has a purpose. When a contact leaves, their row goes (`contacts/`, protocol in `memory-template.md`).

**Write before you move on:** the roster row moves to `past`, `paused` or `fired` with the end date and a one-line reason; the project file gets `status: closed` and its close date, and is kept, not deleted; the handover goes to `artifacts/handover-<client>.md` and the post-mortem to `artifacts/postmortem-<client>.md`, each with its `## Boxes` line in the same turn; the final invoice appears in `## Receivables` until paid, then moves to `revenue/<year>.md`; the re-contact date, any licence cancellation date and any surviving obligation go to `## Due`; credential pointers for ended access are deleted from `roster/<client-slug>.md`; departed contacts are removed from `~/Clawic/data/contacts/contacts.md` with the date noted in `memory.md`.
