## Description: <br>
Deploy a public web presence (HTML + Docker + DNS + Domain) in ~15 minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to turn a directory of HTML files into a public website on a VPS by preparing Docker deployment steps, DNS record guidance, and verification commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change live Docker services and DNS records. <br>
Mitigation: Confirm the exact domain, VPS IP, container name, ports, DNS zone, and cleanup target before running commands. <br>
Risk: DNS provider tokens and VPS details may grant broad infrastructure access. <br>
Mitigation: Use a least-privileged DNS token scoped to the intended zone and provide secrets through approved environment variables or explicitly approved local paths. <br>
Risk: The skill references reading credentials from a home-directory file path. <br>
Mitigation: Do not allow the agent to inspect home-directory credential files unless the user has reviewed and approved the exact path. <br>


## Reference(s): <br>
- [Axiomata Web Deploy on ClawHub](https://clawhub.ai/kofna3369/axiomata-web-deploy) <br>
- [Hostinger DNS zones API endpoint](https://api.hostinger.com/api/vps/v1/dns/zones) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/assets/index.html](artifact/assets/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, HTML, Dockerfile, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment, DNS setup, cleanup, HTTPS, and verification guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
