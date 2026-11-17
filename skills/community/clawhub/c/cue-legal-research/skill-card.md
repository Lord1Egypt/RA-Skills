## Description:

Uses Cue to run deep legal and compliance research for Chinese laws, regulations, administrative orders, regulatory inquiries, compliance risk checks, enforcement monitoring, litigation drafting, and legal practice analysis with source-backed outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, legal practitioners, compliance teams, and developers use this skill to select a Cue legal-compliance research workflow, confirm credit usage, run the Cue research runner, and return a source-linked report for review. It supports public-data research and drafting workflows, but it does not replace professional legal advice, due diligence, underwriting, or compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download or update mutable external runner code before execution.

Mitigation: Review the runner repository, pin a trusted commit where practical, and run it in a sandboxed environment.

Risk: The Cue runner can read the user's local Cue API key and consume credits.

Mitigation: Use a narrowly scoped Cue API key and require explicit user confirmation before any credit-consuming research run.

Risk: Legal and compliance outputs may be incomplete or unsuitable for a specific matter.

Mitigation: Treat reports as source-linked research drafts and have qualified legal or compliance reviewers verify conclusions before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-legal-research)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown guidance with shell commands and source-linked research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, python3, a Cue account API key, and explicit confirmation before consuming Cue credits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
