## Description:

A free deterministic checker for canteen purchase-inspection and food-sample retention records that runs six built-in checks and cites the source row and raw text for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External canteen administrators and operations staff use this skill for monthly self-checks and pre-inspection review of purchase-inspection and sample-retention tables. It checks quantities, amounts, meal-sample completeness, sample weights, duplicate supplier batches, and required-field integrity when users provide tabular record text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat table checks as a complete food-safety or regulatory inspection.

Mitigation: Use the findings as record-review support only; the artifact states it does not assess actual food safety conditions, physical samples, certificate authenticity, or official inspection outcomes.

Risk: The skill processes user-provided canteen records through a local Node command.

Mitigation: Install and run it only after reviewing the package and provide only intended input files; server security evidence reports no hidden networking, persistence, or data exfiltration behavior.

Risk: The free version omits several checks available in a separate full version.

Mitigation: Do not infer results for omitted checks such as sample-retention duration, disinfection-record gaps, supplier-license validity, shelf-life review, or grouped remediation summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/canteen-inspection-record-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or structured JSON with findings, cited source rows, summaries, missing-input guidance, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tabular canteen record text with recognizable headers; insufficient input returns missing fields without a compliance conclusion.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
