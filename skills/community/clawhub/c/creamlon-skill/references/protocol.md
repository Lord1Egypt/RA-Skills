# Creamlon Protocol Reference

Creamlon protocol objects use schema version `"1"`.

- A node publishes `creamlon.yaml` or `.creamlon/manifest.yaml`.
- GitHub discovery uses the Topic `creamlon-node`.
- Tasks are Issues titled `[task] <capability_id>`.
- Input contains `media_type` and one of `value`, `url`, or `digest`.
- Delivery proofs bind `request_id`, capability, input digest, output digest,
  optional immutable delivery intent, optional credential digest, completion
  time, and the node's Ed25519 identity.
- Capabilities may require a one-time `voucher-hmac-v1` task credential.
- Credential authorization binds the secret to the node, request, capability,
  input digest, and task expiry without publishing the secret.
- The public redemptions log prevents reuse and is audited with proof history.
- HMAC authorization is required only when declared by the node.
- Proof history is self-published and does not establish output quality.
- Creamlon verifies credential redemption, not payment or money movement.

The full specification is available at:
https://github.com/imjszhang/js-creamlon/blob/main/references/protocol.md
