## Description:

Manage Duplicati backups on the server using secure Bearer tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robnew](https://clawhub.ai/user/robnew)

### License/Terms of Use:


## Use Case:

Developers, operators, and backup administrators use this skill to monitor Duplicati server status, list backup jobs, start selected jobs, and retrieve recent error logs through the Duplicati REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived backup-administration token can expose backup control if it is stored insecurely or leaked.

Mitigation: Store DUPLICATI_TOKEN in a protected secret source where possible, restrict file permissions, and rotate or revoke the token if exposed.

Risk: Plain HTTP Duplicati URLs can expose administrative backup traffic or tokens on the network.

Mitigation: Use the skill only with HTTPS, a trusted local tunnel, or another encrypted channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robnew/skills/duplicati-skill)
- [Publisher profile](https://clawhub.ai/user/robnew)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Duplicati REST API endpoints, status explanations, job identifiers, storage free-space details, and recent log summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
