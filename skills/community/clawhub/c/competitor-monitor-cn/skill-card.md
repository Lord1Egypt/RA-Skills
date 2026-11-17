## Description:

Competitor Monitor helps ecommerce sellers track competitor price changes, availability, and promotions across JD, Taobao, Tmall, Pinduoduo, and Amazon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and developers use this skill to monitor competitor product prices and stock status, generate markdown alerts or reports, and optionally send notifications through configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured product URLs and webhooks can cause broad outbound network activity.

Mitigation: Use trusted configuration files, restrict product URLs to real marketplace hosts, and keep webhook notifications disabled unless the destination is verified.

Risk: The monitoring scripts write local alert, report, and price history files.

Mitigation: Run the skill as an unprivileged user in a workspace where generated output files are expected.

Risk: Running the skill on networks with access to internal services could expose those services to configured outbound requests.

Mitigation: Avoid running it on privileged networks or hosts that can reach internal services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zt6558609-cpu/skills/competitor-monitor-cn)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown alerts and reports with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local markdown alert/report files and can send configured webhook notifications.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
