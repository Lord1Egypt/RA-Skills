## Description: <br>
读取收钱吧邮箱中来自 screport@shouqianba.com（市场邮件推送）的网销数据邮件，进行团队/个人排名分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales operations users and authorized mailbox administrators use this skill to analyze daily web-sales email reports, rank teams and individuals, track new staff performance, and identify zero-approval personnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically accesses mailbox contents using configured credentials. <br>
Mitigation: Install only with mailbox-owner or administrator authorization and use a dedicated least-privilege app password or secret manager. <br>
Risk: TLS certificate verification is disabled in the IMAP connection options. <br>
Mitigation: Remove disabled TLS certificate verification before operational use. <br>
Risk: Cron or Standing Orders can create ongoing automated mailbox access. <br>
Mitigation: Enable scheduled execution only where continuous access is intended and documented. <br>
Risk: The skill depends on a separate email skill for IMAP configuration and dependencies. <br>
Mitigation: Keep the dependent email skill trusted, reviewed, and up to date. <br>


## Reference(s): <br>
- [imap-smtp-email-chinese dependency](https://clawhub.ai/skills/imap-smtp-email-chinese) <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/daily-screport-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON data for agent summarization into Markdown ranking reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads authorized IMAP email reports and outputs team, individual, aggregate, new-person, and zero-approval ranking fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
