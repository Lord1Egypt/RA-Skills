## Description:

Automates Buy Me a Coffee and Ko-fi creator-account workflows, including content updates, supporter thank-you messages, promotion, and earnings summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Creator-operators and developers use this skill to produce agent guidance, code, and configuration for automating supporter engagement and monetization workflows on Buy Me a Coffee or Ko-fi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Buy Me a Coffee or Ko-fi account credentials and broad account authority.

Mitigation: Use a protected secret store, a unique password, and MFA where available; do not place passwords in ordinary settings.

Risk: Automated posting, thank-you messages, promotions, and account scraping can violate platform rules or publish unintended content.

Mitigation: Require manual review before any post, message, promotion, or scrape, and check the platforms' automation rules before use.

Risk: The release appears incomplete because the scripts referenced by the skill are not included in the artifact.

Mitigation: Review generated or supplied scripts before installation and verify expected files are present before running account automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/buymeacoffee-autobot)
- [Buy Me a Coffee](https://buymeacoffee.com)
- [Ko-fi](https://ko-fi.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated automation scripts, content schedules, account settings, and operational guidance.]

## Skill Version(s):

1.0.18 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
