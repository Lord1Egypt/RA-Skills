## Description: <br>
在修改环境变量或系统变量时，记录改了什么，并用电脑小白能听懂的话解释这次改动会带来什么影响；当程序、命令、环境或系统功能出现不明问题时，优先查看相关日志、报错或可见线索，再继续排查其他可能原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marerlee](https://clawhub.ai/user/marerlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support staff, and less technical users use this skill to record environment or system variable changes and understand their impact in plain language. It is also used for beginner-friendly troubleshooting that starts from logs, error messages, or visible clues before moving to broader environment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Environment changes can break commands or applications if the proposed value is wrong. <br>
Mitigation: Ask the agent to show the exact change and a rollback plan before applying real environment changes. <br>
Risk: Local change logs may accidentally capture secrets such as API keys, tokens, or passwords. <br>
Mitigation: Redact secrets from any local change log before saving or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marerlee/env-change-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with explanations, change records, and command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes environment change records to logs/env-change-log.md when variables are changed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
