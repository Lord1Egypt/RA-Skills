## Description: <br>
A visual directory tree generator that creates a collapsible HTML report of a local folder and supports delivery through Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdsds222](https://clawhub.ai/user/sdsds222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to inspect or share a local folder structure as a self-contained HTML report. It is intended for cases where the folder path, names, timestamps, and sizes are acceptable to send through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local folder paths, names, timestamps, and sizes may be shared externally through Telegram. <br>
Mitigation: Use only on folders whose metadata is acceptable to send through Telegram, and confirm the target folder and chat destination before delivery. <br>
Risk: Sensitive directories could expose private project or system structure. <br>
Mitigation: Avoid sensitive directories unless there is explicit per-use consent or a local-only workflow is added. <br>
Risk: The Telegram bot token can grant access to send reports if mishandled. <br>
Mitigation: Keep the token protected as an environment variable and do not ask users to paste it into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdsds222/folder-visualizer-html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML report file path with supporting command and delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Telegram bot token environment variable for Telegram delivery.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
