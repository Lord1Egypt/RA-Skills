## Description:

Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jenish-sojitra](https://clawhub.ai/user/jenish-sojitra)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to inventory installed skills, submit security scan data, and review results in a Clawned dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends credentials and local machine metadata to a configurable remote server.

Mitigation: Use only the official HTTPS Clawned server unless the endpoint is fully trusted, and treat CLAWNED_API_KEY as sensitive and revocable.

Risk: Initial sync can disclose hostname, OS family, installed-skill inventory, and local agent state.

Mitigation: Review the privacy impact before installing and run the skill only in environments where this metadata sharing is acceptable.

Risk: Explicit path scans can send selected skill file contents to the Clawned server for analysis.

Mitigation: Scan only directories intended for review and avoid scanning files that contain secrets or private content.

## Reference(s):

- [Clawned homepage](https://clawned.io)
- [ClawHub skill page](https://clawhub.ai/jenish-sojitra/skills/clawnedhub)
- [Detection Patterns](references/detection-patterns.md)
- [Threat Model](references/threat-model.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and CLAWNED_API_KEY; CLAWNED_SERVER may override the default server.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
