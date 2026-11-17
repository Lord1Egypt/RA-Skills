## Description:

Create agent company packages conforming to the Agent Companies specification (agentcompanies/v1), either from scratch or around an existing repository or skills collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlowne12](https://clawhub.ai/user/marlowne12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to interview for, design, and scaffold Paperclip/Agent Companies packages. It supports new companies, teams or departments, and company packages derived from existing repositories or skill collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated company package files or repo-derived instructions may contain incorrect or misleading guidance.

Mitigation: Review generated files before importing or deploying the company package.

Risk: Referenced third-party skills or repositories may add behavior outside the generated package.

Mitigation: Verify referenced skills, provenance, and licenses before use.

Risk: Optional secret inputs such as GH_TOKEN can broaden access if assigned unnecessarily.

Mitigation: Provide secrets only to agents that need them and use least-privilege tokens.

## Reference(s):

- [Agent Companies Specification](https://agentcompanies.io/specification)
- [Agent Companies Protocol](https://agentcompanies.io/)
- [Paperclip](https://github.com/paperclipai/paperclip)
- [Agent Companies Specification Reference](references/companies-spec.md)
- [Example Company Package](references/example-company.md)
- [Creating a Company From an Existing Repository](references/from-repo-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with YAML frontmatter, configuration files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated company packages should be reviewed before import or deployment.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
