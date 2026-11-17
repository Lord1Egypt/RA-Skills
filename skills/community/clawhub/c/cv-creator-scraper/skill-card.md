## Description:

Creativault Creator Scraper helps agents search, collect, export, and contact creator and influencer prospects across TikTok, YouTube, Instagram, and Twitter using Creativault APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativault](https://clawhub.ai/user/creativault)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, partnerships, and growth teams use this skill to discover creators, collect creator profile data, export campaign lists, find similar creators, and manage outreach follow-up. Developers and operators can also use it to run Creativault API-backed workflows through Node.js scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional self-update path can change installed skill files when enabled.

Mitigation: Keep CV_SKILL_AUTO_UPDATE unset and review updates manually before running the confirmed update command.

Risk: The skill requires Creativault API credentials and an operator identity for live API calls.

Mitigation: Use a scoped API key, keep credentials out of shared logs or files, and use only a trusted HTTPS Creativault API endpoint.

Risk: Creator exports and outreach records can contain contact information and other sensitive personal data.

Mitigation: Treat exported XLSX, CSV, HTML, and contact lists as sensitive data and share them only with authorized users.

Risk: Outreach workflows can send creator emails, including batch sends.

Mitigation: Confirm recipient lists, subject lines, and message bodies before sending, and keep the skill's user-confirmation step enabled.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Platform Parameters](references/platform-params.md)
- [Industry Categories](references/industry-categories.md)
- [Country Codes](references/country-codes.md)
- [Language Codes](references/language-codes.md)
- [Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with tables, JSON API results, shell command examples, and exported XLSX, CSV, or HTML file links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20.6+ and Creativault API credentials for live API calls.]

## Skill Version(s):

1.8.0 (source: release evidence, skill metadata, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
