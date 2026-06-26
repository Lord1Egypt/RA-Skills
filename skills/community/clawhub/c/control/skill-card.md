## Description: <br>
Advanced desktop automation with mouse, keyboard, and screen control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Breckengan](https://clawhub.ai/user/Breckengan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add supervised desktop automation workflows, including mouse and keyboard control, screenshots, image lookup, window management, clipboard access, and higher-level task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live desktop control can click, type, drag, launch applications, and trigger hotkeys in the active user session. <br>
Mitigation: Keep failsafe enabled, use approval mode where possible, and supervise actions before running the skill against sensitive applications. <br>
Risk: Screenshots, clipboard reads, logs, and typed text can expose private or sensitive data. <br>
Mitigation: Close sensitive windows, avoid passwords and private documents, and treat screenshots, logs, and clipboard output as sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Breckengan/control) <br>
- [Desktop Control Skill Documentation](artifact/SKILL.md) <br>
- [AI Desktop Agent Guide](artifact/AI_AGENT_GUIDE.md) <br>
- [Desktop Control Quick Reference](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown documentation with Python and bash code blocks; runtime helpers return Python objects such as screenshots, coordinates, window lists, clipboard text, and task result dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Desktop actions can affect the live user interface; screenshots, logs, typed text, and clipboard values may contain sensitive data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
