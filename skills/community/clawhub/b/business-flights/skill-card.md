## Description: <br>
Search business class flights, priority boarding tickets, and work-friendly airline seats with extra legroom for business travelers using flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to collect route details, run flyai business-class flight searches, compare real-time flight options, and present booking links in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global or privileged flyai CLI installation can change the user's system-wide package environment. <br>
Mitigation: Install only after verifying the package source, and avoid sudo or global installation unless the user explicitly accepts the system-wide change. <br>
Risk: Travel-search details are sent to the flyai provider. <br>
Mitigation: Use the skill only when the user is comfortable sending origin, destination, dates, budget, and related travel-search details to that provider. <br>
Risk: Local execution logs may contain personal travel details. <br>
Mitigation: Disable, delete, or tightly control logs when travel details should not persist locally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/business-flights) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flyai CLI commands, comparison tables, booking links, and concise travel guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every listed flight result should include a detailUrl booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
