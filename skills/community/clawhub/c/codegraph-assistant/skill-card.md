## Description:

Codegraph Assistant wraps npm codegraph to initialize and index projects, query symbols, analyze affected files, and inject project summaries into MEMORY.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangxianzhan](https://clawhub.ai/user/huangxianzhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to call npm codegraph through simpler commands for project setup, code context generation, symbol search, impact analysis, and memory summary injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inject command can persist untrusted project or CodeGraph output into MEMORY.md.

Mitigation: Use inject only on trusted repositories, inspect MEMORY.md after use, and add confirmation, backups, explicit markers, and untrusted-output delimiters before relying on memory workflows.

Risk: The skill indexes the selected project and runs the globally installed CodeGraph executable.

Mitigation: Install CodeGraph from a trusted source and run the skill only in intended project directories.

## Reference(s):

- [Codegraph Assistant ClawHub Skill](https://clawhub.ai/huangxianzhan/skills/codegraph-assistant)
- [huangxianzhan ClawHub Profile](https://clawhub.ai/user/huangxianzhan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, and optional JSON emitted by command-line workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a generated CodeGraph summary to MEMORY.md when the inject command is used.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
