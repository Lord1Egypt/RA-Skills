## Description: <br>
Use one API key to pull Reddit data, including subreddits, posts, threads, user activity, search, and community data, as structured JSON for agents, automations, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, automation builders, analysts, and data teams use this skill to call the agntdata Reddit API for social listening, content research, creator intelligence, alerts, digests, dashboards, and downstream AI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agntdata API key and sends Reddit query details to the agntdata service. <br>
Mitigation: Treat AGNTDATA_API_KEY like a password, scope access according to internal policy, and avoid submitting sensitive investigation targets or personal data unless approved. <br>
Risk: The skill recommends a separate OpenClaw Reddit plugin for native tools. <br>
Mitigation: Review the separate @agntdata/openclaw-reddit plugin independently before installing it. <br>


## Reference(s): <br>
- [agntdata Reddit API Reference](https://agnt.mintlify.app/apis/social/reddit) <br>
- [agntdata Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill](https://clawhub.ai/jaencarrodine/agntdata-reddit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, endpoint descriptions, and JSON tool schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY and curl for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
