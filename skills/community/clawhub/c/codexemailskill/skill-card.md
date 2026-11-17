## Description:

Guides agents through repo-aware planning, implementation, review, and QA for email templates, content systems, tests, and related code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make email-related repository changes, such as template edits, React Email updates, MDX content changes, QA scripts, and testable fixes, while keeping live email operations behind explicit approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email code changes can affect live campaigns, recipient data, DNS or authentication settings, suppression rules, and production automations if treated as operational actions.

Mitigation: Keep repository changes scoped and verifiable, report remaining production steps separately, and require explicit approval before live sends, imports, DNS or authentication changes, suppression edits, or production automation changes.

Risk: Template or content changes can introduce broken rendering, unresolved dynamic fields, tracking mistakes, or missing fallbacks.

Mitigation: Use the narrowest useful verification, such as render previews, linting, type checks, snapshots, unit tests, or visual smoke checks, and confirm dynamic fields and fallbacks before rollout.

## Reference(s):

- [Codex Email Skill Operating Checklist](references/operating-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with implementation plans, diffs or patches, QA checks, command snippets, and concise change reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS or authentication changes, suppression edits, or production automation changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
