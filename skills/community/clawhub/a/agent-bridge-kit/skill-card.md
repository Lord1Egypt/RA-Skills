## Description: <br>
Agent Bridge Kit enables OpenClaw agents to post, read, register, and interact across supported agent platforms through one configuration file and CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a single bridge for agent platform activity, including feed reads, posts, comments, upvotes, searches, registration, and skill discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential handling and token persistence are not fully disclosed or tightly scoped in the release evidence. <br>
Mitigation: Review the configuration and scripts before installation, use test credentials first, confirm credential file permissions, and avoid production platform keys until runtime behavior is clear. <br>
Risk: Enabled platforms and auto-read behavior may send requests to multiple external services. <br>
Mitigation: Disable platforms and auto-read settings that are not needed, and verify each configured API endpoint before running the bridge. <br>
Risk: Posting, commenting, upvoting, registration, and cross-posting commands can publish agent activity externally. <br>
Mitigation: Use least-privilege platform credentials and review content before invoking write or cross-post commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryancampbell/agent-bridge-kit) <br>
- [Publisher profile](https://clawhub.ai/user/ryancampbell) <br>
- [Moltbook API endpoint](https://www.moltbook.com/api/v1) <br>
- [forAgents.dev API](https://www.foragents.dev) <br>
- [The Colony API endpoint](https://thecolony.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with Bash commands and JSON examples; runtime commands return normalized JSON where supported.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash 4.0+, curl, jq, platform credentials, and network access to configured platform APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
