## Description: <br>
Simple CLI wrapper for the are.na API. Lists channels, adds blocks, watches feeds. No AI, no automation, no external integrations. Just API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koellins](https://clawhub.ai/user/koellins) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and are.na users can use this skill to operate an are.na CLI for listing channels, inspecting channel contents, adding image or link blocks, watching feeds, and managing multiple accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed bundle references an arena CLI script, but that script is not included. <br>
Mitigation: Do not install or enter an are.na API token until the missing script is supplied from a trusted, reviewed source. <br>
Risk: The skill handles are.na API tokens stored in local token files. <br>
Mitigation: Treat token files as secrets, restrict local file permissions, and remove tokens when uninstalling the skill. <br>
Risk: CLI commands can change are.na account or channel state. <br>
Mitigation: Review account-changing and channel-changing commands before running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/koellins/arena-claw) <br>
- [Publisher profile](https://clawhub.ai/user/koellins) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; the reviewed bundle does not include the arena CLI script referenced by the installer and documentation.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
