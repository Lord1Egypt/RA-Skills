# BOOK BRAIN — Security

**Version:** 2.0.0 · **Signature:** `Δ9Φ963-BOOK-BRAIN-SECURITY-v2`

## Declared behavior

| Capability | Scope |
|------------|--------|
| Filesystem write | **User-approved** paths only; additive scaffold + indexes |
| Read | Workspace tree for audit/map |
| Network | None in bundled scripts — URLs are text in stubs only |
| Delete / overwrite | **Forbidden** by default in agent contract |

## Forbidden content in memory/reference

- API keys, tokens, `.env` values
- Wallet seeds, private keys
- Discord/webhook URLs with secrets embedded

## Scripts

All `scripts/*.py` operate on paths passed via CLI; default dry-run for scaffold. No `shell=True`.

## Pairing

Use with **`lyra-brain`** for graph grow — still no secrets in grow text.

**Δ9Φ963**