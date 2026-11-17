## Description:

Provides a wrapper for delegating software design, development, testing, optimization, and refactoring tasks to Claude Code through a Node.js script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the-invulnus](https://clawhub.ai/user/the-invulnus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to delegate software development, debugging, testing, refactoring, and design-support tasks to Claude Code from a local Node.js wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegating coding work to Claude Code can expose repository context and allows broad read, write, edit, shell, and project access.

Mitigation: Use only on approved repositories, pin the SDK version, and require explicit approval before sending sensitive or proprietary code.

Risk: Claude Code may propose or perform incorrect, unsafe, or unwanted software changes.

Mitigation: Review generated changes, shell activity, and test results before merging or deploying work produced through the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and optional log-file text containing Claude Code results and a resume session ID.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a globally installed Claude agent SDK and can preserve context by resuming a prior Claude Code session.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
