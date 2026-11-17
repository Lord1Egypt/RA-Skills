## Description:

Scans any website for GDPR/DSGVO compliance from the terminal with no API key or signup required, returning a 0-100 score plus findings for trackers, cookies, consent banners, pre-consent tracking, fonts, and third-party transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2g4y1](https://clawhub.ai/user/2g4y1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and compliance reviewers use this skill to run a terminal-based GDPR/DSGVO quick scan of a public website and summarize returned findings. It is suited for checking trackers, cookies, consent banners, pre-consent tracking, external fonts, mail/TLS signals, and whether a fuller scan is warranted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned URLs are sent to compliancescan.eu and may expose sensitive query strings or non-public targets.

Mitigation: Scan only URLs the user is comfortable sharing with that service, avoid confidential query strings, and reject private or internal address targets.

Risk: The skill can use COMPLIANCESCAN_API_KEY for paid or full-scan API calls.

Mitigation: Configure the API key only when full-scan access is intended, never print or log the key, and use authenticated calls only when the environment variable is present.

Risk: Quick-Scan results are limited, may be cached, and are not legal advice.

Mitigation: Report only returned fields, identify cached or limited-scope results, and direct users to a full scan or professional review for compliance decisions.

Risk: Provider responses may include upgrade, registration, or provider links.

Mitigation: Present such links as service-provided options and keep the compliance findings distinct from upsell messaging.

## Reference(s):

- [Compliancescan homepage](https://compliancescan.eu)
- [Quick-Scan endpoint](https://compliancescan.eu/api/scanner/quick)
- [Authenticated API](https://compliancescan.eu/api/v1)
- [ClawHub skill page](https://clawhub.ai/2g4y1/skills/compliancescan)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Concise localized Markdown with compliance score, counts, risk flags, scan scope, cache notes, and failure details when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command snippets using curl and jq; responses are limited to data returned by compliancescan.eu and should not be treated as legal advice.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
