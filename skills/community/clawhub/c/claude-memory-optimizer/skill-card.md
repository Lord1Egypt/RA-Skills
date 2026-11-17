## Description:

Structured memory system with 4-type classification, frontmatter metadata, and automated migration for OpenClaw memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystour](https://clawhub.ai/user/mystour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to migrate unstructured memory files into categorized memory folders, add frontmatter metadata, and configure structured memory practices for future recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration script can overwrite long-term OpenClaw memory files, including MEMORY.md and log or categorized memory files.

Mitigation: Review and back up the OpenClaw workspace before running the migration; test it on a copy before using valuable memory data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mystour/skills/claude-memory-optimizer)
- [Publisher profile](https://clawhub.ai/user/mystour)
- [README.md](README.md)
- [MEMORY-OPTIMIZATION.md](MEMORY-OPTIMIZATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a JavaScript migration script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The migration script can modify workspace memory files; review and back up the workspace before execution.]

## Skill Version(s):

1.3.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
