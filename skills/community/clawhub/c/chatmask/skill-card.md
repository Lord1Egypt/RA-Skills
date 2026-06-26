## Description: <br>
Pixelate chat and messaging app screenshots to hide chat names, profile pictures, and display names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankz2020](https://clawhub.ai/user/frankz2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ChatMask to redact identity elements from chat screenshots before sharing, publishing, or reviewing them. The skill helps an agent locate requested chat UI elements and run local image processing for each screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can automatically change system packages and fetch helper code from GitHub. <br>
Mitigation: Review the setup commands first, preinstall python3-venv where possible, and verify the pinned commit and Python requirements before use. <br>
Risk: Temporary input and output folders may retain sensitive chat screenshots after processing. <br>
Mitigation: Delete `/tmp/chat_pixelate_in_*` and `/tmp/chat_pixelate_out_*` folders after processing sensitive screenshots. <br>


## Reference(s): <br>
- [ChatMask homepage](https://github.com/frankz2020/chatmask) <br>
- [ChatMask on ClawHub](https://clawhub.ai/frankz2020/chatmask) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files plus Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes each screenshot separately and writes pixelated image files to a temporary output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
