## Description:

Safe content workflow (drafts/reviewed/revised/approved/posted) with human-in-the-loop approval, plus CLI to list/move/review and post to LinkedIn/X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larsderidder](https://clawhub.ai/user/larsderidder)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to set up a human-reviewed content workflow for drafting, revising, approving, and posting social content through the Agent Content Pipeline CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs a global, unpinned npm CLI that operates on local content directories.

Mitigation: Use a pinned and reviewed package version before installation, and install only in environments where the publisher and package are trusted.

Risk: The CLI supports social-account posting flows and may handle browser or session credentials.

Mitigation: Use dry runs first, keep credentials isolated, and provide browser tokens or cookies only when intentional posting through those accounts is acceptable.

Risk: Content can be prepared for public social platforms, creating reputational or policy risk if posted without review.

Mitigation: Preserve the documented human approval boundary: agents draft and revise, while humans approve and post.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/larsderidder/skills/agent-content-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML frontmatter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human review before approval or posting.]

## Skill Version(s):

0.2.3 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
