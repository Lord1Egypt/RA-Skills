## Description:

Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, research-ready outputs, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run AIsa-backed web research, multi-source retrieval, recent-signal scans, comparison research, and research brief generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and optional system prompts are sent to AIsa's API.

Mitigation: Do not include passwords, private customer data, confidential internal instructions, or other sensitive content unless policy allows sending it to AIsa.

Risk: The skill requires an AISA_API_KEY for API access.

Mitigation: Store the API key securely and verify trust in AIsa before installation and use.

Risk: Long-running deep research requests can time out or fail.

Mitigation: Use narrower prompts, retry later, or switch to a faster Sonar mode when deep research is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/aisa-perplexity-sonar-search)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON API responses and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; sends the query and optional system prompt to AIsa Sonar endpoints.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
