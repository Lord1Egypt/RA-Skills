## Description:

Decomposes AI claims into evidence chains tagged by source type and independent verifiability, then reports evidence support and unsupported claims without deciding whether a claim is true.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to structure evidence for AI claims, fact checks, and source credibility reviews. It distinguishes independently verifiable evidence from internal or asserted material and flags claims that lack enough verifiable support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evidence labels or scores can be mistaken for confirmation that a claim is true, even though the tool evaluates evidence categories and coverage rather than claim truth.

Mitigation: Check the cited original sources independently and treat the score as a summary of supplied labels, not a factual verdict.

Risk: Inconsistent permission declarations may not enforce file access limits in the host runtime.

Mitigation: Provide only input files intended for agent access and enforce file-access limits in the host environment.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured JSON data or a Markdown evidence-chain report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a support score, evidence items with source types, and an unsupported-claim indicator; it does not determine claim truth.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
