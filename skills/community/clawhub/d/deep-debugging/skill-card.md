## Description:

Evidence-first debugging and incident triage for AI coding agents with concise workflow, progressive checklists, and safe local snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to debug unclear, recurring, production-like, or high-risk software failures by stabilizing incidents, collecting evidence, testing one hypothesis at a time, and verifying the root cause before changing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debugging may expose logs, git metadata, dependency versions, listening ports, and environment variable names.

Mitigation: Use redacted diagnostic evidence, print environment key names only, and omit secrets, tokens, cookies, customer data, and raw production payloads.

Risk: Production writes, deploys, rollbacks, database actions, or external API changes can affect live systems.

Mitigation: Require explicit user approval before production-changing actions and prefer evidence collection, feature flags, rollback planning, and minimal reversible fixes.

## Reference(s):

- [Incident-First Debugging Reference](references/incident-first.md)
- [Output Templates](references/output-templates.md)
- [Stack Checklists](references/stack-checklists.md)
- [Deep Debugging ClawHub release](https://clawhub.ai/brasco05/skills/deep-debugging)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, incident snapshots, checklists, code changes, configuration notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted diagnostic evidence and safe environment metadata; secrets, tokens, cookies, customer data, and raw production payloads should be omitted.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
