## Description:

Read and change Buy Me a Pie lists, including lists, items, purchased state, sharing, unique items, and account checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powtac](https://clawhub.ai/user/powtac)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Buy Me a Pie shopping lists through API-backed commands for reading lists, adding or updating items, changing purchased state, sharing lists, and checking account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Buy Me a Pie credentials can be sent to an arbitrary API URL if the base URL is misconfigured.

Mitigation: Use protected environment variables for credentials, avoid passing the PIN on the command line, and use the default HTTPS Buy Me a Pie API endpoint unless another endpoint has been verified.

Risk: The skill can read, create, update, share, and delete shopping-list data under the configured account.

Mitigation: Review commands before execution, resolve list and item IDs before writes, and confirm destructive or sharing changes against current list state.

Risk: The API surface is inferred rather than an official public API contract and may drift.

Mitigation: Treat authentication or state errors as possible API drift, stop on unexpected server responses, and use browser fallback for signup, PIN reset, OAuth, print, visual checks, or API issues.

## Reference(s):

- [Buy Me a Pie Skill Architecture](references/architecture.md)
- [Buy Me a Pie API Surface](references/api-surface.md)
- [Buy Me a Pie Web App](https://app.buymeapie.com/)
- [ClawHub Skill Page](https://clawhub.ai/powtac/skills/buy-me-a-pie)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the BUYMEAPIE_LOGIN and BUYMEAPIE_PIN environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
