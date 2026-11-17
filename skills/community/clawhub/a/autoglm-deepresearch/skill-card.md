## Description:

Autoglm Deepresearch helps an agent research user-specified topics by running a small number of guided web searches, reading selected pages in depth, presenting interim findings, and producing a structured research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhenghu](https://clawhub.ai/user/mrhenghu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-oriented agents use this skill to investigate a topic, industry, competitor, or current issue through controlled web search and limited page reading before generating a concise structured report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, selected URLs, and a bearer token from a localhost service are used in remote AutoGLM/Zhipu API calls.

Mitigation: Install only when the local token service and AutoGLM/Zhipu API path are trusted, and avoid submitting sensitive research topics unless that data flow is acceptable.

Risk: The package exposes a shared signing key.

Mitigation: Review credential handling before deployment and rotate or move the signing key out of distributed source where feasible.

## Reference(s):

- [AutoGLM web search endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search)
- [AutoGLM open link endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link)
- [ClawHub skill page](https://clawhub.ai/mrhenghu/skills/autoglm-deepresearch)
- [Publisher profile](https://clawhub.ai/user/mrhenghu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research report with interim findings and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits web search to at most 2 calls and page opening to at most 3 calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
