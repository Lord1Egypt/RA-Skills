## Description: <br>
Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renning22](https://clawhub.ai/user/renning22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need Perplexity-powered search through AIsa for cited answers, stronger synthesis, multi-step reasoning, or deep research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user prompts to an external AIsa/Perplexity API using a declared API key. <br>
Mitigation: Keep AISA_API_KEY protected and avoid sending secrets, private documents, or sensitive personal data unless that sharing is intended. <br>
Risk: Long-running deep research requests may time out. <br>
Mitigation: Use narrower prompts, retry later, or switch to sonar-pro or sonar-reasoning-pro for faster responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renning22/aisa-perplexity-search) <br>
- [AIsa Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [AIsa Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [AIsa Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [AIsa Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; deep research requests may take longer and can time out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
