## Description:

File Finder helps agents search and summarize filesystem contents by file name, extension, size, recency, empty entries, duplicate candidates, and directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use File Finder to locate files and inspect directory contents during workspace cleanup, codebase navigation, and filesystem triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe argument handling in embedded Python blocks could allow a crafted path argument to execute code with the invoking user or agent's access.

Mitigation: Do not install or run this version until argument passing is fixed; evaluate only in an isolated workspace with trusted path inputs.

Risk: Filesystem analysis behavior is broader than the manifest describes and may expose file paths, sizes, duplicate candidates, or directory summaries outside the intended scope.

Mitigation: Restrict use to explicit directories and review generated output before sharing it outside the execution environment.

## Reference(s):

- [ClawHub File Finder listing](https://clawhub.ai/ckchzh/skills/file-finder)
- [Referenced inspiration project: sharkdp/fd](https://github.com/sharkdp/fd)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with file paths, counts, and directory summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May traverse user-selected directories and prints capped result sets to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
