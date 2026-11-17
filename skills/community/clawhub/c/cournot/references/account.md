# Credentials and account management

Use only `scripts/cournot-client.mjs` for these operations. No key goes in a URL, command argument, payment intent, error log, or generic API output. API keys and wallet secrets are different: a user may supply a Cournot key for import, but never request a wallet private key or seed phrase.

## Balance, key, import

```sh
node <skill-root>/scripts/cournot-client.mjs balance
node <skill-root>/scripts/cournot-client.mjs key
node <skill-root>/scripts/cournot-client.mjs import
```

`import` reads the key from **stdin**, not arguments. Use a tool's stdin channel or a hidden local terminal prompt. Do not construct `echo <key>` / inline shell commands containing the secret. If secure input is unavailable, ask the user to run the command locally and supply the key through stdin. Do not echo an imported key back into chat.

- `balance`: show balance and masked key. Label `balance.remaining` as remaining calls, `balance.total` as total calls, and `balance.used` as used calls, localized to the user's language; never label total calls as the available balance. Apply these labels to every account/key/purchase result. `/account` does not return the free allowance; do not promise that it does.
- `key`: run the `key` command first to verify and display the saved key; do not start wallet recovery unless that command reports missing or invalid credentials. This is the only explicit action allowed to reveal `api_key`. Include the client's secrecy warning.
- `import`: validate through `/account` before atomically replacing the saved key. Report import success only when the client returns `credentialSource=import` and `saved=true`; an ordinary account read does not prove import. Invalid or empty keys preserve the old file. Accept KOL/manual keys, including those with no wallet. Import never rotates a key or buys a pack.
- `credential_missing`: ordinary queries still work anonymously. For an explicit `key` request, offer wallet recovery below; for balance, explain that no local key is configured and offer import or wallet recovery.
- `key_invalid`: likely invalid or rotated elsewhere; use another device's current key plus import, or wallet recovery. Do not automatically rotate.

Credentials are stored as `~/.cournot/credentials/<URL-encoded-origin>.json`, shared by agents running as the same OS user. Separate files isolate dev, production and local tests. The caller may set `COURNOT_CREDENTIAL_DIR` to a private storage directory; preserve that supplied value rather than constructing a new path. Unix directory/file modes are 700/600; on Windows ensure the user profile's ACL restricts access. Files are plaintext, not encrypted. `COURNOT_API_KEY` has priority only for its `COURNOT_API_KEY_BASE` (defaults to production). The client never edits environment variables or host configuration files.

If a save returns `active=false`, explain that the environment variable still overrides the file. Do not claim the new key is active, expose either full key, or silently remove the override. Ask the user to update or unset it in the host environment.

## Recover an existing key with the wallet

The backend can return the current key through wallet authentication; losing the local file does not require rotation or another purchase.

```sh
node <skill-root>/scripts/cournot-client.mjs auth-prepare --action account
```

Add `--reveal true` **only** when fulfilling an explicit `/cournot key`. Omit it for purchase recovery and balance. Successful recovery saves the current key to the active environment's credentials file.

## Rotate

Only for suspected compromise or an explicit rotation request. Explain before execution: the old key immediately stops working on every device; the wallet balance remains unchanged. A second device should import, not rotate.

```sh
node <skill-root>/scripts/cournot-client.mjs auth-prepare --action rotate
```

Both actions use the bundled client's wallet authentication flow. The client constructs and validates all signing parameters internally and never accesses private keys. Developer Mode must be enabled by the user in the Binance App.

## Signature confirmation and completion

Only a `state=complete` response from the corresponding `auth-execute` or `auth-status` establishes that the operation completed. A successful balance read does not prove rotation. Empty output or process exit code zero without JSON is not success: stop and report an unconfirmed operation rather than claiming that a key changed.

For `signature_confirmation_required`, apply the shared customer-communication principles. The decision-relevant facts are the public wallet, action and known effects. A successful rotation invalidates the old key on every device without changing remaining calls; account recovery reads and saves the current key without payment. Reveal a full key only for an explicit key request. Include any material returned risk or authority change, without interpreting absent fields as an assurance of no risk.

The client owns the signing payload and confirmation state. Keep protocol data internal and unchanged; obtain confirmation before execution. Payment authorization does not authorize key rotation.

At this preview stage, ask for confirmation in chat. Direct the user to confirm in the Binance App only after execution returns `signature_pending`; a prepared preview alone does not mean an App confirmation is waiting. Label account balances as numbers of calls in the user's language, not currency.

```sh
node <skill-root>/scripts/cournot-client.mjs auth-execute --intent '<intentId>' --confirmed true
```

- `signature_pending`: ask the user to confirm in the Binance App. Preserve the **new** returned intent id. Query it with `auth-status --intent '<intentId>'`; this retrieves the existing signature and does not sign again. Stop polling on rejected/expired results; do not loop automatically.
- `complete`: show balance, save status, and masked key, except the explicit `key` reveal. `hasKey=false` with zero balance means the wallet has no key record, not an authentication failure.
- `developer_mode_required`: ask the user to enable Developer Mode in the Binance App. Do not change wallet settings automatically.
- `wallet_required`: assist the selected Binance wallet's login; do not show a payment or funding prompt for authentication.
- `WALLET_351817`: wallet does not support the requested message; stop, do not substitute another signature scheme.
- `WALLET_351801`: Developer Mode is disabled. `WALLET_10003002`: session expired; sign in again. Other wallet errors: explain that the wallet operation could not complete without guessing a cause or changing wallets. Use [errors.md](errors.md) for all customer-facing errors; the codes below are internal mappings, not text to display.
- `api_error` with `8000`: invalid/expired wallet authentication. `4400`: no key for the wallet. `22004`: manual key cannot self-rotate. Do not describe these as insufficient funds.
- `credential_save_failed`: funds/remaining calls are still owned by the wallet. Recover with wallet `/account`; do not buy or rotate again.
- `account_result_unknown`, HTTP 5xx or a connection failure during rotation: do not repeat rotate. Use a fresh **account** recovery to inspect the current key.

Wallet signatures and returned keys stay inside the client. No direct wallet signing or authenticated curl commands through the model.
