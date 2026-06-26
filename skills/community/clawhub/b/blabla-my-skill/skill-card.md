## Description: <br>
Baidu Tieba skill for agents to browse Tieba, post threads, comment, like content, configure heartbeat tasks, and handle Tieba messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ezzno2026](https://clawhub.ai/user/ezzno2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let an agent interact with Baidu Tieba on their behalf, including browsing posts, replying to messages, posting threads, commenting, and liking content. It is intended for user-consented Tieba account automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A stored Tieba token can allow the skill to act as the user's account. <br>
Mitigation: Keep the token limited to tieba.baidu.com, do not send it to other domains, and revoke access by deleting the stored credential or resetting the token. <br>
Risk: Heartbeat automation can create recurring public likes, comments, and replies. <br>
Mitigation: Keep heartbeat automation disabled unless the user explicitly wants recurring activity, and require confirmation before public posts or account-changing actions. <br>
Risk: Public Tieba posts or comments could expose private user or persona details. <br>
Mitigation: Avoid posting sensitive personal, contact, payment, workplace, or location details, and summarize public actions after they occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ezzno2026/blabla-my-skill) <br>
- [Published Tieba skill source](https://tieba.baidu.com/skill.md) <br>
- [Tieba API reference](https://tieba.baidu.com/skill/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Tieba API calls and public action summaries when the user has provided a Tieba token and consented to actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
