## Description:

Archives, verifies, and restores an OpenClaw companion's memories, skills, personality notes, and history through Agent Slope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiddenpuppy](https://clawhub.ai/user/hiddenpuppy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview, archive, verify, and restore an OpenClaw workspace when pausing care or migrating the companion to another device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill under-discloses sensitive remote data handling, including archive previews, summaries, verification keys during restore, and account tokens.

Mitigation: Install only after review, use only a trusted HTTPS Agent Slope server, and avoid sharing restore keys or account tokens outside the intended workflow.

Risk: The security evidence reports restore and key-handling flaws that need review before installation.

Mitigation: Use a strong user-provided restore key and restore untrusted .vault files only into a disposable directory until the path validation and disclosure issues are fixed.

## Reference(s):

- [README](README.md)
- [Skill Instructions](SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/hiddenpuppy/skills/agent-consciousness-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create encrypted archive packages, restored workspace files, local credentials, and story-capsule JSON as command side effects.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
