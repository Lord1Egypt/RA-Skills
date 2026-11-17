## Description:

Boxed fs provides WebAssembly-sandboxed file read, write, append, copy, remove, and listing operations within explicitly declared directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and modify files through a WASM sandbox scoped to a declared workDir and optional mapped directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to download and run an unpinned remote WebAssembly component that can modify or delete exposed files.

Mitigation: Use it only when the remote WASM source and sandbox plugin are trusted, and map only the narrow directories needed for the task.

Risk: Write, overwrite, append, copy, and remove operations can change user data within exposed directories.

Mitigation: Require explicit confirmation before write, overwrite, append, copy, or remove operations.

Risk: Overly broad mapped directories can expose sensitive files to file-management operations.

Mitigation: Avoid mapping sensitive folders and keep workDir and mapDirs scoped to task-specific paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyoung/skills/boxed-fs)
- [Usage reference](references/USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code/tool-call examples and plain-text file operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations are constrained to the declared workDir and explicitly mapped directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
