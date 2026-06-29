# Repo Policy Profiles

A repository MAY declare one or more of these labels:

- `strict-clean`
- `warning-dirty`
- `commit-required`
- `push-required`
- `local-proof-heavy`

## Semantics

- `strict-clean`: dirty repo state blocks continuation
- `warning-dirty`: dirty repo state is reported but does not automatically block continuation
- `commit-required`: a successful round MUST end in a commit
- `push-required`: a successful round MUST end in a push when network and auth allow it
- `local-proof-heavy`: stronger deterministic proof is required before continuation

If the repository already defines equivalent policy, use the repository definition as source of truth.
