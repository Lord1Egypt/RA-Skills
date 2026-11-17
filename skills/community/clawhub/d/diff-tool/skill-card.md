## Description:

Diff Tool compares text strings or files, highlights added and removed lines, and can emit standard, simple, or JSON diff output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and documentation maintainers use this skill to compare two text inputs or local files and inspect added or removed content during code review, document comparison, or version comparison workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool reads and prints differences from user-specified local file paths, which may expose sensitive file contents in terminal output.

Mitigation: Only compare files the user intends to inspect and avoid passing secrets or private data unless that output is appropriate for the session.

Risk: The generic diff trigger may be invoked in contexts where the intended scope is ambiguous.

Mitigation: Use explicit trigger phrases or direct commands when comparing content, and document the tool scope clearly for users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/diff-tool)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, ANSI-colored terminal output, or JSON diff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads only user-specified strings or local file paths; supports standard, simple, and JSON output modes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
