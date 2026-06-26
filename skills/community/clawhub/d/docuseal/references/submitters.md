# Submitters

## `docuseal submitters list`

List all submitters.

| Option | Description |
|---|---|
| `--submission-id <value>` | Filter by submission ID |
| `--q <value>` | Filter by name, email, or phone partial match |
| `--slug <value>` | Filter by unique slug |
| `--external-id <value>` | Filter by external ID |
| `--completed-after <value>` | Filter by completion date (after) |
| `--completed-before <value>` | Filter by completion date (before) |
| `-l, --limit <value>` | Number of results (default 10, max 100) |
| `-a, --after <value>` | Pagination cursor — pass `pagination.next` from previous response |
| `--before <value>` | Pagination end cursor |

```bash
docuseal submitters list
docuseal submitters list --submission-id 502
docuseal submitters list --q "john@example.com"
```

---

## `docuseal submitters retrieve <id>`

Get a submitter by ID.

```bash
docuseal submitters retrieve 201
```

---

## `docuseal submitters update <id>`

Update a submitter — change contact info, pre-fill fields, re-send notifications, or mark as completed.

| Option | Description |
|---|---|
| `--name <value>` | Full name |
| `--email <value>` | Email address |
| `--phone <value>` | Phone in E.164 format (e.g. +1234567890) |
| `--external-id <value>` | App-specific unique key |
| `--send-email` | Re-send signature request email |
| `--send-sms` | Re-send via SMS |
| `--completed` | Mark as completed (auto-signed) |
| `--reply-to <value>` | Reply-To email address |
| `--completed-redirect-url <value>` | Redirect URL after completion |
| `--require-phone-2fa` | Require phone 2FA |
| `--require-email-2fa` | Require email 2FA |

| Data param (`-d`) | Description |
|---|---|
| `values[fieldName]` | Pre-filled field value |
| `metadata[key]` | Submitter metadata |
| `message[subject]` | Custom email subject |
| `message[body]` | Custom email body |
| `fields[N][name]` | Field name (required) |
| `fields[N][default_value]` | Default value |
| `fields[N][readonly]` | Read-only (true/false) |
| `fields[N][required]` | Required (true/false) |

```bash
docuseal submitters update 201 --email new@acme.com
docuseal submitters update 201 --completed
docuseal submitters update 201 \
  -d "values[First Name]=John" \
  -d "metadata[department]=Sales"
```
