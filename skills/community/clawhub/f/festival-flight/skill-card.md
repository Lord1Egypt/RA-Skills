## Description:

Book flights for holiday festivals, cultural events, and seasonal celebrations with flexible date ranges, powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel assistants use this skill to find festival and holiday flight options, compare recommendations, and return booking links from live provider results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to install a global flyai CLI.

Mitigation: Install the CLI only with explicit user approval, preferably pinned to a reviewed version and isolated from the host environment.

Risk: Festival routes, dates, and travel preferences may be sent to an external booking service.

Mitigation: Disclose external transmission of travel details before lookup and avoid collecting unnecessary personal information.

Risk: User-provided travel parameters could be unsafe if interpolated through a shell.

Mitigation: Pass origin, destination, dates, and filters as structured command arguments rather than evaluating user text as shell input.

Risk: Flight prices and availability can be misleading if results are not refreshed from the provider.

Mitigation: Run a fresh flyai lookup for each request and include only results that contain provider booking links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/palexu/skills/festival-flight)
- [Parameter and output templates](references/templates.md)
- [Festival flight playbooks](references/playbooks.md)
- [Failure recovery fallbacks](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when troubleshooting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live flyai CLI results, includes detailUrl booking links, and avoids raw JSON in the final response.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
