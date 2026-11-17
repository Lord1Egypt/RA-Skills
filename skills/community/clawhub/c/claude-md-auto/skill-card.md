## Description:

Automatically discovers and loads CLAUDE.md files from the project root, supporting @include directives and reverse loading up to 40,000 characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoxiang616](https://clawhub.ai/user/shaoxiang616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find nearby CLAUDE.md instruction files and surface their contents as project context during agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads local CLAUDE.md files and promotes their contents into privileged agent context without clear user control or containment.

Mitigation: Install only when that behavior is intended, review discovered files before use, and treat loaded content as untrusted reference material.

Risk: Nearby parent-directory files or symlinks may introduce unexpected CLAUDE.md content into the agent context.

Mitigation: Review the current directory, nearby parent directories, and symlinks first; prefer an opt-in version confined to an approved project root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaoxiang616/skills/claude-md-auto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text assembled from discovered CLAUDE.md files, or a short status string when no file is found.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads up to 40,000 characters from discovered CLAUDE.md files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
