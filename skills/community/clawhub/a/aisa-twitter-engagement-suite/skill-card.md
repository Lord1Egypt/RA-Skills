## Description:

Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research X/Twitter accounts and content, publish posts after OAuth approval, and perform account engagement actions through the AIsa relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the full AISA_API_KEY in normal command output.

Mitigation: Avoid sensitive accounts until fixed, treat existing authorize/post logs as potentially containing the key, and rotate the key if exposed.

Risk: The skill can directly publish posts or change likes, follows, and unfollows on the authorized X/Twitter account.

Mitigation: Confirm the intended account, target, and content before action, require OAuth approval where applicable, and only report success after the relay returns success.

Risk: Twitter/X requests and media uploads are routed through api.aisa.one.

Mitigation: Use the skill only when the user trusts AIsa and api.aisa.one with Twitter/X relay access and uploaded media.

## Reference(s):

- [AIsa Twitter Engagement](artifact/references/engage_twitter.md)
- [AIsa Twitter OAuth](artifact/references/post_twitter.md)
- [AIsa homepage](https://aisa.one)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; actions are performed through the AIsa relay after required authorization.]

## Skill Version(s):

1.0.3 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
