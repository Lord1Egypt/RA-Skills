# Security policy

This skill touches local signing and irreversible blockchain operations. Use these rules before any quote, signature, approval, broadcast, cancellation, or recovery step.

## Private key handling

- Never request private keys, mnemonics, seed phrases, or wallet backup material in chat.
- Prefer hardware wallets, OS keychains, encrypted keystores, or local signer services.
- If a raw local private key is unavoidable for a prototype, require it to be supplied through a local environment variable such as `LOCAL_PRIVATE_KEY` and never print it.
- Do not pass private keys as command-line flags because they can leak through process lists and shell history.
- Redact environment dumps, error traces, provider responses, and logs before showing them to the user.

## Local key generation (bootstrap)

Use this section when the user has no usable wallet and asks the agent for help configuring one. The skill never accepts a key in chat; it only orchestrates a generator that runs entirely on the user's machine.

- Run a local generator (for example `examples/generate_wallet.py`) on the user's machine. Do not generate, transmit, or display key material on any remote service.
- Default mode is `keystore`: an encrypted EIP-2335-style JSON file protected by a passphrase the user types into the local terminal. Use `file` (raw 0x key in a `0600` file) only for short-lived prototypes; use `env` (one-shot `export` line printed to the terminal) only when the user understands their shell history risk.
- The generator must use a CSPRNG, refuse to overwrite an existing wallet without `--force`, set parent directory to `0700` and the wallet file to `0600`, and never echo the private key or mnemonic through any channel that the agent can read.
- Print only the new wallet address to the agent-visible standard output. Print the BIP-39 mnemonic and any other recovery material on the local TTY only.
- Run a backup ceremony before the script exits: ask the user to write the mnemonic on paper or store it in an offline password manager, and require the user to retype a confirmation phrase. Do not proceed with planning, signing, or funding while the user has not confirmed they have a backup.
- After generation, refer to the wallet only through `signer_ref` strings of the form `keystore:<absolute path>`, `file:<absolute path>`, or `env:<VAR_NAME>`. The plan must never embed the key.
- Treat freshly generated wallets as low-balance starter wallets until the user has demonstrated a successful recovery from the backup on a separate machine or new shell. Do not move large funds in before that.
- Recommend the user revoke or migrate to a hardware-backed wallet for long-term holdings; the bootstrap mode exists to unblock first-time users, not as a permanent posture.

## Approval and allowance policy

- Prefer existing finite allowance, EIP-2612 permit, Permit2, EIP-712 resource lock, or provider-specific gasless authorization.
- Avoid unlimited approvals by default.
- If an approval transaction is required, label the route as `not fully gasless` or `gasless after approval`.
- Verify the spender contract from official docs or the provider response. Do not approve an unverified arbitrary address.
- Show current allowance, required allowance, approval amount, spender, token, chain id, and revoke instructions.

## Typed-data and calldata checks

Before signing typed data:

- Verify domain name, version, chain id, and verifying contract.
- Verify user, recipient, source and destination assets, amounts, nonce, deadline, and fill deadline.
- Verify oracle, settler, input settler, resource lock, and output settler when using intents.
- Reject expired, replayable, or chain-mismatched typed data.

Before signing a transaction:

- Verify `to`, `data`, `value`, `chainId`, gas fields, nonce, and token transfer effects.
- Simulate via `eth_call`, provider estimate, tenderly-like simulation, or the official provider estimator when available.
- Reject transactions that transfer more value than the accepted plan.

## Route risk limits

Default limits unless the user sets stricter values:

- maximum slippage: 100 bps for stable/stable, 300 bps for volatile routes, 500 bps absolute ceiling
- maximum approval amount: exact input amount or the smallest finite amount needed for repeated planned orders
- deadline: short enough to limit stale execution, long enough for cross-chain finality
- destination recipient: must be explicitly provided or must default to the same local wallet address

## Audit artifacts

Persist only non-secret data:

- normalized execution plan
- plan hash
- raw quote response with secrets redacted
- provider name and endpoint
- token and chain metadata
- signature hash, order id, transaction hash, and timestamps
- final status and receipt links

Never persist:

- private keys
- mnemonics
- raw hash-lock secrets
- keystore passwords
- bearer tokens or API keys
- unredacted provider responses containing secrets

## User approval wording

For real execution, require a user response equivalent to:

```text
approve this exact plan: <plan hash>
```

Do not accept vague phrases such as `go ahead with anything`, `trade whenever`, or `use my wallet as needed` for a real signature or broadcast.
