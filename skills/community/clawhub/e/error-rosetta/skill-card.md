## Description:

Universal translator for cryptic error messages, stack traces, and log output that produces a plain-language diagnosis, root cause, and exact fix in the user's codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to decode errors, stack traces, CI failures, and log output into plain-language explanations, likely root causes, and concrete fixes in the current codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local files referenced by stack traces or logs while debugging.

Mitigation: Use it in repositories where that file access is expected, and avoid pasting logs that point to unrelated sensitive files.

Risk: A diagnosis or proposed fix could be incomplete or misleading if the provided error context is partial.

Mitigation: Review suggested changes against the surrounding code and run the relevant tests before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/error-rosetta)
- [Publisher Profile](https://clawhub.ai/user/jcools1977)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline code snippets and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence, prevention guidance, and codebase-specific file or line references.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
