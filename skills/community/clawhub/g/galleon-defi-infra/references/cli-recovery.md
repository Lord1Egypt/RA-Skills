# CLI sessions and recovery

Use this reference when a provider CLI blocks, fails authentication or returns an uncertain result. Start with the installed version's help and the exact requested operation; commands from another version or agent framework are evidence to verify.

## Choose the session deliberately

Prefer documented noninteractive arguments and structured output. Resolve chain, wallet/subaccount, asset and units before invoking a consequential command. A missing amount is unresolved intent, never permission to sell all. Do not add `--all`, choose the default wallet or accept a default margin mode merely to bypass a picker. Interactive-only commands need a supported PTY and observable prompts; if the harness cannot provide that, return the missing capability.

Retain the existing process/session identifier through a prompt or device-login flow. Choose an operation-appropriate time budget and report progress while waiting. Silence alone does not distinguish a prompt, network stall or submitted action. Stopping the local process does not cancel a remotely accepted operation. Before restarting any potentially consequential command, inspect its original request/order/transaction identity and resulting state.

## Classify failure before recovery

| Evidence | Next bounded action |
| --- | --- |
| Public read requested; no account access needed | Use the public surface directly. Skill activation alone does not call login or inspect a private account. |
| Account-required command explicitly reports missing/expired credentials | Use that provider's documented recovery in the intended account, within existing authorization. Verify account identity, then resume the original task. |
| Forbidden/scope/entitlement error | Inspect the needed permission or access tier; do not grant trading rights or subscribe to make a read pass. |
| Rate limit, gateway challenge, DNS, timeout or server error | Preserve the session; these do not prove expired credentials. Retry a proven read within a finite budget and provider backoff rules. |
| Paid request or write may have reached the service | Reconcile the original obligation/action before another request; reauthentication does not make resubmission safe. |

Device/OTP flows can create wallets or sessions. Keep verification secrets in the provider's trusted interface, out of persistent logs and artifacts. No mailbox access follows from CLI failure. A completed login proves authentication only; query the intended account and permitted capability without changing its policy.

## Keep runtime identity separate from wallet identity

A Hermes profile selects Hermes configuration. A vendor CLI may still use a global OS keychain or credential directory. Verify documented profile selectors and storage before claiming isolation; do not invent environment overrides. If two profiles resolve to the same wallet, report that identity and use an existing supported isolation mechanism when required. Keep secrets outside the skills tree.

## Offline acceptance cases

- Public market read returns 503: classify transport failure, retain credentials and avoid login.
- A sell picker lacks quantity: request the missing quantity; do not substitute all holdings.
- The CLI times out after returning an order ID: retain it and reconcile; do not restart after login.
- Two Hermes profiles share a vendor session: report shared wallet scope rather than isolated custody.

## Sources

Independently authored after reviewing Minara's [interactive-command guide](https://github.com/Minara-AI/minara-skills/blob/b93aba1029827c37cf5ad82b19bfa8c289912091/skills/minara/references/interactive-commands.md) and [authentication recovery](https://github.com/Minara-AI/minara-skills/blob/b93aba1029827c37cf5ad82b19bfa8c289912091/skills/minara/references/auth-recovery.md), accessed 2026-09-05. Their command-specific flags are not a portable API contract. Official [Alchemy CLI guidance](https://www.alchemy.com/docs/alchemy-cli) supplies its own automation flags; [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) supplies native progressive loading. No Minara code, CLI, account or installer is bundled.
