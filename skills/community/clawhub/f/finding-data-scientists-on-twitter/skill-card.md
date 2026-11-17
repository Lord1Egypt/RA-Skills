## Description:

Finds data scientists and ML engineers to recruit using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiting teams, ML engineering hiring managers, AI research labs, and data-driven startups use this skill to discover, enrich, filter, and score data science and ML candidate profiles from Twitter/X signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identifiable recruiting searches and profile data are sent to Apify.

Mitigation: Use an approved Apify account, minimize collected profile fields, and confirm the recruiting workflow meets applicable privacy and employment compliance requirements.

Risk: API-token handling appears in usage examples.

Mitigation: Use a least-privilege Apify token stored in the environment or an approved secrets manager, and prefer authorization headers over URL token parameters.

Risk: Candidate CSV or JSON exports may contain personal data.

Mitigation: Define retention limits, access controls, and review procedures before exporting or sharing candidate files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-data-scientists-on-twitter)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/twitter-user-scraper](https://apify.com/apidojo/twitter-user-scraper)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown candidate tables with optional CSV or JSON exports and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate scores, profile highlights, Apify actor inputs, and export instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
