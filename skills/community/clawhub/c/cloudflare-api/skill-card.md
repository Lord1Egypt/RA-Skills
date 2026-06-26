## Description: <br>
Connect to Cloudflare API for DNS management, tunnels, and zone administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucassynnott](https://clawhub.ai/user/lucassynnott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer Cloudflare zones, DNS records, and Cloudflare tunnels from an agent-assisted shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real DNS and tunnel changes using a powerful Cloudflare API token. <br>
Mitigation: Use a least-privilege token limited to the needed account and zones, and confirm every DNS or tunnel change before execution. <br>
Risk: Cloudflare API tokens and tunnel run tokens are secrets. <br>
Mitigation: Protect ~/.cloudflare_token, prefer secure environment handling where appropriate, and avoid exposing tunnel run tokens in logs or shared transcripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lucassynnott/cloudflare-api) <br>
- [Cloudflare](https://cloudflare.com) <br>
- [Cloudflare API token management](https://dash.cloudflare.com/profile/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from Cloudflare API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Cloudflare API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
