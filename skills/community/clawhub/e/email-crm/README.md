# OpenClaw Email CRM Skill

A small, local SQLite CRM core for email workflows. It records sourced contacts, email lifecycle events, and email suppressions without binding to a sender, lead provider, or enrichment service.

## Requirements

- Python 3.9 or later
- SQLite 3.24 or later (for safe upserts)

## What it does

- Stores normalized email contacts with an accountable source.
- Records neutral email lifecycle events.
- Provides a deterministic readiness check before an external sender queues or sends mail.
- Makes unsubscribe and manual do-not-contact requests idempotent.

## What it does not do

- Discover, enrich, scrape, or import leads.
- Send email or provide legal advice.
- Store phone, address, call, website, recording, or transcript data.

## Quick start

```bash
python3 scripts/init_email_crm.py --db /absolute/private/path/email_crm.sqlite
printf '%s\n' 'alice@example.com' | python3 scripts/upsert_contact.py --db /absolute/private/path/email_crm.sqlite --email-stdin --source manual-review
printf '%s\n' 'alice@example.com' | python3 scripts/check_email_readiness.py --db /absolute/private/path/email_crm.sqlite --email-stdin
```

The CLI also accepts `--email` for attended use. Agent automation should pass addresses through stdin with `--email-stdin` so they do not appear in process arguments. Upserts store the trimmed, lowercased address in both email columns and return JSON with `ok` and `contact_id`.

Run the test suite with:

```bash
python3 -m unittest discover -s tests -v
```

## ClawHub release identity

The public ClawHub skill is **`email-crm`** (version `1.0.0`). Publish it from
a clean export of this directory, not from a working tree that contains local
worktrees or runtime data. Use the `email-crm` slug explicitly so the catalog
identity remains stable.

For the first public release, use the `productivity` and `security` categories
with the `email`, `crm`, `sqlite`, and `suppression` topics:

```bash
clawhub skill publish ./email-crm \
  --slug email-crm \
  --name "Email CRM" \
  --version 1.0.0 \
  --categories productivity,security \
  --topics email,crm,sqlite,suppression
```

## Data handling

This package deliberately ships with no database, exports, logs, or real contact fixtures. Keep runtime databases and backups out of source control. The `.gitignore` covers common SQLite, export, environment, and log artifacts.

Use `--db` or `EMAIL_CRM_DB` to select an explicit location. Otherwise the CLI uses `$XDG_DATA_HOME/openclaw-email-crm/email_crm.sqlite`, falling back to `~/.local/share/openclaw-email-crm/email_crm.sqlite`; it never writes relative to an arbitrary current working directory. The database and its SQLite sidecars are kept owner-only (`0600`).

Before using an external email sender, configure and satisfy the legal, consent, and policy requirements that apply to your jurisdiction and provider. The readiness result is a technical gate, not a compliance certification.

## License

MIT-0. See [LICENSE](LICENSE). ClawHub releases are also distributed under
MIT-0.
