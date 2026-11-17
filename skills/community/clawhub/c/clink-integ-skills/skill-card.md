## Description:

Clink Integration helps coding agents design, scaffold, validate, and review ClinkBill/Clink payment integrations, including CLI-based setup, checkout and subscription APIs, webhook automation, sandbox validation, and developer handoff artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clink](https://clawhub.ai/user/clink)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and implement ClinkBill payment integrations, configure sandbox-first authentication, generate or review checkout, subscription, webhook, and catalog artifacts, and validate readiness before production promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment secrets and webhook signing secrets could be exposed or stored unsafely.

Mitigation: Use environment-variable references, platform secrets, or OS-managed secret stores; keep .env files ignored and permission-restricted, and do not echo real secrets in final output.

Risk: Remote documentation, payment-skill context overrides, or API host overrides could point the agent at untrusted sources.

Mitigation: Do not set CLINK_DOCS_URL or payment-skill URL/path overrides to untrusted locations, and use only approved Clink API hosts for authenticated commands.

Risk: Automated restart commands can run unsafe shell behavior during agent-run flows.

Mitigation: Avoid --restart-command in agent-run flows unless the restart action is explicit, reviewed, and safe for the current project.

Risk: The release requires review because the security verdict is suspicious.

Mitigation: Install only in a trusted workspace, keep work sandbox-first, and complete review before relying on authenticated payment workflows.

## Reference(s):

- [README](README.md)
- [Skill Definition](SKILL.md)
- [Clink Integ CLI Integration](references/clink-integ-cli-integration.md)
- [Standard Integration](references/standard-integration.md)
- [Elements Integration](references/elements-integration.md)
- [New User Onboarding](references/new-user-onboarding.md)
- [Merchant Skill for OpenClaw Integration](references/agent-integration.md)
- [Merchant Skill for Generic Agent Integration](references/generic-agent-integration.md)
- [Validation Workflow](references/validation-workflow.md)
- [Output Artifacts](references/output-artifacts.md)
- [Review Checklist](references/review-checklist.md)
- [Clink Docs Export](https://docs.clinkbill.com/llms-full.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, JSON contracts, checklists, validation reports, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce developer-facing artifacts such as catalog JSON, payment handoff contracts, webhook checklists, and production promotion plans when gated validation passes.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
