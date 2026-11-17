## Description:

Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores (CRISPR Chronos), drug sensitivity data, and gene effect profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erisonbarros](https://clawhub.ai/user/erisonbarros)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and oncology data analysts use this skill to query DepMap resources, interpret CRISPR Chronos dependency scores, and plan analyses for target validation, biomarker discovery, synthetic lethality, and drug sensitivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large DepMap CSV downloads can consume significant local storage or mix dataset versions.

Mitigation: Check file sizes before download, record the DepMap release identifier, and keep analyses scoped to one dataset version.

Risk: Dependency scores and biomarker associations can be misinterpreted as validated therapeutic targets.

Mitigation: Use the documented score thresholds, account for pan-essential genes and copy-number effects, apply multiple-testing correction, and require domain review before decisions.

## Reference(s):

- [DepMap Dependency Analysis Guide](references/dependency_analysis.md)
- [DepMap Portal](https://depmap.org/portal/)
- [DepMap Data Downloads](https://depmap.org/portal/download/all/)
- [DepMap API](https://depmap.org/portal/api/)
- [DepMap Portal GitHub](https://github.com/broadinstitute/depmap-portal)
- [DepMap 24Q4 Public Dataset](https://figshare.com/articles/dataset/DepMap_24Q4_Public/27993966)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown with Python code examples, API endpoint guidance, dataset references, and analysis recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public DepMap API calls or local CSV analysis steps; no credentials are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
