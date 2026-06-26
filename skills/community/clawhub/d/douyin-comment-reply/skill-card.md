## Description: <br>
Monitors Douyin creator comments for the Qiqi Story Garden account, stages new comments as JSON, classifies them with LLM assistance, and prepares safe replies with retry handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators or account operators use this skill to collect, classify, review, and reply to comments on a named Douyin account while maintaining local state and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publicly reply from a logged-in Douyin account. <br>
Mitigation: Operate only the intended Douyin account and prefer manual review before posting automated replies. <br>
Risk: Commenter data is retained in hard-coded local Obsidian paths. <br>
Mitigation: Verify or change the local paths before use, restrict access to the stored files, and use the archive workflow for stale records. <br>
Risk: Generated replies may mishandle sensitive or personal-information requests. <br>
Mitigation: Use the documented blocking and human-review rules for contact details, addresses, schools, URLs, and uncertain comments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/douyin-comment-reply) <br>
- [Publisher profile](https://clawhub.ai/user/vincentlau2046-sudo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, JSON state files, and Markdown logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-operation guidance, comment classification prompts, reply decisions, local JSON state, and human-readable comment logs.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
