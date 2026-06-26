## Description: <br>
Lets OpenClaw share single workspace files through expiring, tokenized HTTP links intended for local-network or VPN access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tradmangh](https://clawhub.ai/user/tradmangh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when they need to make a single workspace file available from a browser or another local/VPN-connected machine without publishing it publicly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes selected local files over the network. <br>
Mitigation: Share only files intentionally meant for local/VPN access, keep validity windows short, use one-time links when practical, and stop the printed server PID when finished. <br>
Risk: Active tokenized links may be readable from a predictable temporary log while the share is running. <br>
Mitigation: Use the skill on trusted machines, avoid sharing sensitive files, and remove or protect temporary share logs after stopping the server. <br>
Risk: VPN-connected or shared-network clients may be able to reach the server if they have the token. <br>
Mitigation: Review network exposure before use and avoid running shares on untrusted shared networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tradmangh/expiring-local-fileshare) <br>
- [Publisher profile](https://clawhub.ai/user/tradmangh) <br>
- [Publisher homepage](https://github.com/tradmangh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and a generated HTTP link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a tokenized local-network URL, server PID, and stop command for a selected file.] <br>

## Skill Version(s): <br>
1.0.2 (source: METADATA.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
