## Description: <br>
AIDSO 虾搜 GEO is an integrated agent skill for binding and checking an API key, generating brand diagnostic reports, managing brand knowledge, producing GEO content, and researching GEO monitoring questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and brand operators use this skill to run AIDSO GEO workflows for brand reporting, AI-search question research, brand knowledge additions, and content generation. It is intended for users who can provide and manage an AIDSO GEO API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores AIDSO_GEO_API_KEY in a local .env file when the bind flow is used. <br>
Mitigation: Prefer environment variables or a scoped, revocable API key; protect the .env file and delete it when no longer needed. <br>
Risk: The skill transmits API keys and brand data to AIDSO endpoints and can persist brand knowledge remotely. <br>
Mitigation: Install only if the user trusts AIDSO with the submitted API key and brand data, and review knowledge-base additions before sending them. <br>
Risk: prompt_research.py can use GEO_API_BASE_URL to change the API endpoint. <br>
Mitigation: Do not set GEO_API_BASE_URL unless the replacement endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tangyuanmile-coder/aidso-xiasou-geo) <br>
- [Publisher profile](https://clawhub.ai/user/tangyuanmile-coder) <br>
- [AIDSO GEO API key settings](https://geo.aidso.com/setting?type=apiKey) <br>
- [AIDSO GEO](https://geo.aidso.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from Python tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local .env file for AIDSO_GEO_API_KEY and a .state file for prompt-research task state.] <br>

## Skill Version(s): <br>
2.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
