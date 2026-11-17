## Description:

Book flights to Malaysia, including Kuala Lumpur, Penang, and Kota Kinabalu, with support for related travel planning outputs powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent operators use this skill to collect flight-search parameters, run the flyai CLI, and present Malaysia travel options with booking links. It is intended for real-time flight-search workflows rather than general travel advice from model knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global third-party npm CLI.

Mitigation: Approve installation manually and prefer running the skill in an isolated environment.

Risk: Flight-search details are sent to a third-party service.

Mitigation: Share only the itinerary details needed for the search and avoid unnecessary personal data.

Risk: Outputs are routed through commercial booking links and FlyAI branding.

Mitigation: Treat booking links as commercial output and compare results before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-malaysia)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel results with comparison tables, booking links, and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for factual flight data and requires booking links for each included result.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
