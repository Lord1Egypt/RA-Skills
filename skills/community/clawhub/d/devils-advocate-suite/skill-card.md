## Description:

Execute structured adversarial thinking to stress-test high-stakes decisions, identify systemic risks, and prevent groupthink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midnightstudioai](https://clawhub.ai/user/midnightstudioai)

### License/Terms of Use:

MIT-0

## Use Case:

Teams, developers, and decision-makers use this skill to run structured strategy reviews, pre-mortems, PR/FAQ stress tests, dialectical inquiry, and TRIZ-style contradiction analysis before high-stakes decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision-review outputs could be mistaken for expert legal, financial, safety, or operational approval.

Mitigation: Use the skill as a facilitation checklist and require qualified reviewers to approve high-stakes decisions.

Risk: The pre-mortem aggregator reads JSON from standard input, so hostile or oversized input could produce excessive terminal output or misleading display.

Mitigation: Provide small, trusted JSON arrays with 1-5 likelihood and impact values.

## Reference(s):

- [Methodology Summary](references/methodology_summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command snippets and JSON risk-matrix output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local helper scripts for pre-mortem aggregation and TRIZ contradiction suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
