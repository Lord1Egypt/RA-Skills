---
name: esign-automation
description: Automate contract signing, esign, and signature workflows by calling the eSignGlobal CLI tool. The eSignGlobal CLI is agent-friendly, with JSON output by default, making eSignGlobal signing operations easy to parse and chain. Supports creating draft envelopes, obtaining sender view URLs, sending envelopes, querying envelope details, sending reminders, cancelling envelopes, downloading signed files, verifying PDF signatures locally, rendering templates to generate documents for signing, comparing two PDF contracts side by side, managing envelope attachments, managing CC (carbon copy) recipients, and adding or removing signers from draft envelopes.
metadata: {"openclaw":{"primaryEnv":"ESIGNGLOBAL_APIKEY"}}
version: 1.7.5
homepage: https://github.com/esign-cn-open-source/skills
---

# eSign Automation

This skill provides automation capabilities for the eSignGlobal electronic signature platform.
It enables AI agents to automate document signing workflows and integrate with eSignGlobal APIs.
This skill is maintained by the eSignGlobal team and is intended for safe automation of contract signing workflows.

## Best For

Use this skill when the user wants to:

- send a contract, agreement, or approval form for signature
- launch a new e-sign workflow from a local file
- send one document to one or more recipients for signing
- create a draft envelope and get an interactive sender view URL to configure and send it
- open an envelope preparation page in the browser to add files and signers interactively
- query the status and details of an envelope
- send a reminder to signers who have not yet signed
- cancel an in-progress envelope
- download signed documents or certificates after an envelope is completed
- check what files are available for a completed envelope
- verify or validate signatures in a signed PDF file
- check whether a PDF has been tampered with after signing
- inspect signer identity, signing time, or certificate details in a PDF
- look up a template and its fields
- render a template with filled-in field values to produce a document
- send a rendered template document for signature using its file key
- compare two versions of a contract to identify differences
- compare a draft contract against a standard baseline document
- check what changed between two PDF files
- add attachments (reference files) to a draft envelope
- delete attachments from a draft envelope before it is sent
- add CC (carbon copy) recipients to a draft or in-progress envelope
- remove CC recipients from a draft envelope
- add signers to a draft envelope
- remove signers from a draft envelope

Example requests:

- "Send this contract to John for signature"
- "Start a signing workflow for this PDF"
- "Send this agreement to Alice and Bob"
- "Create a draft envelope called Offer Letter"
- "Get me a sender view link for envelope abc123"
- "Open the envelope preparation page so I can add files and signers"
- "What is the status of envelope abc123?"
- "Who has signed and who is still pending for this envelope?"
- "Remind the signers of envelope abc123 to sign"
- "Cancel envelope abc123, the signer info was wrong"
- "Download the signed files for envelope abc123"
- "Get me the signed PDF and certificate for this envelope"
- "Verify the signatures in this PDF"
- "Check if this signed PDF has been tampered with"
- "Who signed this document and when?"
- "What fields does template abc123 have?"
- "Render template abc123 with these values and send it to Alice for signing"
- "Use template abc123 to generate a contract and send it to Bob"
- "Compare these two contract PDFs and show me the differences"
- "Check what changed between contract_v1.pdf and contract_v2.pdf"
- "Compare this draft against our standard template"
- "I need to review the changes between the old and new version of this agreement"
- "Add this file as an attachment to envelope abc123"
- "Remove the attachment fileKey1 from envelope abc123"
- "Add alice@example.com as a CC recipient to envelope abc123"
- "Remove bob@example.com from the CC list of envelope abc123"
- "Add Bob Smith as a signer to envelope abc123"
- "Remove alice@example.com from the signer list of envelope abc123"

## Installation

Use the external CLI through `npx`:

```bash
npx @esignglobal/envelope-cli <command>
```

## Setup

Before calling any send action, set `ESIGNGLOBAL_APIKEY` in the shell environment.
If the user does not already have an api key, direct them to:

1. Sign in at `https://www.esignglobal.com?source=agent`
2. Open `Settings -> Integration -> Apps`
3. Create an application and copy the generated api key

```bash
# Windows PowerShell
$env:ESIGNGLOBAL_APIKEY="your_api_key"

# macOS / Linux
export ESIGNGLOBAL_APIKEY="your_api_key"

# Verify connectivity
npx @esignglobal/envelope-cli config health
```

Credential handling rules:

- The CLI reads credentials only from `ESIGNGLOBAL_APIKEY`
- Do not implement local credential storage inside this skill
- Do not print or persist secrets


## External CLI Pattern

Use the external command-line tool instead of bundled scripts:

```bash
npx @esignglobal/envelope-cli create-envelope --subject <subject> [--remark <remark>] [--expire <seconds>] [--redirect-url <url>] [--callback-url <url>]
```

```bash
npx @esignglobal/envelope-cli sender-view --envelope-id <envelopeId> --return-url <url> [--starting-page <page>] [--submit-action <action>] [--no-back-button] [--lock <document|signerInfo>]
```

```bash
npx @esignglobal/envelope-cli send-envelope --file <filePath> --signers '<signersJson>' [--subject <subject>] --confirm
```

```bash
npx @esignglobal/envelope-cli send-envelope --file-key <fileKey> --signers '<signersJson>' [--subject <subject>] --confirm
```

```bash
npx @esignglobal/envelope-cli get-template --template-id <templateId>
```

```bash
npx @esignglobal/envelope-cli render-template --template-id <templateId> [--file-name <name>] [--fields '<fieldsJson>'] [--callback-url <url>]
```

```bash
npx @esignglobal/envelope-cli get-render-result --task-id <taskId>
```

```bash
npx @esignglobal/envelope-cli get-envelope --envelope-id <envelopeId>
```

```bash
npx @esignglobal/envelope-cli urge-envelope --envelope-id <envelopeId>
```

```bash
npx @esignglobal/envelope-cli cancel-envelope --envelope-id <envelopeId> --reason <reason> --confirm
```

```bash
npx @esignglobal/envelope-cli download-envelope --envelope-id <envelopeId> --type list
```

```bash
npx @esignglobal/envelope-cli verify-signature --file <filePath>
```

```bash
npx @esignglobal/envelope-cli contract-compare (--standard-file <filePath> | --standard-file-key <key>) (--comparative-file <filePath> | --comparative-file-key <key>) [--filter-header-footer] [--filter-symbols <sym1,sym2,...>]
```

```bash
npx @esignglobal/envelope-cli add-attachments --envelope-id <envelopeId> --file-keys '<fileKeysJson>'
```

```bash
npx @esignglobal/envelope-cli delete-attachments --envelope-id <envelopeId> --file-keys '<fileKeysJson>' --confirm
```

```bash
npx @esignglobal/envelope-cli add-cc --envelope-id <envelopeId> --cc-infos '[{"userEmail":"...","userName":"..."}]'
```

```bash
npx @esignglobal/envelope-cli delete-cc --envelope-id <envelopeId> --cc-infos '[{"userEmail":"..."}]' --confirm
```

```bash
npx @esignglobal/envelope-cli add-signers --envelope-id <envelopeId> --signers '[{"userName":"...","userEmail":"...","signOrder":1}]'
```

```bash
npx @esignglobal/envelope-cli delete-signers --envelope-id <envelopeId> --signers '[{"userEmail":"..."}]' --confirm
```

Check available commands if needed:

```bash
npx @esignglobal/envelope-cli help
```

### Create envelope example

```bash
npx @esignglobal/envelope-cli create-envelope --subject "Service Agreement" --remark "Please review and send" --expire 604800
```

### Sender view example

```bash
# Step 1: create a draft envelope
npx @esignglobal/envelope-cli create-envelope --subject "Offer Letter"

# Step 2: get the interactive sender view URL
npx @esignglobal/envelope-cli sender-view --envelope-id <envelopeId> --return-url "https://app.example.com/done"
```

### Send envelope example

```bash
npx @esignglobal/envelope-cli send-envelope --file "C:\\docs\\contract.pdf" --signers '[{"userName":"Bob Smith","userEmail":"bob@example.com"}]' --subject "Please sign this contract" --confirm
```

### Get envelope example

```bash
npx @esignglobal/envelope-cli get-envelope --envelope-id abc123
```

### Urge envelope example

```bash
# Send a reminder to pending signers (rate limit: once per 30 minutes per envelope)
npx @esignglobal/envelope-cli urge-envelope --envelope-id abc123
```

### Cancel envelope example

```bash
npx @esignglobal/envelope-cli cancel-envelope --envelope-id abc123 --reason "Signer information was incorrect." --confirm
```

### Download envelope example

```bash
# List signed files and their individual download URLs (requires envelope to be completed)
npx @esignglobal/envelope-cli download-envelope --envelope-id abc123 --type list
```

### Verify signature example

```bash
npx @esignglobal/envelope-cli verify-signature --file "/tmp/signed_contract.pdf"
```

### Add attachments example

```bash
# Add two attachments to a draft envelope
npx @esignglobal/envelope-cli add-attachments \
  --envelope-id abc123 \
  --file-keys '["fileKey1","fileKey2"]'
```

### Delete attachments example

```bash
# Remove an attachment from a draft envelope
npx @esignglobal/envelope-cli delete-attachments \
  --envelope-id abc123 \
  --file-keys '["fileKey1"]' \
  --confirm
```

### Add CC example

```bash
# Add CC recipients to a draft or in-progress envelope
npx @esignglobal/envelope-cli add-cc \
  --envelope-id abc123 \
  --cc-infos '[{"userEmail":"alice@example.com","userName":"Alice"}]'
```

### Delete CC example

```bash
# Remove a CC recipient from a draft envelope
npx @esignglobal/envelope-cli delete-cc \
  --envelope-id abc123 \
  --cc-infos '[{"userEmail":"alice@example.com"}]' \
  --confirm
```

### Add signers example

```bash
# Add two signers to a draft envelope with sequential signing order
npx @esignglobal/envelope-cli add-signers \
  --envelope-id abc123 \
  --signers '[{"userName":"Bob Smith","userEmail":"bob@example.com","signOrder":1},{"userName":"Alice Jones","userEmail":"alice@example.com","signOrder":2}]'
```

### Delete signers example

```bash
# Remove a signer from a draft envelope
npx @esignglobal/envelope-cli delete-signers \
  --envelope-id abc123 \
  --signers '[{"userEmail":"bob@example.com"}]' \
  --confirm
```

### Contract compare example

```bash
# Compare two local PDF files
npx @esignglobal/envelope-cli contract-compare \
  --standard-file "/tmp/contract_v1.pdf" \
  --comparative-file "/tmp/contract_v2.pdf"

# Compare using existing file keys
npx @esignglobal/envelope-cli contract-compare \
  --standard-file-key "standardFileKey" \
  --comparative-file-key "comparativeFileKey"

# Ignore page headers/footers and specific punctuation
npx @esignglobal/envelope-cli contract-compare \
  --standard-file "/tmp/contract_v1.pdf" \
  --comparative-file "/tmp/contract_v2.pdf" \
  --filter-header-footer \
  --filter-symbols ".,。、"
```

### Template example

```bash
# Step 1: inspect the template fields
npx @esignglobal/envelope-cli get-template --template-id <templateId>

# Step 2: render the template with field values
npx @esignglobal/envelope-cli render-template --template-id <templateId> --fields '[{"fieldId":"<fieldId>","fieldValue":"<value>"}]'

# Step 3: poll until taskStatus is Succeeded (2)
npx @esignglobal/envelope-cli get-render-result --task-id <taskId>

# Step 4: send the rendered document for signing using the returned fileKey
npx @esignglobal/envelope-cli send-envelope --file-key <fileKey> --signers '[{"userName":"Bob Smith","userEmail":"bob@example.com"}]' --subject "Please sign this document" --confirm
```

## Required Configuration

- Node.js 18 or later
- Access to the trusted external CLI, either preinstalled or available through `npx`
- `ESIGNGLOBAL_APIKEY` must already be configured in the shell environment

## Create Envelope Workflow

1. Collect a subject from the user; optionally collect remark, expiry, redirect URL, and callback URL
2. Run `create-envelope` to create a draft envelope (status `0`)
3. Return the `envelopeId` — it is needed for `sender-view` or further configuration

## Sender View Workflow

1. Obtain a draft `envelopeId` (status `0`) from the user or a previous `create-envelope` response
2. Collect a `return-url` from the user (required — the page to redirect to after the sender submits)
3. Optionally collect `--starting-page`, `--submit-action`, `--no-back-button`, or `--lock` preferences
4. Run `sender-view` to retrieve the interactive URL
5. Present the URL to the user — they can open it in a browser or embed it in an iframe to add documents, configure signers, and send the envelope

### Safety Rules

- Only call `sender-view` for envelopes in Draft status (`0`); other statuses will be rejected by the API
- Never follow or open the returned URL automatically; present it to the user for their action
- Do not store or log the `tcode` token embedded in the URL

### Required Inputs

- `envelopeId`: draft envelope ID (status `0`)
- `returnUrl`: valid https/http URL, max 2048 characters

## Send Envelope Workflow

Two modes are supported — provide exactly one of `--file` or `--file-key`:

- `--file <filePath>` — upload and send a local PDF file
- `--file-key <fileKey>` — send a file already on the server (e.g. from `get-render-result`)

1. Determine whether the user has a local file or an existing `fileKey`
2. Collect signer list and optional `subject`
3. If using `--file`, confirm the file is a `.pdf` at an absolute path
4. Run the external CLI command with `--confirm`
5. Return the CLI result to the user

### Safety Rules

- Only use a file path the user explicitly provided for this task
- Only handle one local PDF file per run
- Refuse relative paths; require an absolute path to a `.pdf` file
- Reject any non-PDF file before invoking the CLI
- Never print or persist secrets
- Do not scan directories, expand globs, or discover files on the user's behalf
- Only call the trusted eSignGlobal CLI configured for this environment
- `--file` and `--file-key` are mutually exclusive

### Required Inputs

- `filePath` (or `fileKey`): absolute path to an existing local PDF file, or an existing file key
- `signers`: JSON array of signer objects
- `subject`: optional email or envelope subject

Each signer must include:
- `userName`
- `userEmail`

Optional field:
- `signOrder` as an integer `>= 1`


### filePath

`filePath` must be an absolute path to an existing local PDF file.

Example:

```text
/tmp/contract.pdf
```

### signers

Each signer must include:

- `userName`
- `userEmail`

Optional field:

- `signOrder` (integer, minimum `1`)

Single signer example:

```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com"
  }
]
```

Sequential signing example:

```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com",
    "signOrder": 1
  },
  {
    "userName": "Alice Jones",
    "userEmail": "alice@example.com",
    "signOrder": 2
  }
]
```

Parallel signing example:

```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com",
    "signOrder": 1
  },
  {
    "userName": "Alice Jones",
    "userEmail": "alice@example.com",
    "signOrder": 1
  }
]
```

## Template Workflow

1. Run `get-template` to inspect the template fields (`fieldId`, `fieldName`, `fieldType`, `required`)
2. Run `render-template` with the collected field values — returns a `taskId`
3. Run `get-render-result` and poll until `taskStatus` is `Succeeded (2)` — returns a `fileKey`
4. Run `send-envelope --file-key` with the `fileKey` to send the rendered document for signing

### Safety Rules

- Only fill field values the user has explicitly provided
- Do not invent or guess field values
- `--file` and `--file-key` are mutually exclusive; use `--file-key` when a fileKey is already available

### Required Inputs

- `templateId`: template ID provided by the user
- `fields`: array of `{ fieldId, fieldValue }` for required fields
- `signers`: signer list (same format as Send Envelope Workflow)

## Get Envelope Workflow

1. Obtain the `envelopeId` from the user or a previous `send-envelope` response
2. Run `get-envelope` to retrieve full envelope details
3. Present the status, signer progress, and document list to the user using the **Get Envelope Output Format** below

Envelope status codes: `0=Draft`, `1=In Progress`, `2=Completed`, `3=Expired`, `4=Declined`, `5=Canceled`

Signer status codes: `0=Pending`, `1=Signing`, `2=Signed`

### Get Envelope Output Format

Always present `get-envelope` results using this exact template:

```
🔍 Contract Details: [subject]

Current Status: [envelope_status_icon] [envelope_status_label]

Signing Progress:
● [icon] Initiator: [initiator.userName] ([initiator_status_label])
● [icon] Signer N: [userName] ([signer_status_label]) [bottleneck_marker]
● [icon] CC: [ccName] ([cc_status_label])
```

**Envelope status icon and label mapping:**

| Code | Icon | Label |
|------|------|-------|
| 0 | ⚪ | Draft |
| 1 | ⏳ | Waiting for Others |
| 2 | ✅ | Completed |
| 3 | ❌ | Expired |
| 4 | ❌ | Declined |
| 5 | ❌ | Canceled |

**Initiator:** always show as `✅ Sent`

**Signer status icon and label mapping:**

| Code | Icon | Label |
|------|------|-------|
| 0 | ⚪ | Pending |
| 1 | ⏳ | Signing |
| 2 | ✅ | Signed |

**Bottleneck marker:** append `<- Current Bottleneck` to the first signer whose status is `0` (Pending) or `1` (Signing) when the envelope is In Progress.

**CC status:** always show as `⚪ Pending Sync` if envelope is not yet Completed, `✅ Synced` if Completed.

**Rules:**
- Omit the CC row if `ccInfos` is empty
- Number signers sequentially: Signer 1, Signer 2, …
- Use `[subject]` from the envelope response as the file name
- Always use this format — never use a table or other layout for `get-envelope` output

## Urge Envelope Workflow

1. Confirm the envelope is in progress (status `1`) before sending a reminder
2. Run `urge-envelope` to notify all pending signers
3. Inform the user that reminders are rate-limited to once every 30 minutes per envelope

## Cancel Envelope Workflow

1. Confirm the reason for cancellation with the user before proceeding
2. Run `cancel-envelope` with `--confirm` — cancellation is irreversible
3. After cancellation the envelope is suspended and all signatures within it are invalid

## Download Envelope Workflow

1. Obtain the `envelopeId` from a previous `send-envelope` response or from the user
2. Run `--type list` to check envelope status and retrieve individual file download URLs
3. If `envelopeStatus` is `2` (Completed), share the `downloadUrl` for each file with the user
4. If the envelope is not yet completed, inform the user and wait

Envelope status codes: `0=Draft`, `1=Signing`, `2=Completed`, `3=Expired`, `4=Rejected`, `5=Voided`

File types in the list response:
- `CONTRACT` — the signed document
- `CERTIFICATE` — the signing audit certificate
- `ATTACHMENT` — any attachments
- `COMBINED` — merged PDF (if enabled on the account)

> Individual file download URLs are valid for **60 minutes**. Download can only proceed when the envelope is Completed.

## Verify Signature Workflow

1. Obtain an absolute path to a local PDF file from the user
2. Run `verify-signature` — no API key required, verification runs entirely offline
3. Parse and present the JSON result to the user

The command outputs:
- `integrity` — `true` (unmodified) / `false` (tampered) / `null` (unknown)
- `signatureCount` — number of signatures found
- Per-signature fields:
  - `isValid` — `true` / `false` / `null`
  - `signer` — common name from the signing certificate
  - `declaredTime` — signing time (trusted timestamp preferred over local clock), UTC+08:00
  - `signatureAlgorithm` — e.g. `RSA / SHA-256`
  - `timestampIssuer` — TSA certificate issuer, or `"Local time"` when no trusted timestamp is present
  - `certificate.serialNumber`, `certificate.validFrom`, `certificate.validUntil`

> `verify-signature` works fully offline and does **not** require `ESIGNGLOBAL_APIKEY`.

## Contract Compare Workflow

1. Determine whether the user has local PDF files or existing file keys for both the standard (baseline) and comparative documents
2. Optionally collect `--filter-header-footer` preference and any punctuation to ignore via `--filter-symbols`
3. Run `contract-compare` — if local paths are provided, the CLI uploads them automatically before comparing
4. Return the `contractCompareUrl` to the user so they can open it in a browser to review highlighted differences

### Safety Rules

- Only use file paths the user explicitly provided for this task
- Require absolute paths to `.pdf` files when local files are given
- `--standard-file` and `--standard-file-key` are mutually exclusive; same for the comparative pair
- Never follow or open the returned URL automatically; present it to the user for their action
- Supports PDF files up to 30 MB each

### Required Inputs

- `standardFile` (or `standardFileKey`): absolute path to the baseline PDF, or an existing file key
- `comparativeFile` (or `comparativeFileKey`): absolute path to the PDF to compare against, or an existing file key

### Optional Inputs

- `--filter-header-footer`: exclude headers and footers from comparison
- `--filter-symbols`: comma-separated punctuation marks to ignore (e.g. `".,。、"`)

### Contract Compare Output Format

Present the result using this exact template:

```
**Contract Comparison Ready**

Open the link below to view highlighted differences between the two documents:

[contractCompareUrl]

Comparison ID: {contractCompareBizId}
```

Rules:
- Always display the full URL on its own line so the user can click or copy it
- Always show the `contractCompareBizId` for reference
- Do not attempt to parse or summarize the differences — the comparison page handles that visually

## Add Attachments Workflow

1. Obtain a draft `envelopeId` (status `0`) from the user or a previous `create-envelope` response
2. Collect the list of `fileKey` strings to attach (upload files first via the Upload Documents API if needed)
3. Run `add-attachments` with the envelope ID and file keys JSON array
4. Return the result to the user

### Safety Rules

- Only add attachments when the envelope is in Draft status (`0`)
- Do not upload or discover files on the user's behalf; require explicit file keys from the user
- Attachments are reference-only and are not signed

## Delete Attachments Workflow

1. Obtain the `envelopeId` and the `fileKey` values to remove from the user
2. Confirm the deletion with the user before proceeding — it cannot be undone once the envelope is sent
3. Run `delete-attachments` with `--confirm`
4. Return the result to the user

### Safety Rules

- Attachments can only be deleted before the envelope is initiated
- Always require `--confirm` before proceeding
- Never delete attachments the user has not explicitly listed

## Add CC Workflow

1. Obtain the `envelopeId` from the user or a previous `create-envelope` / `send-envelope` response
2. Collect the list of CC recipients — each must have `userEmail` and `userName`
3. Run `add-cc` — supported for envelopes in Draft (`0`) or In Progress (`1`) status
4. Return the updated CC list to the user

### Safety Rules

- The same email address cannot be added as CC more than once; the API will reject duplicates
- CC recipients can only view the envelope — they cannot sign
- `userName` must not contain these special characters: `/ \ : * " < > | ？` or emoji

### Required Inputs

- `envelopeId`: envelope ID (Draft or In Progress)
- `ccInfos`: JSON array of `{ userEmail, userName }` objects

## Delete CC Workflow

1. Obtain the `envelopeId` and the email addresses of CC recipients to remove from the user
2. Confirm the deletion with the user before proceeding
3. Run `delete-cc` with `--confirm` — only supported for envelopes in Draft status (`0`)
4. Return the remaining CC list to the user

### Safety Rules

- CC recipients can only be deleted from envelopes in Draft status (`0`)
- Always require `--confirm` before proceeding
- Never remove CC recipients the user has not explicitly listed

### Required Inputs

- `envelopeId`: draft envelope ID (status `0`)
- `ccInfos`: JSON array of `{ userEmail }` objects to remove

## Add Signers Workflow

1. Obtain a draft `envelopeId` (status `0`) from the user or a previous `create-envelope` response
2. Collect the list of signers — each must have `userName`, `userEmail`, and `signOrder`
3. Run `add-signers` — new signers can only be appended after existing ones; inserting before a current or completed signer is rejected by the API
4. Return the updated signer list to the user

### Safety Rules

- Only add signers when the envelope is in Draft status (`0`)
- The same email address cannot be added twice (use delete then re-add to update)
- Maximum 10 signers per envelope
- `userName` must not contain these special characters: `/ \ : * " < > | ?` or emoji

### Required Inputs

- `envelopeId`: draft envelope ID (status `0`)
- `signers`: JSON array of `{ userName, userEmail, signOrder }` objects

### Optional Signer Fields

- `businessId`: developer-defined business number
- `deliveryMethods`: `auto` (default), `none`, `email`, `sms`, `WhatsApp`
- `freeFormSign`: `true` to allow free stamp/signature placement
- `authModes`: `noAuth` (default), `accessCode`, `sms`, `emailAuth`, etc.

## Delete Signers Workflow

1. Obtain the `envelopeId` and the email addresses of signers to remove from the user
2. Confirm the deletion with the user before proceeding
3. Run `delete-signers` with `--confirm` — only supported for envelopes in Draft status (`0`)
4. Return the remaining signer list to the user

### Safety Rules

- Signers can only be deleted from envelopes in Draft status (`0`)
- Always require `--confirm` before proceeding
- Never remove signers the user has not explicitly listed

### Required Inputs

- `envelopeId`: draft envelope ID (status `0`)
- `signers`: JSON array of `{ userEmail }` objects to remove

## Output

Return the external CLI result. Do not bundle or implement upload logic inside this skill.

### Verify Signature Output Format

Present each signature using this exact template:

```
**Signature is VALID** 
(or **Signature is INVALID** / **Signature status unknown** )

**Signer:**
{signer}

**Signing Time:**
{declaredTime}

**Signature Time Source:**
{timestampIssuer}

**Signature Algorithm:**
{signatureAlgorithm}

---

**Signer Certificate**

**Serial Number:**
{certificate.serialNumber}

**Valid From:**
{certificate.validFrom}

**Valid Until:**
{certificate.validUntil}
```

Rules:
- Use no emoji for `isValid === true` or `isValid === false`;`
- Repeat the block for each signature if `signatureCount > 1`
- If `signatureCount === 0`, output: "No signatures found in this PDF"

## Support

If you encounter any issues during invocation, visit the official website at https://www.esignglobal.com?source=agent to submit a support ticket.
