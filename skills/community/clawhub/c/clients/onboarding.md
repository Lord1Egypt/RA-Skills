# Onboarding — From Signature to Working

Scope: the two weeks that decide whether the engagement is calm or expensive. Includes procurement, vendor portals and security questionnaires, which are their own mini-project. Running the work afterwards is `delivery.md`; who the people are is `stakeholders.md`.

Read the roster row, the signed scope, and any `artifacts/onboarding-*.md` from a similar client before starting — most of this checklist is reusable and only the client-specific rows change.

**Contents:** [The Order](#the-order) · [The Onboarding Checklist](#the-onboarding-checklist) · [The Working Agreement](#the-working-agreement) · [Access, and Where Credentials Do Not Go](#access-and-where-credentials-do-not-go) · [The Kickoff Meeting](#the-kickoff-meeting) · [Procurement and Vendor Onboarding](#procurement-and-vendor-onboarding) · [Security Questionnaires and Insurance](#security-questionnaires-and-insurance) · [The First Week](#the-first-week)

## The Order

Deposit → paper → access → kickoff → work. Every inversion has a standard failure:

- Work before deposit: the deposit becomes negotiable, and the first invoice becomes a conversation.
- Kickoff before access: the meeting produces a to-do list of things you cannot start.
- Work before the working agreement: the channel and the revision count get set by whoever asks first, and it is never you.

The exception is a paid discovery, which is itself the onboarding for the larger engagement.

## The Onboarding Checklist

Reusable; save the client-specific version to `artifacts/onboarding-<client>.md` the first time you run it.

| Item | Done when |
|---|---|
| Signed scope or agreement on file | You have the countersigned copy, not "it's with legal" |
| Deposit received | Cleared, not "sent" |
| Invoicing details captured | Legal entity name, billing address, VAT or registration number, PO number if required, AP email, portal if they use one |
| Named approver confirmed in writing | One person, with their limit; escalation path above it (`stakeholders.md`) |
| Channel agreed | Where requests arrive, where decisions get confirmed, response expectations both ways |
| Access provisioned and tested | You have logged in successfully to each system — untested access is not access |
| Calendar set | Kickoff, status day, milestone reviews, and the client's blackout periods |
| Their obligations dated | Content, assets, feedback windows, decisions — each with an owner and a date |
| Definition of done agreed | What the client will look at to accept each deliverable |
| Emergency path | Who to contact when something breaks outside hours, and whether that is even in scope |

Anything unchecked after the kickoff is a risk item stated in the first status note, not a private worry.

## The Working Agreement

Half a page, sent in the kickoff follow-up email, not buried in the contract. It is the cheapest scope-creep prevention that exists because it is short enough to be read.

- **Where requests go**, and what happens to requests that arrive elsewhere: they get moved there before being actioned. Say it once, then do it silently.
- **Response times**, in both directions. Yours, and theirs for feedback and approvals.
- **Revision rounds** per deliverable, and what a round is: one consolidated set of feedback from all stakeholders, not comments arriving over two weeks.
- **What counts as out of scope**, in their language, with the change-order path (`scope.md`).
- **Meeting rhythm and length**, and that meetings without an agenda get rescheduled.
- **Working hours**, including whether out-of-hours contact is answered at all.
- **How decisions are recorded**: written back the same day, silence against a dated restatement counts as agreement (SKILL.md Rule 7).

Write it once as a template, reuse it, and keep the client-specific version in `roster/<client-slug>.md`.

## Access, and Where Credentials Do Not Go

Clients hand over logins in a single email, in plain text, at exactly this moment. It is the highest-risk five minutes in the whole relationship.

- **Ask for access, not credentials**: a named account for you in their system, with the permissions the work needs, is better for both sides than a shared password. It also survives your departure cleanly.
- Where a shared credential is unavoidable, it goes to the user's password manager and **only a pointer is written into any Clawic file**: `1password:Clients/Acme/wp-admin`, `keychain:acme-sftp`, `env:ACME_API_TOKEN`. Never the value, in any file, including one the user pastes and asks you to keep.
- Request the least access that lets the work happen, and say so — it reads as professional and it shrinks what you are liable for.
- **Record what you have in the client's `roster/<client-slug>.md`**, not what it unlocks: system, account name, who granted it, date, and the credential pointer where there is one. That list is what offboarding revokes (`offboarding.md`), and an unrecorded access is one that stays live for years.
- Test every credential the day you get it. Discovering on day nine that the staging login never worked costs a week and looks like your delay.

## The Kickoff Meeting

Sixty minutes, agenda sent in advance, and it is a working meeting rather than a welcome.

1. **Confirm the outcome in one sentence** and get the approver to say it back. Divergence here is common and cheap to fix now.
2. **Walk the timeline**, including their obligations with dates. Say out loud what happens if a feedback window is missed — the deadline moves by at least the delay.
3. **Confirm who decides**, in the room, with their limit. If the approver is absent from kickoff, that is your first Warning Signal.
4. **Agree the working agreement** and send it in the follow-up.
5. **Name the risks you already see**, in one line each. Raising a risk on day one is competence; raising it in week six is an excuse.
6. **End with three dated next steps**, each with an owner.

Send the recap the same day. Not minutes — decisions, owners, dates, and anything you are waiting on.

## Procurement and Vendor Onboarding

In organisations above roughly 200 people, being chosen and being able to be paid are separate projects. Treat procurement as its own workstream with its own dates:

- **Ask at proposal stage** whether vendor onboarding is required and how long it took the last supplier. The answer is routinely 2-8 weeks, and it delays *first payment*, not first work — which is exactly the trap.
- Typical requirements: W-9 or local tax form, proof of insurance, bank details submitted through their portal, a supplier code of conduct, sometimes a security review, occasionally a diversity or modern-slavery declaration.
- **No PO, no invoice.** Many enterprises will not pay an invoice without a purchase-order number on it, and will not raise the PO retroactively. Get the PO number before starting and put it in the roster row.
- Portals (Ariba, Coupa, and the client's own) require an account and reject invoices for formatting reasons that are never explained. Submit the first invoice early and small, to discover the rejection while it does not matter.
- **Do not do meaningful work before the PO exists** unless the amount is one you can afford to lose. This is the single most common way experienced freelancers lose five figures to an organisation that fully intended to pay.
- Keep the completed answer set in `artifacts/procurement-<client>.md` — the next enterprise asks 80% of the same questions.

## Security Questionnaires and Insurance

- Questionnaires (a spreadsheet of 60-300 controls, sometimes a SIG or CAIQ) arrive late and are treated as a formality until they block signature. Answer honestly; "not applicable, we do not process that data" is a valid and common answer for a small supplier.
- Build the answer set once and keep it in `artifacts/security-questionnaire.md`, with every credential, endpoint and internal hostname stripped to pointers. Reuse cuts the second one from days to hours.
- Common blockers worth pre-empting: professional indemnity and public liability insurance at a stated level, a written data-processing agreement where personal data is involved, named subprocessors, a breach-notification commitment, and multi-factor authentication on your own accounts.
- If a control genuinely does not exist, say what compensates for it rather than claiming it. A false yes on a questionnaire is a contractual misrepresentation.

## The First Week

- Deliver something visible in the first week, even if small. It converts the client's anxiety into confidence and buys patience for the slow middle.
- Send the first status note on the agreed day, even if the answer is "on track, nothing needed from you". The pattern matters more than the content.
- Watch for the first out-of-channel request and the first out-of-scope ask. Both arrive early, and how the first one is handled sets the rest of the engagement (`scope.md`).

**Write before you move on:** the roster row gets terms, channel, approver, PO number and start date; every person met goes to `~/Clawic/data/contacts/contacts.md` as one row keyed by their email; the engagement gets its file at `~/Clawic/data/projects/<project>.md` with milestones and the client named as a pointer; the working agreement, approval chain and quirks go to `roster/<client-slug>.md`, and so does the access list — one line per system with account name, granter, date and credential pointer, never a value; the completed checklist, procurement answers and questionnaire go to `artifacts/` with their `## Boxes` lines; kickoff decisions go to `contact-log/<client-slug>.md` and the project's decisions table; the status day, invoicing day and any renewal date go to `## Due`.
