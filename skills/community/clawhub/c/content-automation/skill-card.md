## Description:

Content Automation helps agents generate social media posts, video scripts, content ideas, publishing schedules, content calendars, and content optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to draft and organize social media and video content workflows, including batch content plans, video scripts, publishing schedules, and calendar exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned external MoneyPrinterV2 repository that may change over time.

Mitigation: Review the external repository and dependencies, pin a known commit, and run the workflow in an isolated virtual environment before use.

Risk: Configured credentials can enable social account publishing, scheduled posting, affiliate tracking, or other account-affecting actions.

Mitigation: Keep credentials out of broadly readable configuration files and require explicit confirmation before uploads, scheduled posts, affiliate tracking, or account-affecting actions.

Risk: Generated content may be incorrect, misleading, or inconsistent with platform rules if posted without review.

Mitigation: Require human review for generated content and confirm that each post complies with applicable platform terms, community standards, and legal requirements.

## Reference(s):

- [ClawHub Content Automation skill page](https://clawhub.ai/antonia-sz/skills/content-automation)
- [MoneyPrinterV2 project documentation](https://github.com/FujiwaraChoki/MoneyPrinterV2/tree/main/docs)
- [MoneyPrinterV2 contribution guide](https://github.com/FujiwaraChoki/MoneyPrinterV2/blob/main/CONTRIBUTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce draft content plans, scripts, metadata, recommendations, and local export file instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
