## Description:

Benchmark CPU, memory, disk I/O, and network on your system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local CPU, memory, disk I/O, network, and comparison checks when measuring server performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The disk benchmark can write and delete a predictable file in a user-provided directory.

Mitigation: Review before installing, do not run the disk benchmark in sensitive, shared, or privileged directories, and do not run it with elevated privileges.

Risk: The network benchmark contacts the host provided by the user.

Mitigation: Use only approved hosts and review network policy before running the network benchmark.

Risk: The compare command can reveal file contents or differences from arbitrary files the skill can access.

Mitigation: Run comparisons only on intended files and avoid sensitive paths.

## Reference(s):

- [Benchmark Tool on ClawHub](https://clawhub.ai/bytesagain1/skills/benchmark-tool)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and textual benchmark output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can write benchmark data under ~/.local/share/benchmark-tool and can run local shell commands that inspect system resources.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
