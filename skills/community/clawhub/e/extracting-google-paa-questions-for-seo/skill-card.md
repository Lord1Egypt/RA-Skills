## Description:

Extracts Google People Also Ask questions for SEO content planning using apidojo's Google Search scraper on Apify, returning PAA questions, SERP position, related keywords, and content structure recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

SEO strategists, content writers, editors, and agents use this skill to collect Google People Also Ask questions for keyword research and convert them into content briefs, FAQ sections, heading ideas, and featured-snippet opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried keywords and related parameters are sent to Apify and Google.

Mitigation: Avoid submitting confidential keyword sets or sensitive campaign details unless that data sharing is acceptable.

Risk: Apify token exposure could allow unwanted API use.

Mitigation: Use a limited Apify token stored in an environment variable or secret store, avoid sharing logs or screenshots containing commands, and prefer authorization-header authentication over tokens in URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/extracting-google-paa-questions-for-seo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown brief with tables, lists, inline shell commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scored PAA question banks, intent classifications, FAQ recommendations, heading suggestions, and featured-snippet opportunity flags.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
