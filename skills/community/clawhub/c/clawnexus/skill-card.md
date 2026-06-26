## Description: <br>
Discover, name, and manage OpenClaw instances on your LAN. Scan for AI agents, check status, set aliases, resolve .claw names, and get connection URLs via the ClawNexus daemon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alan-stratcraftsai](https://clawhub.ai/user/alan-stratcraftsai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to discover OpenClaw instances, check their status, assign aliases, resolve .claw names, and produce connection URLs for local or registered instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger local network scans for OpenClaw instances. <br>
Mitigation: Use scan commands only on networks where probing devices is allowed. <br>
Risk: The local daemon persists discovered instance history in ~/.clawnexus/registry.json. <br>
Mitigation: Review or clear the registry file when discovered instance history should not be retained. <br>
Risk: The skill depends on a locally installed clawnexus daemon and npm package. <br>
Mitigation: Install only when the clawnexus package is trusted and confirm the daemon is running before using commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alan-stratcraftsai/clawnexus) <br>
- [Project homepage](https://github.com/SilverstreamsAI/ClawNexus) <br>
- [Publisher profile](https://clawhub.ai/user/alan-stratcraftsai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes curl is available and the ClawNexus daemon listens on localhost:17890.] <br>

## Skill Version(s): <br>
0.4.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
