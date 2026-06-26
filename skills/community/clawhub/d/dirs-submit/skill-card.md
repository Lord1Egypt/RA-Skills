## Description: <br>
CLI guidance for using the ship command to log in, submit URLs, preview metadata, check versions, and self-update for aidirs.org and backlinkdirs.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinaigc](https://clawhub.ai/user/allinaigc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to run ship CLI workflows for browser login, URL submission, metadata preview, version checks, and self-update handling across supported directory sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented installer and self-update flow can replace local CLI code. <br>
Mitigation: Review or pin the installer and confirm release assets before running install or self-update commands. <br>
Risk: The CLI stores account tokens in ~/.config/ship/config.json. <br>
Mitigation: Protect the config file, avoid sharing logs or screenshots that expose tokens, and re-run login if authorization fails. <br>
Risk: Submit commands send user-provided URLs to a selected directory site. <br>
Mitigation: Confirm the target site and URL before running submit commands. <br>


## Reference(s): <br>
- [Dirs Submit Homepage](https://github.com/RobinWM/ship-skills#dirs-submit) <br>
- [API Reference](references/api.md) <br>
- [Config Reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and status interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local token configuration at ~/.config/ship/config.json and command output from the ship CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
