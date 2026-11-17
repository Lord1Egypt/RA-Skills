## Description:

Analyze contracts and legal documents to extract key terms, identify risks, flag red flags, and provide a clear summary with recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze contracts, NDAs, leases, employment agreements, terms of service, and other legal documents for plain-English summaries, key clauses, risk scores, red flags, and version differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract text, party names, payment terms, and sensitive clauses may be displayed in terminal output or JSON logs.

Mitigation: Run the skill only on documents suitable for local terminal display and avoid storing or sharing generated logs that contain confidential contract details.

Risk: The analysis is automated and may miss legal context or overstate the significance of matched clauses.

Mitigation: Use the output as triage guidance and have a qualified attorney review important contracts before making binding legal decisions.

## Reference(s):

- [Eternal Contract Analyzer on ClawHub](https://clawhub.ai/eternal0404/skills/eternal-contract-analyzer)

## Skill Output:

**Output Type(s):** [text, json, guidance, shell commands]

**Output Format:** [Plain-text terminal report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes one contract or compares two versions; supported inputs include PDF, DOCX, text, and image files when the required local extractors are installed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
