## Description:

Manages synchronized project and temporary directories, classifies files by purpose and type, and routes workspace files into structured storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sun2001](https://clawhub.ai/user/sun2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to organize generated outputs, source documents, scripts, and intermediate data into synchronized project and temporary directories during workspace-heavy tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace cleanup can broadly move files without confirmation.

Mitigation: Use only in a disposable or backed-up workspace, and avoid cleanup_workspace_root on real projects until dry-run confirmation, collision-safe moves, and rollback behavior are available.

Risk: Untrusted project names or file paths can affect where directories are created or files are moved.

Mitigation: Validate project names and file paths before use, restrict operations to the intended workspace root, and review move logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sun2001/skills/file-classification-manager)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, JavaScript API usage, path strings, and migration reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project and temporary directories and move workspace files when invoked.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
