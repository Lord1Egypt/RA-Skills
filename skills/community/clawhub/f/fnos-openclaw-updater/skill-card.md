## Description: <br>
Helps update OpenClaw on fnOS by checking the running version, finding the latest stable version, running npm install in the managed-install directory, and verifying the updated gateway version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandaltsgo](https://clawhub.ai/user/pandaltsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers maintaining OpenClaw on fnOS use this skill to choose the managed-install update path, avoid global-install permission failures, and verify that the active gateway package has been updated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update command replaces the OpenClaw package currently used by the gateway. <br>
Mitigation: Confirm the current and target versions first, run the command only for the intended managed install, and keep a rollback or backup plan. <br>
Risk: An incorrect OPENCLAW_DATA_DIR could point the update at the wrong OpenClaw installation. <br>
Mitigation: Verify OPENCLAW_DATA_DIR resolves to the intended managed-install path before running npm install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pandaltsgo/fnos-openclaw-updater) <br>
- [Publisher profile](https://clawhub.ai/user/pandaltsgo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides version checks, managed-install npm update commands, and post-update verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
