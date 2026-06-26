## Description: <br>
Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to call AIsa-hosted Perplexity Sonar endpoints for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts, optional system instructions, and authenticated requests are sent to the external AIsa/Perplexity service. <br>
Mitigation: Use a revocable API key and avoid submitting secrets, private documents, or sensitive personal data unless sharing that data with the provider is intended. <br>
Risk: Long-running deep research requests can time out or return delayed failures. <br>
Mitigation: Narrow the query, retry later, or use sonar-pro or sonar-reasoning-pro for a faster response. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chaimengphp/aisaclaw-perplexity-search) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa Sonar API](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [AIsa Sonar Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [AIsa Sonar Reasoning Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [AIsa Sonar Deep Research API](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; Sonar Deep Research uses a longer timeout with retries and may still require narrower prompts or a faster endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
