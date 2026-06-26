## Description: <br>
Deploy and manage 3X-UI on a root-managed Ubuntu or Debian VPS using Docker Compose, nginx, ACME certificates, SSH panel tunneling, UFW hardening, and Xray VLESS over XHTTP behind nginx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegtsvetkov](https://clawhub.ai/user/olegtsvetkov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and VPS operators use this skill to deploy, harden, update, and troubleshoot a 3X-UI based Xray VLESS service on a root-managed Ubuntu or Debian host. It guides explicit, manual-first operations for panel isolation, nginx TLS termination, inbound creation, additional clients, and conservative stack updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad root-level changes to a VPS, including package updates, firewall rules, Docker services, nginx configuration, ACME certificates, and 3X-UI settings. <br>
Mitigation: Use it only on a VPS you control, preferably a dedicated Ubuntu or Debian host, and review the bundled scripts before execution. <br>
Risk: Plain-text SSH passwords and public panel exposure can increase operational security risk. <br>
Mitigation: Prefer SSH keys over --ssh-password, keep the panel reachable only through a localhost SSH tunnel or trusted HTTPS panel URL, and avoid publishing the panel through nginx. <br>
Risk: The security evidence notes under-disclosed safety gaps, including that add-inbound-client --dry-run should not be treated as offline-only until fixed. <br>
Mitigation: Follow the security guidance, back up firewall and service configuration before changes, and do not rely on add-inbound-client --dry-run as an offline-only check. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olegtsvetkov/3x-ui-vps) <br>
- [Architecture](references/architecture.md) <br>
- [Manual Bootstrap](references/manual-bootstrap.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and generated VLESS client URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for remote VPS changes and may invoke bundled shell or Python scripts when explicitly requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
