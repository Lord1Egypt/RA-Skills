## Description:

AI 开源项目技术尽调与公众号内容自动化 automates GitHub Trending monitoring, in-depth technical analysis, WeChat article generation, and Feishu knowledge-base capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical bloggers, developer advocates, startup CTOs, and technical media operators use this skill to identify open-source projects worth analyzing, produce structured technical due-diligence reports, turn them into WeChat-ready articles, and save the analysis to a Feishu knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles or reports may be published or synced externally without sufficient review.

Mitigation: Configure the workflow for draft-only output or require manual review before publishing to WeChat or syncing to Feishu.

Risk: Repository context from private or proprietary projects could be shared through generated content or knowledge-base sync.

Mitigation: Use only approved repositories and confirm data-sharing permissions before running the workflow on non-public code.

Risk: The unattended cron publish example can automate external publication without clear approval safeguards.

Mitigation: Do not enable scheduled publication unless account scope, destination permissions, and human review controls are defined.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown reports and articles, JSON insights, shell commands, and Feishu document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate technical reports, WeChat article drafts, cover prompts, and Feishu document records from repository or GitHub Trending inputs.]

## Skill Version(s):

1.0.0 (source: workflow.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
