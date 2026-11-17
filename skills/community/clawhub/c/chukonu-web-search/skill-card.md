## Description:

Uses the Chukonu remote MCP search and research tools to retrieve web, academic, patent, financial, and Chinese legal evidence for cited real-time research and verification tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhhwor](https://clawhub.ai/user/hhhwor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need externally sourced, current, citable evidence for search, fact checking, counter-evidence, Chinese legal retrieval, financial-news research, PDF review, and persistent multi-turn research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and research objectives are sent to the Chukonu remote MCP service.

Mitigation: Avoid submitting sensitive information unless the user accepts that remote processing; use the normal OAuth flow and let the host manage tokens.

Risk: Static Authorization headers, API tokens, or leaked OAuth material could create authentication and credential-handling risk.

Mitigation: Do not configure static Authorization headers or CHUKONU_SEARCH_API_TOKEN, and do not print or persist authorization codes, callback URLs, access tokens, or refresh tokens.

Risk: Legal and financial results may have incomplete coverage, unsupported filters, missing public links, or source-specific limitations.

Mitigation: Check retrieval assessments, failures, filter execution, legal status, and financial data plans before making claims; present limitations and use primary or professional review for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhhwor/skills/chukonu-web-search)
- [Chukonu remote MCP endpoint](https://search.houdutech.cn/web/mcp/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with citations, inline JSON examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cited evidence, retrieval limitations, research status, and OAuth setup guidance.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
