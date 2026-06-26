## Description: <br>
Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for explicit, user-approved engagement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user has identified a Twitter/X account, tweet, or campaign and wants researched, explicit follow-through such as reading context, liking, following, replying, quoting, posting, or uploading approved media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live Twitter/X actions such as likes, follows, replies, posts, and media uploads once invoked. <br>
Mitigation: Require explicit confirmation of the exact account, tweet, post text, and media files before allowing any engagement or publishing command. <br>
Risk: The skill requires a sensitive AISA_API_KEY and security evidence notes that command output may expose the key. <br>
Mitigation: Use a scoped, rotatable key, avoid sharing logs or terminal output, and rotate the key if exposure is suspected. <br>
Risk: Twitter/X data and uploaded media are routed through AIsa's relay. <br>
Mitigation: Use the skill only when routing through AIsa is acceptable for the user's data, account, and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bibaofeng/aisa-twitter-research-engage-relay-aisa-api) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and explicit confirmation before live Twitter/X engagement or posting actions.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
