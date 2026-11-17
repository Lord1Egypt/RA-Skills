## Description:

Finds low-cost flight options between cities by using flyai CLI results to compare fares, sort by lowest price, highlight budget options, and produce booking-link results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search budget flight options, compare fares and timing, and produce Markdown results with provider booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned third-party flyai CLI.

Mitigation: Review the CLI package before use, pin an approved version where possible, and require user or operator approval before installing or updating it.

Risk: Travel searches are sent to a third-party provider and results include provider booking links.

Mitigation: Disclose the provider path to users, avoid sending sensitive personal or payment details in search prompts, and verify booking pages before purchase.

Risk: The artifact describes persistent local logging of raw travel queries.

Mitigation: Disable raw query logging when possible, avoid logging sensitive travel details, and periodically delete local execution logs.

Risk: Unvalidated command arguments could cause failed or unintended CLI requests.

Mitigation: Restrict generated commands to documented flyai parameters and report CLI errors without substituting unsourced travel data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/cheap-flight)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, savings tips, and inline shell commands for setup or failure recovery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on flyai CLI output and may include provider booking links; the artifact also describes optional local execution logging.]

## Skill Version(s):

3.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
