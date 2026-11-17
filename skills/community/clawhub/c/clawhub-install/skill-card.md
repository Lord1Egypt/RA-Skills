## Description:

Download and install skills from ClawHub directly via curl, bypassing official CLI rate limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upupc](https://clawhub.ai/user/upupc)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install one or more ClawHub skills when the official installation command is rate-limited or failing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can overwrite or delete an existing local skill directory.

Mitigation: Require explicit confirmation before replacement and review the resolved workspace and target skill paths before execution.

Risk: Downloaded packages are installed without checksum or signature verification.

Mitigation: Prefer the official ClawHub/OpenClaw install path or require integrity verification before extraction.

Risk: Unvalidated skill names and archive entries may create unsafe local paths during download or extraction.

Mitigation: Use strict skill-name validation, safe temporary directories, and archive-entry validation before installing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upupc/skills/clawhub-install)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, unzip, and the OpenClaw CLI; downloads and extracts requested skills into the configured OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
