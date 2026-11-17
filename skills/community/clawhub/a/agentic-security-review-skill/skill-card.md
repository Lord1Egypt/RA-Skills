## Description:

Creates CompleteTech LLC security, safety, permissions, and production-readiness review artifacts for agentic development workflows before launch or when tools, data, credentials, integrations, retrieval sources, or external actions change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and teams preparing agentic workflows use this skill to choose and draft security-review artifacts for permissions, data exposure, credentials, retrieval, external actions, launch readiness, rollback, incidents, and signoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated security-review artifacts are drafts and may contain placeholders or unverified project facts.

Mitigation: Replace placeholders and verify workflow, data, tool, permission, credential, approval, logging, rollback, and incident-response facts before sharing or relying on an artifact.

Risk: The PDF workflow is CompleteTech-branded and may be inappropriate for neutral or differently branded reports.

Mitigation: Use the skill only when CompleteTech-branded reports are appropriate, or use Markdown-only output or edited branding defaults for neutral reporting.

Risk: Python package installation and optional PDF or PNG rendering introduce dependency and runtime-environment risk.

Mitigation: Pin dependencies and run installs, validation, and rendering in a restricted environment for higher-assurance use.

Risk: The skill helps document security review but does not establish compliance, legal approval, penetration-test completion, or guaranteed production readiness.

Mitigation: Require appropriate human, client, legal, compliance, or technical review before making those claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/agentic-security-review-skill)
- [Homepage](https://github.com/CompleteTech-LLC/agentic-security-review-skill)
- [Security Review Catalog](references/security-catalog.md)
- [Use-Case Decision Table](references/use-case-decision-table.md)
- [Security Review Lifecycle](references/security-lifecycle.md)
- [Security Positioning](references/security-positioning.md)
- [Template Index](references/template-index.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown drafts and optional branded PDF files, with inline shell commands for rendering.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft artifacts require verified project facts before sharing, storing, or relying on them.]

## Skill Version(s):

1.0.2 (source: server release evidence, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
