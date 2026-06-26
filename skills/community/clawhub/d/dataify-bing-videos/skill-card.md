## Description: <br>
Use when a user run a Bing video search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language Bing video search requests into Dataify Bing Videos API parameters, confirm the request, and run the Dataify API call through the bundled script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the Dataify service during live Bing Videos API calls. <br>
Mitigation: Avoid sensitive search terms and use the dry-run confirmation table before approving a live API call. <br>
Risk: Live calls require a Dataify bearer token. <br>
Mitigation: Use a dedicated, least-privilege token and avoid sharing tokens in conversation history or persistent command logs. <br>
Risk: The bundled script stores the resolved bearer token in process-wide environment state during execution. <br>
Mitigation: Prefer running the skill in an isolated session and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [Dataify Bing Videos API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-bing-videos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, shell command guidance, and direct API response text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live calls require a Dataify API bearer token and send search parameters to the Dataify Bing Videos API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
