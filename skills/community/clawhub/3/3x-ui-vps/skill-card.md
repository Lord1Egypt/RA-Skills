## Description:

Deploys and manages 3X-UI on a root-managed Ubuntu or Debian VPS using Docker Compose, nginx, ACME certificates, SSH panel tunneling, UFW hardening, and Xray VLESS over XHTTP behind nginx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegtsvetkov](https://clawhub.ai/user/olegtsvetkov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VPS operators use this skill to deploy, harden, repair, update, and operate a 3X-UI/Xray VLESS service on a dedicated Ubuntu or Debian VPS. It is intended for explicit, manual infrastructure actions that configure Docker, nginx, ACME certificates, UFW rules, loopback-only panel access, and VLESS client setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs root-level VPS changes that can replace firewall policy, Docker state, nginx configuration, and 3X-UI state.

Mitigation: Install only on a dedicated VPS where these changes are acceptable, review the planned operation before execution, and back up current UFW rules and /opt/3x-ui.

Risk: The security summary identifies supply-chain, firewall, update, and credential-handling risks.

Mitigation: Review or pin Docker, acme.sh, and 3X-UI sources before running; prefer SSH keys over --ssh-password and handle panel credentials as sensitive secrets.

Risk: The security guidance notes that add-inbound-client.py --dry-run should be treated as contacting the panel unless fixed.

Mitigation: Use dry-run only against the intended tunneled panel, or patch and verify dry-run behavior before relying on it for offline review.

## Reference(s):

- [Architecture](artifact/references/architecture.md)
- [Manual Bootstrap](artifact/references/manual-bootstrap.md)
- [ClawHub Skill Page](https://clawhub.ai/olegtsvetkov/skills/3x-ui-vps)
- [Publisher Profile](https://clawhub.ai/user/olegtsvetkov)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python command examples, configuration notes, and generated VLESS client URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include deployment checklists, remote command invocations, script patch guidance, validation commands, and ready-to-import vless:// client URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
