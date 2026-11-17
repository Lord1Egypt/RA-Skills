## Description:

Execute deep research by performing comprehensive web searches and synthesizing findings into detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bird-frank](https://clawhub.ai/user/bird-frank)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-focused agent operators use this skill to execute a structured research plan, search across English and Chinese sources when appropriate, synthesize findings, and produce cited Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow performs broad web research and may synthesize inaccurate, stale, or weakly supported source material.

Mitigation: Review source diversity, citation accuracy, and final claims before relying on the generated report.

Risk: The workflow writes Markdown reports under report/ and appends entries to index.md.

Mitigation: Run it only in a workspace where those report files and index updates are desired, or explicitly direct the agent to avoid file writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bird-frank/skills/deep-research-executor)
- [Publisher profile](https://clawhub.ai/user/bird-frank)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with citations and an index entry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under report/ and an index.md entry is appended when the workflow is followed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
