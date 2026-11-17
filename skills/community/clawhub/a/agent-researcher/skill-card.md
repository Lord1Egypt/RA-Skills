## Description:

Knowledge builder that extracts entities, relationships, and key facts from web pages, documents, and files into a searchable knowledge base with entity resolution and auto-summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to extract entities, relationships, summaries, and key facts from web pages and local documents, then search or summarize a persistent local research knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL extraction can contact arbitrary user-supplied HTTP or HTTPS URLs, including internal or private-network destinations.

Mitigation: Use only trusted public URLs, avoid localhost and private-network targets, and add egress controls such as an allowlist or proxy before use in sensitive environments.

Risk: Extracted content, entities, summaries, and relationships are stored persistently and may include confidential information or PII.

Mitigation: Do not process confidential or PII-bearing sources unless retention, deletion, and redaction controls are added; manually review and clean memory/research/ as needed.

Risk: Local file and directory extraction can read broad workspace inputs and add them to the persistent knowledge base.

Mitigation: Run the skill from a scoped workspace and provide only approved files or directories for extraction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/agent-researcher)
- [Publisher profile](https://clawhub.ai/user/jlacroix82)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CLI text output, and persistent local JSON knowledge-base files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local state under memory/research/; URL extraction can make outbound HTTP requests to user-supplied URLs.]

## Skill Version(s):

1.1.5 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
