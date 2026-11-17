# Security boundary

## What the adapter guarantees

- BailingHub connectivity is outbound-only long polling plus heartbeat and result reporting.
- Plain HTTP is rejected except for loopback installation tests.
- The executor token is read from the environment and is never placed in child-process arguments.
- The OpenClaw child process starts from a minimal system environment rather than inheriting the complete parent environment.
- Additional model-provider or network variables are forwarded only when an operator names each one in `OPENCLAW_FORWARD_ENV`.
- The child does not receive the BailingHub executor token, job metadata, internal project paths, or task-level business-tool credentials.
- A result includes the dispatch `claim_token`, allowing BailingHub to reject a late result after re-dispatch.
- The runner invokes the OpenClaw binary directly without a shell and enforces bounded task, response, stdout, stderr, and timeout behavior.
- The published skill contains the exact runner it executes. It does not download executable code at runtime.

## What the adapter does not guarantee

- It does not authenticate or authorize the final business action. The business system must keep final authority.
- It does not make a compromised OpenClaw runtime trustworthy.
- It does not prove that an approval authority or audit writer is independent from the runtime.
- It does not hide task text from the configured OpenClaw model provider.
- It does not grant OpenClaw direct access to BailingHub-governed business tools. Tool credentials are deliberately withheld in this first release.
- It does not replace host hardening, secret rotation, endpoint authorization, or incident response.

## Deployment rules

1. Use a dedicated OS account with the minimum filesystem and network permissions needed by OpenClaw.
2. Scope each executor token to the smallest practical target set and rotate it after suspected exposure.
3. Use TLS with a trusted certificate. For private PKI, configure Node.js trust explicitly instead of disabling TLS verification.
4. Keep task data classification compatible with the selected model provider and region.
5. Keep BailingHub, OpenClaw, and the business system on independently reviewable audit trails where stronger evidence is required.
6. Test token revocation, executor shutdown, stale results, and task timeout before production use.
7. Keep `OPENCLAW_FORWARD_ENV` as small as possible and review it whenever the service account gains a new environment variable.
