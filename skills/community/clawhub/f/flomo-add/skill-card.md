## Description:

flomo-add sends a single memo to a configured flomo webhook using a Python requests script that reads .flomo.config and supports dry-run inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giraffe-tree](https://clawhub.ai/user/giraffe-tree)

### License/Terms of Use:


## Use Case:

Developers and users who keep notes in flomo use this skill to add a single memo from an agent workflow or command-line flow. It is suited for quick thought capture, temporary notes, or automated one-off memo creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memo content is sent to the configured flomo webhook.

Mitigation: Install and use the skill only when sending note content to flomo is intended.

Risk: The flomo webhook URL functions like a credential and may appear in configuration or dry-run output.

Mitigation: Treat the webhook URL like a password, avoid sharing dry-run output, and verify .flomo.config points to the correct HTTPS flomo webhook before sending sensitive notes.

## Reference(s):

- [flomo](https://flomoapp.com)
- [ClawHub skill page](https://clawhub.ai/giraffe-tree/skills/flomo-add)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or runs a single memo submission request and may print request details during dry runs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
