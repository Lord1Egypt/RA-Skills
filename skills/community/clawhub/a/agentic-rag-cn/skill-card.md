## Description:

Deep web research across 11 Chinese and international sources (Baidu, Bing, Sogou, Quark, ChinaSo, WeChat, Yandex, Zhihu, Bilibili, V2EX, GitHub).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nb-clh](https://clawhub.ai/user/nb-clh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-capable agents use this skill to run multi-source deep web research, especially for Chinese platforms, through a local Agentic RAG-CN API and present answers with evidence, sources, confidence, and contradictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search questions are sent to a local Agentic RAG-CN service that may store logs or contact external search providers.

Mitigation: Avoid sending sensitive prompts unless you understand and accept that local service's logging and provider behavior.

Risk: The skill depends on a trusted local service running on port 18888.

Mitigation: Run the health check before use and install only when you intentionally operate or trust that local service.

## Reference(s):

- [API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/nb-clh/skills/agentic-rag-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with answer summaries, evidence tables, contradiction notes, and source lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores and source URLs returned by the local API.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
