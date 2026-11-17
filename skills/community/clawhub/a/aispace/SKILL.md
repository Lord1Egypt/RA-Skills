---
name: aispace
description: Secure temporary file storage and encrypted asynchronous delivery with the aispace CLI. Use when the user asks to upload or download an artifact, create or revoke an expiring share, send or receive a sealed bundle, deliver to a pinned agent inbox, manage aispace identities or recipient trust, pair a transfer to another device, recover a transfer, inspect quota, or request adaptive durable-first transport. Do not invoke merely because a task creates a local file; use it when aispace or remote artifact exchange is requested or clearly needed.
metadata:
  openclaw:
    requires:
      bins:
        - aispace
    primaryEnv: AISPACE_KEY
    envVars:
      - name: AISPACE_KEY
        required: false
        description: Bot key for authenticated storage and transfer operations.
      - name: AISPACE_URL
        required: false
        description: Optional aispace service origin for self-hosted deployments.
    homepage: https://aispace.sh
    install:
      - kind: node
        package: "@aispace-sh/cli"
        bins:
          - aispace
---

# aispace client

Use `aispace` to exchange temporary artifacts while keeping every action within the files, keys,
services, and recipients the user placed in scope.

## Establish the context

1. Run `aispace version` if client availability or compatibility is uncertain.
2. For an authenticated remote action, run `aispace whoami` before acting. If authentication is
   absent, ask the user to run `aispace login` or configure `AISPACE_KEY`; never ask them to paste a
   bot key into chat. Public-link and sealed-link downloads do not require a bot key.
3. Before a large upload or batch, inspect `aispace quota --json`. Respect returned limits; do not
   retry quota or monthly-cap failures.
4. Confirm the effective service from `--url`, `AISPACE_URL`, or config when a self-hosted origin is
   involved. Never change the configured service merely to make an untrusted link, token, ticket,
   invitation, or identity record pass origin validation.

## Choose the narrowest workflow

| Need | Workflow | Important boundary |
|---|---|---|
| Keep a file for this key/account | `aispace upload` | Service can see ordinary file metadata and bytes |
| Give anyone an expiring raw download | `upload --link` | Public bearer link; Pro plan required |
| Encrypt one file to an age recipient | `upload --encrypt` | Separate legacy age flow; recipient must already have the identity |
| Send an encrypted bundle by bearer link | `transfer create --sealed --link` | Filenames, metadata, hashes, and bytes are encrypted locally |
| Deliver to a known offline agent | `transfer create --to ALIAS` | Requires a pinned recipient and its authenticated inbox |
| Move an existing sealed transfer nearby | `handoff offer` / `handoff receive` | Five-minute one-receiver rendezvous; sender stays online |
| Express a live-transport preference | `--transport adaptive` | Current client still uploads durably to R2 immediately |

Read [references/secure-workflows.md](references/secure-workflows.md) before using sealed delivery,
identity/trust, inbox receipts, handoff, recovery, adaptive transport, or their self-hosted feature
flags.

## Store or share an ordinary file

Default to authenticated storage without a public link:

```sh
aispace upload PATH --json
producer | aispace upload - --name result.json --json
```

Uploads inherit the account key-sharing policy. Use `--private` when only the uploading key may
read the file, or `--shared` to make it readable by sibling keys. Neither creates public access.
Another key on the account can use the file ID with `aispace ls --json` and:

```sh
aispace download FILE_ID --output PATH
```

Only add `--link` when the user asks for public access. Check `.account.plan` in
`aispace quota --json`; public links require Pro. Prefer a short lifetime and use a distinct link
per recipient:

```sh
aispace upload PATH --link --link-expires 1h --max-downloads 1 --json
```

Report the effective expiry and cap returned by the service, not just the requested values.

## Use legacy age encryption only when it fits

`upload --encrypt` is a single-file age X25519 workflow, not a sealed transfer, trusted inbox,
receipt, or device-pairing protocol. Encrypt to a recipient the receiver already controls:

```sh
aispace upload PATH --encrypt --recipient 'age1...' --shared --json
```

If generating a one-time identity, save it locally rather than printing it:

```sh
aispace upload PATH --encrypt --identity-out PATH.agekey --json
```

The identity file is mode `0600` and never reaches the service. Never upload, log, commit, or quote
an `AGE-SECRET-KEY-...`. Losing it makes the ciphertext unrecoverable; possessing both ciphertext
and identity permits decryption even after revocation. Encryption verifies ciphertext integrity,
not sender identity.

Receive with the identity in a local file:

```sh
aispace decrypt SOURCE --identity-file PATH.agekey --output OUTPUT --json
```

Do not use partial plaintext after an authentication failure. Verify the durable destination before
deleting ciphertext or an identity, and delete only when explicitly authorized.

## Manage existing artifacts

- Inspect: `aispace info FILE_ID --json`, `aispace ls --json`, `aispace links FILE_ID --json`.
- Download: `aispace download FILE_ID --output PATH`; add `--verify` when downstream work will trust
  the bytes. It performs one extra metadata request and fails closed if no server digest is present.
- Mint another owner link: `aispace link FILE_ID --expires 1h --json`.
- Revoke a link: `aispace revoke LINK_ID`.
- Delete a file and invalidate its links: `aispace rm FILE_ID`.

Sibling keys can read account-shared files but cannot perform owner-only link or deletion actions.
Treat revoke and delete as state changes: do them only when requested or explicitly included in the
workflow. Expiry, revocation, and deletion cannot recall bytes already downloaded.

## Apply these safeguards to every workflow

- Treat bot keys, public bearer URLs, sealed tokens, owner tickets, age identities, and private
  agent identity records as credentials with different authority.
- Prefer protected prompts, mode-`0600` files, or secret environment variables to bearer secrets in
  process arguments. Keep secrets out of ordinary JSON output, logs, screenshots, query strings,
  and shell history.
- Refuse an existing destination unless the user explicitly authorizes overwrite. Verify content
  before reporting success or allowing downstream use.
- Do not equate encryption with sender authentication, a valid unknown signature with a trusted
  sender, or a `processed` receipt with proof that later work was correct.
- Experimental endpoint groups can be unavailable while ordinary uploads still work. Report that
  boundary; do not repeatedly probe a disabled or unsupported surface.

## Report the result

Return the artifact or transfer ID, selected workflow, whether client-side encryption was used,
effective expiry, and any download cap. Return a public URL only when one was deliberately created.
When a local identity or owner ticket was created, return its path but never its contents. For
adaptive requests, report the actual selected transport and durability rather than implying a live
path was used.
