## Description: <br>
Summarizes WeChat group chat highlights into structured normal or opt-in roast digests using the local wx-cli binary, while maintaining per-group history, participant profiles, and group fact memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with local WeChat access use this skill to turn WeChat group history into readable digests, optional sarcastic variants, per-user profile updates, and durable group memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires unsandboxed local access to private WeChat data. <br>
Mitigation: Use it only when the user understands and accepts that access, and review the local wx-cli and WeChat data access requirements before running. <br>
Risk: The skill creates durable local archives of group messages, digests, participant profiles, and memory files. <br>
Mitigation: Choose a manageable data_root, restrict file access, and delete histories, profiles, and memory files when they are no longer needed. <br>
Risk: Group members may not expect their messages to be summarized or profiled. <br>
Mitigation: Avoid using the skill on groups where participants would not expect this processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-wechat-summary) <br>
- [Baoyu Skills Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-wechat-summary) <br>
- [wx-cli](https://github.com/jackwener/wx-cli) <br>
- [Output Formats](references/output-formats.md) <br>
- [Profiles](references/profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown digests with configuration and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce normal digests by default, opt-in roast digests, profile files, history files, and group memory updates.] <br>

## Skill Version(s): <br>
1.117.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
