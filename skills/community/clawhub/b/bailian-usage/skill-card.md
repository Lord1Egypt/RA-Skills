## Description:

Automatically queries Alibaba Cloud Bailian Coding Plan package status, remaining quota, usage consumption, and expiration details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwude](https://clawhub.ai/user/jackwude)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Alibaba Cloud Bailian users use this skill to check Coding Plan quota, consumption windows, subscription status, and expiration from an authenticated console session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically uses saved Alibaba Cloud credentials from TOOLS.md.

Mitigation: Use a least-privileged Alibaba Cloud account, enable MFA and login alerts, and restrict local file permissions on TOOLS.md.

Risk: The password may be briefly visible to local process-monitoring tools during login automation.

Mitigation: Run the skill only in a trusted local environment and avoid invoking it on shared hosts or during untrusted local process monitoring.

Risk: The skill controls an authenticated browser session to access Billing Plan data.

Mitigation: Review before installing, invoke it only for explicit Bailian quota checks, and require manual confirmation or verification when the login flow triggers additional checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackwude/skills/bailian-usage)
- [README.en.md](artifact/README.en.md)
- [SKILL.md](artifact/SKILL.md)
- [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with package status, usage percentages, reset times, model availability, and usage analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local OpenClaw browser session and credentials stored in TOOLS.md.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
