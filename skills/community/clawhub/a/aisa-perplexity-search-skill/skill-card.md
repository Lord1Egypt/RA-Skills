## Description:

Perplexity Search lets agents call AIsa-hosted Perplexity Sonar endpoints for citation-backed web answers, analytical reasoning, and long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route explicit Perplexity-powered search requests to AIsa Sonar endpoints for cited answers, comparison, reasoning, or deep research when structured retrieval is not the desired path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and optional system messages are sent to api.aisa.one under the user's AIsa account.

Mitigation: Avoid submitting secrets, private documents, regulated data, or internal prompts unless that disclosure is acceptable for the account and use case.

Risk: Sonar Deep Research requests can be slower and may time out.

Mitigation: Use narrower prompts, retry later, or switch to sonar-pro or sonar-reasoning-pro when a faster response is needed.

## Reference(s):

- [Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar)
- [Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; Sonar Deep Research uses a longer timeout and automatic retries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
