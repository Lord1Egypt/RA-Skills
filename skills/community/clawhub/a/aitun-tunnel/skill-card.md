## Description: <br>
Expose local web pages and HTTP services to the public internet via secure tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish a local web page, dashboard, HTTP service, webhook endpoint, or local API through an AiTun public tunnel for previews, demos, and integration testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing a local service can expose non-sensitive previews or test endpoints to the public internet. <br>
Mitigation: Use the skill only when public access is intended, prefer temporary non-sensitive previews or test webhooks, and stop the tunnel when finished. <br>
Risk: TCP forwarding for SSH, RDP, or databases can expose powerful services if used without adequate controls. <br>
Mitigation: Avoid --tcp-ports for SSH, RDP, and databases unless the operator fully understands the exposure and has appropriate access controls. <br>
Risk: Remote shell installers increase supply-chain risk compared with package-manager installation. <br>
Mitigation: Prefer pip or uv installation over curl-to-shell or PowerShell remote installer commands. <br>


## Reference(s): <br>
- [AiTun Homepage](https://aitun.cc) <br>
- [ClawHub Skill Page](https://clawhub.ai/ctz168/skills/aitun-tunnel) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ctz168) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a public tunnel URL for a running local service.] <br>

## Skill Version(s): <br>
4.0.5 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
