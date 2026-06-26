## Description: <br>
Helps an agent send local files or images through a Feishu or Lark app by uploading them to the appropriate messaging API and sending the returned file or image key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kururu111](https://clawhub.ai/user/kururu111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to send a local file attachment or correct a failed image send where the recipient only received a local path string. It is intended for Feishu or Lark workflows that have an authorized app ID, app secret, and explicit recipient ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected local files or images through Feishu or Lark. <br>
Mitigation: Verify the file path and recipient before running the scripts, and avoid sensitive or regulated files unless the sender is authorized. <br>
Risk: The scripts accept app credentials as command-line arguments. <br>
Mitigation: Prefer adapting credential handling to read the app secret from a protected environment variable or secret store. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kururu111/feishu-send-file-1-2-1) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [send_file.py](artifact/scripts/send_file.py) <br>
- [send_image.py](artifact/scripts/send_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with command-line examples and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local file path or image path, Feishu or Lark app credentials, recipient type, recipient ID, and optional domain selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports skill package version 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
