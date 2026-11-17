## Description:

Search Google Play for apps, rankings, or store results through Dataify; it is not for collecting reviews from a known app URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate Google Play app search, ranking, category, region, language, and device requests into Dataify Scraper API calls and return compact app-store results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Play search terms and related parameters are sent to Dataify and may consume Dataify credits.

Mitigation: Review broad, multi-page, or credit-intensive searches before execution, and use dry-run previews when request scope is unclear.

Risk: Passing the Dataify token directly on the command line may expose credentials through shell history or process listings.

Mitigation: Set DATAIFY_API_TOKEN in a session-scoped environment variable and avoid printing or pasting the token into chat.

## Reference(s):

- [Dataify Google Play API Reference](references/google_play_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-play)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries by default, with raw JSON or HTML when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DATAIFY_API_TOKEN and Dataify credits; dry-run modes can preview request parameters without calling the API.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
