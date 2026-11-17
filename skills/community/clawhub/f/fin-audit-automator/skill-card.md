## Description:

Fin Audit Automator helps agents perform finance compliance review tasks including AML pattern checks, invoice validation, related-party transaction review, and audit report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, compliance, and audit teams can use this skill to triage transaction data for AML patterns, check invoice or contract content, and draft internal audit reports. Results should support, not replace, licensed audit or compliance review.

### Deployment Geography for Use:

Global; content is focused on Chinese financial compliance workflows.

## Known Risks and Mitigations:

Risk: The skill may overstate sandboxing, tamper-proof audit logging, and compliance protections.

Mitigation: Treat the skill as a local demo or prototype, review its behavior before deployment, and do not rely on it as a production compliance control.

Risk: The skill stores identifiable audit and trial data under ~/.openclaw.

Mitigation: Review and protect the local ~/.openclaw files, apply retention controls, and avoid processing sensitive production data without an approved data handling process.

Risk: AML, invoice, and audit outputs can be incomplete or incorrect.

Mitigation: Require independent human verification before using outputs for financial, audit, or regulatory decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/andyxcg/skills/fin-audit-automator)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Python dictionaries and Markdown audit report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include AML alerts, invoice or contract validation results, trial status fields, and generated audit report drafts.]

## Skill Version(s):

1.2.0 (source: server release evidence; artifact files also mention 1.1.0 and 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
