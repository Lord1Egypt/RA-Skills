## Description:

Build RAG (Retrieval Augmented Generation) pipelines with web search and LLMs using Tavily Search, Exa Search, Exa Answer, and OpenRouter-hosted LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and AI agent builders use this skill to assemble retrieval-augmented generation workflows for research assistants, fact-checking, grounded answers, knowledge retrieval, URL content analysis, and research report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The primary setup path runs a mutable remote installer directly through the shell.

Mitigation: Review the installer before use or prefer a manual, pinned, checksum- or signature-verified CLI installation.

Risk: Example workflows may send queries, private documents, confidential URLs, or retrieved content to external search and LLM providers.

Mitigation: Use only provider accounts approved for the data involved, and avoid submitting secrets or confidential material.

## Reference(s):

- [Ai Rag Pipeline on ClawHub](https://clawhub.ai/okaris/skills/ai-rag-pipeline)
- [inference.sh](https://inference.sh)
- [Adding Tools to Agents](https://inference.sh/docs/agents/adding-tools)
- [Building a Research Agent](https://inference.sh/blog/guides/research-agent)
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with bash examples and JSON command inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include search results, LLM prompts, grounded summaries, fact-check reports, and reusable shell snippets.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
