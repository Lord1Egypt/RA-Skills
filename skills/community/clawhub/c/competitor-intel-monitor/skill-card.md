## Description:

Monitor competitors' websites, social media, pricing, and product changes automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and market analysts use this skill to configure competitor tracking, run scheduled website checks, review change history, and generate competitive intelligence briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill contacts competitor sites and stores page text locally.

Mitigation: Use only trusted competitor names and public http/https URLs, and review what page text is retained before using the skill in sensitive environments.

Risk: The security review says URLs and local files are handled too broadly for safe installation without review.

Mitigation: Validate URLs, constrain storage paths, and limit retained data before operational deployment.

Risk: The security review says the skill overstates some features.

Mitigation: Treat unsupported social monitoring, alert-channel, RSS, SEO, and tech-stack claims as requiring implementation or removal before relying on them.

## Reference(s):

- [Competitive Intelligence Report Templates](references/ci-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/johnnywang2001/skills/competitor-intel-monitor)
- [Publisher Profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text with JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores competitor configuration and page snapshots under the user's home directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
