## Description:

权益法核算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and consolidation reporting teams use this skill before monthly or annual equity-method accounting and audit preparation to check equity-method investment tables for arithmetic consistency, missing required fields, duplicate investees, and out-of-scope control signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input may contain sensitive financial table data that is read from the local input file.

Mitigation: Run the skill only in a trusted local environment and provide only the table content needed for the check; evidence.security reports no network transfer or persistence in the inspected artifact.

Risk: The skill checks table arithmetic and disclosed free-edition rules but does not decide the underlying accounting treatment.

Mitigation: Have qualified finance or audit personnel decide whether equity-method accounting is appropriate and review any findings before relying on them.

Risk: The free edition omits several additional checks listed by the artifact.

Mitigation: Treat the reported withheld checks as outside this skill's coverage and perform separate review for those items when they matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/equity-method-investment-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Chinese-language console text or JSON with executed checks, withheld checks, findings, and summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; the free edition reports unsupported checks instead of fabricating conclusions.]

## Skill Version(s):

1.0.18 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
