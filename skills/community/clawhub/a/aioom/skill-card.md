## Description:

AI-powered memory guardian for Windows that helps an agent inspect memory use, preview process cleanup, manage aioom monitoring, open a local Web GUI dashboard, and invoke related storage cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support or developer agents use this skill to inspect memory pressure, preview high-risk processes, start or stop aioom monitoring, open the local dashboard, and coordinate storage cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run local aioom and storage-clean programs from hardcoded Windows paths.

Mitigation: Install only when those local files are trusted and verify the resolved executable, script, and working directory paths before execution.

Risk: Memory cleanup can terminate processes and may affect user work or system stability.

Mitigation: Use dry-run or preview output first, verify exact process IDs and process names, and require explicit user approval before cleanup.

Risk: Storage cleanup delegates file deletion or recycling to another local skill.

Mitigation: Review the generated report and target paths before cleanup, and prefer reversible methods such as recycle when available.

Risk: Running with elevated privileges can extend process and filesystem authority.

Mitigation: Avoid administrator privileges unless the user intentionally needs system-wide process and filesystem access.

## Reference(s):

- [Aioom project homepage](https://github.com/bettermen/aioom)
- [Aioom ClawHub skill page](https://clawhub.ai/bettermen/skills/aioom)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process IDs, memory statistics, local file paths, dashboard URLs, configuration examples, and cleanup status summaries.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and changelog mention 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
