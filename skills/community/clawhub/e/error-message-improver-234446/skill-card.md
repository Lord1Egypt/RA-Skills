## Description:

Helps users and support teams turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite unclear errors, plan troubleshooting communication, and produce templates, checklists, analysis, code changes, or decision support that make next steps explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may route general support or debugging requests to this skill when another specialized skill would be more precise.

Mitigation: Review and narrow trigger keywords or disable implicit invocation in environments with many specialized skills.

Risk: Generated rewrites or troubleshooting suggestions may be incomplete when the request lacks logs, reproduction steps, constraints, or expected behavior.

Mitigation: Provide the relevant context and review generated text, commands, configuration, or code changes before using them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-234446)
- [Boot loop](https://github.com/zampierilucas/kindle-hid-passthrough/issues/87)
- [[FEATURE]: API Rate Limiting for Chat and Sandbox Submissions](https://github.com/nandinigoyaldev/Open-Source-Contribution-Atelier/issues/1609)
- [PGSSUB format is not supported and fails at burn-in](https://github.com/botagas/Breezyfin/issues/20)
- [OpenShift Impersonation for Multi-Cluster Auth](https://github.com/kiali/kiali/issues/10038)
- [error-messages](https://segmentfault.com/t/error-messages)
- [A road to Lisp: Why Lisp](https://news.ycombinator.com/item?id=48862125)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with templates, checklists, code snippets, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, success criteria, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
