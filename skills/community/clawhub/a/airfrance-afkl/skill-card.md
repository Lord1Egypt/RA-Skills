## Description:

Track Air France flights through the Air France-KLM Open Data Flight Status API for status monitoring, delay, gate, aircraft alerts, previous-flight chain analysis, and polling schedule guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iclems](https://clawhub.ai/user/iclems)

### License/Terms of Use:


## Use Case:

Travelers, travel operations teams, and developers use this skill to query or monitor Air France flight status, receive compact change alerts, inspect previous-flight delay risk, and tune polling within API limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AFKL API credentials, and the security evidence warns that credential handling has overly broad network scope.

Mitigation: Use a dedicated, low-privilege AFKL API key, keep the credential state directory private, and harden the HTTP helper so credentials are only sent to https://api.airfranceklm.com.

Risk: Aircraft registration values may be sent to Planespotters and cached locally during aircraft enrichment.

Mitigation: Disable or remove aircraft enrichment when AFKL-only network traffic is required, and clear local aircraft caches when registration lookups should not be retained.

Risk: Aircraft, Wi-Fi, cabin recency, and previous-flight delay signals are best-effort and may not reflect the final operational state.

Mitigation: Treat enrichment and heuristic analysis as advisory, and verify important travel decisions against official airline or airport sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iclems/skills/airfrance-afkl)
- [Air France-KLM Developer Portal](https://developer.airfranceklm.com)
- [AFKL Flight Status Field Reference](artifact/references/fields.md)
- [AFKL Flight Status API Endpoint](https://api.airfranceklm.com/opendata/flightstatus/{id})
- [Planespotters Public Registration Lookup](https://api.planespotters.net/pub/photos/reg/{reg})
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON flight-status responses, and compact plain-text watcher alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AFKL API credentials and may perform optional aircraft registration enrichment through Planespotters with local caching.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
