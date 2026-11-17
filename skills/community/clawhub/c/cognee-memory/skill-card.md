## Description:

Cognee Memory System helps agents remember, recall, forget, and improve knowledge using Cognee's vector and graph memory tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent memory, semantic recall, and knowledge-graph-backed context retrieval to assistants, copilots, and multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install external Python and npm packages.

Mitigation: Review package sources and versions in an isolated workspace before using the skill with sensitive projects.

Risk: The described OpenClaw plugin can persist prompts, tool actions, and session context.

Mitigation: Avoid storing secrets or regulated data, confirm where memory is stored, and treat recalled content as untrusted context.

Risk: Bulk forget and persistent-memory behavior may not match user expectations.

Mitigation: Confirm deletion behavior and test forget commands before relying on them in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smseow001/skills/cognee-memory)
- [Cognee Website](https://cognee.ai)
- [Cognee GitHub Repository](https://github.com/topoteretes/cognee)
- [Cognee LLM Provider Configuration](https://docs.cognee.ai/setup-configuration/llm-providers)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external package installation steps and memory operation examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
