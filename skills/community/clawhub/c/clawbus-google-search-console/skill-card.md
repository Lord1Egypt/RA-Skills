## Description:

Google Search Console helps agents query connected MyBrandMetrics Search Console sitemap status, including submitted and indexed URL counts, warnings, errors, pending status, content type, and last downloaded time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review sitemap health for a connected Google Search Console property through MyBrandMetrics. It supports checks for indexing coverage, warnings, errors, pending sitemap processing, content type, and recent download status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or connected Search Console data could be exposed through command history, terminal logs, screenshots, or shared output.

Mitigation: Use MYBRANDMETRICS_API_KEY instead of --api-key, redact secrets before sharing output, and rotate any key pasted into shell history.

Risk: The skill sends sitemap queries and connection identifiers to MyBrandMetrics.

Mitigation: Install and run it only when the user trusts MyBrandMetrics with the connected Search Console data.

Risk: Local dependency installation can affect the user's Python environment.

Mitigation: Install requests in an isolated environment when dependencies are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbus/skills/clawbus-google-search-console)
- [Clawbus](https://www.clawbus.com/)
- [MyBrandMetrics](https://mybrandmetrics.com/)
- [Configuration](references/configuration.md)
- [Dimensions and Metrics](references/dimensions.md)
- [Query Patterns](references/query-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MyBrandMetrics API key and a connected Google Search Console connection ID.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
