## Description: <br>
Manage Cloudflare zones, DNS records, workers, rules, firewall settings, and account resources through ClawLink-backed Cloudflare API tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and manage Cloudflare DNS, zones, firewall rules, tunnels, workers, and account resources from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare write actions such as DNS, WAF, tunnel, and delete operations can affect production traffic. <br>
Mitigation: Use least-privileged Cloudflare API tokens, preview changes, and require explicit user confirmation before executing writes. <br>
Risk: The skill relies on ClawLink to broker Cloudflare access and credentialed API calls. <br>
Mitigation: Install only when the user trusts ClawLink for Cloudflare access and verify the Cloudflare connection before making tool calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/cloudflare-infrastructure) <br>
- [Cloudflare API documentation](https://developers.cloudflare.com/api/) <br>
- [Cloudflare DNS Records API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone) <br>
- [Cloudflare Zones API](https://developers.cloudflare.com/api/operations/zones) <br>
- [ClawLink OpenClaw docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Cloudflare API-backed read and write actions through ClawLink tools; write actions require preview and user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
