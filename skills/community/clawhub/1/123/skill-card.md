## Description: <br>
Claims to automate Minecraft Java Edition from screenshots and keyboard/mouse commands, while the bundled executable code targets a different game workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyhahalife-11](https://clawhub.ai/user/skyhahalife-11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users would use this skill to guide game automation with screenshot observation and keyboard or mouse actions. Reviewers should not use it expecting Minecraft automation until the documented behavior and executable package are reconciled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented Minecraft behavior does not match the executable code's game workflow. <br>
Mitigation: Do not use for Minecraft automation until the publisher provides a corrected package with matching documentation. <br>
Risk: Executable code depends on missing unreviewed roco_actions code. <br>
Mitigation: Require the missing source or a pinned reviewed dependency before installing or running the skill. <br>
Risk: The code references QQ login-state persistence. <br>
Mitigation: Require clear documentation for login/session storage and removal before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyhahalife-11/123) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/skyhahalife-11) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance and Python helper functions returning text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The executable code depends on roco_actions, which is not included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
