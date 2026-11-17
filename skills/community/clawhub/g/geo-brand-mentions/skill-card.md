## Description:

Scans brand mentions and platform authority signals for AI visibility, producing a Brand Authority Score with platform-specific recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and brand teams use this skill to assess AI visibility across public platforms such as YouTube, Reddit, Wikipedia, LinkedIn, and community sites. It produces a brand authority report with platform scores, findings, and prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on an undeclared local `seogeo brand-scan` shell command as authoritative evidence.

Mitigation: Install and trust that command only in a controlled environment, or review its behavior before allowing the skill to run it.

Risk: The skill writes a `GEO-BRAND-MENTIONS.md` report into the active workspace.

Mitigation: Run it in the intended project directory or a disposable workspace when testing, and review generated content before sharing or committing it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/asale-ai/skills/geo-brand-mentions)
- [Publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report written to GEO-BRAND-MENTIONS.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Brand Authority Score, platform breakdowns, findings, recommendations, and optional competitive context.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
