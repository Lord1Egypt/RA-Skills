## Description:

Tool for manual per-paper arXiv paper processing: batch/source/PDF download, model-driven full-text reading, and summary.md writing in the selected language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:


## Use Case:

Developers and research workflows use this skill to download arXiv paper artifacts for one paper or a batch, then have the agent read the source or PDF and write grounded per-paper summaries in a selected language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded arXiv source bundles may write files outside the intended extraction folder because source archive containment is insufficient.

Mitigation: Run the skill in an isolated workspace without sensitive files, avoid arbitrary untrusted arXiv IDs, and patch source extraction to enforce path-aware containment and reject links or special tar members before broad batch use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xukp20/skills/arxiv-paper-processor)
- [Summary Format Reference](references/summary-format.md)
- [English Summary Example](references/summary-example-en.md)
- [Chinese Summary Example](references/summary-example-zh.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries and JSON download logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes summary.md per paper and may create source/PDF artifacts and download logs under the paper or run directory.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
