## Description:

Runs independent red-team reviews of skills, designs, arguments, code, and knowledge bases through five lenses, separating reproducible findings from unproven flags without editing the target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to probe authorized targets for overlooked defects and receive reproducible findings, separate suspicions, and explicit coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reproduction steps may act on systems or sensitive data.

Mitigation: Use only authorized targets and run reproductions on copies or branches, not production data.

Risk: Evidence checks may disclose search queries or fetched-source context to external services.

Mitigation: Review sensitive material before enabling web search or external evidence checks.

Risk: Some question-list formats can be silently omitted from extracted shadow maps.

Mitigation: Check extracted maps against source lists, especially when questions follow blank lines or use uncommon numbering.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vincentjiang06/skills/attacker)
- [Proof and flag adjudication](references/prove-or-flag.md)
- [Seed recipes](references/seed-recipes.md)
- [Fix-audit guidance](references/fix-audit.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured findings, flags, and coverage notes in Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include reproduction steps and severity; flags remain separate from proven findings.]

## Skill Version(s):

0.8.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
