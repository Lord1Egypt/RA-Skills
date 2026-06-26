# Install and authenticate

## Install

```bash
npm install -g @factucat/cli
```

Verify:

```bash
factucat --help
```

## Update

```bash
npm install -g @factucat/cli@latest
```

## Save an API key

First obtain an API key in FactuCat:

1. Sign in to `https://factucat.com`
2. Open the settings area
3. On any settings screen, with no input, textarea, or select focused, type the Konami code:
   `↑ ↑ ↓ ↓ ← → ← → B A`
4. FactuCat unlocks the hidden `API keys` section in the settings sidebar
5. Open `API keys`, create a new key, and copy it immediately

Important:

- The full token is shown only once after creation
- If the sidebar does not change, make sure keyboard focus is not inside a form field while typing the sequence

Interactive:

```bash
factucat auth api-key set
```

Explicit value:

```bash
factucat auth api-key set --value fc_live_xxxxx
```

Standard input:

```bash
printf 'fc_live_xxxxx\n' | factucat auth api-key set
```

## Verify auth

Human-readable:

```bash
factucat auth status
```

Machine-readable:

```bash
factucat auth status --json
```

If the user sees `API key inválida o revocada`, re-save a valid key and retry.
