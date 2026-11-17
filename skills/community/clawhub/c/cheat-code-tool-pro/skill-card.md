## Description:

能力扩展工具专业版 helps agents perform enterprise knowledge retrieval across configured sources, with batch querying, local caching, and team-sharing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise teams use this skill to guide agents through multi-source technical knowledge lookup, batch research, cache configuration, and shared knowledge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad access to internal or external knowledge sources and credentials.

Mitigation: Use narrowly scoped tokens and enable only the data sources required for the current workflow.

Risk: The skill can write local or team-shared caches that may contain sensitive project details.

Mitigation: Confirm cache and shared-storage locations before use, and avoid sharing sensitive results unless the team repository is approved for that data.

Risk: The activation language is partly mismatched and broad, which can cause the skill to be selected outside its intended scope.

Mitigation: Review the requested task before activation and use the skill only for configured knowledge retrieval, caching, and team-sharing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cheat-code-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured text, tables, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration examples for data sources, cache settings, API credentials, and team-sharing workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
