## Description:

Plan Korea travel using flyai CLI results for flights, hotels, attractions, itinerary planning, visa information, travel insurance, car rental, and booking-linked recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search Korea flights, hotels, attractions, and related travel services through flyai CLI output, then present concise Markdown recommendations with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run a third-party flyai CLI and install it globally through npm if missing.

Mitigation: Review and install a pinned CLI version manually before use; inspect proposed commands before execution.

Risk: Travel queries may be sent to a third-party provider and booking links may route users to external services.

Mitigation: Avoid entering sensitive passport, payment, or private itinerary details unless the provider's data handling is acceptable.

Risk: The artifact describes local execution logging that can include raw user queries.

Mitigation: Review or disable local logging before production use, especially for personal or confidential travel requests.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and occasional bash commands for CLI setup or retry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
