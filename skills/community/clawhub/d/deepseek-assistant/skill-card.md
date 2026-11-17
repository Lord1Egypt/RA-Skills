## Description:

Deepseek聊天 helps agents run DeepSeek API chat workflows with Chinese interaction, API-key setup guidance, and parameterized automation for integrations and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and workflow operators can use this skill to request Chinese-language DeepSeek chat assistance, configure API access, and support integration or batch-processing workflows. It is not suitable for decisions that require independent human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the skill asks for broad file and command access while its actual scope and behavior are unclear.

Mitigation: Install only from a trusted publisher, review proposed file and shell operations before execution, and grant the minimum local authority needed for the specific workflow.

Risk: The security guidance rates the release as suspicious despite no clear malicious behavior.

Mitigation: Review carefully before installing and use a constrained environment for any workflow that touches files, secrets, or commands.

Risk: The artifact requires API-key configuration for DeepSeek-style chat workflows.

Mitigation: Store API keys in environment variables or a secret manager, avoid committing keys, and rotate credentials if exposure is suspected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request API-key configuration and broad local read, write, and command-execution authority; review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
