## Description: <br>
This skill helps agents route traffic through the Anyone Network using a local SOCKS5 proxy for IP masking and hidden-service access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rA3ka](https://clawhub.ai/user/rA3ka) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run the Anyone Protocol client, start a local SOCKS5 proxy, and route requests through the Anyone Network when IP masking or hidden-service access is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Traffic is intentionally routed through the Anyone Network, which may be inappropriate for secrets, regulated data, or internal requests. <br>
Mitigation: Use the proxy only when this routing is intended and allowed by policy; avoid secrets, regulated data, and internal traffic unless explicitly approved. <br>
Risk: The setup uses a globally installed NPM package and starts a local SOCKS5 proxy that persists across requests. <br>
Mitigation: Verify the @anyone-protocol/anyone-client package and publisher before installation, use trusted package sources, and stop the proxy when finished. <br>


## Reference(s): <br>
- [Anyone Protocol homepage](https://anyone.io) <br>
- [Anyone Network IP check endpoint](https://check.en.anyone.tech/api/ip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires installing @anyone-protocol/anyone-client and starting a local SOCKS5 proxy on port 9050.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
