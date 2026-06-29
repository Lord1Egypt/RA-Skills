---
name: creamlon-skill
description: "Turn any GitHub repo into an async agent service store: publish services, accept paid tasks via Issues, and deliver results with signed proof. Works with OpenClaw, Claude Code, Codex, Cursor, or any agent."
version: 0.8.2
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
      bins:
        - npx
    primaryEnv: GITHUB_TOKEN
---

# Creamlon

Use Creamlon when a user wants to turn a GitHub repository into an agent
service store, sell or gate agent work, place an async order through Issues, or
verify a signed delivery receipt.

Run the published CLI through npm:

```bash
npx --yes creamlon@0.8.2 help
```

Require Node.js 18 or newer. Public reads can run anonymously but are
rate-limited. Use `GITHUB_TOKEN`, `GH_TOKEN`, or `--token` for writes and higher
read limits.

Never print tokens, complete `crv1_...` credentials, HMAC secrets, private
keys, private task content, private artifact URLs, or plaintext private
artifacts.

## Use This Skill When

- The user wants to publish an agent service from a GitHub repository.
- The user wants to sell paid or controlled access to an agent capability.
- The user wants OpenClaw, Claude Code, Codex, Cursor, or another agent to
  accept async tasks through GitHub Issues.
- The user wants to place an order with another melon and later verify a
  signed delivery proof.
- The user needs a GitHub-native transaction history for agent work.
- The user asks about Creamlon, GAP, melons, `creamlon.yaml`, `crv1_...`,
  signed delivery proofs, or Creamlon nodes.

## When NOT To Use

- Do not use Creamlon for low-latency streaming RPC, high-throughput APIs, or a
  direct MCP tool call.
- Do not treat Creamlon as a payment processor, escrow system, marketplace
  ranking service, or output-quality judge.
- Do not use public GitHub Issues for confidential inputs, outputs, or metadata
  unless the user also configures a private delivery extension.

## What Success Looks Like

For a store operator:

1. A public repository publishes `creamlon.yaml` or `.creamlon/manifest.yaml`
   and has the GitHub Topic `creamlon-node`.
2. The operator can run `watch` and see pending Issue orders as valid or
   rejected.
3. The operator can `deliver`, refresh `status`, and commit public trust
   records without committing private state.

For a customer:

1. The customer discovers and inspects a melon before ordering.
2. The customer submits a task Issue with the correct media type and optional
   credential.
3. The customer accepts the result only after `fetch-proof --verify` succeeds.

## Open a Melon

Create a melon and signing identity:

```bash
npx --yes creamlon@0.8.2 init ./my-agent-store --name my-agent-store
npx --yes creamlon@0.8.2 keygen --out ./my-agent-store/.creamlon/runtime
```

Add a service:

```bash
npx --yes creamlon@0.8.2 capability add \
  --repo-path ./my-agent-store \
  --id code_review \
  --description "Review a pull request and return Markdown feedback" \
  --input-type text/uri-list \
  --output-type text/markdown \
  --access free
```

Publish the repository with Issues enabled and the Topic `creamlon-node`. To
turn an existing repository into a melon instead, use `init . --layout bundled`.

For paid or controlled access, declare credential access and issue a private
one-time credential:

```bash
npx --yes creamlon@0.8.2 credential create \
  --repo-path ./my-agent-store \
  --capability-id code_review \
  --pretty
```

Deliver the complete credential through the operator's payment or approval
channel. Creamlon verifies credential redemption, not money movement.

## Process Orders

Validate pending orders:

```bash
npx --yes creamlon@0.8.2 watch owner/my-agent-store \
  --repo-path ./my-agent-store \
  --once \
  --pretty
```

Execute only tasks reported as valid. Reject malformed or unauthorized orders
without signing a proof:

```bash
npx --yes creamlon@0.8.2 reject owner/my-agent-store <issue-number> \
  --repo-path ./my-agent-store \
  --reason "unsupported input" \
  --pretty
```

Deliver a result:

```bash
npx --yes creamlon@0.8.2 deliver owner/my-agent-store <issue-number> \
  --repo-path ./my-agent-store \
  --output-file ./result.md \
  --pretty

npx --yes creamlon@0.8.2 status --repo-path ./my-agent-store
```

Commit public trust files for the selected layout: `trust/*` for root layout or
`.creamlon/trust/*` for bundled layout. Never commit `.creamlon/runtime/`,
credential stores, authorization key maps, delivery outboxes, private keys, or
tokens.

## Buy a Service

Discover and inspect:

```bash
npx --yes creamlon@0.8.2 discover code_review \
  --input-type text/uri-list \
  --output-type text/markdown \
  --pretty

npx --yes creamlon@0.8.2 inspect owner/my-agent-store --pretty
```

Place an order:

```bash
npx --yes creamlon@0.8.2 submit owner/my-agent-store \
  --capability-id code_review \
  --media-type text/uri-list \
  --input-url "https://github.com/alice/project/pull/42" \
  --requester github:your-user/your-repo \
  --pretty
```

Use exactly one of `--input`, `--input-url`, or `--input-digest`. Prefer a
digest and private delivery when the input must not be public.

When a service requires a credential, obtain the full `crv1_...` privately and
add `--credential "crv1_..."`. Never put that value in an Issue, comment, log,
or committed file.

Verify delivery:

```bash
npx --yes creamlon@0.8.2 fetch-proof owner/my-agent-store <issue-number> \
  --verify \
  --pretty
```

Accept a result only when signature and task binding verification succeed. A
valid proof establishes identity and input/output binding, not output quality.

## Private Delivery

Core Issues carry public metadata and digests. For encrypted input/output
transport, use the RFC 9180 `delivery-hpke-v2` extension and follow the
repository documentation. For GitHub delivery, never submit before
`send-input` has written `delivery.github.input_commit` into the task,
extensions file, and outbox.

## Troubleshooting

- Authentication failure: set `GITHUB_TOKEN` or `GH_TOKEN`, or pass `--token`.
- No discovery results: check repository visibility, Topic `creamlon-node`,
  Issues availability, capability media types, status, and the public manifest.
- Verification failure: check task binding, trusted comment author, proof
  timestamp, input/output digests, and identity rotation history.
