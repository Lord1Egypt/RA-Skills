## Description: <br>
Semantic failure memory for AI agents: search past reasoning failures before acting, and record new failures and resolutions after they happen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyrtl](https://clawhub.ai/user/heyrtl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent failure memory to AI agent workflows, so agents can search known failure patterns before risky steps and record resolutions after failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages storing task and failure details in a hosted persistent memory service, which can expose secrets, personal data, account identifiers, customer data, regulated information, or detailed file contents if users record them directly. <br>
Mitigation: Use sanitized summaries for records, avoid sensitive or regulated data, and use a private or self-hosted deployment for sensitive work. <br>
Risk: Persistent failure memory can return outdated or misleading resolutions that affect future agent behavior. <br>
Mitigation: Review retrieved resolutions before acting and update records when a resolution is no longer correct. <br>


## Reference(s): <br>
- [FOSSIL homepage](https://github.com/heyrtl/fossil) <br>
- [FOSSIL docs](https://github.com/heyrtl/fossil/tree/main/docs) <br>
- [FOSSIL protocol](https://github.com/heyrtl/fossil/blob/main/FOSSIL.md) <br>
- [FOSSIL REST API health endpoint](https://fossil-api.hello-76a.workers.dev/health) <br>
- [ClawHub skill page](https://clawhub.ai/heyrtl/fossil) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to send summarized task and failure details to a hosted FOSSIL service.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
