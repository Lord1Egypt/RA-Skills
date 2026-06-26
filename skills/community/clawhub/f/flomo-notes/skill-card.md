## Description: <br>
Save user-provided notes to Flomo through a configured Flomo inbox webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoluoboding](https://clawhub.ai/user/xiaoluoboding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save selected chat notes or short text snippets into their Flomo inbox from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Flomo webhook URL can post to the user's inbox if exposed. <br>
Mitigation: Keep FLOMO_WEBHOOK_URL private and configure it only through trusted environment or per-skill configuration. <br>
Risk: Selected note text is sent to Flomo. <br>
Mitigation: Avoid sending secrets or highly sensitive content as notes. <br>
Risk: Documentation examples pass note text as an argument while the script reads note text from stdin. <br>
Mitigation: Invoke the script with note text on stdin unless the documentation is corrected. <br>


## Reference(s): <br>
- [Flomo](https://flomoapp.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoluoboding/flomo-notes) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaoluoboding) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Shell command execution with a short text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts note content to the configured Flomo webhook and appends an OpenClaw origin tag.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
