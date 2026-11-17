## Description:

Book flights to Canada including Vancouver, Toronto, and Montreal, with support for hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy-powered flyai results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agents use this skill to search Canada-bound flights and related travel options through the flyai CLI, then present current results with booking links. It is intended for English or Chinese travel planning queries where live provider data is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI.

Mitigation: Review CLI installation manually, pin or verify the package where possible, and require explicit approval before global npm installation or execution.

Risk: User-derived travel text may be transformed into shell commands.

Mitigation: Validate and quote route and date parameters, restrict execution to documented flyai flags, and do not run generated commands from untrusted text without review.

Risk: Booking links and travel results depend on a commercial flyai/Fliggy provider.

Mitigation: Use only CLI-returned detailUrl booking links, disclose provider dependence, and ask the user to verify fare and booking details before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-canada)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and concise travel guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current flyai CLI output; should not fabricate travel options when CLI results are unavailable.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
