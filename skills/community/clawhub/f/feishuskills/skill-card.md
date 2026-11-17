## Description:

Automates Feishu integration with minimal manual input by handling authentication, messaging, events, APIs, error recovery, and fallback solutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhi8145](https://clawhub.ai/user/wangzhi8145)

### License/Terms of Use:

MIT License

## Use Case:

Developers and engineers use this skill to diagnose and generate implementation guidance for Feishu Open Platform integrations, including authentication, bot messaging, document access, webhooks, permissions, API calls, and fallback manual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated implementation files may expose Feishu credentials or tokens.

Mitigation: Review generated files before use, avoid supplying real secrets until storage behavior is verified, and rotate any secrets that may have been written to disk.

Risk: Webhook examples may be deployed without complete authentication checks.

Mitigation: Verify webhook signature handling before deployment and require valid verification tokens or encrypt keys for incoming Feishu events.

Risk: Broad Feishu app permissions can increase impact if generated code mishandles credentials.

Mitigation: Limit Feishu app scopes to the exact operations needed for the integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhi8145/skills/feishuskills)
- [Feishu Open Platform documentation](https://open.feishu.cn/document)
- [Feishu server-side SDK overview](https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/server-side-sdk/overview)
- [Feishu webhook verification troubleshooting](https://open.feishu.cn/document/faq/trouble-shooting/webhook-verification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON reports with generated implementation code and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated solution files to a workspace solutions directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
