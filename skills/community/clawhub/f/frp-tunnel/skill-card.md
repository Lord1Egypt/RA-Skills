## Description: <br>
Share local development servers via self-hosted frp tunnel with custom domains and auto HTTPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darwin7381](https://clawhub.ai/user/darwin7381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to expose selected local development servers through a self-hosted frp tunnel with custom domains and HTTPS for demos, client review, and mobile testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing a tunnel can expose selected local services to the public internet. <br>
Mitigation: Expose only intended services and avoid tunneling sensitive, unauthenticated, or debug-only local applications. <br>
Risk: The setup uses broad root SSH access and DNS credentials. <br>
Mitigation: Avoid passphrase-less root SSH where possible and store a least-privilege Cloudflare token with strict permissions. <br>
Risk: An exposed frp dashboard can leak operational details or control surfaces. <br>
Mitigation: Restrict or disable the frp dashboard before using the tunnel in shared or public environments. <br>
Risk: Downloaded binaries are installed into privileged paths. <br>
Mitigation: Verify downloaded binaries before installation and replace all hardcoded IPs, domains, tunnel names, and paths with environment-specific values. <br>


## Reference(s): <br>
- [frp releases](https://github.com/fatedier/frp/releases) <br>
- [Hetzner Cloud](https://www.hetzner.com/cloud/) <br>
- [Skill page](https://clawhub.ai/darwin7381/frp-tunnel) <br>
- [Publisher profile](https://clawhub.ai/user/darwin7381) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, TOML, Caddyfile, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational setup and troubleshooting guidance; users must replace environment-specific IPs, domains, paths, tunnel names, and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
