## Description:

Deprecated legacy release for a Bash-based OpenClaw context cleanup skill that analyzes workspace memory files, proposes archival candidates, and archives them after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irideas](https://clawhub.ai/user/irideas)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this deprecated compatibility release to inspect memory-log volume, identify low-value or older Markdown memory records, and archive candidates after reviewing a plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe JSON generation can produce unreliable output or create command-execution exposure in crafted environments.

Mitigation: Avoid --json until JSON serialization is fixed, suppressed JSON errors are removed, and the node dependency is explicitly declared if JSON output remains supported.

Risk: Archive filename collisions can overwrite workspace memory files.

Mitigation: Avoid archive mode on workspaces with untrusted or duplicate-named memory files until collision-safe archive paths are implemented.

Risk: Archive mode changes workspace files.

Mitigation: Run analyze and plan first, use --dry-run for review, and require explicit confirmation before archive execution.

## Reference(s):

- [Context Cleanup Policy](references/policy.md)
- [ClawHub Skill Page](https://clawhub.ai/irideas/skills/bobo-context-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown and terminal text summaries with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archive mode can move selected memory Markdown files into memory/archive after confirmation or --yes.]

## Skill Version(s):

0.2.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
