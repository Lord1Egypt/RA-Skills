## Description:

Cross-post content to Twitter/X, Reddit, and LinkedIn from one prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drspx](https://clawhub.ai/user/drspx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, preview, and publish similar content across Twitter/X, Reddit, and LinkedIn from a single command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to public social accounts when valid credentials are configured.

Mitigation: Use it only for intended immediate public posting, run the preview command first, and review the exact content and target platform before posting.

Risk: The skill requires social API credentials and stores configuration locally.

Mitigation: Provide narrowly scoped credentials, keep secrets out of recorded or shared terminals, and verify the local config file remains protected.

Risk: All-platform posting and scheduling claims are unreliable in this version.

Mitigation: Post to specific platforms explicitly and do not rely on this release for scheduled publishing.

## Reference(s):

- [Cross-Post on ClawHub](https://clawhub.ai/drspx/skills/cross-post)
- [Publisher profile: drspx](https://clawhub.ai/user/drspx)
- [Twitter/X developer setup](https://developer.twitter.com)
- [Reddit app preferences](https://www.reddit.com/prefs/apps)
- [LinkedIn developers](https://developers.linkedin.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger API calls that publish public social posts when the user runs the posting command with valid credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
