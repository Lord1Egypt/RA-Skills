## Description:

ERiC Compliance Suite helps agents run ERiC SaaS checks for design patents, invention patents, graphic and text trademarks, copyright images, and e-commerce policy compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wteng2286](https://clawhub.ai/user/wteng2286)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce compliance operators use this skill to screen product titles, descriptions, and images for intellectual-property and marketplace-policy risks before listing or reviewing products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send product titles, descriptions, images, and the ERiC token to the ERiC SaaS service.

Mitigation: Use only organization-approved data and avoid confidential, unreleased, regulated, or customer-sensitive material unless vendor data handling has been approved.

Risk: The CLI can fetch image content from URLs supplied by a user.

Mitigation: Prefer approved local image files or trusted image URLs, and avoid untrusted sources.

Risk: The script can install the requests dependency at runtime if it is missing.

Mitigation: Run the skill in a controlled Python environment with requests installed from a trusted, pinned source.

Risk: P005 and P006 can change remote account feature-word configuration.

Mitigation: Review feature-word save and delete operations before execution and restrict use to authorized account operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wteng2286/skills/eric-compliance-suite)
- [ERiC service](https://eric-bot.com)
- [Design patent detection reference](references/design-patent.md)
- [Invention patent detection reference](references/invention-patent.md)
- [Logo detection reference](references/logo-detection.md)
- [Trademark detection reference](references/trademark-detection.md)
- [Copyright detection reference](references/copyright-detection.md)
- [Policy detection reference](references/policy-detection.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize ERiC API results, risk labels, point costs, and account feature-word operations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
