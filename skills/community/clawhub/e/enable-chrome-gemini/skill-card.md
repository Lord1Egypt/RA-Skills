## Description: <br>
Set up or repair Gemini in Chrome (Glic) on Windows, macOS, or Linux when enabling it for the first time outside the US or when the sidebar, floating panel, Alt+G shortcut, or top-bar entry disappears. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[at386369-ai](https://clawhub.ai/user/at386369-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users use this skill to enable or repair native Gemini/Glic in Chrome profiles on Windows, macOS, or Linux by backing up and patching Chrome Local State, then checking the required flags and language settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair script changes Chrome Local State, including Gemini eligibility, region, experiment flags, and language settings. <br>
Mitigation: Run --dry-run first, confirm the Chrome profile path, close Chrome before applying changes, avoid --force unless necessary, and keep the generated backup. <br>
Risk: Managed Chrome profiles or enterprise policy may block the setup. <br>
Mitigation: Stop and report the policy constraint instead of changing unrelated Chrome profile files. <br>


## Reference(s): <br>
- [Enable Chrome Gemini on ClawHub](https://clawhub.ai/at386369-ai/enable-chrome-gemini) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides execution of a Python repair script that supports dry-run, profile path, force, and language options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
