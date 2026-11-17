## Description:

Fetches and formats the latest flash-news items from Futu's official news channel for requests such as recent updates, refreshes, or rolling flash-news checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loveni](https://clawhub.ai/user/loveni)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve up to 10 current Futu flash-news items, formatted with Beijing timestamps, item text, and detail links when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes user-requested GET requests to news.futunn.com and depends on that public endpoint returning current, valid data.

Mitigation: Use the skill only when live Futu flash-news retrieval is expected, and treat HTTP failures, invalid JSON, nonzero API codes, or empty lists as fetch errors rather than substituting unsourced news.

Risk: Output uses Chinese-market defaults, including Beijing time and zh-CN request preferences.

Mitigation: Confirm that Beijing timestamp formatting and Chinese-language source content are appropriate for the user's task before relying on the returned items.

## Reference(s):

- [Futu Flash skill release](https://clawhub.ai/loveni/skills/futu-flash)
- [Futu live news page](https://news.futunn.com/main/live)
- [Futu flash-list API endpoint](https://news.futunn.com/news-site-api/main/get-flash-list)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON]

**Output Format:** [Markdown or JSON-formatted summaries of fetched flash-news items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns at most 10 items and uses Beijing time formatting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
