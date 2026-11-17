## Description:

Screens transaction records for suspicious patterns such as structuring, rapid in-and-out flows, cross-border transfers without KYC, and unreported large amounts, then returns flags for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial monitoring teams can use this local command-line skill to screen caller-selected transaction JSON or JSONL records for suspicious AML patterns. Its scores and flags support triage and require human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script's advertised file-access restrictions are not enforced.

Mitigation: Select only the intended transaction files and run in a restricted filesystem environment; network and write access are unnecessary.

Risk: Screening scores are basic heuristic flags and may need interpretation.

Mitigation: Have a qualified human review flagged transactions before taking action.

## Reference(s):

- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Plain-text or JSON screening results with risk scores, levels, and matched flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic screening results that require human review]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
