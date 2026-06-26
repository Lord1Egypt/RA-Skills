## Description: <br>
Helps an agent browse an external avatar gallery, choose an avatar, preview it with the user, and download the selected image locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when they want an agent to select an avatar from a designated gallery, ask for user approval, and save the approved image to the workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt unsolicited avatar-selection behavior after installation. <br>
Mitigation: Disable unsolicited post-install actions and require the user to explicitly request avatar selection before the agent starts browsing. <br>
Risk: The skill browses an external avatar gallery. <br>
Mitigation: Confirm that browsing the configured gallery is acceptable before use and review any selected image URL before downloading. <br>
Risk: The skill can write a downloaded image to the local workspace. <br>
Mitigation: Require explicit confirmation for downloads and verify the destination path before saving workspace/assets/avatar.jpg. <br>
Risk: The artifact includes intimate or persona-specific prompt wording that may be inappropriate for some deployments. <br>
Mitigation: Remove or adapt persona-specific language before enabling the skill in shared, professional, or customer-facing environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/avatar-helper) <br>
- [Publisher profile](https://clawhub.ai/user/adminlove520) <br>
- [Avatar gallery](https://wallpaper.dfyx.click/avatar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown conversation with browser actions and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save an avatar image to workspace/assets/avatar.jpg after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
