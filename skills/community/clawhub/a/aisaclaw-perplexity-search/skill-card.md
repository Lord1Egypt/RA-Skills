## Description:

Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, and Sonar Deep Research through AIsa when they need citation-backed search answers, synthesis, reasoning, or research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and optional system instructions are sent to AIsa's Perplexity API using AISA_API_KEY.

Mitigation: Avoid submitting secrets, regulated data, private documents, or confidential internal context unless that sharing is approved for the environment.

Risk: Sonar Deep Research can time out on broad prompts.

Mitigation: Narrow the query, retry later, or use sonar-pro or sonar-reasoning-pro for faster responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/skills/aisaclaw-perplexity-search)
- [AIsa Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar)
- [AIsa Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [AIsa Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [AIsa Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; Sonar Deep Research may take longer and can time out on broad prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
