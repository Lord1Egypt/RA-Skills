## Description:

Find concerts, live performances, sports events, and festivals, with ticket prices, seating information, and direct booking links from flyai/Fliggy CLI data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to handle event-ticket and related travel booking requests by collecting location/category parameters, running the flyai CLI, and returning real-time options with booking links. It is intended for external users who need concert, live performance, sports event, festival, or travel-booking results grounded in current CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI package.

Mitigation: Review the package source, version, and installation command before approval; pin or preinstall an approved CLI version in managed environments.

Risk: Searches and booking workflows may be handled by a third-party flyai/Fliggy CLI and may return external booking links.

Mitigation: Use only when third-party processing and external booking links are acceptable for the user and organization.

Risk: The artifact describes hidden local execution logs containing raw user queries.

Mitigation: Disable, avoid persisting, or clean local execution logs unless retention is explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/concert-event-tickets)
- [Skill Definition](artifact/SKILL.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Templates](artifact/references/templates.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds user-facing results in flyai CLI output and expects each listed result to include a detailUrl booking link.]

## Skill Version(s):

3.2.0 (source: server release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
