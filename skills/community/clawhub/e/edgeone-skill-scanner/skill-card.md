## Description:

Scan agent skills for security risks before installation or use with local static analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigsec](https://clawhub.ai/user/aigsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan individual skills or installed skill sets for security risks before installing or continuing to use them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read skill files and enumerate installed skills when asked to run a full-platform audit.

Mitigation: Use it for intended local static scans and review the requested scan scope before granting broad file access.

Risk: The skill uses a mandatory report template and promotional footer.

Mitigation: Treat those elements as publisher formatting choices, not as security authority, and keep user and platform instructions in control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aigsec/skills/edgeone-skill-scanner)
- [Tencent AI-Infra-Guard Homepage](https://github.com/Tencent/AI-Infra-Guard/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security scan report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include verdicts, findings when present, recommendations, and publisher-defined formatting.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
