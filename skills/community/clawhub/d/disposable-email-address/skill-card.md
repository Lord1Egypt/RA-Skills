## Description: <br>
Disposable Email Address creates temporary 24-hour email addresses, checks inboxes, and lists active addresses for AgentPMT-hosted workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create short-lived inboxes for service signups, verification links, one-time codes, automated testing, and temporary communications without exposing a permanent email address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary inbox messages and verification codes may be visible to other agents sharing the same AgentPMT budget. <br>
Mitigation: Use the skill only for low-risk temporary workflows and avoid important accounts, password resets, financial services, private communications, or sensitive verification codes. <br>
Risk: Remote calls may return full email content, including sender, subject, body, and received timestamp. <br>
Mitigation: Keep tool inputs scoped to the task and avoid routing private or sensitive communications through disposable inboxes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/disposable-email-address) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/disposable-email-address) <br>
- [Disposable Email Address Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API calls, Text] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote tool responses may include temporary email addresses, inbox message counts, full message contents, timestamps, and active-address lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
