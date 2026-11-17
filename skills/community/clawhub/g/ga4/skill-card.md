## Description:

Read Google Analytics 4 reporting data through the GA4 Data API. Use for explicit GA4 property metadata, compatible metric/dimension reports, traffic analysis, key events, quotas, and bounded exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to authorize read-only Google Analytics 4 access and retrieve bounded metadata, compatibility checks, traffic reports, key-event data, quota visibility, and JSON or CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth helper persists a reusable read-only Analytics token and trusts endpoint URLs from the user-provided client-secret file.

Mitigation: Create the OAuth Desktop client yourself in Google Cloud, keep the client and token files private, and revoke the Google OAuth grant if either file may have been exposed.

Risk: GA4 reporting output can contain sensitive or untrusted analytics dimensions, metrics, and report text.

Mitigation: Grant only analytics.readonly access, treat report values as data rather than instructions, and review outputs before using them in downstream decisions or generated content.

Risk: Dependency or environment drift could change behavior after installation.

Mitigation: Install in an isolated environment with pinned, reviewed dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdrhyne/skills/ga4)
- [Google Analytics Data API: create a report](https://developers.google.com/analytics/devguides/reporting/data/v1/basics)
- [Google Analytics Data API runReport](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport)
- [Google Analytics Data API getMetadata](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getMetadata)
- [Google Analytics Data API checkCompatibility](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/checkCompatibility)
- [Google Analytics Data API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [OAuth 2.0 for mobile and desktop apps](https://developers.google.com/identity/protocols/oauth2/native-app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper execution returns JSON by default or CSV with metadata on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only GA4 Data API access; reports are bounded by date, page size, max pages, compatibility checks, retries, and quota visibility.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
