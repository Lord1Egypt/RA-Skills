## Description:

DingTalk and Feishu/Lark integration guidance for enterprise messaging, bots, calendar workflows, approval flows, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to connect agents and workflows with DingTalk or Feishu/Lark messaging, webhook bots, SDK clients, schedule updates, approval processes, and operational notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs, app IDs, and app secrets can expose enterprise messaging integrations if copied into logs, tickets, repositories, or shared prompts.

Mitigation: Treat these values as credentials, store them in secret managers or protected environment variables, rotate leaked tokens, and redact them from agent transcripts and CI logs.

Risk: Installing SDKs directly in shared production or CI environments can introduce unreviewed dependency changes.

Mitigation: Install SDKs in isolated environments and pin reviewed dependency versions before production or CI use.

Risk: Automated notifications can overwhelm chat channels or approval workflows when triggers fire too often.

Mitigation: Use rate limits, deduplication, batching, and clear channel ownership for alerting and workflow automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/dingtalk-feishu-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes webhook examples, SDK setup snippets, platform comparison notes, use cases, and credential-handling reminders.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
