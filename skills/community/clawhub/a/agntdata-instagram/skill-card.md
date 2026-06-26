## Description: <br>
Use one API key to pull Instagram data including profiles, media, discovery, locations, hashtags, reels, and related account data for agents, automations, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, data teams, marketers, and research teams use this skill to integrate agntdata Instagram API calls into agent workflows for social listening, creator intelligence, dashboards, alerts, and content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive agntdata API credential and sends Instagram targets and query details to a third-party API. <br>
Mitigation: Store AGNTDATA_API_KEY only in an environment variable, avoid including secrets or confidential client details in prompts, logs, or registration use-case text, and install only when agntdata is trusted for the intended data workflow. <br>
Risk: Credit-based API usage can incur cost or quota consumption during automated runs. <br>
Mitigation: Monitor credit usage and constrain automated calls to the minimum endpoints, fields, and query volume needed for the task. <br>
Risk: The skill recommends a separate OpenClaw plugin path that is not the same artifact as this markdown skill. <br>
Mitigation: Review the separate plugin package before choosing the plugin route. <br>


## Reference(s): <br>
- [agntdata Instagram API Reference](https://agnt.mintlify.app/apis/social/instagram) <br>
- [agntdata Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaencarrodine/agntdata-instagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY and curl for authenticated API examples; API responses are structured JSON from agntdata.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
