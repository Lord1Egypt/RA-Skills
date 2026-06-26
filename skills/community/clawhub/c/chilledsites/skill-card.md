## Description: <br>
ChilledSites is an AI-powered website generation and deployment skill for generating, editing, and deploying websites to .chilledsites.com in seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgosnell](https://clawhub.ai/user/paulgosnell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use ChilledSites to generate, edit, upload, and deploy websites or AI-generated media through the ChilledSites REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create service credentials and publish live websites. <br>
Mitigation: Require explicit user approval before signup, website generation, deployment, edits, or deletion. <br>
Risk: API keys and secrets could be exposed through prompts, logs, generated site files, or public pages. <br>
Mitigation: Store credentials only in environment variables and keep them out of prompts, logs, generated content, and deployed assets. <br>
Risk: Website and media generation can spend ChilledSites tokens. <br>
Mitigation: Check token balance and confirm budget-sensitive actions before generation or paid usage. <br>


## Reference(s): <br>
- [ChilledSites ClawHub listing](https://clawhub.ai/paulgosnell/chilledsites) <br>
- [ChilledSites homepage](https://chilledsites.com) <br>
- [ChilledSites API base](https://api.chilledsites.com) <br>
- [ChilledSites OpenClaw setup guide](https://chilledsites.com/for-openclaw) <br>
- [ChilledSites pricing](https://chilledsites.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST API examples and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deployed website URLs and consume ChilledSites tokens when the agent calls the service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
