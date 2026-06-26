## Description: <br>
Perplexity Search lets agents call AIsa Perplexity Sonar endpoints for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user specifically requests Perplexity-powered search, comparison, analytical reasoning, or deep research through AIsa Sonar endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and optional system instructions are sent to AIsa/Perplexity. <br>
Mitigation: Avoid including secrets or sensitive private data in prompts sent through this skill. <br>
Risk: The skill requires an AISA_API_KEY for authenticated API calls. <br>
Mitigation: Use a dedicated, revocable API key and avoid hardcoding it in prompts, files, or shared logs. <br>
Risk: Deep research requests can be slow or time out. <br>
Mitigation: Narrow the query, retry later, or use Sonar Pro or Sonar Reasoning Pro when a faster answer is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/aisa-perplexity-search-skill) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [AIsa Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [AIsa Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [AIsa Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-backed responses with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Citation-backed answers may vary by selected Sonar endpoint; deep research can take longer and may time out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
