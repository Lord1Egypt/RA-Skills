## Description: <br>
Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AIsa relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to research X/Twitter content and perform approved posting, liking, following, and unfollowing workflows through AIsa relay clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorization and posting command output may expose the AIsa API key in logs or transcripts. <br>
Mitigation: Use a rotatable AIsa API key, avoid sharing authorize/post command output until the key-output issue is fixed, and redact secrets from logs. <br>
Risk: Media attachments and engagement actions are sent through api.aisa.one and may affect public Twitter/X content. <br>
Mitigation: Attach only files intended for relay upload or publication, and confirm targets before posting, liking, following, or unfollowing. <br>


## Reference(s): <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-twitter-engagement-suite) <br>
- [AIsa homepage](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; Twitter/X actions are relay-based through api.aisa.one.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
