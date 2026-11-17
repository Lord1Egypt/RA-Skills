## Description:

Scans content for product mentions and auto-inserts or suggests tracked affiliate links with FTC compliance disclosures for blogs, product reviews, and guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, bloggers, ecommerce marketers, agencies, and developers use this skill to identify monetization opportunities, insert or suggest affiliate links, and generate disclosure and compliance reporting for content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest or make affiliate-link changes to live content, including WordPress posts.

Mitigation: Use suggest-only or read-only scanning by default, review changes before publishing, and test on staging or keep backups for live posts.

Risk: The skill text prompts for WordPress API keys or application passwords in chat.

Mitigation: Do not paste credentials into chat; provide scoped secrets through environment variables or a secret manager and prefer read-only credentials where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/affiliate-link-injector)
- [Amazon Associates](https://affiliate-program.amazon.com/)
- [ShareASale](https://www.shareasale.com/)
- [Impact](https://impact.com/)
- [CJ Affiliate](https://www.cjaffiliates.com/)
- [FTC Endorsements, Influencers, and Reviews](https://www.ftc.gov/endorsements)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text reports, CSV-style reports, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FTC disclosure text, affiliate link mappings, compliance notes, and monetization reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
