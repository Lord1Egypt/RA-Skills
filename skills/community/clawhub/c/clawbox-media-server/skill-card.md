## Description: <br>
Clawbox Media Server provides bidirectional LAN file sharing for AI agents through a static file server for downloads and an upload server with a browser upload UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techthrasher](https://clawhub.ai/user/techthrasher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to exchange files with users over a trusted local network when the chat channel cannot carry media or larger artifacts directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated upload and download servers can expose files to any device that can reach the configured ports. <br>
Mitigation: Use only on trusted networks, bind to localhost or a specific trusted interface when possible, and firewall ports 18801 and 18802. <br>
Risk: Files placed in the shared media directory may become visible or downloadable on the local network. <br>
Mitigation: Keep sensitive files out of ~/projects/shared-media and remove shared files when they are no longer needed. <br>
Risk: User services can keep file sharing available after the immediate transfer workflow is complete. <br>
Mitigation: Stop or disable the media and upload services when sharing is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/techthrasher/clawbox-media-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, local URLs, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Node.js and Python servers on configurable LAN ports; no external service is required for file exchange.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
