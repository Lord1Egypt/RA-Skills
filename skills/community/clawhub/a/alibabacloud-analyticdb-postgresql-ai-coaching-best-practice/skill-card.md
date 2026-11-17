## Description:

Implement AI Coaching best practices on AnalyticDB for PostgreSQL (ADBPG) by using Supabase projects for training data management and ADBPG instances with vector optimization to build RAG-driven coaching systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to provision and verify Alibaba Cloud Supabase and AnalyticDB for PostgreSQL resources for RAG-driven coaching systems. It supports workflow coaching, decision support, skill development, and onboarding use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe installation guidance for the Aliyun CLI.

Mitigation: Use a verified, pinned Aliyun CLI installation path instead of curl-to-bash setup commands.

Risk: The skill can require broad Alibaba Cloud permissions and may create billable or network-exposing resources.

Mitigation: Grant least-privilege temporary credentials and require explicit confirmation before every resource creation, billing, or network exposure change.

Risk: The security review flags risky password, session, and secret handling.

Mitigation: Do not paste live passwords, access keys, API keys, or namespace secrets into chat or saved scripts; mask any displayed secrets.

Risk: Persistent automatic plugin installation and broad plugin updates can change the local CLI execution surface.

Mitigation: Avoid persistent auto-plugin installation and broad plugin updates unless explicitly needed and reviewed.

## Reference(s):

- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Related APIs and CLI Commands](references/related-apis.md)
- [Alibaba Cloud RAM Permissions](references/ram-policies.md)
- [Database Schema](references/database-schema.md)
- [Acceptance Criteria: AI Coaching Best Practice](references/acceptance-criteria.md)
- [Verification Methods](references/verification-method.md)
- [Aliyun CLI Parameter Guide](references/cli-parameter-guide.md)
- [Official Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step cloud setup, verification, and troubleshooting guidance for Alibaba Cloud CLI workflows.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
