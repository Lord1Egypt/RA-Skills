# ADAHandle Concepts

## What are ADAHandles?

ADAHandles are human-readable identifiers for Cardano addresses. Instead of sharing a long bech32 address like `addr1qx...`, users can share a simple handle like `$alice`.

Handles are Cardano native tokens minted under a well-known policy ID. Owning the token means owning the handle — it lives in the wallet like any other native asset.

## Handle Format

- Handles are typically lowercase alphanumeric strings.
- When displayed to users, prefix with `$` (e.g. `$alice`).
- The MCP tool returns handles without the `$` prefix.

## Resolution

A handle resolves to whichever address currently holds the handle token. If the token moves to a new address, the handle points to the new address automatically.
