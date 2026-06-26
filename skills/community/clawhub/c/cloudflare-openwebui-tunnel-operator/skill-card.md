## Description: <br>
Create and maintain a Cloudflare Tunnel for Open WebUI using a 1Password-managed API token, Docker runtime, and optional systemd persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grey0758](https://clawhub.ai/user/grey0758) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose an existing local Open WebUI service through a Cloudflare Tunnel while keeping Cloudflare API credentials in 1Password. It guides tunnel, DNS, Docker, optional systemd persistence, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can intentionally expose Open WebUI through a public Cloudflare hostname. <br>
Mitigation: Use the skill only when public exposure is intended, and confirm the zone, hostname, tunnel name, and origin service before applying changes. <br>
Risk: Cloudflare API tokens and tunnel runtime tokens may be present in 1Password, local env files, or runtime environments. <br>
Mitigation: Use a least-privilege Cloudflare token, protect local env files, and avoid publishing secret values or raw transcripts. <br>
Risk: Optional systemd persistence can keep the tunnel running after reboot. <br>
Mitigation: Enable systemd persistence only when continuous tunnel availability after reboot is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/grey0758/cloudflare-openwebui-tunnel-operator) <br>
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [README](artifact/README.md) <br>
- [Workflow](artifact/WORKFLOW.md) <br>
- [FAQ](artifact/FAQ.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should include current workflow status, missing artifacts, next single best action, and verification after that.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
