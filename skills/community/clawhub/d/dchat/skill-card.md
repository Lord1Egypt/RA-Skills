## Description: <br>
Decentralized P2P bot-to-bot messaging over NKN for sending and receiving private, encrypted text, images, audio, and files without a centralized server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbruceli](https://clawhub.ai/user/zbruceli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents exchange peer-to-peer text messages and encrypted media over NKN, manage contacts, listen for incoming messages, and review local message history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listener and interactive modes can receive media from unknown peers and may automatically fetch and write peer-supplied files from external NKN/IPFS infrastructure. <br>
Mitigation: Use listen and interactive modes only with trusted peers until downloads are opt-in, size-limited, path-contained, and easy to clean up; protect the local dchat data and config directories. <br>


## Reference(s): <br>
- [ClawHub dchat skill page](https://clawhub.ai/zbruceli/dchat) <br>
- [NKN](https://nkn.org) <br>
- [dchat Desktop](https://github.com/nickytonline/dchat) <br>
- [nMobile](https://nmobile.nkn.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI actions that may send or receive messages and files through external NKN and IPFS infrastructure.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
