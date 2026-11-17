## Description:

Build or update the BlueBubbles external channel plugin for Clawdbot (extension package, REST send/probe, webhook inbound).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin19830331](https://clawhub.ai/user/kevin19830331)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build or update a BlueBubbles channel plugin for Clawdbot, including REST send and probe flows, webhook inbound handling, runtime integration, and plugin catalog onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugin work may affect message content, attachments, webhook traffic, and a BlueBubbles server password.

Mitigation: Review the eventual plugin implementation separately before deployment, with attention to credential handling, webhook exposure, and media processing.

Risk: BlueBubbles payloads may vary by version, which can lead to incorrect sender or chat routing if handled too narrowly.

Mitigation: Normalize sender and chat identifiers defensively and test webhook payloads from the deployed BlueBubbles version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin19830331/skills/bluebubbles)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code paths, helper names, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide edits to a BlueBubbles channel plugin that handles message content, attachments, webhook traffic, and server credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
