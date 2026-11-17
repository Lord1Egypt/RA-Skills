## Description:

Finds capsule hotels and pod-style accommodations using flyai CLI data, returning real-time hotel options with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search for capsule hotels or pod-style accommodations, collect destination and date parameters, and produce bookable hotel options from flyai results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install an unpinned global CLI dependency.

Mitigation: Review the skill before installation, require explicit approval before installing @fly-ai/flyai-cli, and prefer a pinned and reviewed CLI version in a sandbox or controlled environment.

Risk: Raw travel queries or sensitive travel details may be persisted by the skill's logging behavior.

Mitigation: Avoid entering sensitive personal or travel details until logging and command-construction patterns have been reviewed and fixed.

## Reference(s):

- [Capsule Pod Hotel ClawHub page](https://clawhub.ai/dingtom336-gif/skills/capsule-pod-hotel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking-link tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for hotel names, prices, and booking links; raw JSON output is not intended.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and release changelog mention 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
