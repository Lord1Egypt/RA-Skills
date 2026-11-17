## Description:

Standard SAPCONET SSH command templates for bird reads, Puppeteer runs, and inbox messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run standardized SSH command templates for SAPCONET health checks, bird reads, Puppeteer prerequisite checks, and inbox messaging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a default SAPCONET SSH target.

Mitigation: Install only for this SAPCONET target or set SAPCONET_TARGET explicitly before use.

Risk: Message text passed to msg-sapconet.sh can affect remote shell command construction.

Mitigation: Do not pass untrusted or externally supplied message text until the remote command construction is fixed.

Risk: The bundled scripts are unfinished templates with remote command placeholders.

Mitigation: Review and replace placeholder remote commands before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/billy-sapconet-ssh-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SAPCONET_TARGET configuration and review of remote command placeholders before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
