## Description:

Fact Check Guard compares key claims with supplied source text and labels them supported, dubious, or unsourced to help review content before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and content reviewers use it to compare factual claims in AI-generated articles, reports, or replies with supplied sources, then identify claims that need independent verification before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword matching can incorrectly label a false claim as supported.

Mitigation: Independently verify the cited sources and require explicit approval before publishing; do not treat a supported label or successful exit code as proof of accuracy.

Risk: Selected file contents may appear unredacted in output, and the promised file-access limits are not enforced.

Mitigation: Use trusted inputs, check filesystem containment, and review output for sensitive content before sharing it.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory (canonical)](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper (DOI)](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON results or plain-text claim labels, with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-claim labels; results are a review aid and do not establish factual accuracy or enforce publication approval.]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
