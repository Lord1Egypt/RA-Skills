## Description: <br>
Automates Douyin community interactions by generating short comment replies and DM greetings, and by guiding browser workflows for comments, private messages, likes, and topic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media operators and developers use this skill to generate Douyin interaction text and follow browser automation steps for comment replies, private messages, likes, and search. It is intended for account interaction workflows that remain under explicit human approval and platform-policy review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post comments, send private messages, and like content through a user's Douyin account without clear approval or scope limits. <br>
Mitigation: Require explicit approval for each comment, DM, and like; restrict execution to reviewed target lists; and apply conservative rate limits before browser actions are run. <br>
Risk: Automated or unsolicited messages may be deceptive, spam-like, or inconsistent with platform rules. <br>
Mitigation: Use only user-reviewed message text, avoid unsolicited outreach and human-mimicking behavior, and confirm that each workflow complies with Douyin policies before use. <br>
Risk: The reply generator can keep a local history of replied comment IDs, which may expose account activity patterns if the workspace is shared. <br>
Mitigation: Monitor, protect, or clear the local reply-history file when account activity is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/douyin-automation-v2) <br>
- [Publisher profile](https://clawhub.ai/user/linbo405) <br>
- [Douyin homepage](https://www.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text replies, Python CLI output, and Markdown browser workflow instructions with inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local reply-history state when comment IDs are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
