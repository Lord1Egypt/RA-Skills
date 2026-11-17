## Description:

Create professional, dark-themed architecture diagrams as standalone HTML files with inline SVG graphics for system, infrastructure, cloud, security, network topology, and technical component diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate self-contained HTML architecture diagrams that visualize system components, relationships, cloud infrastructure, network topology, and security boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagrams can contain system architecture details supplied by the user.

Mitigation: Review and sanitize generated HTML before sharing it outside the intended audience.

Risk: Opening generated HTML may contact Google Fonts.

Mitigation: Use approved network settings or replace the font import with a local font when external requests are not allowed.

Risk: Generated diagram files are saved locally under /tmp.

Mitigation: Inspect, move, or delete local outputs according to the user's data handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zmy1006-sudo/skills/fmtwiki-architecture-diagram)
- [Publisher Profile](https://clawhub.ai/user/zmy1006-sudo)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Self-contained HTML with embedded CSS and inline SVG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams are saved as local HTML files under /tmp and may load JetBrains Mono from Google Fonts when opened.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
