## Description: <br>
Automatically send workspace files to Feishu/Lark when files are generated or updated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace automation users use this skill to identify generated files, create file-send tool calls, and optionally watch a workspace directory for new files to deliver to Feishu/Lark recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic or broad file-transfer workflows can send unintended workspace files to Feishu/Lark. <br>
Mitigation: Use explicit file paths or narrow file patterns, avoid watching directories that may contain secrets or unrelated work, and stop watch mode as soon as the task is complete. <br>
Risk: Files may be delivered to the wrong Feishu/Lark recipient if the open_id is incorrect. <br>
Mitigation: Confirm the recipient open_id before every send operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/auto-file-sender) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Auto-send helper script](artifact/scripts/auto_send.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-send instructions and helper-script commands; the helper script prints JSON send commands rather than sending files directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
