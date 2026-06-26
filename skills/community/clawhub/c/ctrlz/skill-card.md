## Description: <br>
AI Operation Undo System. When user executes /ctrlZ or says "undo last step", automatically revert all file modifications, installations, etc. from the recent conversation round. Default keeps 1 undo unit, configurable to 3 or 5. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisluo5311](https://clawhub.ai/user/chrisluo5311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use CtrlZ to record AI-driven file, directory, and package-installation operations during a conversation round and roll back recent changes with /ctrlZ commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language undo triggers can delete or overwrite local files without preview or confirmation. <br>
Mitigation: Use explicit /ctrlZ commands, inspect the undo list before rollback, and require operator confirmation before applying destructive undo actions. <br>
Risk: Backups and recorded file contents can include secret-bearing files. <br>
Mitigation: Avoid recording secrets, restrict permissions on the undo database and backup directory, and clear records when rollback data is no longer needed. <br>
Risk: Package installs and external command side effects are not fully undone automatically. <br>
Mitigation: Treat package-removal output as manual remediation guidance and review external side effects separately after rollback. <br>


## Reference(s): <br>
- [ClawHub CtrlZ release page](https://clawhub.ai/chrisluo5311/ctrlz) <br>
- [README.md](README.md) <br>
- [TEST_CASES.md](TEST_CASES.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SQLite-backed local undo records and backup files under the OpenClaw skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
