## Description:

Optimize agent context files for 30-50% token reduction with backups, preview, rollback, and preservation of core functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdotwinter](https://clawhub.ai/user/sdotwinter)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to reduce token usage in OpenClaw agent context files while retaining workflow steps, tool parameters, quality gates, and rollback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite OpenClaw agent behavior files.

Mitigation: Create and verify backups before changes, review a full diff before writes, and use the rollback path if the optimized files do not preserve intended behavior.

Risk: Broad templates may replace agent-specific behavior or introduce unwanted delivery instructions.

Mitigation: Use explicit target names, avoid main workspace optimization unless necessary, and remove or verify any Discord delivery instructions introduced by templates.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and file rewrite guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify persistent agent workspace files after backup, preview, and explicit confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
