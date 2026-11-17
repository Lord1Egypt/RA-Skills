## Description:

Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for workflows where the user already knows the target account, tweet, or campaign and needs explicit engagement or approved posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to research known Twitter/X targets, prepare approved posts, and run explicit like, follow, reply, quote, or media-upload workflows through AIsa-backed clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIsa API key can drive Twitter/X account actions and may be exposed in command output.

Mitigation: Use the skill only in environments where command output is not logged or shared, and rotate the key if exposure is suspected.

Risk: Media upload commands can read arbitrary local paths that the runtime can access.

Mitigation: Pass only user-selected media files from a safe workspace path and confirm that files are intended for upload before execution.

Risk: Likes, follows, replies, quotes, and posts can affect a real Twitter/X account.

Mitigation: Require explicit target and content approval, and do not report success until the AIsa API response confirms the action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/aisa-twitter-research-engage-relay)
- [baofeng-tech Publisher Profile](https://clawhub.ai/user/baofeng-tech)
- [AIsa Twitter Engagement](artifact/references/engage_twitter.md)
- [AIsa Twitter OAuth](artifact/references/post_twitter.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell-command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; command results should be checked before claiming Twitter/X action success.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
