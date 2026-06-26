## Description: <br>
Intelligent web search routing across Gemini and Brave APIs with quota management, circuit breaker, and web_fetch fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AiraAlfredSF](https://clawhub.ai/user/AiraAlfredSF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need current web search results while routing queries across configured providers and preserving shared API quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Gemini, Brave, and web_fetch search engines. <br>
Mitigation: Avoid using the skill for secrets, credentials, regulated data, or confidential business queries unless those provider disclosures are acceptable. <br>
Risk: Search logs are retained locally in plaintext for up to 30 days. <br>
Mitigation: Protect the OpenClaw shared workspace logs and clear or restrict access to logs when queries may contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AiraAlfredSF/aira-smart-search) <br>
- [OpenClaw configuration reference](references/openclaw-config.md) <br>
- [Quota system deep dive](references/quota-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search responses may include provider selection, remaining quota, fallback status, warnings, web_fetch engine, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
