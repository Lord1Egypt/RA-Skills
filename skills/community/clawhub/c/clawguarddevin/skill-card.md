## Description:

Security scanner for OpenClaw/Clawdbot skills - detect malicious patterns before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinfloyd1](https://clawhub.ai/user/devinfloyd1)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use ClawGuard to review OpenClaw and Clawdbot skills for documented malicious patterns before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents scanner commands for scan.py, but the inspected files do not include that executable scanner implementation.

Mitigation: Review the linked repository or source package before relying on scanner behavior or integrating it into release checks.

## Reference(s):

- [ClawGuard repository listed in artifact](https://github.com/devinfloyd1/clawguard)
- [ClawHavoc research by Koi Security](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; documented scanner outputs include console text, JSON, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The inspected artifact documents scan.py commands but does not bundle scan.py.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact frontmatter lists 0.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
