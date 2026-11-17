## Description:

Perform data clustering analysis using k-means and hierarchical algorithms. Use when you need to group, classify, or segment datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data practitioners use this skill to run local k-means or hierarchical clustering on numerical CSV or JSONL datasets, inspect clustering metrics, and export or reuse clustering runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clustering runs and source input paths are saved locally under ~/.cluster.

Mitigation: Avoid highly sensitive datasets when local retention of run metadata is not acceptable, and clear local run records when they are no longer needed.

Risk: Exports can overwrite an existing file when OUTPUT points to that path.

Mitigation: Choose export paths deliberately and confirm that the target file can be replaced before running an export.

## Reference(s):

- [Cluster ClawHub release page](https://clawhub.ai/ckchzh/skills/cluster)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Terminal text with optional JSON, CSV, and JSONL exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores clustering run records and configuration locally under ~/.cluster.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
