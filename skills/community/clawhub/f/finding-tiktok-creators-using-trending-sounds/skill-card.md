## Description:

Finds TikTok creators using trending sounds or viral audio tracks through apidojo's TikTok Music Scraper on Apify, returning creator metrics and song metadata for each post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External music, brand, and influencer marketing teams use this skill to find TikTok creators who are using a specific sound or viral audio trend, then rank creators by follower count, engagement, and views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok sound URLs and run settings are sent to Apify under the user's Apify account.

Mitigation: Use the skill only for data you are comfortable sending to Apify, and keep APIFY_TOKEN secret.

Risk: Unbounded or broad runs may increase cost or return more data than needed.

Mitigation: Set a maxItems cap when cost, volume, or review effort matters.

Risk: Optional custom mapping code or output files could expose sensitive data if misused.

Mitigation: Avoid placing sensitive data in customMapFunction logic or generated output files.

Risk: Missing, removed, duplicate, or region-specific TikTok sounds can lead to empty, noisy, or geographically skewed results.

Mitigation: Verify the sound page URL, try an alternate sound when needed, deduplicate by creator username, and review regional relevance before acting on rankings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-tiktok-creators-using-trending-sounds)
- [Apify Actor Run API](https://api.apify.com/v2/acts/apidojo~tiktok-music-scraper/runs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, text, markdown]

**Output Format:** [Markdown guidance with shell, JSON, and Python snippets; expected run results can be table, CSV, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TikTok music or sound page URLs; supports maxItems caps, optional custom mapping, creator scoring, classification, and deduplication.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
