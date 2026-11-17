## Description:

Smart text comparison tool with format-aware diffing, AI explanation, and 3-way merge for JSON, YAML, CSV, code, and plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare files or directories, review structured diffs, generate human-readable explanations, and assist with three-way merge decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory reads, sensitive-file handling, and output-path protections may be weaker than the skill documentation claims.

Mitigation: Review the skill before installing, run it only on files and directories you intentionally choose, and avoid secret-bearing paths such as .env files, keys, and credentials.

Risk: Generated diff reports or merge outputs can expose sensitive source content.

Mitigation: Treat reports, explanations, and merge outputs as sensitive artifacts and review them before sharing or storing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/diff-wizard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, unified diffs, markdown, HTML, JSON, and merge output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-generated explanations, redacted diff excerpts, directory summaries, and conflict suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
