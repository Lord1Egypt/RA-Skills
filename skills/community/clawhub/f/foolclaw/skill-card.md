## Description: <br>
OpenClaw prank skill with local pranks and a quiet background operator. `Start FoolClaw` leaves a desktop prank and quietly arms FoolClaw in one step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[treapgogo](https://clawhub.ai/user/treapgogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use FoolClaw to run playful OpenClaw pranks such as desktop notes, browser taunts, media pranks, desktop manifesto files, and optional background operator turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep a recurring background prank operator active after startup. <br>
Mitigation: Install only where recurring prank behavior is acceptable, and use the documented disarm or reset flows when the prank session should stop. <br>
Risk: The skill can create desktop artifacts and open browser content. <br>
Mitigation: Run it only in user-approved workspaces and review generated local artifacts before sharing the environment. <br>
Risk: The skill may inspect available messaging capabilities and potentially contact other people through host-exposed channels. <br>
Mitigation: Limit or disable messaging and social-channel permissions unless that behavior is explicitly intended and consented to. <br>


## Reference(s): <br>
- [FoolClaw ClawHub release](https://clawhub.ai/treapgogo/foolclaw) <br>
- [Publisher profile](https://clawhub.ai/user/treapgogo) <br>
- [local-pranks](references/local-pranks.md) <br>
- [friend-pranks](references/friend-pranks.md) <br>
- [social-media-pranks](references/social-media-pranks.md) <br>
- [creative-pranks-light](references/creative-pranks-light.md) <br>
- [accomplice-pranks](references/accomplice-pranks.md) <br>
- [creative-pranks-wild](references/creative-pranks-wild.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown and short text responses with inline shell commands; runtime commands can create local text, HTML, and configuration/state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node. Supports win32, darwin, and linux according to release metadata.] <br>

## Skill Version(s): <br>
0.5.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
