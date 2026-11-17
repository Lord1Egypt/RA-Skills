## Description:

Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on responsive email design, component systems, dark-mode behavior, and accessibility checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and email operators use this skill to audit, plan, and improve responsive email templates, module systems, dark-mode behavior, accessibility, and design handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email-system changes can affect live recipients, authentication, suppressions, migrations, or production automations.

Mitigation: Require explicit approval before live sends, contact imports, suppression-list edits, DNS/authentication changes, provider migrations, or production automation edits.

Risk: Email design guidance may miss client-specific rendering issues such as Outlook table behavior, Gmail clipping, dark-mode inversions, unsupported CSS, webfont fallbacks, or image blocking.

Mitigation: Use the operating checklist to document client risk, responsive behavior, accessibility checks, and fallback behavior before implementation.

## Reference(s):

- [Email Design Skill Operating Checklist](references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/emaildesignskill)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with audits, QA tables, accessibility notes, implementation diffs, module specs, and handoff checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS/authentication changes, suppression-list edits, provider migrations, or production automation changes.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
