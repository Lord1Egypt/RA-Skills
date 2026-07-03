## Description: <br>
Bulk-validate up to 1,000 email addresses with NeverBounce through AgentPMT-hosted remote tool calls using the user's connected NeverBounce API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to clean marketing, CRM, migration, or outreach email lists by verifying deliverability, flagging disposable or duplicate addresses, and returning summary counts plus per-address results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email lists may be submitted to a paid third-party validation service without clear activation boundaries. <br>
Mitigation: Invoke the skill only for explicit bulk email validation requests and confirm the list owner has permission to share those addresses with NeverBounce. <br>
Risk: Tool inputs can contain contact data. <br>
Mitigation: Submit only the minimum email addresses needed for the task and avoid unnecessary contact data in prompts, logs, or retries. <br>
Risk: Credential handling is required for the connected NeverBounce API key. <br>
Mitigation: Use AgentPMT credential handling and do not place API keys or account secrets in tool inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/bulk-email-address-validation-neverbounce) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce) <br>
- [Action schema](./schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces AgentPMT invocation guidance for the verify action and describes JSON results with job status, aggregate counts, per-email classifications, flags, and suggested corrections.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
