## Description:

Benchmarks Instagram influencer engagement by running apidojo's Instagram scraper on Apify and reporting follower counts, average likes, average comments, engagement rate, recent post performance, and anomaly flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, influencer agencies, and campaign analysts use this skill to vet Instagram creators before paid partnerships, compare competitor accounts, and audit recent post performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram account targets and retrieved data are sent to Apify during scraping.

Mitigation: Run the skill only for accounts approved for third-party processing and disclose the Apify dependency to reviewers or customers.

Risk: The documented curl fallback places APIFY_TOKEN in the request URL, which can expose the token through logs or command history.

Mitigation: Prefer the helper script or MCP path, or revise the REST call to pass credentials through an authorization header or other non-URL secret handling.

Risk: The underlying scraper supports broader inputs than account benchmarking, including hashtags, locations, audio pages, and reels.

Mitigation: Constrain routine use to account handles and reasonable post limits unless broader collection is explicitly approved.

Risk: Private accounts and accounts with fewer than 10 recent posts can produce incomplete or unreliable engagement benchmarks.

Mitigation: Skip private accounts and flag low-post samples as low confidence in the final report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/benchmarking-instagram-influencer-engagement)
- [Apify Instagram Scraper Actor](https://apify.com/apidojo/instagram-scraper)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with comparison tables, engagement calculations, benchmark verdicts, and optional JSON or CSV dataset exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN for Apify access; analysis quality depends on public account availability and the number of recent posts retrieved.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
