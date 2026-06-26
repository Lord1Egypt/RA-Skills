## Description: <br>
Capture frames or clips from RTSP/ONVIF cameras. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to configure and run local camsnap camera discovery, snapshots, clips, motion watch, and troubleshooting while keeping camera credentials and footage protected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera credentials or local camera details could be exposed in chat, logs, process lists, or copied files. <br>
Mitigation: Use placeholders in responses, place credentials only in `camsnap add` commands, and keep stored credentials in `~/.config/camsnap/config.yaml`. <br>
Risk: Captured snapshots, clips, or streams could be sent to unintended network destinations. <br>
Mitigation: Keep camsnap outputs local unless the user intentionally chooses network transfer, and avoid piping or redirecting footage to network-transmitting commands. <br>
Risk: Untrusted installation sources could affect camera access and captured media handling. <br>
Mitigation: Verify trust in the `steipete/tap/camsnap` Homebrew tap and `camsnap` binary before installation or use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/camsnap-hardened) <br>
- [Camsnap homepage](https://camsnap.ai) <br>
- [Faberlens camsnap safety evidence](https://faberlens.ai/explore/camsnap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local camsnap commands, diagnostic steps, redacted placeholders, and safety guidance for camera credentials and footage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
