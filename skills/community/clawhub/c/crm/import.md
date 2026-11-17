# Imports, Exports, and Migrating Between Tools

Every import is a write of thousands of records with no undo. Every migration is four imports plus a history that does not travel in a contacts CSV. Both are survivable with the same discipline: export first, map explicitly, dry run, then commit.

**Contents:** [The Import Procedure](#the-import-procedure) · [Field Mapping](#field-mapping) · [CSV Corruption, In Order Of Frequency](#csv-corruption-in-order-of-frequency) · [What To Import And What To Leave](#what-to-import-and-what-to-leave) · [Exports Worth Keeping](#exports-worth-keeping) · [Migrating Between CRMs](#migrating-between-crms) · [Object Order And Id Mapping](#object-order-and-id-mapping) · [Cutover](#cutover) · [API Imports](#api-imports)

**Before any import or migration**, read `## System` in `~/Clawic/data/crm/memory.md` (what the record of truth is), `artifacts/field-dictionary.md` if indexed, and write a dated export to `db/backups/` (SKILL.md Rule 9).

## The Import Procedure

Nine steps. Skipping step 4 is what produces the 4,000-row database nobody trusts.

1. **Export the target first**, dated, to `db/backups/`. This is the rollback.
2. **Read 20 rows of the source by eye**, including the last one. Headers lie; row 4,000 is where the encoding breaks.
3. **Count**: rows, distinct emails, rows with no email. `distinct_emails ÷ rows` below ~0.95 means the source has duplicates you are about to inherit.
4. **Cut the list**: import who you would actually contact this quarter (`hygiene.md`). The rest goes to an archive file, not into the CRM.
5. **Write the mapping** — every source column to a target field, or explicitly to `/dev/null`. Unmapped columns are the ones that arrive as `Custom Field 7`.
6. **Dedupe the source against itself**, then against the target, on the identity key (`hygiene.md`).
7. **Dry run 10 rows.** Open them in the tool. Check dates, accents, currency, and that the enum values landed as values and not as new options.
8. **Import with an `import_batch` tag** carrying the date and source. This is what makes a bad import reversible by filter.
9. **Verify counts** — created, updated, skipped, rejected — and read the rejects. Rejects are silent in most tools and are usually the records you cared about.

## Field Mapping

Write it as a file, not as a UI session, because you will run the import twice.

```markdown
# Import mapping — conference-2026 badge scans → crm
*Read before re-running this import or any similar list. 2026-07-26.*

| Source column | Target field | Transform | Notes |
|---|---|---|---|
| Email Address | email | lowercase, trim | identity key; reject rows without it |
| Full Name | name | trim, collapse spaces | do not split into first/last |
| Company | org | → lookup by domain of email | free-mail domains ⇒ org empty |
| Job Title | role | trim | — |
| — | source | constant `event` | closed list, `schema.md` |
| — | tags | constant `conference-2026` | — |
| — | owner | constant: the user | required field |
| Scanned At | (dropped) | — | badge timestamp is not an interaction |
| Notes | (dropped) | — | 4 of 300 rows had content; handled by hand |
```

Rules: **constants are mappings too** (source, owner, tags — the three that make the batch findable later). A source column with content in under ~2% of rows is handled by hand, not by a field. Anything you drop is written down as dropped, so the next person does not go looking for it.

Save the mapping to `~/Clawic/data/crm/artifacts/import-<source>.md` and index it (`memory-template.md`). Lists from the same source arrive again; deriving the mapping twice is pure waste.

## CSV Corruption, In Order Of Frequency

| Symptom | Cause | Fix |
|---|---|---|
| `Ana Ruíz` → `Ana RuÃ­z` | UTF-8 read as Latin-1, usually via a spreadsheet round-trip | Export as UTF-8, import as UTF-8; never open the file in a spreadsheet in between |
| `03/04/2026` means two different days | Locale date order | Convert to ISO `YYYY-MM-DD` before import, in every source |
| Leading `+` gone from phones, or `6.00123E+11` | Spreadsheet coerced the column to a number | Quote the column as text, or never open the CSV in a spreadsheet |
| Rows shifted by one column | An unescaped comma or newline inside a quoted field | Parse with a real CSV parser, not a split on commas |
| `18.000` becomes 18 | Thousands separator read as a decimal point | Strip separators before parsing; store money as a number plus currency |
| Trailing spaces creating duplicate enum values | No trim | Trim every string column, always |
| Emails uppercase or with display names (`Ana <ana@x.com>`) | Copied from a mail client | Extract the address, lowercase it |
| Every row rejected | BOM on the header line, or a delimiter that is a semicolon | Check the first bytes and the delimiter before debugging anything else |

## What To Import And What To Leave

| Source | Import | Leave |
|---|---|---|
| Old CRM | Contacts with an interaction, all deals, all activity history | Records never touched, dead stages, custom fields under ~30% filled (`hygiene.md`) |
| Email inbox | The people you exchanged replies with | Everyone you ever emailed once — that is an address book, not a CRM |
| Conference list or badge scan | Everyone, tagged with the event, tier C | Their titles as your `role` enum values |
| Purchased list | Nothing before checking lawful basis (`privacy.md`) | Personal email addresses — the highest-risk data you can hold |
| Spreadsheet a colleague maintains | The columns you can define | Their colour coding, which is data you cannot query |
| Form or website signups | All, with consent timestamp and source page | — |

A record without an email, a name, and a reason to exist is not worth a row.

## Exports Worth Keeping

- **Quarterly, all objects, into `db/backups/`** with the date in the filename (`memory-template.md`). This is also the migration prep you will be glad to have.
- Export **contacts, organizations, deals *and* activities** separately, with ids on every object and the foreign keys intact. A contacts-only export is not a backup.
- Check the export opens and has the right row count *the day you make it*. An unverified backup is a belief.
- Prune old exports on the retention schedule (`privacy.md`) — a deletion request that leaves the address in a year of exports has not been honored.

## Migrating Between CRMs

The reason migrations fail is not the contacts. It is the **activity history**, which is what made the old system valuable and what most CSV paths silently drop.

1. **Export everything from the old tool, all objects, before touching the new one.** Include activities and notes even if the new tool cannot import them — a read-only file of history beats no history.
2. **Rebuild the schema in the new tool first**, from `artifacts/field-dictionary.md`, and take the chance to drop the fields under 70% (`schema.md`). Migration is the only cheap moment to delete a field.
3. **Map stages explicitly.** Stage names never match, and an unmapped stage lands in the first one, resetting your entire pipeline to Lead.
4. **Import in dependency order** (below), keeping foreign ids.
5. **Reconcile counts per object** — contacts, orgs, deals, activities — and reconcile pipeline value, which catches the currency and thousands-separator errors that counts do not.
6. **Run both systems for one cycle**, the old one read-only. One cycle means one full sales cycle, not one week.
7. **Decommission**: final export archived, integrations disconnected, tokens revoked, subscription cancelled — in that order. Cancelling first usually costs you the export.

## Object Order And Id Mapping

Import in this order, keeping a lookup table from old id to new id at each step:

`organizations → people → deals → activities`

- Each object carries its **old id in a dedicated field** (`legacy_id`). Without it, the third step cannot attach a deal to the right person and you get orphans that look like data (`schema.md`).
- Activities are last because they reference both people and deals. If the new tool cannot import them, keep the export file, add it to `## Boxes` with the condition "read when history before <date> is needed", and write the *summary* of each active relationship into `interactions/<year>.md` by hand — twenty relationships is an afternoon, and it is the part users regret losing.
- Owners and users must exist in the new tool before the import, or every record lands unassigned.

## Cutover

- Announce the read-only date and the switch date, then honor them. Two live systems for a month means both are wrong.
- Freeze writes to the old system 24 hours before the final export; re-export deltas rather than reconciling by hand.
- The first week after cutover is a hygiene week: run the monthly sweep early, because the import is the biggest single source of duplicates the database will ever see (`hygiene.md`).

## API Imports

When the source has an API, prefer it over CSV: types survive, ids survive, and it is re-runnable.

- **Paginate to exhaustion** and log the cursor; a partial import that looks complete is worse than a failed one.
- **Respect rate limits** with backoff — most CRM APIs throttle per second and per day, and hitting the daily cap mid-migration means finishing tomorrow.
- **Idempotency**: upsert on the identity key, never blind insert. Every retry after a timeout is a duplicate factory.
- **Credentials stay out of everything written** (`memory-template.md`): the token lives in the environment or the OS keychain, and any snippet saved to `artifacts/` carries `<env:CRM_TOKEN>` where the value was.
- Log what ran: object, filter, counts, cursor, date.

**After any import, export or migration**, write to `## Data Health` in `~/Clawic/data/crm/memory.md`: date, source, rows created / updated / skipped / rejected, and the batch tag. Imported people land in the shared `~/Clawic/data/contacts/contacts.md`, and their tier and source in `## People` — count the rows before appending, because an import is the pass most likely to cross a split threshold in one turn. Save the mapping to `artifacts/import-<source>.md` and the migration plan to `artifacts/migration-<from>-to-<to>.md`, each with its `## Boxes` line in the same turn (`memory-template.md`). Update `## System` when the record of truth moved.
