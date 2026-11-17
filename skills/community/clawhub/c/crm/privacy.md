# Privacy — Consent, Suppression, Deletion, Retention

A CRM is a database of other people's personal data held for a commercial purpose. That is the highest-obligation category of data most small operations hold, and the obligations are procedural: they are met by having a suppression list, a retention rule, and a deletion procedure that reaches every copy.

This file gives the operating procedures. Where a situation is in the Red Flags table, it stops being an operating question and goes to a lawyer.

**Contents:** [Lawful Basis](#lawful-basis) · [What Not To Store](#what-not-to-store) · [Suppression Before Deletion](#suppression-before-deletion) · [Handling A Request](#handling-a-request) · [Every Copy](#every-copy) · [Retention](#retention) · [Purchased Lists And Enrichment](#purchased-lists-and-enrichment) · [Vendors And Transfers](#vendors-and-transfers) · [Red Flags](#red-flags)

**Before any bulk contact, import, or deletion**, read `do-not-contact.md` and the `privacy_regime` key in `config.yaml`. Any EU or UK contact makes the GDPR rules apply regardless of what the key says (SKILL.md).

## Lawful Basis

Under GDPR every record needs a basis, stored per row (`schema.md`), because it decides what you may send:

| Basis | Fits | The catch |
|---|---|---|
| **Consent** | Newsletter signups, form fills, event opt-ins | Must be freely given, specific, informed and unambiguous — a pre-ticked box is not consent, and it must be as easy to withdraw as to give |
| **Legitimate interest** | B2B prospecting to a business role, existing-relationship follow-up | Requires a balancing test you can show: your interest, why it is necessary, why it does not override their rights. Untestable = not a basis |
| **Contract** | Clients and their staff, for delivering the work | Ends when the contract does; it never covers marketing |
| **Legal obligation** | Invoices, tax records | Keeps the record alive after an erasure request — this is why financial data survives deletion |

Two rules that hold regardless of basis: the **right to object to direct marketing is absolute** — no balancing test, no exceptions, act on it immediately; and **the basis must be recorded before the first send**, because reconstructing it afterwards is not possible.

Under CAN-SPAM (US), prior consent is not required for commercial email, but a working unsubscribe honored within 10 business days, a valid physical postal address, and non-deceptive headers and subject lines are. Under CCPA/CPRA (California), the obligations are notice at collection, deletion on request, and an opt-out of "sale or sharing" — which includes handing a contact list to some ad platforms.

## What Not To Store

The privacy discipline that costs nothing is not collecting the row in the first place.

- **Never**: national id numbers, payment card data, bank details, health information mentioned in passing, anything about a contact's protected characteristics. None of it makes a follow-up better; all of it raises the cost of a breach by an order of magnitude (`memory-template.md`).
- **Avoid**: personal (non-work) email addresses and personal phone numbers where a work channel exists — they are the highest-risk field in a B2B CRM and the hardest to justify under legitimate interest.
- **Careful**: subjective notes. Write what a person said and what was agreed. "Seemed hungover", "difficult person", "probably underpaid" — an access request obliges you to hand over the record, including that sentence.
- **Fine**: name, work email, role, company, what you discussed, what was agreed, when.

Test before writing a note: **would you send this line to the person it is about?** If not, it does not go in the CRM.

## Suppression Before Deletion

The counter-intuitive rule that prevents the most common failure: **an opt-out must outlive the record it came from.**

Delete the contact and their suppression together, and the next import re-adds them, the next campaign contacts them, and the second complaint is the expensive one. So:

1. Add the identifier to `do-not-contact.md` **first**, with scope and source (`memory-template.md`).
2. Then delete or archive the record.
3. Suppression entries are never removed — only re-scoped if the person opts back in, with a dated note.
4. Where holding the address in the clear is itself the problem, store a one-way hash of the lowercased address and note the algorithm; the check still works, the address is not readable.

The suppression list is read before every outreach, list build, or "who should I contact" answer (SKILL.md Rule 8), which is why it lives in its own file rather than inside `memory.md`.

## Handling A Request

Same procedure for an access, deletion, correction, or objection request. Speed matters: **GDPR gives one month** (extendable by two more for complex cases, with notice); **CCPA gives 45 days** (extendable by 45 with notice).

1. **Log it the day it arrives** — date, identifier, what was asked. The log is the proof it was handled.
2. **Verify the requester** is the person, proportionately — a reply from the address on file is usually enough; do not demand ID as a delaying tactic.
3. **Suppress first** (above).
4. **Enumerate the copies** (next section) before touching anything, so the deletion is one pass rather than four.
5. **Execute**: for access, export their record and interactions in a readable format; for deletion, remove everywhere except what a legal obligation requires you to keep, and say which of those you kept and why.
6. **Confirm in writing**, listing what was done, what was retained and on what basis.
7. **Record the completion** in `do-not-contact.md` (the entry) and `## Data Health` (the pass), with dates.

An objection to marketing needs no verification debate and no delay: suppress on the same day.

## Every Copy

The reason "I deleted the contact" is usually false. Enumerate all of these, once, and keep the list in `## System`:

| Copy | Typical miss |
|---|---|
| The CRM record | — |
| The interaction log | `interactions/<year>.md`, which holds their name and what they said |
| The shared contacts box | `~/Clawic/data/contacts/contacts.md` |
| Exports and backups | `db/backups/` and any CSV downloaded for a report; the biggest and most forgotten copy |
| The mail tool | Sending platforms keep their own contact database; deleting in the CRM does not touch it |
| Enrichment or intent vendors | They hold a copy and are a separate controller or processor |
| Spreadsheets, presentations, a pipeline screenshot in a deck | Personal data leaves the CRM every time someone exports for a meeting |
| Your inbox | Out of scope for CRM deletion, and a reason not to promise more than you can do |

Backups are honored by pruning on the retention schedule, not by surgery inside a backup file — that is the accepted practice, and it works only if the retention window is short and documented.

## Retention

Storage limitation means each category has a defined life, written down and enforced. Defaults worth adopting, all verifiable against your own cycle length:

| Category | Default | Trigger to delete |
|---|---|---|
| Prospect, never engaged | 12-24 months from creation | No interaction in the window |
| Prospect, engaged, no deal | 24 months from last interaction | Annual purge |
| Lost deal | 24-36 months from close | Keeps the win/loss history usable for `metrics.md` |
| Customer | Duration of relationship + the contract/tax period your accountant names | Never earlier than the legal obligation |
| Interaction log | Same as its contact | Deleted with the person |
| Backups and exports | One to two quarters, rolling | Time-based prune, no exceptions |
| Suppression list | Indefinite | Never |

Run the purge annually from `## Due` and note the counts in `## Data Health`. A retention policy nobody executes is worse than none: it is a documented promise that was broken.

## Purchased Lists And Enrichment

- **A purchased list has no consent and usually no defensible legitimate interest for personal addresses.** Under GDPR, contacting people on it is the highest-risk thing a small CRM does; a business role address at a business domain is the defensible end of the spectrum, a personal address is not.
- If a list is used, you still owe **notice at first contact**: who you are, where the data came from, and how to opt out. That is an obligation, not a courtesy.
- **Enrichment vendors** are a processing relationship: you need to know what they hold, and their data becomes yours to defend. Enriching company-level attributes (size, sector, tech) carries a fraction of the risk of enriching personal contact details.
- Scraping a platform that forbids it is a contract problem on top of a data-protection one. Do not.
- **Never import over a suppression flag** (`import.md`). Every import runs against the suppression list first.

## Vendors And Transfers

- Anyone who processes the data on your behalf — the CRM vendor, the mail tool, the enrichment service, a VA — is a processor and needs a data processing agreement. Most vendors publish one; the work is knowing which ones you use.
- Keep a one-page list of them in `artifacts/data-map.md`: vendor, what data, where it sits, DPA link, retention. It is the artifact that answers a customer security questionnaire in ten minutes instead of a week, which is the real reason to keep it.
- Transfers outside the EEA/UK need a mechanism (standard contractual clauses, an adequacy decision). It is the vendor's paperwork, but the obligation is yours.
- A **breach** — an export sent to the wrong person, a shared spreadsheet left public, a stolen laptop with a database on it — has a 72-hour notification clock to the supervisory authority under GDPR. Knowing that number in advance is the point of this line.

## Red Flags

Anything in this table suspends the procedures above: stop, and route to a lawyer or the data protection authority's own guidance before acting.

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Personal data left the CRM to someone who should not have it, or a database is missing | Reportable breach, 72-hour clock running | Contain, document the timeline, take legal advice today — not after the investigation |
| A request cites GDPR/CCPA articles, or arrives from a lawyer | Formal, with deadlines and evidentiary value | Log, acknowledge in writing, take advice before answering substantively |
| The list includes children, patients, or people identified by health, religion, ethnicity, sexuality or political views | Special-category data with a much higher bar | Do not process; do not import; take advice |
| A regulator, an authority, or a complaint reference contacts you | Investigation | Do not delete anything; preserve, then take advice |
| A client asks you to contact a list they will not explain the origin of | You become the sender, and the liability | Refuse until the basis and the notice are documented |
| Deletion is requested but invoices, contracts or a live dispute exist | Competing obligations to keep and to erase | Retain the minimum legally required, erase the rest, document the reasoning |
| Contacts are in a jurisdiction neither you nor `privacy_regime` covers | Unknown local rules (Brazil's LGPD, Canada's CASL, and others differ materially) | Check the local rule before the first send |

**Write in the same turn**: every suppression, opt-out, bounce retirement and completed erasure into `do-not-contact.md` with its date and source; the request and its completion date into `## Data Health`; the retention purge into `## Due`; the vendor map into `artifacts/data-map.md` with its `## Boxes` line (`memory-template.md`). The record of having handled a request correctly is worth as much as having handled it.
