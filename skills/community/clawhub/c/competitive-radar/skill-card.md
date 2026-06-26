## Description: <br>
Tracks competitors weekly across pricing page diffs, homepage positioning changes, blog and RSS posts, job postings, GitHub star velocity and releases, and critical-change alerts for pricing or funding keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manjotpahwa](https://clawhub.ai/user/manjotpahwa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operators use this skill to monitor named competitors and receive weekly or same-day competitive intelligence about pricing, positioning, hiring, content, and GitHub activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with active preset competitors and can create scheduled monitoring jobs. <br>
Mitigation: Clear or deactivate bundled competitors before use and confirm the weekly digest and paid-tier daily alert cron jobs before enabling them. <br>
Risk: The skill can persist monitoring history and sends digests through third-party services. <br>
Mitigation: Avoid tracking internal or private URLs, and use dedicated low-scope tokens or webhooks for Slack, Telegram, Discord, WhatsApp, GitHub, and related integrations. <br>
Risk: Paid license activation stores license identity data locally in plaintext. <br>
Mitigation: Activate only if local plaintext storage of the license key and purchaser email is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/manjotpahwa/competitive-radar) <br>
- [Publisher profile](https://clawhub.ai/user/manjotpahwa) <br>
- [Paid upgrade page](https://manjotpahwa.gumroad.com/l/competitive-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, status text, setup instructions, alerts, and channel-specific digest messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces weekly digests, same-day alerts for paid tiers, local snapshot and digest files, and delivery messages for configured notification channels.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
