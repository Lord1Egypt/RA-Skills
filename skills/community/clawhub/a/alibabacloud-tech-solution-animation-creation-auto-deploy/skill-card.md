## Description:

Alicloud Service Scenario-Based Skill for auto-deploying the "Build AI Animation Story Creation App" solution by creating an OSS bucket, provisioning a DashScope API key, deploying the FC application with a Devs template, and stopping at the experience page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to automate setup and deployment of Alibaba Cloud's AI Animation Story Creation App, including OSS, DashScope/Bailian API key creation, Function Compute deployment, custom domain setup, and verification.

### Deployment Geography for Use:

Alibaba Cloud cn-hangzhou region

## Known Risks and Mitigations:

Risk: Live API key material may be printed or captured in shared terminals or logs.

Mitigation: Run the skill in a dedicated account or tightly scoped deployment identity, avoid shared terminals and logs, and delete or rotate the created API key after use.

Risk: The deployment flow attaches broad FC and OSS permissions and changes RAM role trust in ways that may persist after deployment.

Mitigation: Review required permissions before execution, use the narrowest practical identity, and manually remove policy grants and role trust changes during cleanup.

Risk: The workflow creates cloud resources and a public custom domain that can consume budget or expose user-generated content if shared.

Mitigation: Treat the generated URL as public, share it only with trusted users, monitor costs, and clean up the custom domain, functions, Devs project, OSS bucket, and API key when finished.

Risk: The skill deploys a third-party Devs template and cloud resources on the user's Alibaba Cloud account.

Mitigation: Verify the Devs template and generated deployment configuration before triggering deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-tech-solution-animation-creation-auto-deploy)
- [RAM Policies](references/ram-policies.md)
- [Related Commands](references/related-commands.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI Plugin Repository](https://github.com/aliyun/aliyun-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command sequences and script-driven deployment steps for Alibaba Cloud resources, ending with a public application access URL.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
