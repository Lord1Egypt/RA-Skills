## Description:

Evaluate AI training and RAG data quality using rule-based or LLM-based metrics with Dingo's flexible, multi-format assessment framework and CLI/SDK support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e06084](https://clawhub.ai/user/e06084)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data or ML engineers use this skill to configure and run Dingo evaluations on datasets, generated answers, RAG outputs, and articles. It supports local rule-based checks, provider-backed LLM metrics, safety-oriented evaluators, and fact-checking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-based and fact-checking modes can send selected datasets, articles, claims, or derived content to configured model and search providers.

Mitigation: Use local rule-based evaluators for confidential data and enable provider-backed modes only for content approved for those services.

Risk: Custom OpenAI-compatible endpoints can route data or API credentials to untrusted providers.

Mitigation: Use trusted provider endpoints, avoid untrusted OPENAI_BASE_URL values, and scope provider keys with least privilege.

Risk: Generated outputs may contain original article text, dataset content, evaluation details, or provider-derived verification results.

Mitigation: Review generated output directories before sharing and delete sensitive outputs when they are no longer needed.

## Reference(s):

- [Dingo ClawHub Page](https://clawhub.ai/e06084/skills/dingo)
- [Dingo GitHub Repository](https://github.com/MigoXLab/dingo)
- [Dingo SaaS Platform](https://dingo.openxlab.org.cn/)
- [dingo-python on PyPI](https://pypi.org/project/dingo-python/)
- [Metrics Documentation](https://github.com/MigoXLab/dingo/blob/main/docs/metrics.md)
- [RAG Evaluation Guide](https://github.com/MigoXLab/dingo/blob/main/docs/rag_evaluation_en.md)
- [Dingo MCP Documentation](https://github.com/MigoXLab/dingo/blob/main/README_mcp.md)
- [Advanced Configuration](artifact/references/advanced-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, Python code snippets, shell commands, and structured JSON for fact-checking reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dingo evaluations may produce summary.json, per-item JSONL reports, timestamped output directories, and ArticleFactChecker fields such as accuracy_score, false_claims, and all_claims.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
