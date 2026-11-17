## Description:

Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renning22](https://clawhub.ai/user/renning22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need Perplexity Sonar-backed web answers, comparisons, reasoning, or deeper research reports through AIsa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional system instructions are sent to the AIsa Perplexity Sonar service using an API key.

Mitigation: Avoid submitting confidential, regulated, or private material unless the provider is approved for that data, and keep AISA_API_KEY out of prompts, logs, and shared outputs.

Risk: Sonar Deep Research can be slower and may time out on broad requests.

Mitigation: Narrow the query, retry later, or use sonar-pro or sonar-reasoning-pro when a faster response is needed.

## Reference(s):

- [ClawHub Perplexity Search release](https://clawhub.ai/renning22/skills/aisa-perplexity-search)
- [AIsa Perplexity Sonar API reference](https://docs.aisa.one/reference/post_perplexity-sonar)
- [AIsa Perplexity Sonar Pro API reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [AIsa Perplexity Sonar Reasoning Pro API reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [AIsa Perplexity Sonar Deep Research API reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses from the AIsa client, with Markdown guidance and shell command examples for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; Sonar Deep Research may take longer and retry on transient failures.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
