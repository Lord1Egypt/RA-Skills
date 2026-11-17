# Notion Dashboard

Use this reference when creating, updating, or previewing the ALS lead database. Keep one row/page per business entity and preserve the source evidence that led to the record.

## Recommended properties

| Property | Type | Purpose |
|---|---|---|
| Lead | title | Canonical business name |
| Status | select | New capture, Researching, Verified, Outreach queue, Contacted, Replied, Qualified, Not a fit, Do not contact |
| Location | text | Printed or researched location |
| Source images | files or URLs | Original image paths or links |
| Raw capture | text | Important visible text, including ambiguity |
| Offer / observed need | text | What the business advertises and the evidence-based hypothesis |
| General phone | phone | Printed or official main number |
| Direct business phone | phone | Public role-based business number, if verified |
| General email | email | Official business inbox |
| Decision-maker | text | Publicly verified name |
| Role | text | Publicly verified role |
| Professional email | email | Public business/role-based email |
| Website | url | Official site |
| Social profiles | url or text | Official or clearly professional profiles |
| Confidence | select | High, Medium, Low; use the research ledger for detail |
| Evidence | url or text | Direct sources for material claims |
| Last verified | date | Last research date |
| Next action | text | Call, research, draft email, or other next step |
| Notes | text | Conflicts, unresolved questions, and user notes |

Use a stable identity key outside the visible title when the connector supports it:

normalized business name + normalized location + phone or domain

If no stable key is available, compare name, location, phone, website, and source images before creating a new page. Keep possible duplicates visible for review rather than silently merging them.

## Views

- **New captures:** Status = New capture, sorted by capture date.
- **Research queue:** Status = Researching, with unresolved fields visible.
- **Verified contacts:** Status = Verified, filtered to at least one cited public contact.
- **Outreach queue:** Status = Outreach queue, showing next action and contact channel.
- **Do not contact:** Status = Do not contact, excluded from all send batches.

## Safe update behavior

1. Confirm the target workspace/database when it is not unambiguous.
2. Preview creates, updates, merges, and skipped records before a bulk write.
3. Upsert by stable identity key where possible.
4. Populate empty fields and add new evidence; do not overwrite manual notes or a user's corrected value without calling it out.
5. Keep raw capture, source image, and evidence links even after normalization.
6. Never delete pages or move a lead to Do not contact without the user's instruction.

When Notion tools are unavailable, export the same schema to CSV plus a readable Markdown report and a JSON evidence ledger. The fallback should be importable without redoing OCR or research.
