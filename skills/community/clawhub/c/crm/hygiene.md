# Hygiene — Duplicates, Decay, and Trusting the Database Again

A CRM dies of two diseases: nobody updates it, and nobody believes it. This file treats the second. The measurement is not "does it look clean" — it is the fill rate, the duplicate count, and the bounce rate, written down with a date.

**Contents:** [The Monthly Sweep](#the-monthly-sweep) · [Deduplication](#deduplication) · [Merge Order](#merge-order) · [Bounces](#bounces) · [Decay](#decay) · [Validation At Entry](#validation-at-entry) · [Auditing An Inherited CRM](#auditing-an-inherited-crm) · [Archive, Never Hard Delete](#archive-never-hard-delete) · [Measuring Health](#measuring-health)

**Before any cleanup**, read `## Data Health` in `~/Clawic/data/crm/memory.md` for the last pass and its counts, and write a dated export first (SKILL.md Rule 9). No merge is reversible in most tools.

## The Monthly Sweep

Thirty minutes, once a month, in this order — cheapest signal first, most destructive action last:

1. **Counts.** Total records, created since last pass, records with no interaction ever. A CRM growing faster than its interaction log is a list, not a CRM.
2. **Bounces.** Retire hard bounces, suppress, note the count.
3. **Duplicates.** Exact-email pass, then domain-plus-name pass. Merge the exact matches, queue the fuzzy ones.
4. **Fill rates.** Any field under ~70% goes to the delete-or-require decision (`schema.md`).
5. **Tag vocabulary.** Merge synonyms, delete tags used once.
6. **Stale records.** No interaction in two years and no deal ever → archive.
7. **Orphans.** Deals with no contact, interactions with no contact id, organizations with no people.

Write the pass into `## Data Health` with its counts and the date into `## Due`. "We cleaned it up" without numbers cannot be compared to the next pass, which is the only way to know whether the cleaning is winning.

## Deduplication

Run in this order. Each pass is cheaper and safer than the next; never start with fuzzy matching.

| Pass | Rule | Action |
|---|---|---|
| 1. Exact email | Same lowercased address | Auto-merge |
| 2. Normalized email | Gmail-family dot removal; `+tag` stripped **only when the base address already exists as a record** | Auto-merge |
| 3. Same domain + same name | Identical normalized name at the same company domain | Auto-merge |
| 4. Same domain + similar name | Name similarity above ~0.9 (Levenshtein ratio, or first-initial-plus-surname match) at the same domain | Human list |
| 5. No email | Name plus phone in E.164, or name plus organization | Human list, never auto |
| Anything else | — | Leave it. A missed duplicate costs one awkward email; a wrong merge destroys two histories |

Normalization rules that must not be over-applied: **dots are significant everywhere except Gmail** and its hosted domains — stripping them globally merges two real people. `+tags` are significant at some providers as separate mailboxes, which is why pass 2 requires the base address to exist. Nicknames (Bob/Robert, Paco/Francisco) are a human decision, never a rule.

Organizations dedupe on **domain**, never display name (`schema.md`).

## Merge Order

The trap is merging into the newest record — the newest is usually the emptiest, because the import that created it had three columns.

1. **Survivor = the richest record**, measured by filled fields; ties break toward the oldest `created` date, so provenance survives.
2. **Field by field, non-empty wins.** Where both are non-empty and differ, the *more recently confirmed* value wins — confirmed by an interaction, not by an import.
3. **Union the collections**: tags, emails, phones, interactions, deals. Never drop the loser's interaction history; it is the part that cannot be reconstructed.
4. **Keep both external ids** (`hubspot_id`, `sheet_row`) so a later re-sync does not resurrect the duplicate.
5. **Record the merge**: date, the two ids, the survivor. Without it, the third copy that arrives next quarter looks like a new person.
6. **Never auto-merge across organizations.** Two people with the same name at two companies is normal; one merged record is unrecoverable.

## Bounces

- **A hard bounce (permanent, 5.x.x: mailbox does not exist, domain does not resolve) retires the address on the first occurrence.** Add the address to `do-not-contact.md` with source `hard bounce`, clear it from the record's `email` field, and keep the person. The person is still real; only the address died — usually because they changed jobs, which makes them a trigger event rather than a loss (`followup.md`).
- **Soft bounces (transient, 4.x.x: mailbox full, server unavailable)** retire after three consecutive failures across separate sends. One is weather.
- **A spam complaint is a hard opt-out**, scope `all`, immediately and permanently — never re-add on any later import.
- **A bounce rate above ~2% on a send means the list is stale, not that the tool is broken.** The fix is a dedupe and decay pass before the next send, not a different sending domain.
- Never re-verify a dead address by sending to it again; that is what damages sending reputation.

## Decay

Contact data rots because people move. Do not guess a rate — **measure your own**: the bounce rate of your next broad send is your decay rate since the last one, and it is the only number that describes your list.

| Signal of decay | Detected by | Response |
|---|---|---|
| Job change | Bounce, an out-of-office naming a successor, a public profile update | New organization record; old company keeps the vacancy as an opportunity |
| Company died or was acquired | Domain does not resolve, redirect to another brand | Merge organizations, keep both domains |
| Role change inside the company | Signature change, a reply from a new address | Update role; re-qualify the deal, since the budget may have moved with them |
| Relationship went cold | No inbound in a year | Demote the `Tier` cell in `## People`, do not delete the record (`followup.md`) |

An out-of-office that names a replacement is the highest-value bounce you will ever get: it hands you the new contact and the reason to write to them.

## Validation At Entry

Cheaper than any cleanup. Enforce at creation, in the tool or in the import:

- Email syntactically valid and lowercased; domain resolves (MX check) for anything that will be mailed in bulk.
- Phone in E.164 or empty — never a half-formatted string.
- Dates ISO, values numeric with a currency, enums from the closed list.
- **Duplicate check before insert**, on the identity key — the single control that prevents most of the work in this file.
- Required fields at creation: email (or a documented reason there is none), source, owner, next step. Four fields is the ceiling for what a human will fill while on a call.

## Auditing An Inherited CRM

Never start by cleaning. Start by measuring, because the counts decide whether cleaning or restarting is cheaper.

1. **Counts**: records, records with an interaction ever, records touched in the last year, open deals, deals with a close date in the past. The last number is usually the most revealing.
2. **Fill rates per field.** Fields under ~30% are the previous owner's abandoned process; do not adopt them.
3. **Duplicate estimate**: distinct lowercased emails ÷ total records. Below ~0.9 there is a systemic import problem, not a cleanup problem.
4. **The stage distribution**: a pipeline with most deals sitting in one middle stage means stages were never exited, and every conversion number in the tool is meaningless.
5. **The suppression state**: is there an opt-out list at all, and was it applied? If not, that is the first thing to build, before anything is sent (`privacy.md`).
6. **Decide the boundary**: keep the records with a real interaction history; archive the rest to a file rather than importing them into whatever comes next. Importing 4,000 unqualified rows into a fresh CRM reproduces the disease on day one (`import.md`).

Write the audit into `## Data Health` and, when it drove a keep/archive boundary, into `artifacts/crm-audit-<date-free-name>.md` — name it for what it decided, not for when it ran (`memory-template.md`).

## Archive, Never Hard Delete

- Default posture: archive (a flag, or a move to an archive file), keeping the record findable. Most "delete this contact" requests mean "get it out of my working list".
- **Hard delete only for a legal erasure request** (`privacy.md`) or a genuine junk record, and the suppression entry survives the deletion.
- Archived records are excluded from counts, lists and reports by default; if the tool cannot exclude them, the archive is a separate file, not a tag.
- Junk that deserves immediate deletion: test records, form spam, role addresses you will never write to (`noreply@`, `postmaster@`).

## Measuring Health

Four numbers, monthly, in `## Data Health`. Trends matter; absolutes do not.

| Metric | Formula | Direction |
|---|---|---|
| Duplicate ratio | distinct identity keys ÷ total records | Toward 1.0 |
| Coverage of the identity key | records with an email ÷ total | Toward 1.0 |
| Interaction coverage | records with ≥1 interaction ÷ total | Up; if it falls, the CRM is becoming a list |
| Field fill rate | filled ÷ total, per required field | ≥70%, or the field goes (`schema.md`) |

**Write every sweep result into `## Data Health`** in `~/Clawic/data/crm/memory.md` with counts and the date, add retired addresses to `do-not-contact.md`, delete removed people from the shared `~/Clawic/data/contacts/contacts.md`, and stamp `## Due` (`memory-template.md`). A hygiene pass whose numbers were not written is a pass that will be argued about next month.
