## Description:

Checks an award notice against a draft contract for line-item amount consistency, text consistency, required elements, duplicate entries, and blank or placeholder fields, with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, finance, contract operations, or agency staff use this skill before contract signing to compare an award notice with a draft contract and surface mismatched amount, text, required-field, duplicate, or blank entries. It is a limited free consistency checker and does not provide legal validity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free output omits signing-deadline review, material-deviation thresholding, non-comparable phrasing detection, and single-sided missing-value detection.

Mitigation: Treat the result as a limited consistency check and perform the omitted review steps separately before relying on it for contract approval.

Risk: The tool processes procurement comparison text and presents Chinese-language CLI output.

Mitigation: Run it only in an environment approved for the source material and have a Chinese-proficient reviewer confirm the prompts, findings, and limitations.

Risk: Insufficient or malformed input causes the tool to return no conclusion rather than a consistency decision.

Mitigation: Provide a comparison table with the expected award-notice and draft-contract columns, then review any missing-input messages before drawing conclusions.

Risk: The checker does not judge whether contract terms are legally valid.

Mitigation: Use qualified legal or procurement review for legal-validity questions and treat this skill's findings as objective comparison evidence only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/award-contract-consistency-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style usage guidance with bash commands and either human-readable text or JSON result output from the local Node runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard libraries, accepts a JSON or pasted-text comparison table, returns explicit insufficient-input status instead of a conclusion when required material is missing, and reports omitted free-tier checks.]

## Skill Version(s):

1.0.58 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
