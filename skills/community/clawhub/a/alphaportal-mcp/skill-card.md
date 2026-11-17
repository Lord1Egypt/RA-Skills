## Description:

Access AlphaPortal school transportation data with shell commands and curl by using a signed-in account's refresh token to request API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account holders use the skill to query student, stop, bus location, notification, and transportation request data from AlphaPortal. It also documents settings changes that affect transportation records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable account refresh token can grant access to AlphaPortal data.

Mitigation: Prefer a protected prompt or credential store; keep tokens out of shell history and transcripts, and revoke any exposed credential.

Risk: Shell write commands can change transportation settings without a preview or confirmation.

Mitigation: Prefer read-only use; require explicit approval of the student and proposed values before any setting change.

## Reference(s):

- [Endpoint reference](references/endpoints.md)
- [AlphaRoute API](https://api.alpharoute.app)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/alphaportal-mcp)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may use bearer tokens and account data; write commands can change live transportation settings.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
