## Description: <br>
Queries Alibaba Cloud Bailian Coding Plan package status, remaining quota, usage consumption, and expiration information using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwude](https://clawhub.ai/user/jackwude) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with an Alibaba Cloud Bailian Coding Plan use this skill to retrieve subscription status, remaining quota, usage percentages, reset times, and expiration information from the Bailian console. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Bailian credentials from TOOLS.md and can submit them through automated browser login. <br>
Mitigation: Keep credentials in a clearly labeled Bailian-only section, review the Bailian destination before use, and prefer a confirmation step before login. <br>
Risk: Broad trigger phrases can cause unintended Alibaba Cloud account access. <br>
Mitigation: Use explicit Bailian-related prompts and route generic token or usage questions to a more specific skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackwude/bailian-usage) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text] <br>
**Output Format:** [Markdown report with package status, quota usage, reset times, and usage analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Bailian credentials in TOOLS.md and an OpenClaw browser session.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
