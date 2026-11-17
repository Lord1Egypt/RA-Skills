## Description: <br>
AdMapix Free is a lightweight agent skill for querying AdMapix creative search, app detail, and store ranking endpoints and returning the raw structured JSON responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, advertising analysts, and market research teams use this skill to ask an agent for AdMapix creative, app, and store ranking lookups. The skill guides API-key setup, maps requests to supported AdMapix endpoints, and returns raw JSON for downstream analysis by the calling agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends AdMapix queries and the ADMAPIX_API_KEY credential to the AdMapix API. <br>
Mitigation: Use only with an intended AdMapix account, provide the key through the environment variable, avoid pasting the key into chat or logs, and rotate the key if exposure is suspected. <br>
Risk: Server security evidence flags overbroad declared authority, especially write access and loosely described command or file capabilities beyond a simple API lookup purpose. <br>
Mitigation: Run the skill in a constrained workspace, review proposed shell commands and file writes before execution, and disable unnecessary write authority where the agent platform allows. <br>


## Reference(s): <br>
- [AdMapix API](https://api.admapix.com) <br>
- [AdMapix website](https://www.admapix.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw AdMapix API data without analysis, summarization, sorting, field renaming, or page generation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
