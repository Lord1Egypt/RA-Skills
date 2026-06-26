## Description: <br>
Control Browser's kernel for web automation, including navigation, element interaction, page scrolling, file and video downloading, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handongpu16](https://clawhub.ai/user/handongpu16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to control a QQ Browser/X5 browser session for web navigation, form interaction, page inspection, scrolling, and file or video downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs QQ Browser and x5use system packages from an external supply chain. <br>
Mitigation: Install only in trusted environments after reviewing the package source and approving system-level package changes. <br>
Risk: The skill starts a background local browser-control service and writes logs under /usr/local/qb_logs. <br>
Mitigation: Run it in an isolated workspace, confirm the local service lifecycle, and review log retention or cleanup requirements. <br>
Risk: Typed input is logged by input_text.py, which may expose sensitive values. <br>
Mitigation: Avoid entering secrets or private data through the skill until raw input logging is removed or masked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/handongpu16/automation-browser) <br>
- [QQ Browser and x5use package download source](https://dldir1v6.qq.com/invc/tt/QB/Public/ubuntu_qb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Plain text and Markdown page state from Python and shell commands; downloaded files when download commands are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns action status, current page metadata, and indexed interactive elements for follow-up browser actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
