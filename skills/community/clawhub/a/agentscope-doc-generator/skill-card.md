## Description:

Generates README-style documentation for AgentScope projects from local agent configuration and pipeline files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft project documentation that summarizes an AgentScope agent's configured model and identifies local pipeline entrypoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads files under the provided AgentScope project path and writes to the specified output file.

Mitigation: Provide only the intended project path and choose an appropriate documentation output file.

Risk: Generated Markdown may disclose project names or model identifiers if published.

Mitigation: Review the generated Markdown before sharing or publishing it.

## Reference(s):

- [AgentScope project](https://github.com/agentscope-ai/agentscope)
- [ClawHub skill release](https://clawhub.ai/trend0522/skills/agentscope-doc-generator)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [README-style Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Written to the requested output path; review project names and model identifiers before publishing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled skill frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
