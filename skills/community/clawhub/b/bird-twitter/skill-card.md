## Description:

Twitter/X CLI wrapper using bird - post tweets, reply, read, search, and manage your timeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuhuilove](https://clawhub.ai/user/chuhuilove)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate the bird CLI for Twitter/X posting, replies, timeline reading, search, and account actions from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Twitter/X session cookies that can grant account access if exposed.

Mitigation: Treat AUTH_TOKEN and CT0 like passwords; do not share, log, commit, or paste them into untrusted prompts or tools.

Risk: The skill enables live posting and account changes such as tweets, replies, follows, and unfollows.

Mitigation: Require explicit confirmation before any tweet, reply, follow, or unfollow action, including the target account and final content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chuhuilove/skills/bird-twitter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapped bird CLI can emit plain text or JSON when the corresponding output options are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
