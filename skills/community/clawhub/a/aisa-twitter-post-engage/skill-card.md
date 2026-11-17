## Description:

Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay for Twitter/X research, posting, likes, follows, and related workflows without sharing passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research X/Twitter content and perform OAuth-approved posting, media upload, like, unlike, follow, and unfollow actions through the AIsa relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIsa API key may appear in command output or agent transcripts.

Mitigation: Use a scoped or disposable key where possible, avoid sharing raw command output, and rotate any key that may have been logged.

Risk: Relay-based Twitter/X posting and engagement grants an external service authority to act on the authorized account.

Mitigation: Install only if the AIsa relay is trusted, require explicit OAuth approval, and review each target account, tweet, or post before write actions.

Risk: Ambiguous account or tweet resolution could cause engagement with the wrong target.

Mitigation: Confirm candidates when multiple accounts or tweets match and do not proceed from guessed IDs.

## Reference(s):

- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa service homepage](https://aisa.one)
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/aisa-twitter-post-engage)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with CLI examples and JSON client responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; posting and engagement require explicit OAuth approval.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
