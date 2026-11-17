## Description:

Use this skill when an agent needs to operate the `cosin` CLI from the terminal to list available skills, call COS API paths, and call `/cos/...` skills through x402 pay-and-call requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcipher0](https://clawhub.ai/user/0xcipher0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run authenticated `cosin` CLI commands, validate relative COS paths, inspect available COS-backed skills, and submit direct COS API or `/cos/...` skill requests from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: COS bearer tokens may grant broad authenticated and payment-backed API access if exposed or reused.

Mitigation: Use short-lived, least-privileged tokens; do not print, commit, or hardcode tokens; review commands before execution.

Risk: The `--base-url` override can send authenticated requests to an unintended endpoint.

Mitigation: Use `--base-url` only with a known trusted HTTPS COS endpoint.

Risk: Running an unpinned CLI package with a live token increases supply-chain and credential exposure risk.

Mitigation: Prefer a pinned or locally verified `cosin` CLI before using live credentials.

Risk: `/cos/...` requests are routed as x402 pay-and-call operations and may trigger paid actions.

Mitigation: Confirm the target path, method, and request body before submitting payment-backed calls.

## Reference(s):

- [COS skills catalog endpoint](https://skills.bankofuniverse.org/skills)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, API calls, Configuration]

**Output Format:** [Markdown with inline shell commands and request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a sensitive COS bearer token supplied at runtime.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
