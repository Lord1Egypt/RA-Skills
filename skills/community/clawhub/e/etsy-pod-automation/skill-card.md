## Description:

Use when a user wants to run an Etsy print-on-demand store with Printify integration, automated Etsy listings, AI-generated designs, SEO tags, and scheduled social media promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators can use this skill to guide Etsy print-on-demand workflows, including trend research, design generation, Printify product setup, Etsy listing creation, social promotion, and performance monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that affect live Etsy listings, prices, social posts, and retired products without clear approval gates.

Mitigation: Require dry-run previews and explicit user approval before publishing, posting, changing prices, or retiring listings.

Risk: The workflows rely on credentials for Etsy, Printify, scraping providers, and social media tools.

Mitigation: Use least-privilege tokens, keep secrets out of version control, and avoid unattended cron automation until safeguards are in place.

## Reference(s):

- [Etsy POD Automation Workflows](references/workflows.md)
- [Printify Shops API](https://api.printify.com/v1/shops.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, API workflow guidance, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external platform credentials and approval steps for Etsy, Printify, scraping providers, and social media tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
