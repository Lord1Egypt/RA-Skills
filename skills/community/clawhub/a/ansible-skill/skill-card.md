## Description:

Infrastructure automation with Ansible. Use for server provisioning, configuration management, application deployment, and multi-host orchestration. Includes playbooks for OpenClaw VPS setup, security hardening, and common server configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[botond-rackhost](https://clawhub.ai/user/botond-rackhost)

### License/Terms of Use:


## Use Case:

Developers and infrastructure engineers use this skill to prepare Ansible inventories, run playbooks, and apply reusable roles for VPS provisioning, server hardening, Node.js installation, and OpenClaw deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playbooks can apply broad privileged changes to live servers.

Mitigation: Review and edit the inventory before use, then run against explicit test hosts with --limit plus --check/--diff before applying changes.

Risk: SSH and firewall hardening can interrupt administrative access.

Mitigation: Keep out-of-band server access available before changing SSH or firewall settings.

Risk: Passwordless sudo and command-line passwords can expand credential exposure.

Mitigation: Disable or narrow passwordless sudo, avoid passing passwords on command lines, and use Ansible Vault for secrets.

Risk: Unpinned OpenClaw and package installs can introduce unreviewed changes.

Mitigation: Pin reviewed OpenClaw and package versions and verify repository keys before use.

Risk: Logs or fact caches in shared temporary paths can expose operational details.

Mitigation: Move logs and fact caches out of shared /tmp paths.

## Reference(s):

- [Ansible Skill on ClawHub](https://clawhub.ai/botond-rackhost/skills/ansible-skill)
- [Ansible Best Practices](references/best-practices.md)
- [Ansible Modules Cheatsheet](references/modules-cheatsheet.md)
- [Ansible Troubleshooting](references/troubleshooting.md)
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [geerlingguy Ansible Roles](https://github.com/geerlingguy?tab=repositories&q=ansible-role)
- [Ansible for DevOps](https://www.ansiblefordevops.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing operational guidance and reusable Ansible examples; commands should be reviewed before execution against live hosts.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
