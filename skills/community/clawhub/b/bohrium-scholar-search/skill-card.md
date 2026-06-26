## Description: <br>
Search scholars and fetch scholar profiles through open.bohrium.com by name, affiliation, research direction, or scholar ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for academic researchers and retrieve scholar profile details such as affiliations, publication counts, citations, h-index, research directions, education, and work history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bohrium AccessKey stored in OpenClaw configuration. <br>
Mitigation: Inject the AccessKey through OpenClaw environment configuration only, and avoid hardcoding or logging it. <br>
Risk: Scholar search terms and selected scholar IDs are sent to Bohrium. <br>
Mitigation: Avoid highly sensitive or confidential personal data in queries. <br>
Risk: Invalid or expired credentials can interrupt profile lookup workflows. <br>
Mitigation: Update the configured AccessKey in OpenClaw and restart the session when the API reports an invalid key or HTTP 401. <br>


## Reference(s): <br>
- [Bohrium OpenAPI paper-server endpoint](https://open.bohrium.com/openapi/v1/paper-server) <br>
- [Bohrium AccessKey settings](https://bohrium.dp.tech) <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-scholar-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline Python, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bohrium AccessKey injected through OpenClaw; sends scholar lookup terms and selected scholar IDs to Bohrium.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
