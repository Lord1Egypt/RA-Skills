## Description:

Builds targeted journalist and media contact lists from Twitter/X using apidojo's Twitter scrapers on Apify, returning names, handles, publication signals, follower counts, and recent coverage topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External PR agencies, startup communications teams, and founders use this skill to find journalists, editors, writers, and media contacts who cover a specified beat or publication set on Twitter/X. It helps compile outreach lists with profile signals, recent coverage context, and pitch-angle notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Twitter/X contact collection can create sensitive professional contact lists.

Mitigation: Limit searches to the stated outreach need, set strict maxItems values, avoid follower/following/retweeter collection unless necessary, and retain exported contact lists carefully.

Risk: REST examples that pass APIFY_TOKEN in the query string can expose credentials through shell history, logs, or copied URLs.

Mitigation: Prefer MCP or API calls that place credentials in authorization headers or managed secret storage, and rotate any token that may have been exposed.

Risk: Automated journalist filtering can include non-journalists or stale profile information.

Mitigation: Review the generated list, verify top contacts directly on Twitter/X or publication pages, and personalize outreach only after checking recent posts and articles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/building-journalist-outreach-list-from-twitter)
- [Apify actor: apidojo/twitter-user-scraper](https://apify.com/apidojo/twitter-user-scraper)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown contact list with tables, publication grouping, pitch-angle notes, and optional CSV or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Apify actor results and user-specified beat, publication, geography, type, and list-size filters.]

## Skill Version(s):

1.0.0 (source: evidence.release.version; artifact metadata version: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
