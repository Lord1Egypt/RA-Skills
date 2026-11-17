## Description:

财务月结与对账专家 routes pasted finance-close table data to one of 39 local reconciliation checks and returns line-referenced, reproducible conclusions or missing-column notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations employees use this skill during month-end close and reconciliation work to classify pasted table data, run the matching local rule check, and receive itemized findings. It is a reconciliation aid and should not be treated as accounting, audit, tax, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance reconciliation findings can be incomplete or misleading if source tables lack required columns, contain malformed values, or fall outside the bundled rule checks.

Mitigation: Review findings against source records and have qualified finance personnel confirm material accounting, audit, tax, or legal decisions.

Risk: The local runner creates a trial-use counter in the user's home directory.

Mitigation: Disclose the local counter before use and inspect or remove the state directory according to local policy when testing is complete.

Risk: Pasted or file-provided tables may contain sensitive financial data.

Mitigation: Run the skill only in trusted local environments and avoid sharing input tables or outputs beyond authorized finance workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-finance-close-pub)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON command output from a local Node.js runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list supported sub-skills, run a bundled sample, route pasted table text, or return {subSkill, subSkillName, result} when invoked with --json.]

## Skill Version(s):

1.0.10 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
