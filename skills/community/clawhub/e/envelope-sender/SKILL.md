---
name: envelope-sender
description: Guide agent to send a user-specified local PDF document for signature through eSignGlobal by calling the eSignGlobal CLI tool.eSignGlobal CLI is an agent-friendly CLI — all output is JSON by default, making it easy to parse and chain.
metadata: {"openclaw":{"primaryEnv":"ESIGNGLOBAL_APIKEY"}}
---

# Envelope Sender

Use this skill to send a single local PDF document for signature with eSignGlobal through an external CLI.

## Installation

Use the external CLI through `npx`:

```bash
npx @esignglobal/envelope-cli <command>
```

## Setup

Before calling any send action, set `ESIGNGLOBAL_APIKEY` in the shell environment.

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

## Workflow

1. Collect a single absolute `filePath`, signer list, and optional `subject`
2. Confirm the file is a `.pdf` and the signer data is complete
3. Set `ESIGNGLOBAL_APIKEY` in the current shell session
4. Run the external CLI command to send the envelope
5. Return the CLI result to the user

## Safety Rules

- Only use a file path the user explicitly provided for this task
- Only handle one local PDF file per run
- Refuse relative paths; require an absolute path to a `.pdf` file
- Reject any non-PDF file before invoking the CLI
- Never print or persist secrets
- Do not scan directories, expand globs, or discover files on the user's behalf
- Only call the trusted eSignGlobal CLI configured for this environment

## Required Inputs

- `filePath`: absolute path to an existing local PDF file
- `signers`: JSON array of signer objects
- `subject`: optional email or envelope subject

Each signer must include:
- `userName`
- `userEmail`

Optional field:
- `signOrder` as an integer `>= 1`


## Input Format

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

## External CLI Pattern

Use the external command-line tool instead of bundled scripts:

```bash
npx @esignglobal/envelope-cli send-envelope --file <filePath> --signers '<signersJson>' [--subject <subject>] --confirm
```

Check available commands if needed:

```bash
npx @esignglobal/envelope-cli help
```

Example:

```bash
npx @esignglobal/envelope-cli send-envelope --file "C:\\docs\\contract.pdf" --signers '[{"userName":"Bob Smith","userEmail":"bob@example.com"}]' --subject "Please sign this contract" --confirm
```

## Required Configuration

- Node.js 18 or later
- Access to the trusted external CLI, either preinstalled or available through `npx`
- `ESIGNGLOBAL_APIKEY` must already be configured in the shell environment

## Output

Return the external CLI result. Do not bundle or implement upload logic inside this skill.
