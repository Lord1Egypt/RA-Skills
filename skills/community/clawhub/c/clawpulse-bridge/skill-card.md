## Description: <br>
Configure and maintain ClawPulse integration for OpenClaw, including a token-protected status bridge, Tailscale-safe access, iOS endpoint and token defaults, and troubleshooting for ATS, authentication, and sync issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtual-ny](https://clawhub.ai/user/virtual-ny) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and troubleshoot a ClawPulse status bridge for OpenClaw, including bearer-token setup, monitor mode, endpoint selection, and token rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor exposes an unauthenticated internal status endpoint on all network interfaces by default. <br>
Mitigation: Bind the monitor to localhost or a Tailscale/firewalled interface, or patch, disable, or bearer-token-protect the internal endpoint before use. <br>
Risk: Setup output and generated QR images contain access tokens. <br>
Mitigation: Keep terminal output and QR images private, remove generated setup images when no longer needed, and rotate tokens if they may have been exposed. <br>
Risk: Apply mode starts local HTTP bridge and monitor processes and writes local environment and server files. <br>
Mitigation: Review commands before execution, run dry-run mode first, and use local-only binding when remote device access is not required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/virtual-ny/clawpulse-bridge) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that create local configuration files, start local HTTP services, and print bearer tokens or QR setup links.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
