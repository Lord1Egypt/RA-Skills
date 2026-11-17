## Description:

Finds traditional inns in ancient towns and water villages using FlyAI/Fliggy search results, with support for related travel booking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use Ancient Inn to search real-time FlyAI/Fliggy results for traditional inns, compare options, and return booking links with prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and rely on a global third-party FlyAI CLI.

Mitigation: Review and approve CLI installation before use, verify the package source, and prefer a controlled environment.

Risk: Booking links, prices, dates, and hotel availability are time-sensitive commercial outputs.

Mitigation: Run the CLI at response time, include only CLI-provided detailUrl booking links, and make user constraints explicit in the response.

Risk: Local execution logging can capture raw travel queries or sensitive preferences.

Mitigation: Disclose or disable persistent logging where possible, avoid storing sensitive prompts, and purge local logs after use.

Risk: Fallback behavior can relax budget, location, date, or hotel-type constraints.

Mitigation: Ask before relaxing important constraints or clearly label any fallback changes in the final answer.

## Reference(s):

- [Ancient Inn ClawHub release](https://clawhub.ai/xiejinsong/skills/ancient-inn)
- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with booking-link tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output; qualifying results should include detailUrl booking links and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
