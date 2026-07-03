# SanMar runtime docs index

This directory holds the extended API reference the skill reads before tool
calls. Files travel with the skill (under `skills/sanmar/references/`) and the
agent reaches them at `references/<page>.md`.

Docs are written for LLM/tooling correctness, not end-user marketing prose.

## Pages

- `examples.md` — realistic prompts and the CLI calls to make for each.
- `auth_and_patterns.md` — cross-cutting onboarding, auth, endpoint, transport, and error patterns.
- `web_services.md` — SanMar SOAP web-services operations and response normalization guidance.
- `ftp_feeds.md` — FTP feed families, file conventions, join keys, and cadence expectations.
- `purchase_orders.md` — PO submission/validation workflow and operational safeguards.

## Tool usage linkage

Every tool is invoked through the one CLI entrypoint `scripts/sanmar.py`
(`echo '<json>' | python3 scripts/sanmar.py <action>`), contracted by
`SKILL.md`. The implementation modules live alongside it under `scripts/`
(`sanmar_tools.py`, `sanmar_client.py`, `ftp_resolver.py`, `pdf_parser.py`,
`schemas.py`). Common action mapping:

- Product queries -> `search-products`
- Inventory checks -> `check-inventory`
- Pricing checks -> `get-pricing`
- Pre-submit cart validation -> `validate-cart`
- PO submission -> `create-purchase-order`
- Order status -> `check-order-status`
- Tracking / shipping status -> `get-tracking`
- PDF PO intake -> `parse-po-pdf`
- Marketing-color → mainframe-color resolution (SDL CSV over SFTP) ->
  `lookup-mainframe-color`

## Source PDFs

The original vendor integration guides live in the `sme-sanmar` repository under
`api_docs/` for traceability; they are not copied into this skill. The markdown
pages here are the operational reference — refresh them when a new vendor guide
arrives.

## Authoring standard for future updates

When new SanMar behavior is discovered:

1. Update the closest topical markdown file above.
2. Prefer concrete field names, operation names, and payload examples.
3. Document edge cases that can cause bad writes or silent data drift.
4. Keep this index aligned if a new domain markdown file is added.
