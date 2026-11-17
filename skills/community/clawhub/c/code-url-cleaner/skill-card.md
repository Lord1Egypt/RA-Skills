## Description:

Automatically removes unnecessary spaces from URLs, commands, file paths, and code snippets in agent output and text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ra1nzzz](https://clawhub.ai/user/ra1nzzz)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users install this skill to clean stray spaces from generated URLs, shell commands, file paths, and code snippets. It can run automatically on agent output or be called manually to clean generated text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-wide output rewriting can alter commands, code snippets, paths, and URLs before the user sees them.

Mitigation: Review cleaned output before executing commands or using generated code; prefer scoped or opt-in use when available.

Risk: Automatic hook activation changes agent display behavior immediately when the skill loads.

Mitigation: Enable only in trusted sessions, use a pinned installer version where possible, and prefer a version with a disable switch or original-versus-cleaned comparison.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ra1nzzz/skills/code-url-cleaner)
- [ClawHub publisher profile](https://clawhub.ai/user/ra1nzzz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Cleaned text or Markdown, including inline code and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rewrite URLs, paths, commands, and code snippets before display when the automatic output hook is active.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
