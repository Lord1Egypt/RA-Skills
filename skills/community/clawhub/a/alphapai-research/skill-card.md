## Description:

Alphapai Research helps agents call AlphaPai/PaiPai financial research APIs for question answering, data recall, stock research workflows, announcement lookup, and chart search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boteeenchan-ship-it](https://clawhub.ai/user/boteeenchan-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research users use this skill to configure an AlphaPai API key and run CLI-backed financial research workflows, including investment Q&A, source-data recall, stock and industry analysis, announcement retrieval, and chart search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext API key.

Mitigation: Remove the bundled key before installation, rotate it with the provider, and require users to configure their own AlphaPai API key locally.

Risk: The client can be configured to use a custom API endpoint.

Mitigation: Use the trusted AlphaPai host by default and approve any alternate endpoint only after reviewing the host and data handling implications.

Risk: The upgrade workflow depends on remote Markdown instructions.

Mitigation: Replace the remote Markdown-driven upgrade path with a pinned, reviewable updater before relying on upgrades in managed environments.

Risk: Financial research prompts and API responses may include confidential client or investment information.

Mitigation: Use the skill only when AlphaPai data handling terms are acceptable for the information being submitted.

## Reference(s):

- [AlphaPai Open API reference](artifact/references/api_reference.md)
- [AlphaPai install and upgrade documentation](https://open-api.rabyte.cn/alpha/open-api/v1/file/api-docs/install.md)
- [ClawHub skill page](https://clawhub.ai/boteeenchan-ship-it/skills/alphapai-research)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to preserve AlphaPai API responses and cited sources without summarizing or truncating them unless the user separately asks for a summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
