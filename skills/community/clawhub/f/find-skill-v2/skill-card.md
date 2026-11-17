## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinjackson](https://clawhub.ai/user/kylinjackson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, present matching options, and install selected skills when they want to extend agent capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages external package execution and global skill installation with confirmation prompts disabled.

Mitigation: Confirm the need for an external skill, inspect the source and publisher, prefer pinned trusted versions, and avoid global unattended installs unless explicitly intended.

Risk: Search results or install recommendations may lead users to third-party skills that have not been independently reviewed.

Mitigation: Review the publisher profile, source, and scan results before installation, and run third-party installers in a restricted environment when possible.

## Reference(s):

- [Skills marketplace](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill search results, install commands, and links for further review.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
