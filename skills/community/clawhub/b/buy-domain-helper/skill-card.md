## Description: <br>
3-layer site launcher: tunnel any HTML instantly, deploy permanently to Cloudflare Pages, then buy a domain and link it via DNS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wohaoshuai](https://clawhub.ai/user/wohaoshuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site owners use this skill to make a local HTML folder or server publicly reachable, deploy it to Cloudflare Pages, and connect a custom domain through Cloudflare DNS when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tunnel command can make local folders or ports publicly reachable. <br>
Mitigation: Tunnel only folders or ports intended for public access and stop the tunnel when sharing is no longer needed. <br>
Risk: The deployment and domain commands can change Cloudflare Pages projects, custom domains, and DNS records. <br>
Mitigation: Use narrowly scoped Cloudflare tokens and confirm each deployment, domain attachment, and DNS change before execution. <br>
Risk: The helper may auto-install or run external packages and tools. <br>
Mitigation: Review requested package installs and command invocations before running them in a trusted environment. <br>
Risk: Tokens passed as command arguments can be exposed through shell history or process listings. <br>
Mitigation: Prefer environment variables or a secret manager for Cloudflare tokens instead of command-line `--token` values. <br>
Risk: The package metadata declares an unrelated required `NETA_TOKEN`. <br>
Mitigation: Do not provide `NETA_TOKEN` for this skill unless separate trusted evidence establishes that it is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wohaoshuai/buy-domain-helper) <br>
- [Skill homepage](https://github.com/wohaoshuai/buy-domain-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through tunnel, Pages deployment, domain availability, DNS linking, and verification steps.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
