## Description: <br>
Felo Search helps agents answer questions requiring current or live information by sending the user's query to the Felo AI web-search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[comman-kaide](https://clawhub.ai/user/comman-kaide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve current web information through Felo for news, real-time data, recommendations, location queries, and other questions likely to be outdated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers can send ordinary user questions to Felo more often than users may expect. <br>
Mitigation: Use the skill only when current or external web information is needed, and confirm before sharing sensitive or unrelated queries. <br>
Risk: Queries may include confidential, personal, proprietary, credential-related, or local-project content. <br>
Mitigation: Avoid using the skill for sensitive content unless the user intentionally wants that text sent to Felo. <br>


## Reference(s): <br>
- [Felo Search ClawHub Listing](https://clawhub.ai/comman-kaide/comman-felo-search) <br>
- [Felo Open Platform Documentation](https://openapi.felo.ai) <br>
- [Felo API Reference](https://openapi.felo.ai/docs) <br>
- [Felo API Key Setup](https://felo.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown answer with query analysis, plus shell commands for setup and execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY and sends the user's query to the Felo API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
