# Templates

## `docuseal templates list`

List all templates.

| Option | Description |
|---|---|
| `--q <value>` | Filter by name search |
| `--folder <value>` | Filter by folder name |
| `--slug <value>` | Filter by unique slug |
| `--external-id <value>` | Filter by external ID |
| `--archived` | Get only archived templates |
| `--active` | Get only active templates |
| `-l, --limit <value>` | Number of results (default 10, max 100) |
| `--after <value>` | Pagination cursor — pass `pagination.next` from previous response |
| `--before <value>` | Pagination end cursor |

```bash
docuseal templates list
docuseal templates list --folder Legal --limit 50
docuseal templates list --archived
```

---

## `docuseal templates retrieve <id>`

Get a template by ID.

```bash
docuseal templates retrieve 1001
```

---

## `docuseal templates update <id>`

Update a template.

| Option | Description |
|---|---|
| `--name <value>` | Template name |
| `--folder-name <value>` | Move to folder |
| `--archive` | Archive the template |
| `--unarchive` | Unarchive the template |

| Data param (`-d`) | Description |
|---|---|
| `roles[]` | Submitter role name |

```bash
docuseal templates update 1001 --name "NDA v2"
docuseal templates update 1001 --folder-name Contracts
docuseal templates update 1001 \
  -d "roles[]=Signer" \
  -d "roles[]=Reviewer"
docuseal templates update 1001 --unarchive
```

---

## `docuseal templates archive <id>`

Archive a template.

```bash
docuseal templates archive 1001
```

---

## `docuseal templates create-pdf` _(Pro)_

Create a template from a PDF file.

See [PDF / DOCX Field Tags](field-tags.md) for embedded `{{...}}` field syntax in PDF and DOCX documents.

| Option | Description |
|---|---|
| `--file <path>` | Path to local PDF file |
| `--name <value>` | Template name |
| `--folder-name <value>` | Folder to create in |
| `--external-id <value>` | App-specific unique key |
| `--shared-link` | Make available via shared link |
| `--no-shared-link` | Disable shared link |
| `--flatten` | Remove PDF form fields |
| `--remove-tags` | Remove `{{text}}` tags (default) |
| `--no-remove-tags` | Keep `{{text}}` tags in the PDF |

| Data param (`-d`) | Description |
|---|---|
| `documents[N][name]` | Document name |
| `documents[N][file]` | Local file path or URL |
| `documents[N][fields][M][name]` | Field name |
| `documents[N][fields][M][type]` | text, signature, initials, date, number, image, checkbox, multiple, file, radio, select, cells, stamp, payment, phone, verification, kba |
| `documents[N][fields][M][role]` | Signer role name |
| `documents[N][fields][M][required]` | Required (true/false) |
| `documents[N][fields][M][title]` | Display title |
| `documents[N][fields][M][description]` | Display description (Markdown) |
| `documents[N][fields][M][areas][K][x/y/w/h]` | Position as fraction of page (0-1) |
| `documents[N][fields][M][areas][K][page]` | Page number (starts at 1) |
| `documents[N][fields][M][options][]` | Select/radio option values |

```bash
docuseal templates create-pdf --file contract.pdf --name "NDA"
docuseal templates create-pdf --file form.pdf --folder-name Legal
docuseal templates create-pdf \
  -d "documents[0][file]=./contract.pdf" \
  --name "NDA"
docuseal templates create-pdf \
  -d "documents[0][file]=https://..." \
  --name "NDA"
docuseal templates create-pdf --file form.pdf \
  -d "documents[0][fields][0][name]=Name" \
  -d "documents[0][fields][0][type]=text"
```

---

## `docuseal templates create-docx` _(Pro)_

Create a template from a Word DOCX file.

See [PDF / DOCX Field Tags](field-tags.md) for embedded `{{...}}` field syntax in PDF and DOCX documents.

| Option | Description |
|---|---|
| `--file <path>` | Path to local DOCX file |
| `--name <value>` | Template name |
| `--folder-name <value>` | Folder to create in |
| `--external-id <value>` | App-specific unique key |
| `--shared-link` | Make available via shared link |
| `--no-shared-link` | Disable shared link |

Supports same `-d documents[N]...` data params as `create-pdf`.

```bash
docuseal templates create-docx --file template.docx --name "Contract"
docuseal templates create-docx \
  -d "documents[0][file]=./template.docx" \
  --name "Contract"
docuseal templates create-docx \
  -d "documents[0][file]=https://..." \
  --name "Contract"
docuseal templates create-docx --file template.docx \
  -d "documents[0][fields][0][name]=Name" \
  -d "documents[0][fields][0][role]=Signer"
```

---

## `docuseal templates create-html` _(Pro)_

Create a template from HTML.

See [HTML Field Tags](html-fields.md) for supported tags, attributes, and `style` guidance.

| Option | Description |
|---|---|
| `--html <value>` | Inline HTML with field tags |
| `--file <path>` | Path to local HTML file |
| `--html-header <value>` | Header HTML (shown on every page) |
| `--html-footer <value>` | Footer HTML (shown on every page) |
| `--name <value>` | Template name |
| `--size <value>` | Page size: Letter (default), A4, Legal, A3, A5, A6, Tabloid, Ledger, A0, A1, A2 |
| `--folder-name <value>` | Folder to create in |
| `--external-id <value>` | App-specific unique key |
| `--shared-link` | Make available via shared link |
| `--no-shared-link` | Disable shared link |

| Data param (`-d`) | Description |
|---|---|
| `documents[N][html]` | HTML with field tags |
| `documents[N][name]` | Document name |

```bash
docuseal templates create-html \
  --html '<p><text-field name="Name"></text-field></p>' \
  --name "Simple"
docuseal templates create-html \
  --file template.html \
  --name "Contract"
docuseal templates create-html \
  -d 'documents[0][html]=<p><text-field name="Name"></text-field></p>' \
  -d "documents[0][name]=Page 1"
```

---

## `docuseal templates clone <id>`

Clone a template.

| Option | Description |
|---|---|
| `--name <value>` | Name for the clone (default: original name + "(Clone)") |
| `--folder-name <value>` | Folder to clone into |
| `--external-id <value>` | App-specific unique key |

```bash
docuseal templates clone 1001
docuseal templates clone 1001 --name "NDA Copy"
```

---

## `docuseal templates merge` _(Pro)_

Merge multiple templates into one.

| Option | Description |
|---|---|
| `--name <value>` | Name for the merged template |
| `--folder-name <value>` | Folder to place merged template |
| `--external-id <value>` | App-specific unique key |
| `--shared-link` | Make available via shared link |
| `--no-shared-link` | Disable shared link |

| Data param (`-d`) | Description |
|---|---|
| `template_ids[]` | Template ID to include (required, repeatable) |
| `roles[]` | Submitter role name |

```bash
docuseal templates merge \
  -d "template_ids[]=1001" \
  -d "template_ids[]=1002"
docuseal templates merge \
  -d "template_ids[]=1001" \
  -d "template_ids[]=1002" \
  --name "Combined"
```

---

## `docuseal templates update-documents <id>` _(Pro)_

Update documents within an existing template.

| Option | Description |
|---|---|
| `--merge` | Merge all docs into a single PDF |

| Data param (`-d`) | Description |
|---|---|
| `documents[N][name]` | Document name |
| `documents[N][file]` | Local file path, URL, or base64-encoded content |
| `documents[N][html]` | HTML template with field tags |
| `documents[N][position]` | Position in template |
| `documents[N][replace]` | Replace existing document (true/false) |
| `documents[N][remove]` | Remove document (true/false) |

```bash
docuseal templates update-documents 1001 \
  -d "documents[0][file]=./contract.pdf"
docuseal templates update-documents 1001 \
  -d "documents[0][file]=https://..."
docuseal templates update-documents 1001 \
  -d "documents[0][file]=https://..." \
  -d "documents[0][name]=New Doc"
```
