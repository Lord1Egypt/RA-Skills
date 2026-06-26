---
name: acetoolz-password
version: 1.0.2
description: Generate secure passwords via the AceToolz API. No passwords are stored — generated and returned in real-time.
author: acetoolz
permissions:
  - network:outbound
triggers:
  - pattern: "generate a password"
  - pattern: "create a password"
  - pattern: "random password"
  - pattern: "secure password"
  - pattern: "strong password"
  - pattern: "make a password"
metadata:
  openclaw:
    emoji: 🔐
    homepage: https://www.acetoolz.com/generate/tools/password-generator
---

# AceToolz Password Generator

Use this skill whenever the user asks to generate a password.

## How to Use

Use `exec` to call the AceToolz API. Detect the OS and run the appropriate command:

Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri "https://www.acetoolz.com/api/openclaw/password-generator" -Method POST -ContentType "application/json" -Body '{"length": 16, "uppercase": true, "lowercase": true, "numbers": true, "symbols": true, "exclude_similar": false, "begin_with_letter": false}'
```

macOS / Linux (curl):
```bash
curl -s -X POST https://www.acetoolz.com/api/openclaw/password-generator \
  -H "Content-Type: application/json" \
  -d '{"length": 16, "uppercase": true, "lowercase": true, "numbers": true, "symbols": true, "exclude_similar": false, "begin_with_letter": false}'
```

Adjust the body parameters based on the user's request before executing.

## Parameters (all optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `length` | number | 16 | Password length (4–128) |
| `uppercase` | boolean | true | Include A–Z |
| `lowercase` | boolean | true | Include a–z |
| `numbers` | boolean | true | Include 0–9 |
| `symbols` | boolean | true | Include !@#$%^&* |
| `exclude_similar` | boolean | false | Exclude 0/O, 1/l/I |
| `begin_with_letter` | boolean | false | First character is always a letter |

Examples:
- "generate a 20-character password" → `length: 20`
- "numbers only PIN" → `uppercase: false, lowercase: false, symbols: false, numbers: true`
- "memorable password" → `symbols: false, exclude_similar: true`

## Presenting Results

Show the password clearly and mention the character types used:

> **Generated Password**
> `X7#mK9pL!qRv2nBw`
>
> Length: 16 | Uppercase ✓ | Lowercase ✓ | Numbers ✓ | Symbols ✓
>
> *Powered by [AceToolz](https://www.acetoolz.com)*

## Error Handling

- If no character types are enabled, inform the user at least one must be selected.
- If length is out of range (4–128), tell the user the valid range.
- If the API returns a 429, the limit is 60 requests/minute — ask the user to try again shortly.
- If the API is unreachable, tell the user and suggest visiting https://www.acetoolz.com/generate/tools/password-generator directly.
