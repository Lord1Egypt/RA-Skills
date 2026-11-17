## Description:

Builds a social media audit for a brand using apidojo scrapers, with intended coverage across Twitter, Instagram, TikTok, and YouTube and output including per-platform metrics, engagement rates, posting frequency, and a brand health score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, brand strategists, and agency teams use this skill to audit a brand or competitor across social platforms and summarize performance, content mix, posting frequency, engagement, and strategic gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST examples place APIFY_TOKEN in URL query strings, which can expose the credential through prompts, logs, shell history, or copied URLs.

Mitigation: Use an Authorization header or official client, keep APIFY_TOKEN out of prompts and source files, and prefer a narrowly scoped token.

Risk: Brand and social-account queries plus scraped results are sent through Apify.

Mitigation: Confirm the data-sharing posture is acceptable before use and avoid submitting confidential strategy, campaign, or customer information.

Risk: The release claims multi-platform audit coverage, but the documented workflow is primarily Twitter-focused.

Mitigation: Add or verify per-platform steps for Instagram, TikTok, and YouTube before relying on cross-platform scores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/building-full-social-audit-for-brand)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, summary findings, and inline shell or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify results as CSV or JSON when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
