## Description:

Multi-source search engine powered by AIsa API that combines Tavily web search, Scholar academic search, Smart hybrid search, and Perplexity deep research through a single AIsa API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to run web, academic, hybrid, Tavily, Perplexity, and multi-source searches from an agent workflow. It is suited for source discovery, research triage, URL content extraction, and confidence-scored search synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URLs, and extracted content requests are sent to AIsa and its integrated search providers.

Mitigation: Do not use the skill with secrets, private internal URLs, regulated data, or confidential research topics unless that data flow is approved.

Risk: Search and synthesized research outputs may be incomplete, stale, or affected by source quality.

Mitigation: Review cited sources and independently verify important claims before using results for business, legal, medical, security, or financial decisions.

## Reference(s):

- [AIsa](https://aisa.one)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [AIsa API Documentation](https://docs.aisa.one)
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/aisa-multi-search-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text search results with URLs, extracted content, citations, confidence scoring, and optional JSON-like API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends user-directed queries, URLs, and extraction requests to AIsa-backed APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
