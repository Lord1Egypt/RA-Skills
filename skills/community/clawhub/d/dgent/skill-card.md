## Description:

dgent checks files and commit messages for AI tells before committing, flagging naming patterns, catch-rethrow, AI vocabulary, emoji, and trailers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itscodejac](https://clawhub.ai/user/itscodejac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use dgent before commits to inspect source files, directories, and commit messages for common AI-generated patterns and to apply deterministic cleanup where appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm tool.

Mitigation: Pin or verify the npm package where possible before installing it in important repositories.

Risk: Automatic git-hook cleanup or fix mode can rewrite files or commit messages.

Mitigation: Use JSON/check modes first, review diffs after any --fix run, and confirm hook behavior before enabling it in signed or policy-controlled workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itscodejac/skills/dgent)
- [dgent homepage](https://github.com/ItsCodejac/dgent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can report clean status, fixes, flags, cleaned output, rule catalogs, and exit codes.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
