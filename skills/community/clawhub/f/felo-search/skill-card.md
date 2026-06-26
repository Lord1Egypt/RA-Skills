## Description: <br>
Felo AI real-time web search for questions requiring current/live information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and Claude Code users use this skill to answer questions that need current web information, including news, weather, prices, location recommendations, and recent technical documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic triggering can send routine search queries to Felo. <br>
Mitigation: Use the skill only for current web information and avoid submitting secrets, private file contents, credentials, proprietary code, or sensitive personal information. <br>
Risk: The skill depends on a Felo API key and external API availability. <br>
Mitigation: Store the API key in the FELO_API_KEY environment variable, avoid exposing it in prompts or logs, and handle missing or invalid keys before making requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhiming1999/felo-search) <br>
- [Felo AI](https://felo.ai) <br>
- [Felo Open Platform Documentation](https://openapi.felo.ai) <br>
- [Felo API Reference](https://openapi.felo.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown answer with query analysis and setup or shell-command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FELO_API_KEY and sends search queries to the Felo API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
