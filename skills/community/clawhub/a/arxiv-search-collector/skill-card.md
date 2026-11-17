## Description:

Model-driven arXiv retrieval workflow for building a paper set with a manual language parameter: initialize a run, fetch metadata for each model-designed query, let the model filter irrelevant items per query by keep indexes, then merge and dedupe into per-paper metadata directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to plan arXiv searches, fetch paper metadata, filter query results by model-selected keep indexes, and merge deduplicated paper records into a collection for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted run names, query labels, selection JSON, or cached query-result files may cause reads or writes outside the intended collection folder.

Mitigation: Use only trusted inputs, keep output roots in a dedicated disposable directory, and avoid running the skill near important overwriteable JSON or Markdown files.

Risk: Unsafe path handling remains unresolved in the reviewed release.

Mitigation: Review and fix path traversal issues before using this skill in shared or untrusted workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xukp20/skills/arxiv-search-collector)
- [I/O Contract](references/io-contract.md)
- [Query Plan Format](references/query-plan-format.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json, markdown, files]

**Output Format:** [Markdown guidance with shell commands, JSON query plans, and generated JSON/Markdown collection files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include run metadata, per-query result lists, selected-paper metadata directories, and a papers index.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
