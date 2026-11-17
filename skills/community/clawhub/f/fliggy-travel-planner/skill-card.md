## Description:

Travel itinerary planning skill that automates end-to-end trip research and booking assistance by searching Xiaohongshu destination guides, extracting travel insights, querying Fliggy flight prices, fetching weather forecasts, and compiling a trip report with a budget breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to research destinations, compare travel options, estimate weather and budgets, and produce complete trip-planning reports. It is aimed at itinerary planning and booking assistance rather than autonomous purchase decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser and authenticated-session use may expose account context while researching travel or booking pages.

Mitigation: Use a dedicated browser profile or low-privilege accounts, and require user confirmation before authenticated browsing or booking-related actions.

Risk: Scraped Xiaohongshu content, source links, and booking links may be stale, misleading, or unsafe.

Mitigation: Treat scraped content and links as untrusted, verify important travel details manually, and avoid taking purchase actions without review.

Risk: The documented price-monitor cron behavior could create recurring tasks without a clear stopping condition.

Mitigation: Enable recurring monitoring only with an explicit expiry, cancellation path, and user-approved notification scope.

Risk: Shell-based weather queries can be fragile when user-provided city values are not encoded.

Mitigation: Prefer the bundled Python weather script or encoded HTTP requests over ad hoc shell curl commands.

## Reference(s):

- [Browser Automation Flow](references/browser-flow.md)
- [Prompt Templates](references/prompts.md)
- [Usage Examples](references/examples.md)
- [Xiaohongshu](https://www.xiaohongshu.com/)
- [Fliggy](https://www.fliggy.com/)
- [Ctrip](https://www.ctrip.com/)
- [Weather China](http://www.weather.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON intermediate data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include travel recommendations, weather tables, budget estimates, source links, and booking links.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
