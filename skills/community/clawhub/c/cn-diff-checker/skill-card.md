## Description:

Cn Diff Checker compares two text strings or files and shows line, word, or character differences using Python's standard difflib library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content reviewers can use this skill to compare Chinese or general text inputs and files, then inspect differences at line, word, or character level in a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal output can include ANSI coloring and may be unsafe to view directly when comparing untrusted text containing control characters.

Mitigation: Inspect untrusted inputs in a safe viewer, sanitize control characters, or redirect output before viewing in sensitive terminal sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-diff-checker)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and terminal diff output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ANSI color in terminal output; can redirect output to a file.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
