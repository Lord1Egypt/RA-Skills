## Description: <br>
NanoClaw runtime traffic monitoring baseline for host-side proxy inspection with container-safe MCP and IPC status surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill as a builder-facing specification for adding opt-in NanoClaw traffic monitoring, redacted local findings, and container-safe status surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the scaffold for a working traffic monitor. <br>
Mitigation: Treat this release as a builder-facing specification until a future version ships an implemented proxy, detector, host service, and MCP tool surface. <br>
Risk: A future proxy implementation could expose sensitive traffic, CA key material, or unredacted findings if the safety contract is not preserved. <br>
Mitigation: Keep monitoring opt-in, keep CA private keys host-side, avoid automatic trust-store changes, redact logs and MCP responses, and expose only status or redacted findings through container-facing tools. <br>


## Reference(s): <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-nanoclaw-traffic-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specification-only scaffold; no active proxy or runtime monitor is shipped in this release.] <br>

## Skill Version(s): <br>
0.0.1-beta5 (source: server release evidence, frontmatter, skill.json, CHANGELOG released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
