## Description: <br>
Provides a comprehensive reference of OpenClaw, GCP, mesh, debugging, configuration, and operator commands for controlling and troubleshooting EVEZ-OS-style gateway and agent environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill as a compact command and configuration reference for OpenClaw gateway control, agent behavior tuning, diagnostics, networking, GCP access patterns, and mesh operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes operator actions that can expose credentials, prompts, traffic, cloud tokens, and administrative control surfaces. <br>
Mitigation: Use only in isolated, owner-authorized environments and avoid unredacted secret or full-payload logging in production. <br>
Risk: The skill includes guidance for disabling authentication and expanding administrative access. <br>
Mitigation: Keep device authentication enabled, restrict administrative endpoints to trusted networks, and review each command before applying it. <br>
Risk: Credentials or tokens may be exposed while following debugging, proxy, or cloud metadata commands. <br>
Mitigation: Rotate any credentials exposed during use and remove captured payloads or diagnostic logs that contain secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-os-cheat-codes) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; commands may require owner authorization and environment-specific credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
