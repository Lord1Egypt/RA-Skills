## Description:

Guides an agent through using the Apify YouTube Email Scraper actor to find publicly listed YouTube channel emails and contact information from keywords or channel URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to run a third-party Apify actor that searches YouTube channels and returns public contact fields for outreach or lead-generation workflows. It should be used only for lawful public business contact collection and with care for privacy and anti-spam obligations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables collection of YouTube contact emails through a third-party scraping service.

Mitigation: Use it only for lawful collection of public business contact information, avoid bulk unsolicited outreach, and treat returned email datasets as sensitive contact data.

Risk: The artifact examples pass the Apify token as a query parameter, which can expose credentials in logs or URLs.

Mitigation: Use a dedicated least-privileged Apify token and prefer Authorization headers over token query parameters when adapting the examples.

Risk: Broad activation wording may cause the skill to run for generic YouTube research when contact extraction was not intended.

Mitigation: Confirm the user explicitly wants contact extraction before running the Apify actor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/futurizerush/skills/apify-youtube-email)
- [Apify Actor Page](https://apify.com/futurizerush/youtube-email-scraper?fpr=rush)
- [Apify API Documentation](https://docs.apify.com/api/v2)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide asynchronous Apify runs that return JSON dataset items containing channel metadata, emails, websites, and processing status.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
