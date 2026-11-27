## Description:

Guides IDaaS administrators through manual or CLI onboarding of DingTalk, WeCom, and Feishu identity providers for account synchronization and authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

IDaaS administrators use this skill to connect DingTalk, WeCom, or Feishu as inbound identity sources or outbound contact destinations, configure synchronization and authentication, and verify each dimension separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a recommendation to bypass an application publication safety gate.

Mitigation: Avoid installation until that recommendation is removed or independently reviewed.

Risk: ClawScan also reports risky account changes and scope and credential-handling concerns; one component was only partially inspected.

Mitigation: Review proposed publishing or account changes carefully, and treat the security findings as incomplete.

## Reference(s):

- [DingTalk onboarding and sync guidance](artifact/references/dingtalk.md)
- [WeCom onboarding and sync guidance](artifact/references/wecom.md)
- [Feishu onboarding and sync guidance](artifact/references/feishu.md)
- [IDaaS identity-provider model and OpenAPI notes](artifact/references/idp-model-openapi.md)
- [CLI tooling and credential-handling guidance](artifact/references/cli-tooling.md)
- [IDaaS RAM policy requirements](artifact/references/ram-policies.md)
- [IDaaS terminology reference](artifact/references/terminology.md)
- [Alibaba Cloud Eiam OpenAPI portal](https://api.aliyun.com/product/Eiam)
- [DingTalk inbound binding guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-idaas-to-dingtalk-inbound)
- [DingTalk outbound binding guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-idaas-to-dingtalk-outbound)
- [WeCom binding guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-idaas-to-wecom)
- [Feishu binding guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/binding-fly-book)
- [Feishu outbound binding guide](https://help.aliyun.com/zh/idaas/eiam/user-guide/bind-feishu-outbound)
- [GetIdentityProvider API reference](https://help.aliyun.com/zh/idaas/eiam/developer-reference/api-eiam-2021-12-01-getidentityprovider)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls]

**Output Format:** [Markdown with console steps and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates sync and authentication status; requires confirmation before write operations and keeps credentials out of conversation.]

## Skill Version(s):

0.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
