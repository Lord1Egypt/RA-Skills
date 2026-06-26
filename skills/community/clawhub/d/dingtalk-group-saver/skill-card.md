## Description: <br>
Automatically saves DingTalk group IDs and names to persistent OpenClaw memory when the agent is mentioned in a DingTalk group chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users who operate DingTalk group bots use this skill to remember group IDs and names after an @ mention so later sessions can route messages or inspect known groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DingTalk group IDs and names are saved into shared long-term OpenClaw memory across sessions. <br>
Mitigation: Use only with workspace consent, restrict access to the memory files, and document how saved groups can be reviewed and deleted. <br>
Risk: The skill rewrites MEMORY.md, which can affect existing long-term memory content if section boundaries are not as expected. <br>
Mitigation: Back up MEMORY.md before enabling the skill and review changes after installation or updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/dingtalk-group-saver) <br>
- [Publisher profile](https://clawhub.ai/user/jiangzhiyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [JSON records and Markdown memory table entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists DingTalk group ID, group name, first-seen timestamp, last-active timestamp, and mention count in workspace memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
