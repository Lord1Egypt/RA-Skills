# Nota Sign Skill

This skill lets Codex send documents for signature through Nota Sign.

`SKILL.md` is the agent-facing source of truth. This `README.md` is a concise operator guide for installing, configuring, and running the bundled script manually.

## What It Does

- sends a supported local file or URL for signature
- sends an uploaded attachment when it resolves to a real local file path
- supports one or more signers
- stores credentials in `~/.notasign/config.json`
- supports `PROD` and `UAT`
- can temporarily bootstrap `node@20` when the local `node` version is below 18

## Requirements

- preferred: Node.js 18 or newer
- fallback: local `npx` available so the skill can temporarily fetch `node@20` and `tsx`
- network access to Nota Sign API
- network access to npm when runtime fallback is needed
- supported file formats: `doc`, `docx`, `pdf`, `xls`, `xlsx`, `bmp`, `png`, `jpg`, `jpeg`
- max size for local files and uploaded attachments: `100MB`
- valid Nota Sign credentials:
  - `appId`
  - `appKey`
  - `userCode`
  - `serverRegion`
  - optional `environment`

## Quick Start

All commands below assume you are in the skill directory.
When installed by Codex, that is usually:

```bash
cd ~/.codex/skills/notasign
```

Initialize credentials:

```bash
npx tsx scripts/send_envelope.ts init
```

Interactive send:

```bash
npx tsx scripts/send_envelope.ts
```

Direct send:

```bash
npx tsx scripts/send_envelope.ts \
  --file /path/to/document.pdf \
  --signers '[{"userName":"Daniel","userEmail":"daniel@example.com"}]' \
  --subject "Newsletter"
```

If `node -v` is below `18`, use this fallback for the current run only:

```bash
npx -y -p node@20 -p tsx -c 'tsx scripts/send_envelope.ts \
  --file /path/to/document.pdf \
  --signers '"'"'[{"userName":"Daniel","userEmail":"daniel@example.com"}]'"'"' \
  --subject "Newsletter"'
```

For initialization with the same fallback:

```bash
npx -y -p node@20 -p tsx -c 'tsx scripts/send_envelope.ts init'
```

## Config File

The script reads `./notasign-config.json` first and falls back to `~/.notasign/config.json`.

Example:

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
- set `environment` to `UAT` for test endpoints
- `PROD` and `UAT` do not share the same credential set
- when switching environments, replace `appId`, `appKey`, `userCode`, and `serverRegion` with values issued for that target environment
- changing only `"environment": "PROD"` to `"environment": "UAT"` is not enough
- protect the file with `chmod 600 ~/.notasign/config.json`

## Parameters

- `--file`, `-f`: local file path, uploaded attachment path, or `http(s)` URL
- `--signers`: JSON array of `{ "userName": "...", "userEmail": "..." }`
- `--subject`, `-s`: optional subject; defaults to the file name

## Regions

| Region | Description |
| --- | --- |
| `CN` | China |
| `AP1` | Singapore |
| `AP2` | Hong Kong |
| `EU1` | Frankfurt |

## Common Tasks

Configure credentials:

```bash
npx tsx scripts/send_envelope.ts init
```

Send to one signer:

```bash
npx tsx scripts/send_envelope.ts \
  --file /path/to/file.pdf \
  --signers '[{"userName":"Alice","userEmail":"alice@example.com"}]'
```

Send to multiple signers:

```bash
npx tsx scripts/send_envelope.ts \
  --file /path/to/file.pdf \
  --signers '[{"userName":"Alice","userEmail":"alice@example.com"},{"userName":"Bob","userEmail":"bob@example.com"}]' \
  --subject "Contract review"
```

## Troubleshooting

- If the script says config is missing, run `npx tsx scripts/send_envelope.ts init`
- If the file path fails, verify the local path exists, the uploaded attachment resolves to a real local file, or use a valid `http(s)` URL
- If the file type is rejected, use one of: `doc`, `docx`, `pdf`, `xls`, `xlsx`, `bmp`, `png`, `jpg`, `jpeg`
- If the local file or attachment is larger than `100MB`, reduce it before sending
- If local Node.js is below `18`, run with `npx -y -p node@20 -p tsx -c 'tsx scripts/send_envelope.ts ...'`
- If the API rejects the request, confirm region, environment, and credentials are correct
