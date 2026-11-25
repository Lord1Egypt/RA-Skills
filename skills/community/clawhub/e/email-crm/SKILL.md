---
name: email-crm
description: Maintain a local, email-only CRM ledger in SQLite. Use for adding sourced email contacts, recording email lifecycle events, checking whether a contact is safe to email, and processing email suppressions or unsubscribes. This skill never discovers contacts or sends email.
version: 1.0.0
metadata:
  openclaw:
    emoji: "✉️"
    homepage: https://github.com/codereyes-1/openclaw-email-crm-skill
    requires:
      bins:
        - python3
    envVars:
      - name: EMAIL_CRM_DB
        required: false
        description: Optional absolute path to the local SQLite database.
---

# Email CRM

Use this skill as a local decision and audit layer for email workflows. It stores only contacts, email events, and suppressions; it does not discover leads, enrich profiles, make calls, or send messages.

## 1. Choose the database

Pass `--db PATH` to every helper for an explicit database. If omitted, helpers use `EMAIL_CRM_DB`, then `$XDG_DATA_HOME/openclaw-email-crm/email_crm.sqlite` (or `~/.local/share/openclaw-email-crm/email_crm.sqlite` when `XDG_DATA_HOME` is unset). The default never depends on the caller's current working directory. Database files and SQLite sidecars are restricted to the owning user (`0600`).

`{baseDir}` below is the absolute installation directory supplied by OpenClaw. Keep it in every script invocation so commands work regardless of the current working directory.

## 2. Initialize before use

```bash
python3 "{baseDir}/scripts/init_email_crm.py" --db /absolute/private/path/email_crm.sqlite
```

The command creates the versioned schema, verifies compatibility with an existing database, and enables SQLite foreign keys for its connection. Confirm that it returns `schema_version: 1`.

## 3. Add or update a sourced contact

```bash
python3 "{baseDir}/scripts/upsert_contact.py" \
  --db /absolute/private/path/email_crm.sqlite \
  --email-stdin \
  --source "manual-review"
```

Provide the email value on standard input. Agents must use `--email-stdin`, passing the value directly as stdin rather than interpolating it into a shell command or exposing it in process arguments. `--email` remains available for attended CLI use.

`--source` is required. The helper trims and lowercases the email before storing it in both email columns, upserts exactly one contact, and returns JSON containing `ok` and the stable numeric `contact_id`. On an existing contact it replaces `source`, refreshes `updated_at`, and preserves DNC state. A suppression created before the contact also sets the new contact's DNC state.

## 4. Check readiness before an external sender acts

```bash
python3 "{baseDir}/scripts/check_email_readiness.py" \
  --db /absolute/private/path/email_crm.sqlite \
  --email-stdin
```

Treat `ready: false` as a hard stop. A caller must run this check immediately before queuing or sending email, then respect every returned reason code. This skill does not itself send email.

## 5. Record email lifecycle events

```bash
python3 "{baseDir}/scripts/log_email_event.py" \
  --db /absolute/private/path/email_crm.sqlite \
  --contact-id 1 \
  --event-type drafted
```

Allowed event types are `drafted`, `queued`, `sent`, `delivered`, `opened`, `replied`, `bounced`, and `failed`. Use `--metadata-json` only for non-sensitive operational metadata.

## 6. Process a manual DNC request or unsubscribe

```bash
python3 "{baseDir}/scripts/suppress_email.py" \
  --db /absolute/private/path/email_crm.sqlite \
  --email-stdin \
  --reason unsubscribe
```

Suppression is normalized, unique, idempotent, and also marks any matching contact as `do_not_contact`. Its JSON `reason` is the reason actually persisted by the first suppression, even if a later idempotent call supplies a different reason. Do not log raw email addresses in surrounding automation.

## Verification

Run `cd "{baseDir}" && python3 -m unittest discover -s tests -v`. The tests use only temporary databases and `example.com` addresses.

See [the schema reference](references/schema.md) and [readiness rules](references/readiness-rules.md) for the stable integration contract.
