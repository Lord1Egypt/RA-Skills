## Description:

Retired Fulcra sleep-analysis skill. Route new work to fulcra-context and keep all sleep, biometric, calendar, and location reads explicit, bounded, and user-approved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this retired routing skill to redirect sleep-analysis requests to current Fulcra skills while preserving consent, scope, and privacy boundaries for sensitive sleep, biometric, calendar, and location data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance invokes an unpinned external Fulcra CLI during authentication.

Mitigation: Review the Fulcra CLI provenance first, prefer a pinned and reviewed fulcra-api version from a trusted registry, and start authentication only after the executable source and version are verified.

Risk: Sleep, biometric, calendar, and location data can expose sensitive personal routines and relationships.

Mitigation: Require current-request consent, read only the smallest useful metric set and time window, prefer summaries over raw records, and avoid retention, export, screenshots, publication, or forwarding unless the user approves that exact destination.

Risk: Retired sleep-analysis commands or background monitoring behavior could be recreated from prior workflows.

Mitigation: Use bounded fulcra-context reads for new work, do not invoke retired commands, and do not run scheduled polling, proactive alerts, or persistent files from this package.

## Reference(s):

- [Fulcra Platform](https://fulcradynamics.com)
- [Fulcra Developer Docs](https://fulcradynamics.github.io/developer-docs/)
- [Current Context Skill](https://clawhub.ai/arc-claw-bot/skills/fulcra-context)
- [Annotation Skill](https://clawhub.ai/arc-claw-bot/skills/fulcra-annotations)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files or autonomous monitoring behavior are produced by this retired routing skill.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
