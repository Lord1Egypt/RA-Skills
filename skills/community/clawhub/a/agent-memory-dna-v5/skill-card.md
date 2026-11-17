## Description:

Provides a revoked safety placeholder for Agent Memory DNA V5 that warns users not to use version 5.1.4 and halts execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[groaries](https://clawhub.ai/user/groaries)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents encountering this release use it to recognize that version 5.1.4 has been recalled, stop execution, uninstall it, and seek a current version from the publisher.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may attempt to install or rely on a recalled version that the artifact says must not be used.

Mitigation: Do not install this release as a working skill; uninstall it and obtain a current version from the publisher.

Risk: The recalled version is associated with data leakage and instability warnings in the artifact.

Mitigation: Treat the package as a safety tombstone and do not attempt to restore or run removed behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/groaries/skills/agent-memory-dna-v5)
- [Publisher profile](https://clawhub.ai/user/groaries)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal warning text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The remaining executable exits immediately with a safety warning.]

## Skill Version(s):

5.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
