# Operations reference

## Start and stop

Run the service from the generated project:

```bash
scripts/run.sh
```

Use a process supervisor appropriate to the deployment environment. Stop the old process before starting a replacement so two listeners do not compete for the same events.

## Safe promotion sequence

Use these stages:

1. `BOT_AUTO_SUBMIT=false`, `BOT_DRY_RUN=true`: receive, recognize, validate, and send confirmation cards without a submission path.
2. `BOT_AUTO_SUBMIT=true`, `BOT_DRY_RUN=true`: Submit builds and records a complete dry-run approval request.
3. `BOT_AUTO_SUBMIT=true`, `BOT_DRY_RUN=false`: Submit uploads the invoice and creates a real approval.

Changing stage 3 requires explicit user authorization. Revert to stage 2 after any approval-definition, mapping, callback, permission, or model change.

## Inspect configuration and records

```bash
PYTHONPATH=src python3 -m invoice_approval_bot.cli validate
PYTHONPATH=src python3 -m invoice_approval_bot.cli records --limit 20
```

The records command can contain invoice and user information. Do not paste its output into public issues, logs, or Skill releases.

Common states:

- `buyer_header_mismatch`: buyer name or tax ID was rejected before confirmation.
- `invoice_risk_rejected`: an individual seller supplied equipment, or tax values were zero, masked, missing, or inconsistent.
- `needs_review`: document type, confidence, required fields, or model review flags prevented automation.
- `pending_confirmation`: the uploader has received a card and no decision has been accepted.
- `declined`: the uploader selected Do not submit.
- `ready_for_review`: the uploader confirmed but auto-submit is disabled.
- `confirmed_dry_run`: the uploader confirmed and a dry-run request was generated.
- `submitting`: a real approval request is in flight.
- `submitted`: an approval instance code was recorded.
- `duplicate`: the invoice fingerprint matches an already submitted invoice.
- `failed`: an exception stopped processing; inspect the stored error and service log.

## Troubleshooting

### Buyer name looks correct but is rejected

Inspect the recognized `buyer_name` for OCR substitutions, not only spacing. The normalizer handles ordinary/full-width parentheses, whitespace, non-breaking spaces, and zero-width characters. It intentionally does not treat different Chinese characters as equal.

### `invoice.expense_category_value` does not exist

The mapping references a derived value. Add `expense_type_options` and include an option ID for every category allowed by `config/invoice-output.schema.json`. Also confirm Codex returned `expense_category`.

### Category has no matching option ID

The JSON Schema enum and `expense_type_options` keys differ, or the approval option IDs are stale. Update both from the current approval definition and rerun tests.

### Card displays but buttons do nothing

Confirm that `card.action.trigger` is subscribed through the same long connection, the application version is published, and the callback reaches the running process. The service rejects callbacks from users other than the original uploader.

### Approval API rejects the form

Compare every widget ID, widget type, nested `fieldList` item, currency, timestamp format, and radio option ID with the current approval definition. A copied ID from another approval version is not interchangeable.

### Codex extraction fails

Run `codex --version`, verify authentication, remove an incompatible `CODEX_MODEL` override, and keep the JSON Schema synchronized with the extraction prompt. Do not silently lower confidence thresholds to force submission.

### Duplicate or repeated callbacks

Do not delete or bypass the SQLite idempotency records during normal operation. Event IDs, message IDs, card decisions, deterministic approval UUIDs, and invoice fingerprints protect against retries and double reimbursement.

## Data handling

Runtime data can include invoice images, extracted JSON, sender open IDs, approval request/response payloads, and instance codes. Restrict filesystem permissions, define an organization-approved retention period, back up only when required, and never include runtime data in a Skill publication.
