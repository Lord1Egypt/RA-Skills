# Creamlon Operations

## Caller sequence

1. Run `discover` for the required capability and media types.
2. Run `inspect` on the selected repository.
3. Run `submit` with one input location.
4. Wait for the node to close the task Issue.
5. Run `fetch-proof --verify`.

Do not publish secrets or private input values in GitHub Issues.

## Private delivery extension

When using `delivery-hpke-v2`:

1. `extension delivery prepare` — create task keys, draft extensions, and outbox.
2. `extension delivery draft` — create the single local task YAML.
3. `extension delivery send-input --task-file ... --extensions-file ... --outbox ...`
   — encrypt and upload input and record the immutable GitHub commit.
4. `submit --task-file ...` to post that same updated task.
5. `fetch-proof --verify` after the Issue closes.
6. `extension delivery fetch-output` — decrypt output, verify `proof.output_digest`, and verify Ed25519 proof by default.

Keep `.creamlon/runtime/outbox/{request_id}.json` local (mode `0600`). Never commit
outbox files or print GET URLs, ephemeral private keys, or artifact plaintext.
Compute digests with `creamlon hash --file`, which hashes raw bytes.

## One-time task credentials

When a capability requires credential access, the node operator creates:

```bash
npx --yes creamlon@0.8.2 credential create \
  --repo-path . \
  --capability-id <id>
```

The caller passes the privately received complete value to
`submit --credential`. The Issue contains only a task-bound HMAC. The node
stores secrets in `.creamlon/runtime/credentials.json` and records successful
redemption in the node's public redemptions log.

Use `credential list` to inspect status and `credential revoke <id>` to revoke
an unused credential. Neither command prints credential secrets.

## Optional node authorization

Free nodes need no key map. To require HMAC authorization, declare
`profiles.authorization.scheme: hmac-sha256` and generate a customer key:

```bash
npx --yes creamlon@0.8.2 hmac-key-new \
  --key-id customer-1 \
  --out .creamlon/runtime/authorization.keys.json
```

## Recovery and audit

- Resume interrupted delivery with `deliver --resume`.
- Run `status --repo-path .` after proof-log changes.
- Run `audit --repo-path .` to verify the local manifest, redemption log, and
  proof history.
- Record identity changes with `key-rotate` before discarding the old key.

See [extensions/payment-bridge-v1.md](../../../extensions/payment-bridge-v1.md)
for external payment to credential patterns.
