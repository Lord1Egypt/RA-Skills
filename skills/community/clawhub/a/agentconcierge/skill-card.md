## Description: <br>
Find and recommend AI agents for any workflow using AgentConcierge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gomisterb](https://clawhub.ai/user/gomisterb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask for AI agent recommendations based on a role, pain point, current tools, budget, and team size. The skill returns five ranked recommendations with match scores and reasons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendation details are sent to AgentConcierge, including role, pain point, current tools, budget, and team-size details provided by the user. <br>
Mitigation: Use generalized descriptions for sensitive workflows and do not include passwords, secrets, private customer data, regulated personal data, or confidential internal plans. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gomisterb/agentconcierge) <br>
- [AgentConcierge](https://agentconcierge.io) <br>
- [AgentConcierge API Reference](references/api-schema.md) <br>
- [AgentConcierge Developer API](https://agentconcierge.io/developers) <br>
- [AgentConcierge Search](https://agentconcierge.io/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with ranked items, match scores, reasons, pricing, and URLs; includes curl-based API call guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to agentconcierge.io; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
