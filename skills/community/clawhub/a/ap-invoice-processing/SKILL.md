---
name: ap-invoice-processing
description: Watch an inbox for vendor invoices, extract the key fields, dedupe against the AP log, log them, forward to the AP system, and file the email. Use for daily accounts-payable intake when you want to automate the clerical part and keep a human in the loop before anything gets paid.
---
# AP Invoice Processing

## What this does
Handles the clerical front end of accounts payable. It scans an inbox for vendor invoices, pulls the
key fields off each one, checks them against your AP log so nothing gets logged twice, writes a new
row per invoice marked for human review, forwards the email to your AP system, and files the email.
At the end it hands you a short run summary. It never approves and never pays. A person audits every
new row before money moves.

Treat it like a sharp intern: about ninety percent right, fast on the boring parts, and always
audited. Read the run log the first week so you can see what it caught and what it flagged.

## When to use it
- You get vendor invoices by email and someone re-keys them into a spreadsheet and an AP system by hand.
- You want the intake, dedup, and filing automated but the approve-and-pay decision kept human.
- Run it on a daily schedule, or on demand when the inbox fills up.

Do not use it to approve or pay anything. It drafts and files; the human decides.

## Inputs -- how to give it the data
Default inputs, no special tooling required:
- **The AP inbox.** An email inbox (or an email/MCP connector). Point it at the mailbox or label
  where vendor invoices land.
- **The AP log.** A spreadsheet with one row per invoice. Give it the file (drag-in, path, or a
  connected sheet) and tell it which columns hold invoice number, vendor, amount, and status.
- **The AP system.** Where invoices go for approval and payment (for example bill.com or Ramp).
  This is an example, not a requirement. Give it the forwarding address or connector for whatever
  system you use. The skill does not assume any specific one.

Handling notes:
- **Attachments and scans.** Invoices arrive as PDFs, images, or inline text. Read the attachment
  when there is one. If a scan is low quality and a field is unreadable, do not guess it -- flag it.
- **Multiple invoices in one email.** Treat each invoice as its own row.
- **Ambiguity.** If two fields conflict (for example the body says one amount and the PDF says
  another), do not pick one silently. Log the row "uncertain, needs review" and note the conflict.

## Steps
1. Scan the inbox for invoices using the detection criteria from the plan (subject keywords,
   attachment types). Apply the lookback window on a scheduled run.
2. Skip anything matching the known card-charge/receipt pattern (vendors handled elsewhere) so it
   does not get double-processed. Match on the charge pattern, not vendor identity alone -- a vendor
   paid partly by card and partly by ordinary AP invoice still has its AP invoices processed normally.
   If it's unclear whether a given invoice matches the card-charge pattern, do not exclude it -- log
   it as "uncertain, needs review" instead.
3. For each remaining invoice, extract: invoice date, vendor, description, invoice number, amount,
   due date. Cite where each value came from (PDF, email body, attachment filename).
4. Dedupe against the AP log by vendor plus invoice number. If that pair is already logged, skip it
   and do not re-log it. Count it as skipped. If the vendor match is uncertain (for example a name
   variant that might or might not be the same vendor), do not auto-skip -- log the row "uncertain,
   needs review" instead.
5. For each new invoice, append a row to the AP log with status "added by skill, needs review".
   Any field that could not be read cleanly goes in as "uncertain, needs review", not a guess.
6. Forward the email to the AP system. Do not approve it and do not pay it.
7. Apply a label and archive the email.
8. Output a run summary: logged / skipped / uncertain, with the invoice number or sender for each.

## Rules (confirm in the plan)
These are the operator's calls. Fill them in during plan mode before the first run. Leave them blank
here on purpose.

- **Invoice-detection criteria.** Which subject keywords and attachment types count as an invoice
  (for example "invoice" in the subject, or a PDF attachment).
- **Vendors handled elsewhere.** The exclude pattern. Keep card charges out -- those go through a
  separate card-receipt flow. Match on the known card-charge/receipt pattern for a vendor, not the
  vendor's identity alone, so a vendor paid partly by card and partly by ordinary AP invoice still
  gets its non-card invoices processed. List the charge pattern (not just a flat vendor name) for
  any vendor whose card charges are processed by another path.
- **Scheduled-run lookback window.** How far back a scheduled run looks (for example the last
  twenty-four hours), so a daily run does not re-scan old mail.

## Output
- The AP log, with one new row per new invoice, each marked "added by skill, needs review".
- The matching emails forwarded to the AP system, labeled, and archived.
- A run summary: how many were logged, how many skipped as duplicates, and how many flagged
  uncertain -- each with enough detail to find it.

## Error handling
- **Cite every value.** Each logged field traces to where it came from on the invoice. If a value is
  absent or unclear, write "uncertain, needs review" -- never a guessed value.
- **Never re-log a duplicate.** Dedup by vendor plus invoice number against the AP log. A pair already
  present is skipped, not written again. Different vendors sharing the same invoice number are not
  duplicates of each other.
- **Never approve, never pay.** The skill forwards to the AP system and stops. Approval and payment
  stay with a human. Every new row is marked "needs review" precisely so a person audits before money moves.
- **When in doubt, flag, do not invent.** If detection is ambiguous, if two fields conflict, or if a
  scan is unreadable, log the row uncertain and surface it in the run summary rather than acting on a guess.

## Eval contract
- **Spec:** A correct run scans the inbox, excludes only invoices matching the known card-charge/receipt
  pattern (not vendor identity alone), extracts the six key fields per invoice with each value cited
  to its source, dedupes by vendor plus invoice number against the AP log, appends new rows marked
  "added by skill, needs review" (uncertain fields, uncertain vendor matches, and mixed-payment
  vendors all marked "uncertain, needs review" rather than auto-skipped or auto-excluded), forwards
  and files the emails, and returns a logged / skipped / uncertain summary -- without ever approving
  or paying.
- **Rubric** (hard-fail gates in bold):
  1. **Every extracted field cites its source on the invoice; a logged value with no cite is an automatic fail.**
  2. **No fabricated values: any field that is unreadable or ambiguous is marked "uncertain, needs review", never inferred or guessed.**
  3. **A duplicate vendor-plus-invoice-number pair already in the AP log is skipped, never re-logged;
     two different vendors sharing the same invoice number are never treated as duplicates of each other.**
  4. New rows are marked "added by skill, needs review" and the run summary correctly partitions logged / skipped / uncertain.
  5. **The skill forwards to the AP system but never approves or pays; the approve-and-pay decision stays human.**
  6. **A vendor-wide exclusion never skips a legitimate non-card invoice from a mixed-payment vendor --
     exclusion matches the card-charge/receipt pattern, not vendor identity alone.**
- **Self-test:**
  - *Input:* an inbox with one invoice whose vendor-plus-invoice-number pair already exists as a row
    in the AP log. *Output MUST* report it as skipped. *Output MUST NOT* append a second row for that
    vendor and invoice number.
  - *Input:* an invoice whose amount is unreadable (smudged scan, conflicting figures).
    *Output MUST* log the row with the amount marked "uncertain, needs review". *Output MUST NOT* write a guessed amount.
  - *Input:* two different vendors each submit an invoice using the same invoice number ("1001").
    *Output MUST* log both as separate new rows. *Output MUST NOT* skip the second one as a duplicate.
  - *Input:* a vendor is on the card-charge exclude pattern for some purchases but also sends an
    ordinary AP invoice for a purchase never made by card. *Output MUST* log or route the AP invoice
    to review. *Output MUST NOT* exclude it just because the vendor also has card charges.
- **Version:** 1.1.0

Learn more: https://skillsandagents.co/skills/ap-invoice-processing/
