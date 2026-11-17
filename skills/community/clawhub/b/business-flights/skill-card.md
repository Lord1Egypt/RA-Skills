## Description:

Searches business class flights, priority boarding tickets, and work-friendly airline seats with extra legroom using flyai as the live travel data source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to collect business flight search parameters, run flyai for live availability and pricing, and format booking options with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global flyai CLI and includes a sudo npm fallback.

Mitigation: Use a reviewed, pinned, user-local or sandboxed CLI installation and do not run the sudo fallback.

Risk: The skill builds shell commands from user-provided travel text.

Mitigation: Validate inputs against the documented parameter table, quote user-provided values, and avoid unsupported flags.

Risk: The skill may store raw travel queries in .flyai-execution-log.json.

Mitigation: Inspect or disable local log persistence and avoid entering sensitive passport, payment, confidential business, or personal travel details.

Risk: The skill produces commercial booking links from a single live source.

Mitigation: Keep the flyai source disclosure, require booking links for displayed options, and treat results as live booking data rather than general travel advice.

## Reference(s):

- [Parameter collection and output templates](references/templates.md)
- [Business flight search playbooks](references/playbooks.md)
- [Failure recovery fallbacks](references/fallbacks.md)
- [Execution log schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the source for flight options and booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
