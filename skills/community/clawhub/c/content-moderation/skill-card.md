## Description: <br>
Moderate text, images, and video using Vettly's content moderation API via MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[code-with-brian](https://clawhub.ai/user/code-with-brian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and moderators use this skill to check user-generated text, image, and video content against Vettly moderation policies, validate policy YAML, review moderation decisions, and monitor usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external MCP package and Vettly as the moderation provider. <br>
Mitigation: Confirm the @vettly/mcp package and provider are approved for the deployment environment, and consider pinning a known-good package version. <br>
Risk: Moderation requests may send text, media URLs, or policy-related data to Vettly. <br>
Mitigation: Do not submit secrets, regulated personal data, or private signed media URLs unless the organization has approved Vettly for that data. <br>
Risk: The skill requires a VETTLY_API_KEY environment variable. <br>
Mitigation: Use the least-privileged Vettly API key available and keep it out of prompts, logs, and checked-in configuration. <br>


## Reference(s): <br>
- [Vettly](https://vettly.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/code-with-brian/content-moderation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or structured text summarizing MCP tool results, policy validation findings, usage statistics, and recent moderation decisions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Vettly MCP server, npx, and VETTLY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
