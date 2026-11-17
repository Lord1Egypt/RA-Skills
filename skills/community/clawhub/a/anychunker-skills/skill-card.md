## Description:

Guides agents in using the `anychunker` Python library to split text, Markdown, code, and long documents for LLM, RAG, and agent pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyforge](https://clawhub.ai/user/anyforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and apply AnyChunker splitting strategies for RAG ingestion, token budgeting, Markdown structure preservation, code chunking, sentence splitting, and semantic chunking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may change behavior across environments.

Mitigation: Use an isolated Python environment and pin package versions for production workflows.

Risk: RAG, embedding, or vector database workflows may expose proprietary code, secrets, PII, or regulated documents to external services.

Mitigation: Confirm data handling requirements before sending sensitive content to any external embedding or vector database provider.

## Reference(s):

- [AnyChunker API Reference](references/api-reference.md)
- [AnyChunker Recipes](references/recipes.md)
- [AnyChunker PyPI Package](https://pypi.org/project/anychunker/)
- [AnyChunker DeepWiki](https://deepwiki.com/anyforge/anychunker/)
- [ClawHub Skill Page](https://clawhub.ai/anyforge/skills/anychunker-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose chunk_size, chunk_overlap, tokenizer, language, embedding, and batching choices based on user intent.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
