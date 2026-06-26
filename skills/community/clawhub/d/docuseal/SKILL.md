---
name: docuseal-cli
description: >
  Manage DocuSeal e-signature workflows from the terminal via the DocuSeal CLI -
  create templates from PDF/DOCX/HTML, send documents for signing, track submissions,
  and update submitters. Use when the user wants to run DocuSeal commands in the shell,
  scripts, or CI/CD pipelines. Always load this skill before running `docuseal` commands.
license: MIT
metadata:
  author: DocuSeal
  version: "1.0.6"
  homepage: https://www.docuseal.com
  source: https://github.com/docusealco/docuseal-cli
  openclaw:
    emoji: "📝"
    requires:
      env:
        - DOCUSEAL_API_KEY
        - DOCUSEAL_SERVER
      bins:
        - docuseal
      primaryEnv: DOCUSEAL_API_KEY
    install:
      - id: npm
        kind: npm
        package: docuseal
        bins:
          - docuseal
        label: Install DocuSeal CLI (npm)
---

## Agent Protocol

**Rules for agents:**
- Supply ALL required flags — the CLI will not prompt for missing parameters.
- Output is always JSON.
- Use `-d key=value` (bracket notation) or `-d '{"..": ".."}'` (JSON) for body and array parameters.

## Authentication

Set environment variables:
- `DOCUSEAL_API_KEY` — API key (required). Get yours at https://console.docuseal.com/api
- `DOCUSEAL_SERVER` — `global` (default), `europe`, or full URL for self-hosted (e.g. `https://docuseal.yourdomain.com`)

## Available Commands

| Command Group | What it does |
|---|---|
| `templates` | list, retrieve, update, archive, create-pdf, create-docx, create-html, clone, merge, update-documents |
| `submissions` | list, retrieve, archive, create, send-emails, create-pdf, create-docx, create-html, documents |
| `submitters` | list, retrieve, update |

Read the matching reference file for detailed flags and examples.

## Common Mistakes

| # | Mistake | Fix |
|---|---|---|
| 1 | **Forgetting `-d template_id=<id>` on `submissions create`** | `--template-id` is a flag; submitters and other body params go via `-d` |
| 2 | **Passing a plain file path as a URL** | `--file` accepts a local path; for remote files use `-d "documents[0][file]=https://..."` |
| 3 | **Expecting array params as comma-separated** | Arrays use bracket notation: `-d "template_ids[]=1"` `-d "template_ids[]=2"` |
| 4 | **Using `templates create-pdf` without a Pro plan** | Commands marked _(Pro)_ require a DocuSeal Pro subscription |
| 5 | **Sending to multiple recipients with `submissions create`** | Use `submissions send-emails --emails a@b.com,c@d.com` for bulk; `submissions create` is per-submitter |

## Security

The CLI accepts user-provided file paths, remote URLs (`documents[0][file]=https://...`), and HTML content as template input. This is by design — all content originates from the authenticated user and is sent directly to the DocuSeal API over HTTPS. The CLI does not fetch, render, or execute remote content locally; it passes references to the server for processing. No user input is interpolated into shell commands.

## Common Patterns

**List templates:**
```bash
docuseal templates list --q "NDA" --limit 20
```

**Create a template from a PDF and send for signing:**
```bash
docuseal templates create-pdf --file contract.pdf --name "NDA"
docuseal submissions send-emails --template-id 1001 --emails signer@example.com
```

**Create a submission with pre-filled fields (bracket notation):**
```bash
docuseal submissions create --template-id 1001 \
  -d "submitters[0][email]=john@acme.com" \
  -d "submitters[0][values][Company Name]=Acme Corp"
```

**Create a submission with pre-filled fields (JSON):**
```bash
docuseal submissions create --template-id 1001 \
  -d '{"submitters": [{"email": "john@acme.com", "values": {"Company Name": "Acme Corp"}}]}'
```

**Check signing status:**
```bash
docuseal submissions list --template-id 1001 --status pending
```

**Update a submitter:**
```bash
docuseal submitters update 201 --email new@acme.com --send-email
```

## When to Load References

- **Creating or managing templates** → [references/templates.md](references/templates.md)
- **Sending documents for signing or tracking status** → [references/submissions.md](references/submissions.md)
- **Using dynamic content variables in DOCX** → [references/docx-variables.md](references/docx-variables.md)
- **Embedding field tags in PDF/DOCX** → [references/field-tags.md](references/field-tags.md)
- **Writing HTML templates with field tags** → [references/html-fields.md](references/html-fields.md)
- **Listing or updating signers** → [references/submitters.md](references/submitters.md)
