## Description:

ActiveCampaign agent for marketers and sales teams: list health, lead scoring, deliverability, campaign postmortems, automation diagnostics, and 40+ more reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ji282h7](https://clawhub.ai/user/ji282h7)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and sales operators use this skill to analyze ActiveCampaign account health, campaign performance, automation hygiene, segmentation, and pipeline activity from live account data. It also produces campaign and automation specifications that users implement in the ActiveCampaign UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some instructions can bypass built-in write safeguards or use direct write examples.

Mitigation: Use a least-privileged ActiveCampaign integration user, set AC_READ_ONLY=1 for analysis-only work, and prefer named scripts or the Python client for changes.

Risk: The webhook audit can probe configured webhook URLs, including internal or sensitive URLs if they are present in the account.

Mitigation: Run webhook_audit.py with --skip-probe unless the configured webhook URLs have been reviewed and outbound probes are acceptable.

Risk: Snapshots, contact exports, suppression exports, and local state can contain customer data.

Mitigation: Treat local outputs as customer data, store them securely, and delete them when they are no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ji282h7/skills/activecampaign-claw)
- [ActiveCampaign v3 API reference](https://developers.activecampaign.com/reference)
- [Contacts reference](references/contacts.md)
- [Deals reference](references/deals.md)
- [Custom fields reference](references/custom-fields.md)
- [Installation guide](INSTALL.md)
- [Security policy](SECURITY.md)
- [Scaling notes](SCALING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, JSON exports, local files, and shell command or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts write local Markdown or JSON outputs; write actions are guarded by confirmation and can be disabled with AC_READ_ONLY=1.]

## Skill Version(s):

1.9.4 (source: frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
