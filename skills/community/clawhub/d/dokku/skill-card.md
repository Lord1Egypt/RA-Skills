## Description:

Installs, upgrades, and manages Dokku apps, deploys code or images, runs tasks, and cleans up containers on Dokku hosts via CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akhil-naidu](https://clawhub.ai/user/akhil-naidu)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to administer Dokku hosts, including installs and upgrades, app deployment, task execution, config and domain management, plugin and certificate operations, process control, and container cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level install, upgrade, and plugin operations can change the host.

Mitigation: Confirm the target host and intended action before running sudo, installer, upgrade, or plugin commands; verify downloaded installers and plugin repositories first.

Risk: SSH key, config, and certificate commands can expose or expand access to sensitive systems.

Mitigation: Add only specific reviewed public SSH keys, treat config output as secret material, and confirm certificate changes before applying them.

Risk: Destroy, prune, force, global-domain, certificate-removal, and bind-all-interfaces actions can remove data or broaden exposure.

Mitigation: Require explicit confirmation for these actions and scope them to the intended app, domain, certificate, network interface, or Docker object set.

## Reference(s):

- [Dokku installation documentation](https://dokku.com/docs/getting-started/installation)
- [Dokku upgrading documentation](https://dokku.com/docs/getting-started/upgrading)
- [Dokku releases](https://github.com/dokku/dokku/releases)
- [Docker system prune reference](https://docs.docker.com/engine/reference/commandline/system_prune/)
- [Dokku letsencrypt plugin](https://github.com/dokku/dokku-letsencrypt.git)
- [dokku-nuke plugin](https://github.com/dokku-community/dokku-nuke)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require sudo or affect host-wide Dokku, Docker, SSH, domain, network, certificate, and app state.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
