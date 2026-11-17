## Description:

Autonomously validates specifications, runs behavioral tests, generates code, executes tests, and produces cryptographically signed outcome reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate structured specifications, run behavioral tests against a mock environment, coordinate an autonomous implementation-and-test workflow, and produce outcome reports for review or feedback-loop analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outcome reports may appear authoritative even though behavioral, unit, and integration results can be based on mock or random execution.

Mitigation: Review reports before using them in approval, CI/CD, security, or provenance workflows, and treat them as demonstrations unless the mock execution paths are replaced with real validation.

Risk: Cryptographic signatures may be hashes of generated report content rather than independent proof of secure generation or authentic signing.

Mitigation: Do not rely on the signature as security evidence until a real signing process and verification policy are integrated and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielfoojunwei/skills/dark-factory)
- [Behavioral Testing Guide](references/behavioral_testing_guide.md)
- [Dark Factory Operations](references/dark_factory_operations.md)
- [Triad Integration](references/triad_integration.md)
- [Specification Schema](references/specification_schema.json)
- [Outcome Report Schema](references/outcome_report_schema.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces specification validation results, behavioral test reports, generated code placeholders, and signed outcome report JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
