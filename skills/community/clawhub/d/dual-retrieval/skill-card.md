## Description:

Combines M-Flow graph topology retrieval with QMD search to merge, deduplicate, and rank results for precise multi-hop and semantic retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve context from both M-Flow memory and QMD indexes, then combine the results for agent responses or investigation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad local QMD cache data and expose indexed content without clear scoping.

Mitigation: Use trusted local memory and index stores only, configure collection scoping before use, and avoid running the skill against sensitive indexes.

Risk: The QMD database path is hardcoded for one local environment.

Mitigation: Verify or change the QMD database path before running the skill in another environment.

Risk: Debug and schema scripts may print sample indexed content from local QMD data.

Mitigation: Run those scripts only on non-sensitive indexes and review console logs before sharing them.

Risk: Test runs may write retrieved content into a Markdown report.

Mitigation: Store generated reports in an approved location and remove sensitive retrieved content before sharing.

## Reference(s):

- [Dual Retrieval Skill Page](https://clawhub.ai/sora-mury/skills/dual-retrieval)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples; retrieval result reports may also be written as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns merged retrieval results with source labels, scores, metadata, and summary statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
