# Jobs

Use live tool discovery first. These are user jobs, not a substitute for discovered schemas. Mechanics live in the named skill.

## Bring contracts in

**They say:** import these, onboard us, migrate the archive, look on disk, Google Drive, SharePoint, or Box.

Find the files with the available file or cloud tools, confirm the set, then import them. Contracko extracts types and parties. Review the extracted configuration before adding more. [contracko-import](../../contracko-import/SKILL.md) owns import; [SKILL.md](../SKILL.md) owns types, fields, parties, and folders.

If the user also wants filing, inspect visible folders, confirm the proposed destination and any batch, then create, rename, move, or file through the discovered folder tools. Do not infer a folder from a missing or unavailable filing state.

**Done when:** the documents are contracts in the intended workspace, types cover the user's questions, and each requested filing change has been read back.

## What is coming up

**They say:** notice dates, end dates, renewals, annual review, reminders, notifications.

Get today's date from the environment. Use inclusive end-date or notice-date filters for dated candidates and complete every returned page. `autoRenewing` identifies a renewal; a date window alone does not. For contracts ending OR needing notice, run separate complete queries and deduplicate by contract ID. Use existing system events for renewal or notice reminders. [contracko-review](../../contracko-review/SKILL.md) owns the calendar.

**Done when:** the user has the urgent bucket, its dates, and any requested reminder confirmed as created.

## Compare these

**They say:** two proposals, vendor A versus B, or a redline versus a previous draft.

Get both records, analyses, and cited document text for disputed terms. Compare metadata and quotes in a table. Add related versions to the existing contract when the user identifies them as versions of one agreement. [contracko-review](../../contracko-review/SKILL.md) owns comparison.

**Done when:** the user can choose with supporting quotes.

## Audit for risk

**They say:** risks, liability, caps, indemnity, or what could hurt us.

Complete the relevant portfolio page set before opening hot contracts. Use `clm_get_contract_analysis`, contract liability fields, and cited clauses. A null analysis field does not prove no risk. [contracko-review](../../contracko-review/SKILL.md) owns audit.

**Done when:** every material finding has a quote, a severity, and a clear extraction-review status.

## File and type contracts

**They say:** organise, folders, contract types, custom fields, or filing.

Import before designing a new workspace. Use types and custom fields for the questions the user asks, then propose and confirm any changes. List visible folders with `clm_list_folders`, inspect a chosen destination, confirm the destination and bulk changes, then use the discovered folder and contract move tools. `folderId: null` unfiles only when the user asks. Access reads are informational; access changes and folder deletion are in the app.

To find unfiled contracts, complete the relevant contract pages and inspect `filing.kind`. Do not send `folderId: null` as a list filter. `unavailable` does not identify an unfiled contract or a hidden folder.

**Done when:** types and fields match the user's model, each requested filing change is verified, and any access work is clearly handed to the app.

## Priorities and gaps

**They say:** report, portfolio, what matters this quarter, or what are we missing.

Start with the narrowest supported `clm_list_contracts` filters. Filters combine with AND. Complete each filtered page set. For OR windows, use complete separate queries and deduplicate. For value, currency, missing fields, custom-field gaps, or unfiled audits, evaluate the complete narrowed result locally. Separate monetary totals by currency. [contracko-review](../../contracko-review/SKILL.md) owns reporting.

**Done when:** the user has ranked results, named gaps, and the count of the completed result set.

## Start a new agreement

[contracko-create](../../contracko-create/SKILL.md) owns the questionnaire and filing the executed copy. Drafting and signature stay in the app.
