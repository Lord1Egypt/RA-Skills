## Description: <br>
Create and manage shell command aliases for frequently used commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and shell users use this skill to create, list, retrieve, and persist local aliases for frequently used shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A saved alias can run any command the user supplied when later invoked. <br>
Mitigation: Only create aliases from trusted text and review command values before saving or using them. <br>
Risk: Persistent aliases stored in ~/.aliasrc may affect future shell behavior. <br>
Mitigation: Review ~/.aliasrc and remove aliases that are no longer needed or were added by mistake. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/alias-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-provided aliases to ~/.aliasrc when the helper script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
