## Description:

Provides prompt engineering guidance for large language model optimization, retrieval-augmented generation systems, fine-tuning, chain-of-thought and few-shot learning, model evaluation, and benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, evaluate, and refine prompts, RAG workflows, fine-tuning plans, and LLM application patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example agent code includes a calculator pattern that could execute arbitrary Python if copied into an operational agent.

Mitigation: Treat examples as illustrative only and replace dynamic evaluation with a constrained expression parser or vetted calculator tool before deployment.

Risk: API, RAG, web-search, and fine-tuning snippets may expose sensitive prompts, documents, or training data to external providers if adapted directly.

Mitigation: Redact sensitive data, review provider data handling, and apply data access controls before using the snippets in production workflows.

## Reference(s):

- [Prompt Engineer Code Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-prompt-engineer)
- [Publisher Profile](https://clawhub.ai/user/mtsatryan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with explanatory prose and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include illustrative API, RAG, web-search, fine-tuning, and evaluation snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
