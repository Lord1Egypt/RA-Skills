## Description:

Fetches and normalizes current weather data from the AWEKAS API with caching, retries, timeout protection, and structured error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michik1712](https://clawhub.ai/user/michik1712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current weather observations from AWEKAS, optionally for a specific station, and receive normalized JSON suitable for automation or downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access to AWEKAS and sends the provided AWEKAS API key to that service.

Mitigation: Use only with an intended AWEKAS account and provide the key through an environment variable or secret manager.

Risk: The package declares a semver-ranged node-fetch dependency and no lockfile is present in the artifact.

Mitigation: Pin dependencies or install from a reviewed lockfile before deploying in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michik1712/skills/awekas-current)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON object or structured error]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source, station, cached status, normalized weather fields, and raw provider payload.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
