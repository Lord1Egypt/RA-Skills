## Description:

工程与建筑结算专家 routes pasted construction and settlement tables across 15 local checking sub-skills and returns row-referenced, reproducible conclusions or missing-column notices when the input is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Construction finance, project controls, and settlement reviewers use this skill to locally check pasted tabular materials for construction settlement, progress payment, materials, capitalization, billing, and related reconciliation workflows. It helps identify applicable sub-checks, produce reproducible row-level findings, and state when required columns or parameters are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local execution creates a hidden usage-count file in the user's home directory.

Mitigation: Run the tool under an appropriate local account or sandbox and review local state expectations before deployment.

Risk: Construction settlement outputs may be mistaken for audit, legal, or payment authorization advice.

Mitigation: Treat results as calculation and checking aids, and require qualified review before audit, legal, contractual, or payment decisions.

Risk: Incomplete tables or missing parameters can lead to no conclusion or only partial checks.

Mitigation: Provide table headers, data rows, and required parameters, then review missing-column and unexecuted-check disclosures in the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-construction-pub)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON checking results from local Node.js execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include matched sub-skill identifiers, original row references, reproducible calculations, missing-column notices, and unexecuted-check disclosures.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter lists 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
