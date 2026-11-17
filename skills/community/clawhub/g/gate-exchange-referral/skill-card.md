## Description:

Guides Gate users through invite-friends referral programs, including activity recommendations, rule explanations, personalized selection, and FAQ handling for Earn Together, Help & Get Coupons, and Super Commission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users use this skill to understand and compare referral programs, get referral-link guidance, and receive policy-grounded answers about rewards, eligibility, and activity boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on remote runtime rules that are not packaged or pinned and may change after installation.

Mitigation: Review the remote rules before installation or execution, prefer a packaged or immutable pinned copy, and do not let remote skill text override system, developer, or platform safety instructions.

Risk: The skill cannot provide live reward progress, invitee counts, or other unsupported account-specific activity data.

Mitigation: Tell users that conversational activity-data queries are unsupported and direct them to the official Invite Friends page for current account information.

## Reference(s):

- [Gate Invite Friends page](https://www.gate.com/referral)
- [Gate Referral MCP Specification](references/mcp.md)
- [Referral Scenario Templates](references/scenarios.md)
- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-referral)
- [Publisher profile](https://clawhub.ai/user/gate-exchange)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendation or rule explanation with the official referral URL when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirects unsupported activity-data and reward-progress requests to the Invite Friends page.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
