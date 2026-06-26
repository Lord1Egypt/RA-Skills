## Description: <br>
Download and install skills from ClawHub directly via curl, bypassing official CLI rate limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upupc](https://clawhub.ai/user/upupc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install one or more ClawHub skills by direct download when the official ClawHub installation command is rate-limited, failing, or not preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can overwrite or delete an existing installed skill directory before extracting a downloaded package. <br>
Mitigation: Back up the OpenClaw skills directory first and run it only when replacing an existing skill is intended. <br>
Risk: The installer downloads remote skill packages into future agent behavior without independent package verification. <br>
Mitigation: Use it only for trusted skill slugs from trusted publishers, review the installed skill before use, and prefer the official ClawHub installer when available. <br>
Risk: Malformed or arbitrary skill names could affect paths outside the intended target. <br>
Mitigation: Pass only known ClawHub skill slugs from trusted sources and avoid arbitrary path-like input. <br>


## Reference(s): <br>
- [ClawHub Install on ClawHub](https://clawhub.ai/upupc/clawhub-install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, unzip, and the OpenClaw CLI; installs downloaded skill packages into the OpenClaw workspace skills directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
