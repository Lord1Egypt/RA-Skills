## Description: <br>
Steam Deck and Bazzite system management for gamescope, Flatpak, Podman, GPU, performance, game mode, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverod](https://clawhub.ai/user/silverod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Steam Deck and Bazzite users, developers, and operators use this skill to inspect system health, troubleshoot gaming sessions, manage Flatpak apps, review GPU and performance state, and configure common gaming tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some commands can expose a local service to a Tailscale tailnet. <br>
Mitigation: Confirm the service, port, and intended tailnet exposure before using `tailscale serve --bg`. <br>
Risk: Some Flatpak commands can delete application data. <br>
Mitigation: Back up important application data and confirm the target app ID before running `flatpak uninstall --delete-data`. <br>
Risk: Some configuration examples make persistent changes to user files. <br>
Mitigation: Review append-style configuration writes such as `>>` before execution and keep a reversible copy of the original configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverod/deckctl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and task checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command examples should be reviewed before execution on the target device.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
