# Submissions

## `docuseal submissions list`

List all submissions.

| Option | Description |
|---|---|
| `--template-id <value>` | Filter by template ID |
| `--status <value>` | pending, completed, declined, expired |
| `--q <value>` | Filter by submitter name, email, or phone |
| `--slug <value>` | Filter by unique slug |
| `--template-folder <value>` | Filter by template folder name |
| `--archived` | Get only archived submissions |
| `--active` | Get only active submissions |
| `-l, --limit <value>` | Number of results (default 10, max 100) |
| `-a, --after <value>` | Pagination cursor — pass `pagination.next` from previous response |
| `--before <value>` | Pagination end cursor |

```bash
docuseal submissions list
docuseal submissions list --status pending
docuseal submissions list \
  --template-id 1001 \
  --limit 50
docuseal submissions list --q "john@example.com"
```

---

## `docuseal submissions retrieve <id>`

Get a submission by ID.

```bash
docuseal submissions retrieve 502
```

---

## `docuseal submissions archive <id>`

Archive a submission.

```bash
docuseal submissions archive 502
```

---

## `docuseal submissions create`

Create a submission from an existing template.

| Option | Description |
|---|---|
| `--template-id <value>` | Template ID (required) |
| `--send-email` | Send signature request emails (default) |
| `--no-send-email` | Do not send signature request emails |
| `--send-sms` | Send signature request via SMS |
| `--order <value>` | `preserved` (default) or `random` |
| `--expire-at <value>` | Expiration date/time |
| `--completed-redirect-url <value>` | Redirect URL after completion |
| `--bcc-completed <value>` | BCC address for signed documents |
| `--reply-to <value>` | Reply-To email address |

| Data param (`-d`) | Description |
|---|---|
| `variables[key]` | Template variable |
| `message[subject]` | Custom email subject |
| `message[body]` | Custom email body |
| `submitters[N][name]` | Full name |
| `submitters[N][role]` | Role name (e.g. "First Party") |
| `submitters[N][email]` | Email address (required) |
| `submitters[N][phone]` | Phone in E.164 format (e.g. +1234567890) |
| `submitters[N][values][fieldName]` | Pre-filled field value |
| `submitters[N][external_id]` | App-specific ID |
| `submitters[N][completed]` | Mark as completed (true/false) |
| `submitters[N][metadata][key]` | Submitter metadata |
| `submitters[N][send_email]` | Send email (true/false) |
| `submitters[N][send_sms]` | Send SMS (true/false) |
| `submitters[N][reply_to]` | Reply-To email |
| `submitters[N][completed_redirect_url]` | Redirect URL after completion |
| `submitters[N][order]` | Signing order (0, 1, 2...) |
| `submitters[N][require_phone_2fa]` | Require phone 2FA (true/false) |
| `submitters[N][require_email_2fa]` | Require email 2FA (true/false) |
| `submitters[N][message][subject]` | Per-submitter email subject |
| `submitters[N][message][body]` | Per-submitter email body |
| `submitters[N][fields][M][name]` | Field name (required) |
| `submitters[N][fields][M][default_value]` | Default value |
| `submitters[N][fields][M][readonly]` | Read-only (true/false) |
| `submitters[N][fields][M][required]` | Required (true/false) |
| `submitters[N][roles][]` | Merge multiple roles |

```bash
docuseal submissions create \
  --template-id 1001 \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create \
  --template-id 1001 \
  -d "submitters[0][email]=a@b.com" \
  -d "submitters[1][email]=c@d.com"
docuseal submissions create \
  --template-id 1001 \
  -d "submitters[0][email]=john@acme.com" \
  -d "submitters[0][role]=Signer"
docuseal submissions create \
  --template-id 1001 \
  -d "submitters[0][email]=john@acme.com" \
  --no-send-email
```

---

## `docuseal submissions send-emails`

Send a template to multiple recipients by email — creates one submission per recipient.

| Option | Description |
|---|---|
| `--template-id <value>` | Template ID (required) |
| `--emails <value>` | Comma-separated list of email addresses |
| `--send-email` | Send signature request emails (default) |
| `--no-send-email` | Do not send signature request emails |

| Data param (`-d`) | Description |
|---|---|
| `message[subject]` | Custom email subject |
| `message[body]` | Custom email body |

```bash
docuseal submissions send-emails \
  --template-id 1001 \
  --emails a@b.com,c@d.com
docuseal submissions send-emails \
  --template-id 1001 \
  --emails a@b.com \
  -d "message[subject]=Please sign" \
  -d "message[body]=Hello"
```

---

## `docuseal submissions create-pdf` _(Pro)_

Create a submission directly from a PDF file (no pre-existing template needed).

See [PDF / DOCX Field Tags](field-tags.md) for embedded `{{...}}` field syntax in PDF and DOCX documents.

| Option | Description |
|---|---|
| `--file <path>` | Path to local PDF file |
| `--name <value>` | Submission name |
| `--send-email` | Send signature request emails (default) |
| `--no-send-email` | Do not send signature request emails |
| `--send-sms` | Send signature request via SMS |
| `--order <value>` | `preserved` or `random` |
| `--flatten` | Remove PDF form fields |
| `--merge-documents` | Merge into single PDF |
| `--remove-tags` | Remove `{{text}}` tags (default) |
| `--no-remove-tags` | Keep `{{text}}` tags in the PDF |
| `--expire-at <value>` | Expiration date/time |
| `--completed-redirect-url <value>` | Redirect URL after completion |
| `--bcc-completed <value>` | BCC address for signed documents |
| `--reply-to <value>` | Reply-To email address |

| Data param (`-d`) | Description |
|---|---|
| `template_ids[]` | Template ID to use alongside provided documents |
| `documents[N][position]` | Position in template |
| `submitters[N][name]` | Full name |
| `submitters[N][role]` | Role name |
| `submitters[N][email]` | Email address (required) |
| `submitters[N][phone]` | Phone (E.164) |
| `submitters[N][values][fieldName]` | Pre-filled field value |
| `submitters[N][external_id]` | App-specific ID |
| `submitters[N][completed]` | Mark as completed (true/false) |
| `submitters[N][metadata][key]` | Submitter metadata |
| `submitters[N][send_email]` | Send email (true/false) |
| `submitters[N][send_sms]` | Send SMS (true/false) |
| `submitters[N][reply_to]` | Reply-To email |
| `submitters[N][completed_redirect_url]` | Redirect URL after completion |
| `submitters[N][order]` | Signing order (0, 1, 2...) |
| `submitters[N][require_phone_2fa]` | Require phone 2FA (true/false) |
| `submitters[N][require_email_2fa]` | Require email 2FA (true/false) |
| `submitters[N][invite_by]` | Role name of inviting party |
| `submitters[N][fields][M][name]` | Field name (required) |
| `submitters[N][fields][M][default_value]` | Default value |
| `submitters[N][fields][M][readonly]` | Read-only (true/false) |
| `submitters[N][fields][M][required]` | Required (true/false) |
| `submitters[N][roles][]` | Merge multiple roles |
| `message[subject]` | Custom email subject |
| `message[body]` | Custom email body |

```bash
docuseal submissions create-pdf \
  --file doc.pdf \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create-pdf \
  -d "documents[0][file]=./doc.pdf" \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create-pdf \
  -d "documents[0][file]=https://..." \
  -d "submitters[0][email]=john@acme.com"
```

---

## `docuseal submissions create-docx` _(Pro)_

Create a submission directly from a DOCX file.

See [PDF / DOCX Field Tags](field-tags.md) for embedded `{{...}}` field syntax. See [DOCX Variables](docx-variables.md) for DOCX-specific variables, loops, and conditional content.

| Option | Description |
|---|---|
| `--file <path>` | Path to local DOCX file |
| `--name <value>` | Submission name |
| `--send-email` | Send signature request emails (default) |
| `--no-send-email` | Do not send signature request emails |
| `--send-sms` | Send signature request via SMS |
| `--merge-documents` | Merge into single PDF |
| `--remove-tags` | Remove `{{text}}` tags (default) |
| `--no-remove-tags` | Keep `{{text}}` tags |
| `--order <value>` | `preserved` or `random` |
| `--expire-at <value>` | Expiration date/time |
| `--completed-redirect-url <value>` | Redirect URL after completion |
| `--bcc-completed <value>` | BCC address for signed documents |
| `--reply-to <value>` | Reply-To email address |

| Data param (`-d`) | Description |
|---|---|
| `variables[key]` | Template variable |
| `template_ids[]` | Template ID to use alongside provided documents |
| `documents[N][position]` | Position in template |

Supports same `-d submitters[N]...` and `message` data params as `submissions create-pdf`.

```bash
docuseal submissions create-docx \
  --file doc.docx \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create-docx \
  -d "documents[0][file]=./doc.docx" \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create-docx \
  -d "documents[0][file]=https://..." \
  -d "submitters[0][email]=john@acme.com"
```

---

## `docuseal submissions create-html` _(Pro)_

Create a submission directly from HTML.

See [HTML Field Tags](html-fields.md) for supported tags, attributes, and `style` guidance.

| Option | Description |
|---|---|
| `--file <path>` | Path to local HTML file |
| `--name <value>` | Submission name |
| `--send-email` | Send signature request emails (default) |
| `--no-send-email` | Do not send signature request emails |
| `--send-sms` | Send signature request via SMS |
| `--merge-documents` | Merge into single PDF |
| `--order <value>` | `preserved` or `random` |
| `--expire-at <value>` | Expiration date/time |
| `--completed-redirect-url <value>` | Redirect URL after completion |
| `--bcc-completed <value>` | BCC address for signed documents |
| `--reply-to <value>` | Reply-To email address |

| Data param (`-d`) | Description |
|---|---|
| `template_ids[]` | Template ID to use alongside provided documents |
| `documents[N][name]` | Document name |
| `documents[N][html]` | HTML template with field tags |
| `documents[N][html_header]` | HTML header for every page |
| `documents[N][html_footer]` | HTML footer for every page |
| `documents[N][size]` | Page size (Letter, A4, ...) |
| `documents[N][position]` | Position in template |

Supports same `-d submitters[N]...` and `message` data params as `submissions create-pdf`.

```bash
docuseal submissions create-html \
  --file template.html \
  -d "submitters[0][email]=john@acme.com"
docuseal submissions create-html \
  -d 'documents[0][html]=<p><text-field name="Name"></text-field></p>' \
  -d "submitters[0][email]=john@acme.com"
```

---

## `docuseal submissions documents <id>`

Get documents for a submission.

| Option | Description |
|---|---|
| `--merge` | Merge all documents into a single PDF |

```bash
docuseal submissions documents 502
docuseal submissions documents 502 --merge
```
