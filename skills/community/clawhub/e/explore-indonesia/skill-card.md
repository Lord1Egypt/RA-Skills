## Description:

Book flights to Indonesia including Bali, Jakarta, and Surabaya. Also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search Indonesia flight options and prepare booking-oriented Markdown summaries from flyai CLI results. It focuses on Bali, Jakarta, Surabaya, and related Indonesia travel planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run the flyai npm CLI before returning travel results.

Mitigation: Require explicit approval before installation, prefer pinned package versions, and run the CLI in a sandboxed environment.

Risk: Travel search details are sent to an external service through the flyai CLI.

Mitigation: Give users a clear privacy disclosure before sending itinerary details and avoid submitting unnecessary personal data.

Risk: Required booking links and flyai branding can introduce commercial-link and URL-safety concerns.

Mitigation: Validate booking URLs before presenting them and make clear that results and links come from the external travel service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/explore-indonesia)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when setup or execution is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the data source and requires booking links for listed results.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
