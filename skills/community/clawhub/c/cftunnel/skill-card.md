## Description: <br>
Expose local services to the internet via Cloudflare Tunnels. CLI (npx cftunnel) and Node.js library for creating tunnels, configuring ingress routes, managing DNS records, and running cloudflared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pirumpi](https://clawhub.ai/user/pirumpi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to expose a local web application, API, or service at a public HTTPS hostname through Cloudflare Tunnel, then manage the related ingress routes, DNS records, and cloudflared connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make local services publicly reachable through Cloudflare Tunnel. <br>
Mitigation: Use it only for services intentionally meant to be public, confirm the hostname and localhost port, and avoid exposing admin panels, databases, SSH, or debug applications. <br>
Risk: The skill can change Cloudflare DNS and tunnel state. <br>
Mitigation: Review proposed route, DNS, and tunnel operations before execution, and prefer scoped Cloudflare API tokens over broad API keys when possible. <br>
Risk: Persistent service mode can keep a tunnel available after reboot. <br>
Mitigation: Do not enable persistent service mode unless the tunnel is intended to survive reboots and has been reviewed as a long-lived exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pirumpi/cftunnel) <br>
- [cftunnel homepage](https://github.com/kyndlo/cftunnel) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and TypeScript examples; cftunnel commands emit JSON on stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cloudflare credentials and node/cftunnel binaries; command progress and errors are described as stderr output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
