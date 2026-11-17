# Secure workflow reference

Use this reference only for sealed transfers, trusted identity/inbox delivery, human/device
handoff, recovery, adaptive transport, or self-hosted feature availability. Ordinary `upload`,
`download`, public-link, and age workflows stay in the main skill.

## Sealed bearer delivery

Create a durable, end-to-end encrypted bundle:

```sh
aispace transfer create report.pdf charts.png \
  --sealed --link --expires 1d --max-downloads 1
```

The client encrypts the private manifest and independently authenticated chunks before upload.
Filenames, content types, per-file sizes, and plaintext hashes remain in the encrypted manifest;
the service sees aggregate declarations and ciphertext. A sealed bearer transfer does not
authenticate its sender.

The HTTPS fragment and CLI token contain equivalent bearer authority. Human output prints the
link. JSON omits both `link` and `token` unless secret emission is explicit and redirected to a
protected file:

```sh
umask 077
aispace transfer create report.pdf --sealed --link \
  --json --include-secret > handoff.json
jq -r .token handoff.json > handoff.token
chmod 600 handoff.token
```

`--include-secret` requires `--json` and is refused when stdout is a terminal. Keep the protected
output out of logs and CI annotations.

Prefer a protected prompt for interactive receipt:

```sh
aispace transfer receive
```

For automation, use a mode-`0600` token file or `AISPACE_TRANSFER_TOKEN`, disable the approval
prompt explicitly, and choose the output directory:

```sh
aispace transfer receive --token-file ./handoff.token \
  --output ./received --yes
```

Supplying a link or token positionally is supported but warns because process arguments can be
visible. The receiver authenticates the manifest before claiming, writes protected partial files,
retries from authenticated chunk boundaries, verifies chunks and whole-file hashes, and only then
commits the claim. `--overwrite` changes only destination replacement; it does not weaken origin or
cryptographic checks.

## Owner recovery and revocation

Creation saves a mode-`0600` owner ticket under the aispace config directory. It contains scoped
resume/revoke capabilities and the recipient token. Keep the original source paths unchanged until
completion.

```sh
aispace transfer status TRANSFER_ID
aispace transfer resume TRANSFER_ID
aispace transfer revoke TRANSFER_ID
```

`resume` re-hashes sources and reuses valid uploaded parts. `revoke` reads its capability from the
ticket instead of a process argument. A ticket is bound to its canonical service origin; never use
it after changing `AISPACE_URL` to another service. Losing the ticket removes the normal CLI resume
and revoke route. Losing the bearer token or needed private identity removes the decryption route;
there is no server key escrow.

## Trusted agent identity and recipient pins

Create private X25519 encryption and Ed25519 signing keys locally:

```sh
aispace identity create --name "Research agent" --handle research-agent
aispace identity list
aispace identity show ID
```

Private identity records are atomically stored mode `0600` beside the CLI config. Only public keys
and proof-of-possession reach the service. Back them up securely: no server-side recovery exists.
The dashboard supplies the public invitation and administers bot-key identity bindings/scopes; the
CLI deliberately does neither. Confirm those controls there before an automated send or receipt.

Rotate through predecessor authorization so recipients can validate continuity:

```sh
aispace identity rotate ID --purpose encryption
aispace identity rotate ID --purpose signing
```

Old encryption private keys stay local so earlier deliveries remain readable. `identity revoke`
stops new use of one public key; `identity disable` stops public lookup and new deliveries. Neither
recalls existing ciphertext or keys.

Import the recipient's exact invitation, then compare the complete fingerprint over another
trusted channel before pinning:

```sh
aispace recipient add "$RECIPIENT_INVITATION" --alias research-agent
aispace recipient verify research-agent --fingerprint "$RECIPIENT_FINGERPRINT"
```

Do not trust a display name, account handle, invitation transport, or merely valid unknown
signature. After `recipient verify`, `--to research-agent` uses that pin. To automate a first send
before a separate verify command, supply the complete expected `--recipient-fingerprint`;
`--trust-on-first-use` is an explicit weaker choice. Each send refreshes the public record and
accepts only the pin or a complete predecessor-signed rotation chain; unexpected replacement stops
the send. An invitation contains public key material rather than a decryption secret, but its
integrity still matters.

## Addressed inbox delivery and receipts

Send to a pinned recipient without an anonymous bearer decryption route:

```sh
aispace transfer create report.pdf \
  --sealed --to research-agent --from my-agent --expires 7d
```

`--from` signs the private manifest with a local identity. Add `--also-link` only when the user
deliberately wants a second anonymous recovery route.

The receiving bot key must be bound to the recipient identity and carry the appropriate inbox and
receipt scopes:

```sh
aispace inbox list --json
aispace inbox receive DELIVERY_ID --output ./incoming --yes
```

Select the exact `deliveries[].id` from structured output using the expected transfer, recipient,
and sender identity IDs; do not automate against display text. For first contact with a signed
sender, import the sender's dashboard invitation and verify its fingerprint through the same
out-of-band process before using unattended `--yes`.

Automated `--yes` receipt refuses unsigned, unknown, unpinned, revoked, expired, or disabled senders
unless `--allow-unknown-sender` is also explicit. That exception accepts the content after a clear
trust downgrade; it does not mark the sender verified. Interactive receipt may show the warning and
ask the operator.

After the consuming application accepts the verified files, record that distinct stage:

```sh
aispace inbox processed DELIVERY_ID
```

Reject without installing files with `aispace inbox reject DELIVERY_ID`. `downloaded` and
`verified` concern cryptographic transfer stages; `processed` is an application acknowledgement,
not proof of correct downstream work. Signed receipt requests and replay state are persisted before
submission so retries reuse the same receipt, claim nonce, signature, and idempotency key.

## Human and device handoff

Start from a completed bearer-capable sealed transfer whose owner ticket is present. The sender must
remain running while the receiver enters the pairing code:

```sh
aispace handoff offer TRANSFER_ID
# code  J7KM-PQRT
# open  https://aispace.sh/pair/J7KM-PQRT

aispace handoff receive J7KM-PQRT --output ./incoming
```

The five-minute code is a rendezvous locator, not a transfer key. The receiver sees the exact
service origin, mode, sender status, aggregate size, file count, and expiry before approval. The
service relays an envelope encrypted to a one-use P-256 device key. A second distinct receiver
before binding crowds and invalidates the room, requiring a restart. After the first receiver is
bound, new attempts are rejected without changing its envelope. Internal retries preserve the
original receiver key, nonce, attempt capability, and approval capability through bounded backoff
rather than creating a second attempt.

`--yes` skips only the approval prompt. Pairing is unavailable with `--json`. Built-in QR rendering,
native OS scheme registration, and PAKE rendezvous are not implemented; the HTTPS pairing page is
the no-install fallback.

For local copy/paste conversion without a pairing room:

```sh
aispace handoff encode
aispace handoff encode --token-file ./handoff.token
```

The command prints equivalent secret-bearing representations and therefore refuses JSON mode. A
positional reference is supported with a warning; prefer its prompt, token file, or
`AISPACE_TRANSFER_TOKEN`. The native URI is only a representation, not installed OS integration.

## Adaptive durable-first intent

Request adaptive intent explicitly:

```sh
aispace transfer create report.pdf --sealed --link \
  --transport adaptive --durability durable-first \
  --transport-privacy relay-only
```

The client discovers capabilities before adding adaptive-only request fields. An older, malformed,
disabled, or temporarily unavailable discovery surface causes a strict legacy stored request. In
all cases the current client begins and completes the durable R2 upload immediately. It ships no
reviewed WebRTC, TURN, native relay, or other live byte driver; adaptive intent does not currently
improve speed. `direct-first`, `live-only`, and ephemeral delivery are rejected.

Use `relay-only` unless the user knowingly accepts that a future `direct` mode may disclose network
addresses to the peer and signaling infrastructure. Always report the selected transport (currently
R2), fallback reason, and durable state—not only the requested mode.

## Self-hosted origin and feature availability

Every participant must use the same canonical service origin:

```sh
export AISPACE_URL=https://files.example.com
```

Provision the bot key through `aispace login` or the execution environment's secret facility; do
not type a live key into a checked-in script or example.

Remote origins must be HTTPS origins without credentials, paths, queries, or fragments. Plain HTTP
is local-loopback development only. Canonical comparison normalizes equivalent host casing and
default ports while preserving meaningful ports and IPv6 authority syntax. Tokens, owner tickets,
identity records, recipient invitations, and pairing summaries are origin-bound; an origin mismatch
must fail before an authenticated request. Never rewrite an embedded origin or forward credentials
to make a foreign reference work.

The secure workflow components depend on the sealed base:

| Capability | Required components |
|---|---|
| Sealed bearer transfer | Transfer storage and migrations |
| Agent identity and inbox | Sealed transfer storage plus identity migrations |
| Pairing handoff | Sealed transfer storage plus the pairing Durable Object |
| Adaptive intent | Sealed transfer storage plus adaptive migrations |

`ADAPTIVE_DIRECT_ENABLED` and `ADAPTIVE_TURN_ENABLED` are additional kill switches, not evidence
that a live driver exists. Core stored R2 delivery requires neither signaling nor TURN. Older or
incomplete deployments may still lack a route; report it as unsupported and keep ordinary uploads
or explicitly requested stored delivery available.
