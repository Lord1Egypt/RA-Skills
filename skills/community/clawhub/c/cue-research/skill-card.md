## Description:

Cue 深研 lets an AI agent run Cue deep research against saved buddy templates or a free-form public-data workflow, confirm credits, and retrieve sourced Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route Chinese or English research requests to Cue, choose an existing research buddy or free-form workflow, and receive sourced research reports. It is scoped to public-data research and instructs agents to refuse private-data scenarios such as medical diagnosis, internal accounting, and real AML review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local documents to Cue for research grounding or mimic behavior.

Mitigation: Use it only for public or intentionally shared documents, confirm every file before upload, and avoid contracts, internal notes, medical, financial, or proprietary files unless the user intends to send them to Cue.

Risk: The skill sends research prompts and background jobs to a remote Cue service.

Mitigation: Review sensitive queries before execution, keep private-data scenarios out of scope, and rely on the documented public-data refusal boundary.

Risk: The skill imports runtime code from a sibling cue-buddy installation.

Mitigation: Install cue-research and cue-buddy only from trusted sources and keep them as sibling folders so shared runtime imports resolve as documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-research)
- [Cue API endpoint](https://cuecue.cn/api)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [Cue website](https://cuecue.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with sourced links, plus concise agent guidance and shell commands for running or monitoring Cue jobs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs can write local report and log files; optional material or mimic files may be uploaded to Cue after user confirmation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
