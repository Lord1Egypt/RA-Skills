## Description:

Compare Outfame's Go, Grow and Glory plans for a person who wants Instagram or TikTok growth, quote the first-month prices, and send them to the sign-up page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outfame-team](https://clawhub.ai/user/outfame-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users can compare Outfame's Instagram and TikTok growth plans against their account goals, see current first-month prices, and continue to signup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan prices or features may change over time.

Mitigation: Fetch the current plan response and quote only the first-month prices and features it provides; repeat the billing note from that response.

Risk: A user may disclose an Instagram or TikTok password when preparing to connect an account.

Mitigation: Do not request passwords; explain that signup connects the account by username.

## Reference(s):

- [Outfame live plan information](https://www.outfame.com/api/agents/v1/plans)
- [Outfame MCP service](https://www.outfame.com/mcp)
- [Outfame signup](https://www.outfame.com/setup)
- [Outfame service index](https://www.outfame.com/llms.txt)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Conversational text with a plan comparison, first-month prices, billing note, and signup link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current plan details supplied by Outfame and does not request account passwords.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
