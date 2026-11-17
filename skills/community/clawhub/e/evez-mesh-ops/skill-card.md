## Description:

EVEZ Mesh Ops is an operations reference for managing distributed AI gateway meshes across cloud nodes, covering node lifecycle, Docker, Git, GCP, Linux, SSH, systemd, cron, networking, security, incident response, and backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure, DevOps, and site reliability engineers use this skill as an operational reference for deploying, securing, debugging, and recovering multi-node AI gateway meshes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports live-looking gateway credentials and public infrastructure details in the skill documentation.

Mitigation: Review before installation, rotate the exposed gateway token if it was ever valid, and remove public IP and secret pairings from operational docs.

Risk: The release evidence reports broad cross-node SSH and unattended cron-based remediation behavior.

Mitigation: Avoid full-mesh SSH key sharing and require explicit approval before restart, prune, secret-read, firewall, cron, or watchdog actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-mesh-ops)
- [EvezArt publisher profile](https://clawhub.ai/user/evezart)
- [Publisher homepage](https://github.com/EvezArt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: evidence release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
