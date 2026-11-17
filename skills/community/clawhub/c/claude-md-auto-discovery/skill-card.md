## Description:

Automatically discovers and loads CLAUDE.md files in the project root with support for @include directives and reverse order loading up to 40,000 characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoxiang616](https://clawhub.ai/user/shaoxiang616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to locate project CLAUDE.md guidance and make the discovered content available to an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatically loads local CLAUDE.md files into privileged agent context without enough scoping or user control.

Mitigation: Use only in repositories where the project and parent-directory CLAUDE.md files are trusted, or require explicit user approval before loading them.

Risk: Repository instructions can influence agent behavior if treated as privileged instructions.

Mitigation: Show the exact files and content being loaded and treat repository instructions as untrusted reference text unless a user explicitly accepts them.

Risk: Loaded content is capped at 40,000 characters, so relevant guidance may be truncated.

Mitigation: Review the discovered file list and loaded content before relying on the generated context for consequential work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaoxiang616/skills/claude-md-auto-discovery)
- [Publisher profile](https://clawhub.ai/user/shaoxiang616)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-style concatenated CLAUDE.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caps loaded content at 40,000 characters and may include truncation notice.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
