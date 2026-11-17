## Description:

Guides an agent through the manual offline DIBP topic clustering workflow for regenerating clusters, reviewing long-tail topics, proposing taxonomy updates, and optionally pushing reviewed cluster results to a backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christinelee3025](https://clawhub.ai/user/christinelee3025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operators use this skill to run and review the DIBP topic clustering batch pipeline, identify taxonomy gaps, and prepare cluster output for frontend or backend use. It is intended for supervised workflow execution where taxonomy edits and backend overwrites require explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can guide an agent to run clustering scripts and update local cluster output files.

Mitigation: Review pipeline summaries, long-tail rates, homogeneity reports, and regression test results before accepting regenerated outputs.

Risk: Backend ingestion can overwrite shared cluster data for a selected date.

Mitigation: Require explicit human approval before ingestion, especially for production, and restate the target environment, date, and overwrite behavior before running commands.

Risk: The semantic clustering path depends on an external model source and may require a local dependency workaround.

Mitigation: Pin or verify the model source when possible, and do not use an unreviewed dependency stub from chat or an unknown source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christinelee3025/skills/dibp-topic-clustering)
- [Publisher profile](https://clawhub.ai/user/christinelee3025)
- [DIBP insight clustering rules](docs/features/dibp-insight-clustering-rules.md)
- [DIBP insight daily clustering design](docs/features/dibp-insight-daily-clustering.md)
- [Xenova bge-small-zh-v1.5 model mirror](https://hf-mirror.com/Xenova/bge-small-zh-v1.5)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and file-path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to regenerate local clustering outputs, propose taxonomy diffs for review, and run backend ingestion only after explicit approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
