## Description: <br>
Checks a specified SKILL for lazy, skipped, or simplified execution patterns, can append a self-audit hook, and can remove that hook to restore the original SKILL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panhongwei](https://clawhub.ai/user/panhongwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-skill maintainers use this skill to locate skill files, add a supplied self-audit hook, or remove a previously added hook across Claude Code, OpenAI Codex CLI, and OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change other skills' instruction files by appending an audit hook. <br>
Mitigation: Use it only on an explicitly named target skill and review the exact diff before replacing any SKILL.md. <br>
Risk: The hook can write local debug audit files that may include task details or prompt content. <br>
Mitigation: Avoid using it where task details should not be written to local files, and review generated debug files before sharing or retaining them. <br>
Risk: The hook content is loaded from a separate file and could alter the behavior of the target skill. <br>
Mitigation: Confirm that skill-audit-hook.txt is trusted before injection and remove the hook when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panhongwei/auto-hook) <br>
- [Publisher profile](https://clawhub.ai/user/panhongwei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and generated skill-file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce modified SKILL.md content and local debug audit files when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
