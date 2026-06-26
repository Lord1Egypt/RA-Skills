## Description: <br>
Re-applies custom patches to claw-lark plugin distribution files after updates so target resolution, account resolution, mention filtering, and thread replies continue to work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pengxiao-Wang](https://clawhub.ai/user/Pengxiao-Wang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers maintaining a local claw-lark/OpenClaw integration use this skill to reapply patch guidance and shell commands after plugin updates. It helps preserve custom Lark message routing behavior, including mention filtering, target resolution, account resolution, and thread replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch script modifies local claw-lark distribution files. <br>
Mitigation: Review the script, confirm CLAW_LARK_DIST points to the intended installation, and keep a backup or reinstall path before applying patches. <br>
Risk: Incorrect bot identity settings can make requireMention filtering behave incorrectly. <br>
Mitigation: Set BOT_OPEN_ID and BOT_NAME for the target bot and verify group, direct-message, and other-bot mention behavior after restarting the gateway. <br>
Risk: claw-lark plugin updates can overwrite the patched files. <br>
Mitigation: Reapply the patches after plugin updates and rerun the documented verification checks before relying on the integration. <br>


## Reference(s): <br>
- [Patch Details](artifact/references/patch-details.md) <br>
- [ClawHub skill page](https://clawhub.ai/Pengxiao-Wang/claw-lark-patches) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JavaScript patch snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a shell script that modifies local claw-lark distribution files when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
