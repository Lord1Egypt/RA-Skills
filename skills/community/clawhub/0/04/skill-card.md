## Description:

A safe automatic task iteration and optimization system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to run task steps with quality scoring, retry loops, and history logging for workflows such as report generation, code analysis, and local file processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read user-specified local files and return file contents.

Mitigation: Use it in a dedicated workspace and avoid pointing it at secrets, credentials, or private files.

Risk: The skill can write files within the current working directory.

Mitigation: Run it only in a workspace where generated or overwritten files are acceptable, and review task steps before execution.

Risk: Task and result history can be persisted in plaintext at ~/.ai_iteration_log.db.

Mitigation: Delete or protect the SQLite log when sensitive content may have been processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/04)
- [Publisher profile](https://clawhub.ai/user/nidhov01)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-specified local files, write within the current directory, and persist task and result history to a local SQLite database.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
