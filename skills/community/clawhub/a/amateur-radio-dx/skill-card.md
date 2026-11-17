## Description:

Monitor DX clusters for rare station spots, track active DX expeditions, and get daily band activity digests for amateur radio operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:

MIT

## Use Case:

External amateur radio operators use this skill to monitor DX cluster spots, identify rare or needed DXCC stations, and generate live alerts or daily activity digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe shared temporary state storage.

Mitigation: Run the skill as a non-root user and move state to a private per-user directory before enabling recurring monitoring.

Risk: Recurring cron automation can repeatedly contact external DX cluster servers.

Mitigation: Review configuration and alert cadence before enabling cron, and keep automated runs scoped to the operator's intended callsign and cluster.

Risk: Operator callsign and local station details may be exposed through DX cluster connections or local configuration files.

Mitigation: Use only callsign and station details the operator is comfortable disclosing, and protect local configuration files that contain QTH or station information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/capt-marbles/skills/amateur-radio-dx)
- [AI-enhanced DX monitor documentation](artifact/README-AI.md)
- [Quick start documentation](artifact/README.md)
- [NG3K Amateur Radio DX Calendar](https://www.ng3k.com/misc/adxo.html)
- [DX World](https://www.dx-world.net/)
- [425 DX News](http://www.425dxn.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DX station callsigns, band and mode details, priority alerts, digest summaries, and cron examples.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
