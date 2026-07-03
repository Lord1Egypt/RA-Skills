## Description: <br>
User behavior correction skill triggered by fix-related feedback that analyzes the mistake, improves the relevant prompt or agent guidance to prevent recurrence, and resumes the current task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to turn corrective feedback into a structured root-cause analysis, prompt or guidance improvement, and completion of the original work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad behavior-correction feedback can lead an agent to modify persistent memory, rules, hooks, or global agent configuration. <br>
Mitigation: Narrow activation to explicit fix commands and require confirmation before writing persistent agent state, rule files, hooks, settings, or infrastructure-related changes. <br>
Risk: The skill may prompt review of sensitive local agent paths and hook registration such as ~/.claude, ~/.agents, and settings.json. <br>
Mitigation: Review filesystem and configuration access before execution, and scan proposed changes before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drumrobot/skills/fix) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/drumrobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, analysis tables, file edits, and command suggestions when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify prompt guidance, task plans, rule files, hook configuration, and follow-up verification notes.] <br>

## Skill Version(s): <br>
0.3.4 (source: server release metadata and CHANGELOG, released 2026-06-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
