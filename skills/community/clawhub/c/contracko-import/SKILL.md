---
name: contracko-import
description: Imports contracts into Contracko from disk, Google Drive, SharePoint, Box or a URL. Use to onboard, migrate, bulk-upload, or file a signed PDF.
---

# Importing contracts into Contracko

Onboarding is this skill plus types in [contracko](../contracko/SKILL.md). Find and file here. Shape types after extraction, not before.

## Find the files first

Contracko MCP does not browse disks or cloud drives. Use the file, Google Drive, SharePoint, Box or OneDrive tools *you already have*. If you have none, ask the user to share the folder, attach files, or paste a signed download link.

1. Ask where the contracts live. Typical: a laptop folder, Google Drive, SharePoint, Box, email exports.
2. List candidates. Keep PDFs and DOCX (and the other ingest types). Skip obvious noise (photos of whiteboards, duplicate `final-final-v3`).
3. Group related files before filing: an MSA with its SOWs, a signed copy next to an unsigned draft. Say the grouping out loud. Nothing in Contracko detects it for you.
4. Confirm workspace, count and names before a bulk send. A single file they just handed you needs no ceremony.

Do not publish a confidential file to a public URL so `remote` import works. A signed or authenticated link from their own store is the remote path.

## Getting the bytes there

MCP has no file transfer, so a document on the user's disk reaches Contracko one of three ways, and the choice is forced by where the file is and how big it is. Decide this first, before anything else.

| The file is | Use | Why |
|---|---|---|
| small, and you want Contracko's own extraction | `clm_import_contracts` with `kind: "inline"` | base64 travels through your context: roughly 1.4x the file size in characters, so a 50 KB PDF costs around 17k tokens. Fine for one contract, ruinous for twenty. |
| large, or a batch, or you have already read it | `clm_create_upload_url` → PUT → `clm_ingest_contract` | the bytes go machine-to-machine and never touch your context. You supply the metadata, and you can supply the analysis too. |
| already behind a URL Contracko can fetch | `clm_import_contracts` with `kind: "remote"` | Contracko downloads it directly. Extraction runs, nothing passes through you. |

**Never publish a contract to a public URL to make `remote` work.** A signed or authenticated link from the user's own document store is what that option is for. Putting a confidential agreement on a public host to save a step is a worse outcome than any of the friction it avoids.

The gap worth knowing: there is no option that combines "bytes bypass your context" with "Contracko runs its own extraction". Upload prepares a reference only `clm_ingest_contract` accepts, and import has no way to take that reference. So for a local file you are choosing between paying context for Contracko's extraction, or doing the extraction yourself.

Requires `contract:write`. Where the tools are absent from your list, the credential is the problem: see the [contracko](../contracko/SKILL.md) skill.

If the document is already associated with a contract the user can see, import and ingest return a duplicate conflict instead of a second copy. Tell them which contract holds it. Only retry with `allowDuplicate: true` if they insist on another copy.

To add a file to an *existing* contract (draft, related, or replace the primary), use `clm_add_contract_documents` with a new idempotency key. That is not an import.

## Confirm before writing

Nothing here can be undone. Contracko deliberately keeps delete and archive out of an agent's hands, so a batch sent to the wrong workspace is cleaned up by hand in the web app, one record at a time.

Before a bulk import, put three things in front of the user and wait: the workspace `auth_validate` reports, how many documents you are about to send, and what they are. A single file the user just handed you needs no ceremony. Fifty files out of a shared drive does.

## Managed import

One call per batch, up to 100 documents, one managed contract per document.

```json
{
  "idempotencyKey": "migration-2026-09-batch-01",
  "files": [
    {"kind": "inline", "fileName": "vendor-msa.pdf", "mimeType": "application/pdf", "dataBase64": "..."}
  ]
}
```

Files are `inline` base64 (encoded total under 25,690,112 characters) or `remote` with a `downloadUrl` and `fileSize`, 25 MiB each.

The `idempotencyKey` is bound to the payload. Replaying it with the same files returns the original import; replaying it with different files returns a 409, which says the key is spent rather than that the import failed. One key per batch, named so a human can recognise it later.

Then poll `clm_get_import_status` with the returned `importId`, waiting `pollAfterMs` between calls. Extraction takes minutes rather than seconds, and scales with the batch. Report progress while `status` is `processing`, and hold the success message until the documents are actually filed.

Per document you get `status`, a `contractId` as soon as the record exists, and on failure an `errorCode` with a `retryable` flag. Retry what is marked retryable, under a new key, and treat the rest as documents that need a human.

### What extraction gives you for free

Worth telling the user, because it changes what they should do first. On a plain NDA, in a workspace with no configuration at all, the import produced:

- title, start and end dates, renewal and notice terms
- both parties, created as counterparty records and linked with roles
- a new contract type, with custom fields inferred from the document
- governing law, jurisdiction, liability summary, notice instructions
- a full analysis with obligations and risks, through `clm_get_contract_analysis`

So for a first-time user with a folder of contracts: import first, configure after. Hand-built contract types are work the extraction was going to do, and then has to reconcile against. After the batch lands, list types and make them comprehensive — [contracko](../contracko/SKILL.md) owns that half.

New contracts land as `entityStatus: "pending-review"`. Say so. A human is expected to confirm the extraction, and nothing about a successful import marks the data as verified.

Once documents are in, the questions start: renewals, notice dates, risk, and what the workspace now holds. That is [contracko-review](../contracko-review/SKILL.md). If the user also asks to place imported contracts in folders, use the confirmed filing workflow in [contracko](../contracko/SKILL.md).

## Prepare and file

Three steps, per contract.

1. `clm_create_upload_url` with `fileName`, `mimeType` and `fileSize`. Returns a signed destination valid for one hour, and a file reference.
2. `PUT` the bytes to that URL with the matching `Content-Type`, expecting a 200. A plain HTTP request, not a tool call.
3. `clm_ingest_contract` with `externalSystem`, `externalId`, the `contract` object, and the file references, `isPrimary` on the main document.

Accepted: PDF, DOCX, TXT, RTF, JPEG, PNG. 25 MiB per file, 100 files per contract.

### The rule that costs a call

`contract.endDate` is absent from the schema's required list and required anyway. Omit it and the call fails with a 400 whose only detail is `code: "custom"` on `endDate`, which tells you nothing.

The rule: **send `endDate`, or send `isOpenEnded: true`.** A contract with no end date by design is legitimate, and that flag is how you say so.

Four defaults apply silently, so set them from the document rather than letting them land: `status` becomes `active`, `autoRenewing` true, the renewal period 1 year, the notice period 1 month. You have read the contract; use what it says.

`externalSystem` and `externalId` are the source system's identity for this contract, and they are how a re-run recognises what it already filed. Where there is no source system, choose something stable and honest about its origin.

## Working the upload path

The three steps, with the parts that actually trip agents up.

**1. Measure the file without reading it.** You need `fileSize` in bytes and a `mimeType`, and neither requires the contents:

```bash
stat -f%z contract.pdf          # bytes (macOS; stat -c%s on Linux)
file --mime-type -b contract.pdf
```

Reading a PDF to size it defeats the entire point of this path.

**2. PUT the bytes.** `clm_create_upload_url` returns a destination valid for one hour and a reference. Send the file with the `Content-Type` you declared, or the upload is rejected:

```bash
curl -sS -X PUT --upload-file contract.pdf \
  -H "Content-Type: application/pdf" \
  "<uploadUrl>" -o /dev/null -w '%{http_code}'
```

Expect `200`. The bytes go from disk to Contracko without passing through you, which is the whole reason for the detour.

**3. Read the document for its content, not its bytes.** To fill the contract and its analysis you need the text, and text is cheap where base64 is not. Extract it locally:

```bash
pdftotext -layout contract.pdf -      # PDF
textutil -convert txt -stdout f.docx  # DOCX on macOS
```

A 50 KB PDF is perhaps 4k tokens as text against 17k as base64, and the text is the part you can actually reason over.

Then call `clm_ingest_contract` with the reference, the metadata you read off the document, and a filled `summary.analysis`.

### For a folder

Do the loop, one contract per document, and keep the whole file out of your context every time: size it, upload it, extract its text, ingest it, move on. Confirm the batch with the user before starting, as above.

Where several files clearly belong to one agreement, a master and its order forms, or a signed and unsigned copy of the same contract, say so before filing them as unrelated records. Nothing detects that for you, and a migration out of a shared drive is full of it.

## When you ingest, do the extraction properly

A contract filed through ingest does not go through Contracko's extraction pipeline. What lands is what you send, so sending a title and two dates produces a thin record that looks identical to a rich one until someone opens it.

`contract.summary.analysis` is built for exactly this, and it takes far more than most callers give it: `risks[]`, `obligations[]`, `warranties[]`, `riskAllocation[]`, `gaps[]` and `deviations[]`, each with a severity, a headline and an `evidenceQuote`, plus `fieldEvidence` pointing at where each extracted value came from. There is also `proposedCategoryFields` for the custom fields this contract implies.

You have read the document. Fill them. Quote verbatim in every `evidenceQuote`, because those are what the app highlights in the document viewer, and a paraphrase highlights nothing.

An ingest that skips the analysis is the one case where the manual path really is worse than the managed one. Done properly it is equal, and it costs no context.

## When something goes wrong

| Symptom | Reading |
|---|---|
| 409 on a retry | the idempotency key is spent; where the payload is identical, the import already exists, so go look it up |
| stuck in `extracting` | normal for minutes; keep honouring `pollAfterMs` before calling it stuck |
| `retryable: false` on an item | the document itself is the problem, so surface it to the user |
| 400 `code: "custom"` on `endDate` | the open-ended rule above |
| the tools are missing entirely | `contract:write` was not granted |
