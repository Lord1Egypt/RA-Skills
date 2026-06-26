## Description: <br>
Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. Use when the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research X/Twitter data and perform approved posting or engagement workflows through AIsa with an AISA_API_KEY and explicit OAuth approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay-mediated posting, liking, following, and unfollowing can perform live Twitter/X account actions. <br>
Mitigation: Review every post, media file, tweet target, and account target before running write or engagement commands, and know how to revoke Twitter/X OAuth authorization. <br>
Risk: Authorization or posting command output can expose the AIsa API key according to the security summary. <br>
Mitigation: Use a dedicated or rotated AISA_API_KEY and avoid sharing command output until the key-printing issue is fixed. <br>
Risk: Media uploads send local files to the relay for publishing. <br>
Mitigation: Upload only files intended for public Twitter/X posting and avoid private local media. <br>


## Reference(s): <br>
- [AIsa Twitter OAuth reference](references/post_twitter.md) <br>
- [AIsa Twitter Engagement reference](references/engage_twitter.md) <br>
- [AIsa homepage](https://aisa.one) <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/aisa-twitter-post-engage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AISA_API_KEY and may return relay status, authorization links, tweet identifiers, or target account details.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
