## Description:

Monitors Twitter/X daily to find and filter new AI Agent, Crypto, and DeFi projects matching configured keywords, producing raw and curated result files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run scheduled Twitter/X searches for early AI-agent, crypto, and DeFi project signals and filter the results into project-focused exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated results and links come from untrusted social-media content.

Mitigation: Review and verify links, accounts, and project claims before acting on any result.

Risk: Crypto or DeFi opportunities surfaced by the skill may be misleading, spam, or financially risky.

Mitigation: Independently validate projects and avoid treating filtered results as recommendations.

Risk: CSV exports may contain formula-leading cells from untrusted source text.

Mitigation: Sanitize exports before opening them in spreadsheet applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/agentfarm-finder)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [CSV, JSON, Markdown, and shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include raw Twitter/X search results, filtered project exports, links, timestamps, and summary counts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
