## Description:

Finds software engineers and developers on Twitter/X for recruiting by using apidojo Twitter scrapers on Apify to search, enrich, score, and summarize candidate profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Technical recruiters, startup hiring managers, and engineering talent acquisition teams use this skill to discover software engineering candidates on Twitter/X, enrich profile data, score fit, and prepare candidate shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback API examples may expose the Apify token when tokens are placed in URLs or copied into chat, command history, or logs.

Mitigation: Use a limited Apify token, prefer Authorization headers or environment variables, and avoid pasting tokens into chats, URLs, or logs.

Risk: Twitter/X search terms, handles, profile data, and recruiting analysis are sent to Apify during collection and enrichment.

Mitigation: Confirm organizational approval for sending this candidate and search data to Apify before using the skill for recruiting workflows.

Risk: Candidate scoring and open-to-work signals can be incomplete or misleading because they are inferred from social profile and tweet content.

Mitigation: Treat the generated shortlist as sourcing assistance and have a recruiter review candidates before outreach or hiring decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-software-engineers-on-twitter)
- [Apify actor: apidojo/twitter-user-scraper](https://apify.com/apidojo/twitter-user-scraper)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown candidate report with tables, scoring notes, and optional Apify command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON or CSV result files when the helper script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
