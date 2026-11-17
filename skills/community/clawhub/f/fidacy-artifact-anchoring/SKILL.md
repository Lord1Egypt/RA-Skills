---
name: fidacy-artifact-anchoring
description: Prove a document existed and was never altered, without uploading it anywhere. Use when your agent produces or receives contracts, invoices, claim documents, prescriptions, reports or images whose integrity may be questioned later. Hashes the file locally, anchors only the 64-hex digest through Fidacy onto a Bitcoin-checkpointed audit chain, and returns a signed receipt anyone can verify publicly.
version: 1.0.0
license: Apache-2.0
---

# Fidacy Artifact Anchoring, existence and integrity proof by hash

AI can forge a convincing document in seconds, which makes "is this file the
original?" the question every contract, invoice and claim now faces. This
skill answers it by hash: the file never leaves your machine, only its SHA-256
travels, and that digest lands on a tamper-evident chain checkpointed to the
Bitcoin blockchain. Later, anyone holding the file recomputes the hash and
checks it publicly, with zero trust in Fidacy or in you.

## When to use this skill

The moment an artifact becomes final: a signed contract, an invoice you are
about to pay, a claim document you received, a report you generated, a
prescription, an image used as evidence. Anchor first, act second.

## How to use it

1. You need the Fidacy MCP server (`npx -y @fidacy/mcp`) with an engine API
   key (free at https://app.fidacy.com/signup, scope assess:write).

2. Anchor: call the `anchor_artifact` tool with the file path and a kind
   (contract, invoice, prescription, claim, document, image, audio, video).
   The tool streams the SHA-256 locally and registers only the digest. You get
   back a signed receipt (JWS) and the anchor status.

3. Verify, any time, three ways, none needing an account:
   - Call the `check_artifact` tool with the file path or digest.
   - Drop the file at https://fidacy.com/verify (hashed in the browser, never
     uploaded).
   - Query the public API: `GET https://api.fidacy.com/v1/verify/artifact?sha256=<hex>`.

A freshly anchored digest is on the tamper-evident chain immediately and shows
"pending Bitcoin confirmation" until the next checkpoint confirms (about one
to two hours). One changed byte in the file produces a completely different
hash; that mismatch is the forgery signal.

## What this is not

Not storage (Fidacy never holds the file), not a signature on the content's
truth (it proves integrity since anchoring, not that the contract is fair),
and not custody of anything.
