## Description:

Track flights in real-time with detailed status, gate info, delays, and live position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[copey02](https://clawhub.ai/user/copey02)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up commercial flight status by IATA flight number and receive formatted departure, arrival, delay, aircraft, and live-position details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the AviationStack API key and flight lookup over unencrypted HTTP.

Mitigation: Use a rotatable, low-impact API key and avoid untrusted networks unless the endpoint is changed to HTTPS or routed through a secure proxy or provider.

Risk: Dependency installation and shell profile setup can expose long-lived local credentials if handled carelessly.

Mitigation: Use a virtual environment with pinned dependencies and avoid storing long-lived API keys in shared or committed shell profile files.

## Reference(s):

- [AviationStack API Setup](references/api-setup.md)
- [AviationStack free API signup](https://aviationstack.com/signup/free)
- [AviationStack flights endpoint](http://api.aviationstack.com/v1/flights)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Formatted terminal text with optional raw JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AVIATIONSTACK_API_KEY and the requests Python package; live data depends on AviationStack availability and plan limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
