## Description:

Better Tavily Search helps agents retrieve fresh web evidence with Tavily using intent profiles, compact result sets, targeted extraction, and site mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soymilkwinsagain](https://clawhub.ai/user/soymilkwinsagain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find current web evidence, discover source links, look up official documentation, verify recent facts, and extract concise evidence from selected URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API endpoint override could send the Tavily API key and user queries to an unintended server.

Mitigation: Install only from a trusted source, avoid setting TAVILY_API_BASE unless the endpoint is trusted, and restrict outbound network access to Tavily where possible.

Risk: Broad or over-expanded web searches can return stale, incomplete, or low-quality evidence.

Mitigation: Use the documented small-result workflow: inspect source metadata, rewrite weak queries, and extract only the strongest 1-3 URLs when more detail is needed.

## Reference(s):

- [Better Tavily Search on ClawHub](https://clawhub.ai/soymilkwinsagain/skills/better-tavily-search)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Escalation Rules](reference/escalation_rules.md)
- [Output Contract](reference/output_contract.md)
- [Parameter Matrix](reference/param_matrix.md)
- [Query Playbook](reference/query_playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown retrieval results with concise shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY. Defaults favor small evidence sets, source metadata, and targeted extraction over large raw-content payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
