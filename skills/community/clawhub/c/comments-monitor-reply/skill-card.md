## Description: <br>
Monitors comments across major social platforms, analyzes sentiment and public opinion, generates personalized replies, sends negative-comment alerts, and produces reports for social media operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xikal](https://clawhub.ai/user/xikal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operations teams use this skill to monitor comments across configured platforms, draft or send replies, identify negative sentiment, and generate public-opinion reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use account cookies or platform API tokens to automatically post public replies. <br>
Mitigation: Use least-privilege platform tokens where possible, avoid main-account cookies, test with a low-risk account, and enable human approval before replies are posted. <br>
Risk: Comment data, reply history, exports, webhook payloads, and credentials may contain sensitive operational or account information. <br>
Mitigation: Limit enabled platforms and webhook destinations, confirm how credentials and logs are stored and deleted, and review the external repository before running dependency installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xikal/comments-monitor-reply) <br>
- [Homepage](https://github.com/openclaw-skills/comments-monitor-reply#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples, generated reply text, alerts, and report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require configured platform credentials and webhook URLs before producing live monitoring or reply outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
