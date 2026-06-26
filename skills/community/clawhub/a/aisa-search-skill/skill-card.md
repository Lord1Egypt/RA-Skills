## Description: <br>
Intelligent search for agents. Multi-source retrieval across web, scholar, Tavily, and Perplexity Sonar models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add web, scholar, Tavily, and Perplexity Sonar retrieval to agent workflows, including fast lookup, citation-rich answers, and longer research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, prompts, and URLs are sent to AIsa-backed external services. <br>
Mitigation: Avoid sending secrets, customer data, confidential research, internal URLs, signed links, or non-public sites unless your organization has approved sharing that data with the external API provider. <br>
Risk: Search results and generated answers may be incomplete, stale, or source-dependent. <br>
Mitigation: Review returned sources and citations before relying on the output for decisions, publications, or downstream agent actions. <br>
Risk: The skill requires an AISA_API_KEY for authenticated API calls. <br>
Mitigation: Store the key in an environment variable or secrets manager and avoid pasting it into prompts, logs, or shared command histories. <br>
Risk: Deep research requests can be long-running and may time out. <br>
Mitigation: Use narrower prompts, retry later, or switch to sonar-pro or sonar-reasoning-pro for faster responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/aisa-search-skill) <br>
- [OpenClaw Homepage](https://openclaw.ai) <br>
- [AIsa Documentation](https://docs.aisa.one) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa Verity Reference Implementation](https://github.com/AIsa-team/verity) <br>
- [Perplexity Sonar API](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [Perplexity Sonar Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [Perplexity Sonar Reasoning Pro API](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [Perplexity Sonar Deep Research API](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [JSON API responses plus Markdown guidance and shell/Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY. Queries, prompts, and URLs are sent to AIsa-backed services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
