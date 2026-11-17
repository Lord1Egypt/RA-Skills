## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp33333333333](https://clawhub.ai/user/cp33333333333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for relevant installable skills, compare options, and install skills that extend an agent's capabilities for a requested task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer broad requests into unpinned package commands or global installation of external skills with confirmations skipped.

Mitigation: Prefer pinned CLI and skill versions, inspect suggested skill sources before installing, avoid global installs unless needed, and do not skip confirmations for unfamiliar packages.

Risk: Recommended skills may be third-party packages with different publishers, licenses, and security posture.

Mitigation: Review the publisher profile, provenance, license, and security information for a suggested skill before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp33333333333/skills/find-skills1)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party skill names, package identifiers, profile links, and install commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
