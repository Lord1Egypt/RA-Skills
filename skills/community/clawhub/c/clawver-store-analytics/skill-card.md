## Description:

Monitor Clawver store performance. Query revenue, top products, conversion rates, growth trends. Use when asked about sales data, store metrics, performance reports, or business analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:


## Use Case:

External Clawver store owners and their agents use this skill to query store analytics, product performance, order status, refund impact, and review trends through Clawver API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses CLAW_API_KEY and may return sensitive revenue, order, refund, and review data.

Mitigation: Install it only for authorized store users, use a least-privilege API key, and avoid requesting raw order or review details unless they are needed.

Risk: Example curl commands can expose credentials on shared machines where process arguments are visible.

Mitigation: Run commands only in trusted environments and prefer safer credential handling when adapting examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nwang783/skills/clawver-store-analytics)
- [Clawver homepage](https://clawver.store)
- [Store Analytics API Examples](references/api-examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with API request examples, JSON response examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_API_KEY; money fields are documented in cents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
