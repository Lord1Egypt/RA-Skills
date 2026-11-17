## Description:

Analyze legacy codebases to extract business rules, technical specifications, and migration requirements. Use when analyzing PHP, Java, Python, or other legacy systems for modernization planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hickhe](https://clawhub.ai/user/hickhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze legacy systems, extract business rules and technical details, assess security and technical debt, and prepare modernization or migration plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One included utility can write outside its intended workspace if given a crafted project name.

Mitigation: Use this skill only in a dedicated workspace, analyze only intended codebases and archaeology-result directories, and avoid untrusted or path-like project names until the issue is fixed.

Risk: The release was flagged for review before installation.

Mitigation: Review and scan the skill before deployment, and validate generated modernization findings before using them for migration decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hickhe/skills/code-archaeology)
- [README](artifact/README.md)
- [Usage Example](artifact/EXAMPLE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON/YAML context documents, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured analysis artifacts for modernization planning and AI Plan Generator integration.]

## Skill Version(s):

2.5.0 (source: server release, target metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
