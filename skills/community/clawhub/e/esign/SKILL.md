---
name: esign
description: Send files for e-signature with Nota Sign. Use for requests to send an envelope, initiate signing, send a signing link, configure Nota Sign credentials, or send a local file, uploaded attachment, or URL for signature in either PROD or UAT. Handles credential setup, environment selection, file validation, signer collection, and execution through scripts/send_envelope.ts, with a temporary node@20 fallback when local Node.js is below 18.
version: 1.0.2
category: Integration
framework: typescript
runtime: nodejs
---

# Nota Sign

Use this skill when the user wants to send a supported file for signature through Nota Sign.

## Supported tasks

- Send a supported local file, uploaded attachment, or URL for signature
- Collect one or more signer names and emails
- Initialize Nota Sign credentials on first use
- Update or replace existing credentials when the user explicitly asks
- Send in `PROD` or `UAT` environment

## Inputs

Collect only the missing fields.

Required to send:
- file path, uploaded attachment path, or URL
- at least one signer with `userName` and `userEmail`

Supported file formats:
- `doc`, `docx`, `pdf`, `xls`, `xlsx`, `bmp`, `png`, `jpg`, `jpeg`

Size limit:
- local files and uploaded attachments must be `<= 100MB`

Optional:
- `subject`
Default to the file name when the user does not provide one.

Required only when config is missing or the user asks to reconfigure:
- `appId`
- `appKey` as Base64 PKCS#8 RSA private key
- `userCode`
- `serverRegion` in `CN | AP1 | AP2 | EU1`
- `environment` in `PROD | UAT`
Default to `PROD`.

Important:
- `PROD` and `UAT` require separate credential sets
- do not assume a `PROD` `appId`, `appKey`, `userCode`, or `serverRegion` can be reused in `UAT`
- do not assume a `UAT` `appId`, `appKey`, `userCode`, or `serverRegion` can be reused in `PROD`
- if the user switches environments, treat it as a full reconfiguration and collect the full target-environment credential set

## Workflow

1. Check whether `./notasign-config.json` exists; if not, check `~/.notasign/config.json`.
2. If config is missing, ask only for the missing credential fields and write the config file.
3. If the user wants to switch between `PROD` and `UAT`, do not only flip `environment`. Collect the full target-environment values for `appId`, `appKey`, `userCode`, and `serverRegion`, then rewrite the config.
4. Validate the file input before sending:
   - local path must exist, or
   - uploaded attachment must resolve to a real local file path, or
   - remote input must start with `http://` or `https://`
5. Validate the file type against the supported list: `doc`, `docx`, `pdf`, `xls`, `xlsx`, `bmp`, `png`, `jpg`, `jpeg`.
6. Reject local files and uploaded attachments larger than `100MB`.
7. If the user uploaded a supported file in chat, treat it as a valid file input when the client exposes a real attachment path. If no real path or URL is available, ask the user for the original file path or a URL instead of guessing.
8. Normalize signer input into JSON:

```json
[{"userName":"Alice","userEmail":"alice@example.com"}]
```

9. Check the local Node.js major version before execution.
10. If `node` exists and the major version is `18+`, run:

```bash
npx tsx scripts/send_envelope.ts --file "PATH_OR_URL" --signers '[{"userName":"Alice","userEmail":"alice@example.com"}]' --subject "Optional subject"
```

11. If local Node.js is missing or below `18`, temporarily download `node@20` and `tsx` for this run only:

```bash
npx -y -p node@20 -p tsx -c 'tsx scripts/send_envelope.ts --file "PATH_OR_URL" --signers '"'"'[{"userName":"Alice","userEmail":"alice@example.com"}]'"'"' --subject "Optional subject"'
```

12. Use the same fallback pattern for `init`:

```bash
npx -y -p node@20 -p tsx -c 'tsx scripts/send_envelope.ts init'
```

13. On success, return the envelope ID and basic send summary.
14. On failure, surface the exact validation or API error and state the next required action.

## Config File

The shared config normally lives at `~/.notasign/config.json`. The script also supports a local override at `./notasign-config.json`.

Write the config in this shape:

```json
{
  "appId": "your_app_id",
  "appKey": "base64_pkcs8_private_key",
  "userCode": "your_user_code",
  "serverRegion": "AP1",
  "environment": "PROD"
}
```

Notes:
- `environment` is optional and defaults to `PROD`
- the config stores one environment's credential set at a time
- switching from `PROD` to `UAT`, or from `UAT` to `PROD`, requires replacing `appId`, `appKey`, `userCode`, and `serverRegion` with the target environment's values
- do not switch environments by editing only the `environment` field
- do not echo secrets back to the user after writing the config
- do not overwrite an existing config unless the user asks to change credentials
- if the temporary runtime fallback is needed, it requires network access to npm

## Response Style

- Ask concise follow-up questions only for missing information.
- Prefer one grouped question instead of several small questions.
- Do not ask for `subject` if the file name is good enough.
- Do not invent emails, file paths, or credential values.
- Keep credentials and private keys out of normal responses.
- Prefer the direct `scripts/send_envelope.ts` command with a runtime check instead of inventing wrappers or extra helper files.
- For user-uploaded files, prefer the attachment's real local path when available. If the attachment exists only as visual context and no path is available, ask for the original file path or URL.
- Reject unsupported file types and local or attachment files above `100MB` before trying to send.

## Examples

This skill should trigger for requests like:

English:

- "Send this file for signature with Nota Sign"
- "Send the file I just uploaded to Daniel with Nota Sign"
- "Use Nota Sign UAT to send this document to two signers"

Chinese:

- "用 Nota Sign 发个信封给 Daniel，附件是 contract.pdf"
- "把我刚上传的文件用 Nota Sign 发给 Daniel"
- "帮我发起电子签署"
