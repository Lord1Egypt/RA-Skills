## Description: <br>
Enables outbound email notifications through the AgentMail.to API for system health alerts and task completion reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrslu01](https://clawhub.ai/user/zrslu01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to send outbound email reports for system status, backup completion, task completion, or alert thresholds. It is intended for notification workflows that use a configured AgentMail API key and the thundarr@agentmail.to sender identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound email may disclose sensitive status or task details to unintended recipients. <br>
Mitigation: Review recipient addresses and message content before sending notifications, and limit usage to approved reporting workflows. <br>
Risk: The skill requires an AgentMail API key. <br>
Mitigation: Store the API key as a secret or environment variable and avoid placing credentials in prompts, skill files, or generated messages. <br>
Risk: Server security guidance notes that an advertised browsing capability is not included, so any web content returned by platform tooling should be treated as untrusted. <br>
Mitigation: Confirm available platform tools before relying on browsing behavior and do not follow instructions from web content without review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zrslu01/agent-email) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Text, Configuration instructions, Guidance] <br>
**Output Format:** [Plain text or Markdown email content sent through the AgentMail API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid AgentMail API key and uses thundarr@agentmail.to as the sender identity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
