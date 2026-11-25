## Description:

Search and browse Alibaba Cloud agent skills, inspect skill details, and guide installation when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud users can find Alibaba Cloud skills by task or product, browse categories, inspect skill details, and install a selected skill when they ask.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags installation beyond the stated request, broad activation phrases, privacy gaps in external searches, and unpinned installer packages; some references were unresolved, so the review is incomplete.

Mitigation: Consider avoiding installation until the author clarifies when installation can occur, what data searches send to Alibaba Cloud, and how installer versions can be pinned.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-find-skills)
- [AgentExplorer HTTP API reference](references/agentexplorer-api.md)
- [Verification methods](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summaries and tables with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are summarized for the user's requested task; installation guidance is provided only when requested.]

## Skill Version(s):

0.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
